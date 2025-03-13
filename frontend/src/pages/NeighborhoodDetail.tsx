import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Tabs,
  Tab,
  Rating,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
} from '@mui/material';
import {
  School,
  DirectionsTransit,
  LocalPolice,
  Restaurant,
  Park,
  Home,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const mockPriceHistory = [
  { month: 'Jan', price: 1200000 },
  { month: 'Feb', price: 1250000 },
  { month: 'Mar', price: 1230000 },
  { month: 'Apr', price: 1280000 },
  { month: 'May', price: 1300000 },
  { month: 'Jun', price: 1320000 },
];

const NeighborhoodDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: Replace with actual API call
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  }, [id]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        {decodeURIComponent(id || '')}
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="Overview" />
          <Tab label="Real Estate" />
          <Tab label="Safety" />
          <Tab label="Education" />
          <Tab label="Transportation" />
          <Tab label="Amenities" />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Neighborhood Scores
              </Typography>
              <List>
                <ListItem>
                  <ListItemIcon>
                    <LocalPolice />
                  </ListItemIcon>
                  <ListItemText primary="Safety Score" />
                  <Rating value={4} readOnly />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <School />
                  </ListItemIcon>
                  <ListItemText primary="Education Score" />
                  <Rating value={4.5} readOnly />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <DirectionsTransit />
                  </ListItemIcon>
                  <ListItemText primary="Transit Score" />
                  <Rating value={5} readOnly />
                </ListItem>
              </List>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Key Features
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                <Chip icon={<Restaurant />} label="245 Restaurants" />
                <Chip icon={<Park />} label="8 Parks" />
                <Chip icon={<School />} label="5 Schools" />
                <Chip icon={<DirectionsTransit />} label="4 Transit Lines" />
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Price History
              </Typography>
              <Box sx={{ height: 300 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={mockPriceHistory}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="price"
                      stroke="#8884d8"
                      activeDot={{ r: 8 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Housing Stats
              </Typography>
              <List>
                <ListItem>
                  <ListItemIcon>
                    <Home />
                  </ListItemIcon>
                  <ListItemText
                    primary="Median Price"
                    secondary="$1,200,000"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <Home />
                  </ListItemIcon>
                  <ListItemText
                    primary="Price per Sq Ft"
                    secondary="$1,000"
                  />
                </ListItem>
              </List>
            </Paper>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Additional tab panels for Safety, Education, Transportation, and Amenities */}
    </Container>
  );
};

export default NeighborhoodDetail; 