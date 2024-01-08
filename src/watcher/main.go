package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"os"
    "time"
	_ "github.com/lib/pq"
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
}


