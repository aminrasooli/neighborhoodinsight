import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Rating,
  Chip,
  LinearProgress,
  Alert,
  TextField,
  MenuItem,
  Slider,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import AddressSearch from '../components/AddressSearch';
import NeighborhoodReviews from '../components/NeighborhoodReviews';
import { School, DirectionsTransit } from '@mui/icons-material';

interface NeighborhoodData {
  name: string;
  safetyScore: number;
  educationScore: number;
  transitScore: number;
  amenitiesScore: number;
  averagePrice: number;
  topFeatures: string[];
  boundaries: {
    addresses: string[];
  };
}

const mockNeighborhoods: NeighborhoodData[] = [
  {
    name: "Mission District",
    safetyScore: 6.8,
    educationScore: 7.5,
    transitScore: 9.2,
    amenitiesScore: 9.5,
    averagePrice: 1200000,
    topFeatures: ["Vibrant Culture", "Food Scene", "Street Art", "Nightlife"],
    boundaries: {
      addresses: [
        "123 Valencia St",
        "456 Mission St",
        "789 Guerrero St",
        "321 24th St",
        "654 Dolores St"
      ]
    }
  },
  {
    name: "Pacific Heights",
    safetyScore: 9.5,
    educationScore: 9.8,
    transitScore: 7.2,
    amenitiesScore: 8.0,
    averagePrice: 2800000,
    topFeatures: ["Luxury Homes", "Bay Views", "Private Schools", "Upscale Shopping"],
    boundaries: {
      addresses: [
        "321 Fillmore St",
        "654 Broadway St",
        "987 Pacific Ave",
        "456 Jackson St",
        "789 Washington St"
      ]
    }
  },
  {
    name: "Hayes Valley",
    safetyScore: 8.2,
    educationScore: 8.0,
    transitScore: 9.0,
    amenitiesScore: 9.3,
    averagePrice: 1650000,
    topFeatures: ["Boutique Shopping", "Performing Arts", "Trendy Restaurants", "Modern Condos"],
    boundaries: {
      addresses: [
        "123 Hayes St",
        "456 Gough St",
        "789 Octavia St",
        "321 Franklin St",
        "654 Laguna St"
      ]
    }
  },
  {
    name: "North Beach",
    safetyScore: 8.5,
    educationScore: 7.8,
    transitScore: 8.7,
    amenitiesScore: 9.4,
    averagePrice: 1450000,
    topFeatures: ["Italian Heritage", "Tourist Spots", "Historic Cafes", "Comedy Clubs"],
    boundaries: {
      addresses: [
        "123 Columbus Ave",
        "456 Grant Ave",
        "789 Stockton St",
        "321 Broadway St",
        "654 Francisco St"
      ]
    }
  },
  {
    name: "Marina District",
    safetyScore: 9.2,
    educationScore: 8.5,
    transitScore: 7.8,
    amenitiesScore: 9.0,
    averagePrice: 2200000,
    topFeatures: ["Marina Views", "Fitness Studios", "Brunch Spots", "Palace of Fine Arts"],
    boundaries: {
      addresses: [
        "123 Chestnut St",
        "456 Union St",
        "789 Lombard St",
        "321 Marina Blvd",
        "654 Bay St"
      ]
    }
  },
  {
    name: "Russian Hill",
    safetyScore: 9.0,
    educationScore: 8.7,
    transitScore: 7.5,
    amenitiesScore: 8.3,
    averagePrice: 2100000,
    topFeatures: ["Scenic Views", "Crooked Street", "Hidden Staircases", "Classic Architecture"],
    boundaries: {
      addresses: [
        "123 Hyde St",
        "456 Leavenworth St",
        "789 Jones St",
        "321 Taylor St",
        "654 Vallejo St"
      ]
    }
  },
  {
    name: "Noe Valley",
    safetyScore: 9.4,
    educationScore: 9.3,
    transitScore: 7.8,
    amenitiesScore: 8.5,
    averagePrice: 1950000,
    topFeatures: ["Family-Friendly", "Farmers Market", "Stroller Valley", "Victorian Homes"],
    boundaries: {
      addresses: [
        "123 24th St",
        "456 Church St",
        "789 Castro St",
        "321 Sanchez St",
        "654 Dolores St"
      ]
    }
  },
  {
    name: "Financial District",
    safetyScore: 8.0,
    educationScore: 7.5,
    transitScore: 9.8,
    amenitiesScore: 8.8,
    averagePrice: 1350000,
    topFeatures: ["Business Hub", "High-rises", "Transit Hub", "Fine Dining"],
    boundaries: {
      addresses: [
        "123 Market St",
        "456 Montgomery St",
        "789 California St",
        "321 Battery St",
        "654 Sansome St"
      ]
    }
  }
];

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [neighborhoods, setNeighborhoods] = useState<NeighborhoodData[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedNeighborhood, setSelectedNeighborhood] = useState<NeighborhoodData | null>(null);
  const [searchAlert, setSearchAlert] = useState<{type: 'success' | 'info' | 'warning'; message: string} | null>(null);
  const [sortBy, setSortBy] = useState<'price' | 'safety' | 'education' | 'transit' | 'amenities'>('price');
  const [priceRange, setPriceRange] = useState<[number, number]>([0, 3000000]);
  const [selectedFeatures, setSelectedFeatures] = useState<string[]>([]);

  useEffect(() => {
    // TODO: Replace with actual API call
    setNeighborhoods(mockNeighborhoods);
    setLoading(false);
  }, []);

  const handleAddressSearch = (address: string) => {
    const foundNeighborhood = mockNeighborhoods.find(n => 
      n.boundaries.addresses.some(a => 
        address.toLowerCase().includes(a.toLowerCase())
      )
    );

    if (foundNeighborhood) {
      setSelectedNeighborhood(foundNeighborhood);
      setSearchAlert({
        type: 'success',
        message: `Found your neighborhood: ${foundNeighborhood.name}`
      });
    } else {
      setSearchAlert({
        type: 'warning',
        message: 'Could not find a matching neighborhood. Showing all neighborhoods instead.'
      });
      setSelectedNeighborhood(null);
    }
  };

  const handleNeighborhoodClick = (name: string) => {
    navigate(`/neighborhood/${encodeURIComponent(name)}`);
  };

  const filteredNeighborhoods = neighborhoods
    .filter(n => {
      const priceInRange = n.averagePrice >= priceRange[0] && n.averagePrice <= priceRange[1];
      const hasSelectedFeatures = selectedFeatures.length === 0 || 
        selectedFeatures.every(feature => n.topFeatures.includes(feature));
      return priceInRange && hasSelectedFeatures;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'price':
          return b.averagePrice - a.averagePrice;
        case 'safety':
          return b.safetyScore - a.safetyScore;
        case 'education':
          return b.educationScore - a.educationScore;
        case 'transit':
          return b.transitScore - a.transitScore;
        case 'amenities':
          return b.amenitiesScore - a.amenitiesScore;
        default:
          return 0;
      }
    });

  if (loading) {
    return <LinearProgress />;
  }

  const displayedNeighborhoods = selectedNeighborhood ? [selectedNeighborhood] : filteredNeighborhoods;

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <AddressSearch onAddressSelect={handleAddressSearch} />
      
      {searchAlert && (
        <Alert severity={searchAlert.type} sx={{ mb: 3 }} onClose={() => setSearchAlert(null)}>
          {searchAlert.message}
        </Alert>
      )}

      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4">
          San Francisco Neighborhoods
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <TextField
            select
            label="Sort By"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            sx={{ minWidth: 150 }}
          >
            <MenuItem value="price">Price</MenuItem>
            <MenuItem value="safety">Safety</MenuItem>
            <MenuItem value="education">Education</MenuItem>
            <MenuItem value="transit">Transit</MenuItem>
            <MenuItem value="amenities">Amenities</MenuItem>
          </TextField>
        </Box>
      </Box>

      <Box sx={{ mb: 4 }}>
        <Typography variant="subtitle1" gutterBottom>
          Price Range
        </Typography>
        <Slider
          value={priceRange}
          onChange={(_, newValue) => setPriceRange(newValue as [number, number])}
          valueLabelDisplay="auto"
          min={0}
          max={3000000}
          step={100000}
          marks
        />
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
          <Typography variant="caption">
            ${priceRange[0].toLocaleString()}
          </Typography>
          <Typography variant="caption">
            ${priceRange[1].toLocaleString()}
          </Typography>
        </Box>
      </Box>

      <Box sx={{ mb: 4 }}>
        <Typography variant="subtitle1" gutterBottom>
          Features
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {Array.from(new Set(neighborhoods.flatMap(n => n.topFeatures))).map(feature => (
            <Chip
              key={feature}
              label={feature}
              onClick={() => {
                setSelectedFeatures(prev =>
                  prev.includes(feature)
                    ? prev.filter(f => f !== feature)
                    : [...prev, feature]
                );
              }}
              color={selectedFeatures.includes(feature) ? 'primary' : 'default'}
            />
          ))}
        </Box>
      </Box>
      
      <Grid container spacing={3}>
        {displayedNeighborhoods.map((neighborhood) => (
          <Grid item xs={12} md={6} key={neighborhood.name}>
            <Card 
              onClick={() => handleNeighborhoodClick(neighborhood.name)}
              sx={{ 
                cursor: 'pointer',
                '&:hover': { boxShadow: 6 }
              }}
            >
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {neighborhood.name}
                </Typography>
                
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Overall Rating
                  </Typography>
                  <Rating 
                    value={(neighborhood.safetyScore + neighborhood.educationScore + 
                           neighborhood.transitScore + neighborhood.amenitiesScore) / 4}
                    precision={0.5}
                    readOnly
                  />
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Average Price
                  </Typography>
                  <Typography variant="body1">
                    ${neighborhood.averagePrice.toLocaleString()}
                  </Typography>
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Key Features
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    {neighborhood.topFeatures.map((feature) => (
                      <Chip 
                        key={feature} 
                        label={feature} 
                        size="small"
                        color={selectedFeatures.includes(feature) ? 'primary' : 'default'}
                      />
                    ))}
                  </Box>
                </Box>

                <Box sx={{ height: 200 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={[
                        { name: 'Safety', score: neighborhood.safetyScore },
                        { name: 'Education', score: neighborhood.educationScore },
                        { name: 'Transit', score: neighborhood.transitScore },
                        { name: 'Amenities', score: neighborhood.amenitiesScore },
                      ]}
                      margin={{ top: 10, right: 10, left: -10, bottom: 0 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis domain={[0, 10]} />
                      <Tooltip />
                      <Bar dataKey="score" fill="#2196f3" />
                    </BarChart>
                  </ResponsiveContainer>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {selectedNeighborhood && (
        <Box sx={{ mt: 4 }}>
          <NeighborhoodReviews 
            neighborhoodName={selectedNeighborhood.name}
            reviews={[]}
          />
        </Box>
      )}
    </Container>
  );
};

export default Dashboard; 