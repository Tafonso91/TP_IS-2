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

  const [selectedPlayer, setSelectedPlayer] = useState("");
  const [playerData, setPlayerData] = useState(null);
  const [players, setPlayers] = useState([]);

  const handlePlayerChange = async (event) => {
    const newValue = event.target.value;
    setSelectedPlayer(newValue);

    try {
      const result = await GET(`/stats_player?nome_jogador=${newValue}`);
      if (result.data) {
        setPlayerData(result.data);
      } else {
        setPlayerData(null);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      setPlayerData(null);
    }
  };

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
          Player Statistics
        </Typography>
        <FormControl variant="outlined" fullWidth>
          <InputLabel id="player-select-label">Pick a player</InputLabel>
          <Select
            labelId="player-select-label"
            id="player-select"
            value={selectedPlayer}
            onChange={handlePlayerChange}
            label="Select Player"
          >
            {players.map((player, index) => (
              <MenuItem key={index} value={player}>
                {player}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Box mt={2}>
          <Paper>
            <Box p={2}>
            {playerData ? (
  <Box>
    <ListItem>
      <ListItemText primary={`Player: ${selectedPlayer}`} />
    </ListItem>
    {playerData.map((stats, index) => (
      <Box key={index}>
        {Object.entries(stats).map(([key, value], innerIndex) => (
          <ListItem key={innerIndex}>
            <ListItemText primary={`${key}: ${value}`} />
          </ListItem>
        ))}
      </Box>
    ))}
  </Box>
) : (
  selectedPlayer ? <CircularProgress /> : "--"
)}
            </Box>
          </Paper>
        </Box>
      </Box>
    </Container>
  );
}

export default PlayersPage;

