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

function PlayersPage() {
  const { GET } = useAPI();

  const [players, setPlayers] = useState([]);

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const result = await GET("/players");
        if (result.data) {
          setPlayers(result.data);
        } else {
          setPlayers([]);
        }
      } catch (error) {
        console.error("Error fetching players:", error);
        setPlayers([]);
      }
    };

    fetchPlayers();
  }, []);

  return (
    <Container maxWidth="md">
      <Box my={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          List of Players
        </Typography>
        <Paper>
          <Box p={2}>
            {players.length > 0 ? (
              <Box>
                {players.map((player, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={player[0]} />
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

export default PlayersPage;
