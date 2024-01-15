package main
import (
	"database/sql"
	"encoding/xml"
	
	"fmt"
	"log"
	"strings"
	

	"github.com/antchfx/xmlquery"
	_ "github.com/lib/pq"
	"github.com/streadway/amqp"
	"github.com/go-resty/resty/v2"
)

type Country struct {
	XMLName xml.Name `xml:"Country"`
	Id      string   `xml:"Id,attr"`
	Name    string   `xml:"Name,attr"`
}

const apiCountriesCreate = "http://api-entities:8080/country" 

func main() {
	connectionString := "postgres://is:is@db-xml/is?sslmode=disable"

	db, err := sql.Open("postgres", connectionString)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	err = db.Ping()
	if err != nil {
		log.Fatal("Erro ao conectar ao base de dados:", err)
	}

	fmt.Println("Conexão com o base de dados estabelecida com sucesso!")

	conn, err := amqp.Dial("amqp://is:is@broker:5672/is")
	if err != nil {
		log.Fatalf("Erro ao conectar ao servidor RabbitMQ: %s", err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("Erro ao abrir o canal: %s", err)
	}
	defer ch.Close()

	// Consume mensagens da fila que já foi declarada pelo watcher
	msgs, err := ch.Consume(
		"menssagem", // Nome da fila que já foi declarada pelo watcher
		"",          // consumer
		true,        // auto-ack
		false,       // exclusive
		false,       // no-local
		false,       // no-wait
		nil,         // args
	)
	if err != nil {
		log.Fatalf("Erro ao consumir mensagens: %s", err)
	}

	var countryNames []string // Mova a declaração para fora do loop principal

for msg := range msgs {
    fileName := string(msg.Body)

    fmt.Printf("Nome do arquivo do XML recebido: %s\n", fileName)

    xmlQuery := "SELECT xml FROM public.imported_documents WHERE file_name = $1"

    var xmlData string
    err := db.QueryRow(xmlQuery, fileName).Scan(&xmlData)
    if err != nil {
        log.Fatalf("Erro ao buscar XML do base de dados: %s", err)
    }

    doc, err := xmlquery.Parse(strings.NewReader(xmlData))
    if err != nil {
        log.Fatalf("Erro ao analisar o XML: %s", err)
    }

    // Altere a consulta XPath para capturar todos os países
    nodes := xmlquery.Find(doc, "//Countries/Country")

    // Limpe o slice antes de cada iteração
    countryNames = nil

    for _, country := range nodes {
        var name string

        for _, attr := range country.Attr {
            if attr.Name.Local == "Name" {
                name = attr.Value
                break
            }
        }

        // Adicione o nome ao slice
        countryNames = append(countryNames, name)
    }

    // Faça o POST na API para criar os países usando Resty
    err = createCountry(apiCountriesCreate, countryNames)
    if err != nil {
        log.Fatalf("Erro ao criar países via API: %s", err)
    }
}
}

func createCountry(apiEndpoint string, countryNames []string) error {
	client := resty.New()

	for _, name := range countryNames {
		
		requestBody := map[string]string{"country_name": name}

		// Faça o POST para a API
		resp, err := client.R().
			SetBody(requestBody).
			SetResult(&map[string]interface{}{}).
			Post(apiEndpoint)

		if err != nil {
			return fmt.Errorf("Erro ao fazer POST para a API: %s", err)
		}

		if resp.StatusCode() != 200  {
			return fmt.Errorf("Falha ao criar país via API. Código de status: %d", resp.StatusCode())
		}

		fmt.Printf("País criado via API: %s\n", name)
	}

	return nil
}