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

function FeetPage() {
  const { GET } = useAPI();

  const [feet, setFeet] = useState([]);

  useEffect(() => {
    const fetchFeet = async () => {
      try {
        const result = await GET("/feet");
        if (result.data) {
          setFeet(result.data);
        } else {
          setFeet([]);
        }
      } catch (error) {
        console.error("Error fetching feet:", error);
        setFeet([]);
      }
    };

    fetchFeet();
  }, []);

  return (
    <Container maxWidth="md">
      <Box my={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          List of Feet
        </Typography>
        <Paper>
          <Box p={2}>
            {feet.length > 0 ? (
              <Box>
                {feet.map((foot, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={foot[0]} />
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

export default FeetPage;
