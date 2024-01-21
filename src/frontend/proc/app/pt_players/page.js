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

function PTPlayersPage() {
  const { GET } = useAPI();

  const [ptPlayers, setPTPlayers] = useState([]);

  useEffect(() => {
    const fetchPTPlayers = async () => {
      try {
        const result = await GET("/pt_players"); // Ajuste aqui para o endpoint correto
        if (result.data) {
          setPTPlayers(result.data);
        } else {
          setPTPlayers([]);
        }
      } catch (error) {
        console.error("Error fetching PT players:", error);
        setPTPlayers([]);
      }
    };

    fetchPTPlayers();
  }, []);

  return (
    <Container maxWidth="md">
      <Box my={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          PT Players
        </Typography>
        <Paper>
          <Box p={2}>
            {ptPlayers.length > 0 ? (
              <Box>
                {ptPlayers.map((player, index) => (
                  <ListItem key={index}>
                  <ListItemText
                    primary={`${player.nome} - Overall: ${player.overall}`}
                    secondary={`Height: ${player.height}, Potencial: ${player.potencial}, Price: ${player.price}, Salary: ${player.salary}`}
                  />
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

export default PTPlayersPage;
