package main
import (
	"database/sql"
	"encoding/xml"
	"encoding/json"
	"fmt"
	"log"
	"strings"
	"time"

	"github.com/antchfx/xmlquery"
	_ "github.com/lib/pq"
	"github.com/go-resty/resty/v2"
	"github.com/streadway/amqp"
)

type Country struct {
	XMLName xml.Name `xml:"Country"`
	Id      string   `xml:"Id,attr"`
	Name    string   `xml:"Name,attr"`
}

const apiCountriesCreate = "http://localhost:8080/country" 

func main() {
	connectionString := "postgres://is:is@db-xml/is?sslmode=disable"

	db, err := sql.Open("postgres", connectionString)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	err = db.Ping()
	if err != nil {
		log.Fatal("Erro ao conectar ao banco de dados:", err)
	}

	fmt.Println("Conexão com o banco de dados estabelecida com sucesso!")

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

	// Loop para receber mensagens da fila
	for msg := range msgs {
		fileName := string(msg.Body)

		fmt.Printf("Nome do arquivo do XML recebido: %s\n", fileName)

		xmlQuery := "SELECT xml FROM public.imported_documents WHERE file_name = $1"

		var xmlData string
		err := db.QueryRow(xmlQuery, fileName).Scan(&xmlData)
		if err != nil {
			log.Fatalf("Erro ao buscar XML do banco de dados: %s", err)
		}

		doc, err := xmlquery.Parse(strings.NewReader(xmlData))
		if err != nil {
			log.Fatalf("Erro ao analisar o XML: %s", err)
		}
		var countryNames []string

		// Altere a consulta XPath para capturar apenas o país com nome "France"
		nodes := xmlquery.Find(doc, "//Countries/Country[@Name='France']")
		
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

			

			fmt.Printf("Nomes dos países: %v\n", countryNames)

			
			for _, name := range countryNames {
				payload := map[string]string{"name": name}
				jsonData, err := json.Marshal(payload)
				if err != nil {
					log.Fatal(err)
				}
			
				client := resty.New()
				resp, err := client.R().
					SetHeader("Content-Type", "application/json").
					SetBody(jsonData).
					Post(apiCountriesCreate)
			
				if err != nil {
					log.Println("Erro ao enviar solicitação:", err)
					log.Fatal(err)
				}
			
				log.Printf("Resposta da API para o país %s: Status %d\n", name, resp.StatusCode())
			
				if resp.StatusCode() != 201 {
					log.Fatalf("Falha ao chamar a API para o país %s. Status: %d", name, resp.StatusCode())
				}
			
				log.Printf("Corpo da resposta para o país %s: %s\n", name, resp.Body())
			
				time.Sleep(1 * time.Millisecond)
			}
			
		}}}