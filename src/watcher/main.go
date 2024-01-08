package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"time"

	_ "github.com/lib/pq"
	"github.com/streadway/amqp"
	_ "github.com/streadway/amqp"
)

const jsonFilename = "arquivos.json"

type Arquivos struct {
	Nomes []string `json:"nomes"`
}

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

	rows, err := db.Query("SELECT file_name FROM public.imported_documents")
	if err != nil {
		log.Fatal("Erro ao executar a consulta:", err)
	}
	defer rows.Close()

	var nomesArquivos []string

	for rows.Next() {
		var fileName string
		err = rows.Scan(&fileName)
		if err != nil {
			log.Fatal("Erro ao ler o resultado da consulta:", err)
		}
		nomesArquivos = append(nomesArquivos, fileName)
		fmt.Printf("Nome do Arquivo: %s\n", fileName)
	}

	atualizarJSON(nomesArquivos)
	
	time.Sleep(time.Minute)
}

    func enviarMensagemBroker(novosNomes []string) {
        // Estabelece conexão com o servidor RabbitMQ
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

        // Declara uma fila no RabbitMQ
        queue, err := ch.QueueDeclare(
            "menssagem", // Nome da fila
            false,          // durable
            false,          // delete when unused
            false,          // exclusive
            false,          // no-wait
            nil,            // arguments
        )
        if err != nil {
            log.Fatalf("Erro ao declarar a fila: %s", err)
        }

        // Envia cada novo nome como uma mensagem para a fila
        for _, nome := range novosNomes {
            err = ch.Publish(
                "",            // exchange
                queue.Name,    // routing key
                false,         // mandatory
                false,         // immediate
                amqp.Publishing{
                    ContentType: "text/plain",
                    Body:        []byte(nome),
                },
            )
            if err != nil {
                log.Fatalf("Erro ao enviar mensagem para a fila: %s", err)
            }
            fmt.Printf("Mensagem enviada para a fila: %s\n", nome)
        }
    }
func atualizarJSON(novosNomes []string) {
    var arquivos Arquivos

  
    if _, err := os.Stat(jsonFilename); err == nil {
        file, err := os.Open(jsonFilename)
        if err != nil {
            log.Fatal("Erro ao abrir o arquivo JSON:", err)
        }
        defer file.Close()

        decoder := json.NewDecoder(file)
        err = decoder.Decode(&arquivos)
        if err != nil {
            log.Fatal("Erro ao decodificar o arquivo JSON:", err)
        }
    }

  
    nomesExistentes := make(map[string]bool)
    for _, nome := range arquivos.Nomes {
        nomesExistentes[nome] = true
    }

   
    for _, nome := range novosNomes {
        if !nomesExistentes[nome] {
            arquivos.Nomes = append(arquivos.Nomes, nome)
            nomesExistentes[nome] = true
        }
    }

  
    file, err := os.Create(jsonFilename)
    if err != nil {
        log.Fatal("Erro ao criar o arquivo JSON:", err)
    }
    defer file.Close()

    encoder := json.NewEncoder(file)
    encoder.SetIndent("", "  ")
    err = encoder.Encode(arquivos)
    if err != nil {
        log.Fatal("Erro ao codificar o arquivo JSON:", err)
    }

    fmt.Println("Arquivo JSON atualizado com sucesso!")
    enviarMensagemBroker(novosNomes)
}


