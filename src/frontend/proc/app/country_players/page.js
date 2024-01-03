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

function ClubsPage() {
  const { GET } = useAPI();

  const [selectedClub, setSelectedClub] = useState("");
  const [Data, setData] = useState(null);
  const [clubs, setClubs] = useState([]);

  const handleClubChange = async (event) => {
    const newValue = event.target.value;
    setSelectedClub(newValue);

    try {
      const result = await GET(`/players_club?nome_club=${newValue}`);
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
    const fetchClubs = async () => {
      try {
        const result = await GET("/clubs");
        if (result.data) {
          setClubs(result.data);
        } else {
          setClubs([]);
        }
      } catch (error) {
        console.error("Erro:", error);
        setClubs([]);
      }
    };

    fetchClubs();
  }, []);

  return (
    <Container maxWidth="md">
      <Box my={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Players by Club
        </Typography>
        <FormControl variant="outlined" fullWidth>
          <InputLabel id="club-select-label">Pick a club</InputLabel>
          <Select
            labelId="club-select-label"
            id="club-select"
            value={selectedClub}
            onChange={handleClubChange}
            label="Select Club"
          >
            {clubs.map((club, index) => (
              <MenuItem key={index} value={club[0]}>
                {club[0]}
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
                selectedClub ? <CircularProgress /> : "--"
              )}
            </Box>
          </Paper>
        </Box>
      </Box>
    </Container>
  );
}

export default ClubsPage;