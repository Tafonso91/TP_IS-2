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

function ClubsPage() {
  const { GET } = useAPI();

  const [clubs, setClubs] = useState([]);

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
        console.error("Error fetching clubs:", error);
        setClubs([]);
      }
    };

    fetchClubs();
  }, []);

  return (
    <Container maxWidth="md">
      <Box my={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          List of Clubs
        </Typography>
        <Paper>
          <Box p={2}>
            {clubs.length > 0 ? (
              <Box>
                {clubs.map((club, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={club[0]} />
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

export default ClubsPage;
