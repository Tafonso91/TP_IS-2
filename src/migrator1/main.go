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

func main() {
	client := resty.New()

	
	apiURL := "http://localhost:20001/country"
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

	// Cria um canal
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
	
		// Consulta para obter o conteúdo XML do banco de dados com base no fileName
		xmlQuery := "SELECT xml FROM public.imported_documents WHERE file_name = $1"
	
		var xmlData string // Variável para armazenar o conteúdo XML obtido do banco de dados
	
		// Executar a consulta para obter o conteúdo XML do banco de dados
		err := db.QueryRow(xmlQuery, fileName).Scan(&xmlData)
		if err != nil {
			log.Fatalf("Erro ao buscar XML do banco de dados: %s", err)
		}
	
		// Parse do documento XML usando xmlquery
		doc, err := xmlquery.Parse(strings.NewReader(xmlData))
		if err != nil {
			log.Fatalf("Erro ao analisar o XML: %s", err)
		}
	
		// Executar a consulta XPath para encontrar todos os nomes dos países
		nodes := xmlquery.Find(doc, "//Countries/Country/@Name")
	
		// Iterar sobre os resultados e imprimir os nomes dos países
		for _, node := range nodes {
			fmt.Printf("Nome do País: %s\n", node.InnerText())
	
			
	resp, err := client.R().
	SetBody(map[string]string{"country_name": node.InnerText()}).
	Post(apiURL)

if err != nil {
	log.Fatalf("Erro ao enviar solicitação POST para a API: %s", err)
}

// Verifique a resposta da solicitação HTTP
fmt.Println("Status:", resp.StatusCode())
}
}
}
