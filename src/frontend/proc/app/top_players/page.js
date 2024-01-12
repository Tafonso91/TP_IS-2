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

function TopPlayersPage() {
  const { GET } = useAPI();

  const [topPlayers, setTopPlayers] = useState([]);

  useEffect(() => {
    const fetchTopPlayers = async () => {
      try {
        const result = await GET("/top_players");
        if (result.data) {
          setTopPlayers(result.data);
        } else {
          setTopPlayers([]);
        }
      } catch (error) {
        console.error("Error fetching top players:", error);
        setTopPlayers([]);
      }
    };

    fetchTopPlayers();
  }, []);

  return (
    <Container maxWidth="md">
      <Box my={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Top Players
        </Typography>
        <Paper>
          <Box p={2}>
            {topPlayers.length > 0 ? (
              <Box>
                {topPlayers.map(([rating, playerName], index) => (
                  <ListItem key={index}>
                    <ListItemText primary={`${playerName} - Rating: ${rating}`} />
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

export default TopPlayersPage;
