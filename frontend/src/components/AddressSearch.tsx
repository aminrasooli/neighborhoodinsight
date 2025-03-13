import React, { useState } from 'react';
import {
  Paper,
  TextField,
  Button,
  Box,
  Typography,
  Autocomplete,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import LocationOnIcon from '@mui/icons-material/LocationOn';

interface AddressSearchProps {
  onAddressSelect: (address: string) => void;
}

const sampleAddresses = [
  // Mission District
  "123 Valencia St, San Francisco, CA",
  "456 Mission St, San Francisco, CA",
  "789 Guerrero St, San Francisco, CA",
  "321 24th St, San Francisco, CA",
  "654 Dolores St, San Francisco, CA",
  
  // Pacific Heights
  "321 Fillmore St, San Francisco, CA",
  "654 Broadway St, San Francisco, CA",
  "987 Pacific Ave, San Francisco, CA",
  "456 Jackson St, San Francisco, CA",
  "789 Washington St, San Francisco, CA",
  
  // Hayes Valley
  "123 Hayes St, San Francisco, CA",
  "456 Gough St, San Francisco, CA",
  "789 Octavia St, San Francisco, CA",
  "321 Franklin St, San Francisco, CA",
  "654 Laguna St, San Francisco, CA",
  
  // North Beach
  "123 Columbus Ave, San Francisco, CA",
  "456 Grant Ave, San Francisco, CA",
  "789 Stockton St, San Francisco, CA",
  "321 Broadway St, San Francisco, CA",
  "654 Francisco St, San Francisco, CA",
  
  // Marina District
  "123 Chestnut St, San Francisco, CA",
  "456 Union St, San Francisco, CA",
  "789 Lombard St, San Francisco, CA",
  "321 Marina Blvd, San Francisco, CA",
  "654 Bay St, San Francisco, CA",
  
  // Russian Hill
  "123 Hyde St, San Francisco, CA",
  "456 Leavenworth St, San Francisco, CA",
  "789 Jones St, San Francisco, CA",
  "321 Taylor St, San Francisco, CA",
  "654 Vallejo St, San Francisco, CA",
  
  // Noe Valley
  "123 24th St, San Francisco, CA",
  "456 Church St, San Francisco, CA",
  "789 Castro St, San Francisco, CA",
  "321 Sanchez St, San Francisco, CA",
  "654 Dolores St, San Francisco, CA",
  
  // Financial District
  "123 Market St, San Francisco, CA",
  "456 Montgomery St, San Francisco, CA",
  "789 California St, San Francisco, CA",
  "321 Battery St, San Francisco, CA",
  "654 Sansome St, San Francisco, CA"
];

const AddressSearch: React.FC<AddressSearchProps> = ({ onAddressSelect }) => {
  const [address, setAddress] = useState<string | null>(null);

  const handleSearch = () => {
    if (address) {
      onAddressSelect(address);
    }
  };

  return (
    <Paper 
      elevation={3} 
      sx={{ 
        p: 3, 
        mb: 4, 
        background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
        color: 'white'
      }}
    >
      <Typography variant="h5" gutterBottom>
        Find Your Neighborhood
      </Typography>
      <Typography variant="body1" sx={{ mb: 3 }}>
        Enter your address to discover insights about your neighborhood
      </Typography>
      
      <Box sx={{ display: 'flex', gap: 2 }}>
        <Autocomplete
          fullWidth
          freeSolo
          options={sampleAddresses}
          value={address}
          onChange={(_, newValue) => setAddress(newValue)}
          renderInput={(params) => (
            <TextField
              {...params}
              placeholder="Enter your address"
              variant="outlined"
              sx={{ 
                backgroundColor: 'white',
                borderRadius: 1,
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: 'transparent',
                  },
                  '&:hover fieldset': {
                    borderColor: 'transparent',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: 'transparent',
                  },
                },
              }}
            />
          )}
          renderOption={(props, option) => (
            <li {...props}>
              <LocationOnIcon sx={{ mr: 1, color: 'primary.main' }} />
              {option}
            </li>
          )}
        />
        <Button
          variant="contained"
          onClick={handleSearch}
          sx={{ 
            bgcolor: 'white', 
            color: 'primary.main',
            '&:hover': {
              bgcolor: 'grey.100',
            }
          }}
          startIcon={<SearchIcon />}
        >
          Search
        </Button>
      </Box>
    </Paper>
  );
};

export default AddressSearch; 