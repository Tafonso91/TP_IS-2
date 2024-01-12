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
} from "@mui/material";
import useAPI from "../crud/crudAPI";

function CountriesPage() {
  const { GET } = useAPI();

  const [countries, setCountries] = useState([]);

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
        console.error("Error fetching countries:", error);
        setCountries([]);
      }
    };

    fetchCountries();
  }, []);

  return (
    <Container maxWidth="md">
      <Box my={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          List of Countries
        </Typography>
        <Paper>
          <Box p={2}>
            {countries.length > 0 ? (
              <Box>
                {countries.map((country, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={country[0]} />
                  </ListItem>
                ))}
              </Box>
            ) : (
              <CircularProgress />
            )}
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}

export default CountriesPage;
