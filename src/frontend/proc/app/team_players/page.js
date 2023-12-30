"use client";
import React, { useEffect, useState } from "react";
import {
  Box,
  Container,
  Typography,
  Paper,
  ListItem,
  ListItemText,
  CircularProgress,
  Autocomplete,
  TextField,
} from "@mui/material";
import useAPI from "../crud/crudAPI";

function PlayersPage() {
  const { GET } = useAPI();

  const [selectedCountry, setSelectedCountry] = useState(null);
  const [procData, setProcData] = useState(null);
  const [countries, setCountries] = useState([]);

  const handleCountryChange = (event, newValue) => {
    setSelectedCountry(newValue);
  };

  useEffect(() => {
    GET("/countries")
      .then((result) => {
        if (result.data) {
          setCountries(result.data);
        } else {
          setCountries([]);
        }
      })
      .catch((error) => {
        console.error("Erro:", error);
        setCountries([]);
      });
  }, []);

  useEffect(() => {
    if (selectedCountry) {
      GET(`/playersByCountry?nome_pais=${selectedCountry}`)
        .then((result) => {
          if (result.data) {
            const apidata = result.data.map((player) => {
              return { player: player };
            });
            setProcData(apidata);
          } else {
            setProcData([]);
          }
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
          setProcData([]);
        });
    }
  }, [selectedCountry]);

  return (
    <Container>
      <Box mt={4}>
        <Typography variant="h2" gutterBottom>
          Country
        </Typography>

        <Autocomplete
          id="country-selector"
          options={countries}
          getOptionLabel={(option) => option.toString()}
          value={selectedCountry}
          onChange={handleCountryChange}
          renderInput={(params) => (
            <TextField {...params} label="Select or enter a country" variant="outlined" />
          )}
        />

        {procData ? (
          <>
            <Typography variant="h5" gutterBottom>
              {procData.length > 0
                ? `Jogadores: "${selectedCountry}"`
                : `Não ha nada nengue"${selectedCountry}"`}
            </Typography>
            {procData.map((item, index) => (
              <Paper key={index} elevation={3} sx={{ padding: "1rem", margin: "1rem" }}>
                <ListItem>
                  <ListItemText primary={item.brand} />
                </ListItem>
              </Paper>
            ))}
          </>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
            <CircularProgress />
          </div>
        )}
      </Box>
    </Container>
  );
}

export default PlayersPage;