import React, { useEffect, useState } from 'react';
import { LayerGroup, useMap } from 'react-leaflet';
import { ObjectMarker } from './ObjectMarker';
import crudAPI from '../crud/crudAPI';

// ... Importações e código anterior ...

function ObjectMarkersGroup() {
  const map = useMap();
  const [players, setPlayers] = useState([]);
  const axios = crudAPI();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.GET('/get_players_with_coordinates');
        setPlayers(response.data);
      } catch (error) {
        console.error('Erro ao buscar dados da API:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <LayerGroup>
      {players.map((player) => (
        <ObjectMarker
          key={player.player_id}
          geoJSON={{
            type: 'feature',
            geometry: {
              type: 'Point',
              coordinates: player.coordinates.coordinates, 
            },
            properties: {
              id: player.country_id,
              name: player.name,
              salary: player.salary,  
              overall: player.overall,  
              imgUrl: `https://cdn-icons-png.flaticon.com/512/805/805401.png`,
            },
          }}
        />
      ))}
    </LayerGroup>
  );
}

export default ObjectMarkersGroup;



