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
	Name    string   `xml:",chardata"`
}

type Club struct {
	XMLName xml.Name `xml:"Club"`
	Id      string   `xml:"Id,attr"`
	Name    string   `xml:"Name,attr"`
}
type StrongFoot struct {
	XMLName xml.Name `xml:"Strong_Foot"`
	Id      string   `xml:"Id,attr"`
	Name    string   `xml:"Name,attr"`
}
type Player struct {
    XMLName   xml.Name `xml:"Player"`
    Id        string   `xml:"Id,attr"`
    Name      string   `xml:"Information>Name,attr"`
    CountryId string   `xml:"countryRef,attr"`
    Salary    string   `xml:"Information>Salary,attr"`
	Overall    string   `xml:"Main_Stats>Over,attr"`
}



const (
	apiCountriesCreate = "http://api-entities:8080/country"
	apiClubsCreate     = "http://api-entities:8080/club"
	apiStrongFootCreate     = "http://api-entities:8080/strong_foot"
	apiPlayersCreate = "http://api-entities:8080/player"
)

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

		// Process countries and send to API
		processCountriesAndSend(doc)
		// Process clubs and send to API
		processClubsAndSend(doc)
		// Process strong_foots and send to API
		processStrongFootAndSend(doc)

		processPlayersAndSend(doc)

		
	}
}

func processCountriesAndSend(doc *xmlquery.Node) {
	nodes := xmlquery.Find(doc, "//Countries/Country")

	var countries []Country

	for _, node := range nodes {
		country := Country{
			Name: node.SelectAttr("Name"),
		}
		countries = append(countries, country)
	}

	// Printar todos os países no array
	fmt.Println("Países encontrados:")
	for _, c := range countries {
		fmt.Printf(" Nome: %s\n", c.Name)
	}

	err := sendCountriesToAPI(countries)
	if err != nil {
		log.Fatalf("Erro ao enviar países para a API: %s", err)
	}
}

func processClubsAndSend(doc *xmlquery.Node) {
	clubNodes := xmlquery.Find(doc, "//Football/Teams/Club")

	var clubs []Club

	for _, clubNode := range clubNodes {
		club := Club{
			Id:   clubNode.SelectAttr("Id"),
			Name: clubNode.SelectAttr("Name"),
		}
		clubs = append(clubs, club)
	}

	// Send clubs to API
	err := sendClubsToAPI(clubs)
	if err != nil {
		log.Fatalf("Erro ao enviar clubes para a API: %s", err)
	}
}

func processStrongFootAndSend(doc *xmlquery.Node) {
	strongFootNodes := xmlquery.Find(doc, "//Strong_Foot/Foot")

	var strongFoots []StrongFoot

	for _, strongFootNode := range strongFootNodes {
		strongFoot := StrongFoot{
			Id:   strongFootNode.SelectAttr("Id"),
			Name: strongFootNode.SelectAttr("Name"),
		}
		strongFoots = append(strongFoots, strongFoot)
	}

	// Send strong_foots to API or perform any necessary logic
	err := sendStrongFootsToAPI(strongFoots)
	if err != nil {
		log.Fatalf("Erro ao enviar strong_foots para a API: %s", err)
	}
}

func processPlayersAndSend(doc *xmlquery.Node) {
    playerNodes := xmlquery.Find(doc, "//Players/Player")

    var players []Player

    for _, playerNode := range playerNodes {
        player := Player{
            Id:        playerNode.SelectAttr("Id"),
            Name:      playerNode.SelectElement("Information").SelectAttr("Name"),
            CountryId: playerNode.SelectAttr("countryRef"),
			Salary:    playerNode.SelectElement("Information").SelectAttr("Salary"),
			Overall:    playerNode.SelectElement("Main_Stats").SelectAttr("Over"),
        }
        players = append(players, player)
    }

    // Send players to API
    err := sendPlayersToAPI(doc, players)
    if err != nil {
        log.Fatalf("Erro ao enviar jogadores para a API: %s", err)
    }
}


