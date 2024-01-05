"use client";
import React, { useEffect, useState } from 'react';
import crudAPI from '../crud/crudAPI';

export default function StrongFootPage() {
  const [strong_foots, setStrongFoot] = useState([]);

  useEffect(() => {
    const fetchStrongFoot = async () => {
      try {
        const response = await crudAPI().GET('/strong_foot'); 
        setStrongFoot(response.data); 
      } catch (error) {
        console.error('Erro ao buscar pés:', error);
      }
    };

    fetchStrongFoot();
  }, []);

  return (
    <main>
      <b>Countries Page</b>: 
      <ul>
        {strong_foots.map((strong_foot) => (
          <li key={strong_foot.id}>{strong_foot.foot_name}</li> 
        ))}
      </ul>
    </main>
  );
}


