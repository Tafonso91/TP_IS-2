"use client";
import React, { useEffect, useState } from 'react';
import crudAPI from '../crud/crudAPI'; 

export default function CountriesPage() {
  const [clubs, setClubs] = useState([]);

  useEffect(() => {
    const fetchClubs = async () => {
      try {
        const response = await crudAPI().GET('/country'); // Chamada para listar os clubes
        setClubs(response.data); // Define os clubes no estado local
      } catch (error) {
        console.error('Erro ao buscar clubes:', error);
      }
    };

    fetchClubs();
  }, []);

  return (
    <main>
      <b>Countries Page</b>: 
      <ul>
        {clubs.map((club) => (
          <li key={club.id}>{club.club_name}</li> 
        ))}
      </ul>
    </main>
  );
}