func sendCountriesToAPI(countries []Country) error {
	client := resty.New()

	for _, country := range countries {
		// Ajuste para o formato JSON esperado pela API
		resp, err := client.R().
			SetHeader("Content-Type", "application/json").
			SetBody(map[string]string{
				"country_name": country.Name,
			}).
			Post(apiCountriesCreate)

		if err != nil {
			return fmt.Errorf("Erro ao enviar país para a API: %s", err)
		}

		if resp.StatusCode() != 201 {
			return fmt.Errorf("Erro ao enviar país para a API. Código de status: %d", resp.StatusCode())
		}

		fmt.Printf("País enviado para a API. Nome: %s\n", country.Name)
	}

	return nil
}

func sendClubsToAPI(clubs []Club) error {
	client := resty.New()

	for _, club := range clubs {
		// Ajuste para o formato JSON esperado pela API
		resp, err := client.R().
			SetHeader("Content-Type", "application/json").
			SetBody(map[string]string{
				"club_name": club.Name,
			}).
			Post(apiClubsCreate)

		if err != nil {
			return fmt.Errorf("Erro ao enviar clube para a API: %s", err)
		}

		if resp.StatusCode() != 201 {
			return fmt.Errorf("Erro ao enviar clube para a API. Código de status: %d", resp.StatusCode())
		}

		fmt.Printf("Clube enviado para a API. Nome: %s\n", club.Name)
	}

	return nil
}

func sendStrongFootsToAPI(strongFoots []StrongFoot) error {
	client := resty.New()

	for _, strongFoot := range strongFoots {
		// Ajuste para o formato JSON esperado pela API
		resp, err := client.R().
			SetHeader("Content-Type", "application/json").
			SetBody(map[string]string{
				"foot_name": strongFoot.Name,
			}).
			Post(apiStrongFootCreate)

		if err != nil {
			return fmt.Errorf("Erro ao enviar strong_foot para a API: %s", err)
		}

		if resp.StatusCode() != 201 {
			return fmt.Errorf("Erro ao enviar strong_foot para a API. Código de status: %d", resp.StatusCode())
		}

		fmt.Printf("Strong_foot enviado para a API. Nome: %s\n", strongFoot.Name)
	}

	return nil
	
}
func getCountryNameByRef(doc *xmlquery.Node, countryRef string) (string, error) {
    countryNode := xmlquery.FindOne(doc, "//Countries/Country[@Id='" + countryRef + "']")
    if countryNode != nil {
        return countryNode.SelectAttr("Name"), nil
    }
    return "", fmt.Errorf("País não encontrado para o countryRef: %s", countryRef)
}


func sendPlayersToAPI(doc *xmlquery.Node, players []Player) error {
    client := resty.New()

    for _, player := range players {
        // Buscar o nome do país no XML pelo countryRef
        countryName, err := getCountryNameByRef(doc, player.CountryId)
        if err != nil {
            return fmt.Errorf("Erro ao buscar o nome do país pelo countryRef: %s", err)
        }

        // Imprimir o conteúdo de countryName para debug
        fmt.Printf("countryName para jogador %s: %s\n", player.Name, countryName)

        // Ajuste para o formato JSON esperado pela API
        resp, err := client.R().
            SetHeader("Content-Type", "application/json").
            SetBody(map[string]string{
                "name":  player.Name,
                "country_name": countryName,
				"salary":       player.Salary,
				"overall":       player.Overall,
            }).
            Post(apiPlayersCreate)

        if err != nil {
            log.Printf("Erro ao enviar jogador para a API: %s\n", err)
            return fmt.Errorf("Erro ao enviar jogador para a API: %s", err)
        }

        if resp.StatusCode() != 201 {
            log.Printf("Erro ao enviar jogador para a API. Código de status: %d\n", resp.StatusCode())
            log.Printf("Resposta da API: %s\n", resp.Body())
            return fmt.Errorf("Erro ao enviar jogador para a API. Código de status: %d", resp.StatusCode())
        }

        fmt.Printf("Jogador enviado para a API. Nome: %s, País: %s\n", player.Name, countryName)
    }

    return nil
}





