"use client";
import React, { useEffect, useState } from 'react';
import crudAPI from '../crud/crudAPI';

export default function PlayersPage() {
    const [players, setPlayers] = useState([]);
  
    useEffect(() => {
      const fetchPlayers = async () => {
        try {
          const response = await crudAPI().GET('/player'); 
          setPlayers(response.data); 
        } catch (error) {
          console.error('Erro ao buscar jogadores:', error);
        }
      };
  
      fetchPlayers();
    }, []);
  
    return (
      <main>
        <b>Players Page</b>: 
        <ul>
          {players.map((player) => (
            <li key={player.id}>{player.name}</li> 
          ))}
        </ul>
      </main>
    );
  }
