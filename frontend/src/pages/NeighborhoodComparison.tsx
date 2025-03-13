import React, { useState } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Autocomplete,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from 'recharts';

interface NeighborhoodData {
  name: string;
  safetyScore: number;
  educationScore: number;
  transitScore: number;
  amenitiesScore: number;
  averagePrice: number;
  crimeRate: string;
  schoolRating: string;
  walkScore: number;
  transitAccess: string;
  restaurants: number;
  parks: number;
}

const mockNeighborhoods: NeighborhoodData[] = [
  {
    name: "Mission District",
    safetyScore: 7.5,
    educationScore: 8.2,
    transitScore: 9.0,
    amenitiesScore: 8.8,
    averagePrice: 1200000,
    crimeRate: "Moderate",
    schoolRating: "Above Average",
    walkScore: 96,
    transitAccess: "Excellent",
    restaurants: 245,
    parks: 8
  },
  {
    name: "Pacific Heights",
    safetyScore: 9.2,
    educationScore: 9.5,
    transitScore: 7.8,
    amenitiesScore: 8.5,
    averagePrice: 2500000,
    crimeRate: "Low",
    schoolRating: "Excellent",
    walkScore: 87,
    transitAccess: "Good",
    restaurants: 156,
    parks: 5
  }
];

const NeighborhoodComparison: React.FC = () => {
  const [neighborhood1, setNeighborhood1] = useState<NeighborhoodData | null>(null);
  const [neighborhood2, setNeighborhood2] = useState<NeighborhoodData | null>(null);

  const getRadarData = (neighborhood: NeighborhoodData) => [
    { subject: 'Safety', A: neighborhood.safetyScore },
    { subject: 'Education', A: neighborhood.educationScore },
    { subject: 'Transit', A: neighborhood.transitScore },
    { subject: 'Amenities', A: neighborhood.amenitiesScore },
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Compare Neighborhoods
      </Typography>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <Autocomplete
            options={mockNeighborhoods}
            getOptionLabel={(option) => option.name}
            value={neighborhood1}
            onChange={(_, newValue) => setNeighborhood1(newValue)}
            renderInput={(params) => (
              <TextField {...params} label="Select First Neighborhood" />
            )}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <Autocomplete
            options={mockNeighborhoods}
            getOptionLabel={(option) => option.name}
            value={neighborhood2}
            onChange={(_, newValue) => setNeighborhood2(newValue)}
            renderInput={(params) => (
              <TextField {...params} label="Select Second Neighborhood" />
            )}
          />
        </Grid>
      </Grid>

      {neighborhood1 && neighborhood2 && (
        <>
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 2, height: 300 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={getRadarData(neighborhood1)}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="subject" />
                    <PolarRadiusAxis domain={[0, 10]} />
                    <Radar
                      name={neighborhood1.name}
                      dataKey="A"
                      stroke="#8884d8"
                      fill="#8884d8"
                      fillOpacity={0.6}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </Paper>
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 2, height: 300 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={getRadarData(neighborhood2)}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="subject" />
                    <PolarRadiusAxis domain={[0, 10]} />
                    <Radar
                      name={neighborhood2.name}
                      dataKey="A"
                      stroke="#82ca9d"
                      fill="#82ca9d"
                      fillOpacity={0.6}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </Paper>
            </Grid>
          </Grid>

          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Metric</TableCell>
                  <TableCell>{neighborhood1.name}</TableCell>
                  <TableCell>{neighborhood2.name}</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                <TableRow>
                  <TableCell>Average Price</TableCell>
                  <TableCell>${neighborhood1.averagePrice.toLocaleString()}</TableCell>
                  <TableCell>${neighborhood2.averagePrice.toLocaleString()}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Crime Rate</TableCell>
                  <TableCell>{neighborhood1.crimeRate}</TableCell>
                  <TableCell>{neighborhood2.crimeRate}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>School Rating</TableCell>
                  <TableCell>{neighborhood1.schoolRating}</TableCell>
                  <TableCell>{neighborhood2.schoolRating}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Walk Score</TableCell>
                  <TableCell>{neighborhood1.walkScore}</TableCell>
                  <TableCell>{neighborhood2.walkScore}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Transit Access</TableCell>
                  <TableCell>{neighborhood1.transitAccess}</TableCell>
                  <TableCell>{neighborhood2.transitAccess}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Number of Restaurants</TableCell>
                  <TableCell>{neighborhood1.restaurants}</TableCell>
                  <TableCell>{neighborhood2.restaurants}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Number of Parks</TableCell>
                  <TableCell>{neighborhood1.parks}</TableCell>
                  <TableCell>{neighborhood2.parks}</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}
    </Container>
  );
};

export default NeighborhoodComparison; 