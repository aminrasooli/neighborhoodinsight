import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
} from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import CompareIcon from '@mui/icons-material/Compare';

const Navbar: React.FC = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Neighborhood Insights
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            color="inherit"
            component={RouterLink}
            to="/"
            startIcon={<HomeIcon />}
          >
            Dashboard
          </Button>
          <Button
            color="inherit"
            component={RouterLink}
            to="/compare"
            startIcon={<CompareIcon />}
          >
            Compare
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar; 