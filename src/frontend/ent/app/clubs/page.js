"use client";
import React, { useEffect, useState } from 'react';
import crudAPI from '../crud/crudAPI';

export default function ClubsPage() {
  const [clubs, setClubs] = useState([]);

  useEffect(() => {
    const fetchClubs = async () => {
      try {
        const response = await crudAPI().GET('/club'); 
        setClubs(response.data); 
      } catch (error) {
        console.error('Erro ao buscar clubes:', error);
      }
    };

    fetchClubs();
  }, []);

  return (
    <main>
      <b>Clubs Page</b>: 
      <ul>
        {clubs.map((club) => (
          <li key={club.id}>{club.club_name}</li> 
        ))}
      </ul>
    </main>
  );
}


