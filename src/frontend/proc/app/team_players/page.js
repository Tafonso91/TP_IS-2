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
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";
import useAPI from "../crud/crudAPI";

function PlayersPage() {
  const { GET } = useAPI();

  const [selectedCountry, setSelectedCountry] = useState("");
  const [Data, setData] = useState(null);
  const [countries, setCountries] = useState([]);

  const handleCountryChange = async (event) => {
    const newValue = event.target.value;
    setSelectedCountry(newValue);

    try {
      const result = await GET(`/players_country?nome_pais=${newValue}`);
      if (result.data) {
        const apidata = result.data.map((player) => {
          return { player: player };
        });
        setData(apidata);
      } else {
        setData([]);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      setData([]);
    }
  };

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const result = await GET("/countries");
        if (result.data) {
          setCountries(result.data);
        } else {
          setCountries([]);
        }
      } catch (error) {
        console.error("Erro:", error);
        setCountries([]);
      }
    };

    fetchCountries();
  }, []);

  return (
    <Container maxWidth="md">
      <Box my={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Players by Country
        </Typography>
        <FormControl variant="outlined" fullWidth>
          <InputLabel id="country-select-label">Escolhe um país</InputLabel>
          <Select
            labelId="country-select-label"
            id="country-select"
            value={selectedCountry}
            onChange={handleCountryChange}
            label="Select Country"
          >
            {countries.map((country, index) => (
              <MenuItem key={index} value={country[0]}>
                {country[0]}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Box mt={2}>
          <Paper>
            <Box p={2}>
              {Data ? (
                <Box>
                  {Data.map((data, index) => (
                    <ListItem key={index}>
                      <ListItemText primary={data.player[0]} />
                    </ListItem>
                  ))}
                </Box>
              ) : (
                selectedCountry ? <CircularProgress /> : "--"
              )}
            </Box>
          </Paper>
        </Box>
      </Box>
    </Container>
  );
}

export default PlayersPage;


