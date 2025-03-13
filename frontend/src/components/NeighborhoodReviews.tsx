import React, { useState, useEffect } from 'react';
import {
  Paper,
  Typography,
  Box,
  Avatar,
  Rating,
  Chip,
  Divider,
} from '@mui/material';
import { format } from 'date-fns';

interface Review {
  id: string;
  author: string;
  rating: number;
  date: string;
  content: string;
  tags: string[];
  helpful: number;
}

interface NeighborhoodReviewsProps {
  neighborhoodName: string;
  reviews?: Review[];
}

// Neighborhood characteristics
const neighborhoodStats = {
  "Mission District": {
    avgRating: 3.8,
    ratingRange: 0.6,
    tags: ['Food', 'Culture', 'Nightlife', 'Transit'],
    helpfulBase: 15
  },
  "Pacific Heights": {
    avgRating: 4.7,
    ratingRange: 0.3,
    tags: ['Luxury', 'Views', 'Safety', 'Schools'],
    helpfulBase: 25
  },
  "Hayes Valley": {
    avgRating: 4.3,
    ratingRange: 0.4,
    tags: ['Shopping', 'Arts', 'Dining', 'Transit'],
    helpfulBase: 20
  },
  "North Beach": {
    avgRating: 4.2,
    ratingRange: 0.4,
    tags: ['Italian', 'Historic', 'Tourist', 'Food'],
    helpfulBase: 22
  },
  "Marina District": {
    avgRating: 4.4,
    ratingRange: 0.4,
    tags: ['Active', 'Views', 'Young', 'Shopping'],
    helpfulBase: 23
  },
  "Russian Hill": {
    avgRating: 4.5,
    ratingRange: 0.4,
    tags: ['Views', 'Historic', 'Quiet', 'Hills'],
    helpfulBase: 24
  },
  "Noe Valley": {
    avgRating: 4.6,
    ratingRange: 0.3,
    tags: ['Family', 'Safe', 'Shopping', 'Parks'],
    helpfulBase: 21
  },
  "Financial District": {
    avgRating: 3.9,
    ratingRange: 0.4,
    tags: ['Business', 'Transit', 'Modern', 'Dining'],
    helpfulBase: 18
  }
};

const NeighborhoodReviews: React.FC<NeighborhoodReviewsProps> = ({ neighborhoodName }) => {
  const [reviews, setReviews] = useState<Review[]>([]);

  useEffect(() => {
    const stats = neighborhoodStats[neighborhoodName] || {
      avgRating: 4.0,
      ratingRange: 0.5,
      tags: ['General'],
      helpfulBase: 20
    };

    const generateRating = () => {
      const min = Math.max(1, stats.avgRating - stats.ratingRange);
      const max = Math.min(5, stats.avgRating + stats.ratingRange);
      return Number((Math.random() * (max - min) + min).toFixed(1));
    };

    const generateHelpful = (rating: number) => {
      const base = stats.helpfulBase;
      return Math.floor(base * (rating / 5) * (0.8 + Math.random() * 0.4));
    };

    const generateReview = (id: string): Review => {
      const rating = generateRating();
      return {
        id,
        author: `User${id}`,
        rating,
        date: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        content: `Review for ${neighborhoodName}. Rating: ${rating}`,
        tags: stats.tags.slice(0, 2 + Math.floor(Math.random() * 3)),
        helpful: generateHelpful(rating)
      };
    };

    const newReviews = [
      generateReview('1'),
      generateReview('2')
    ];

    setReviews(newReviews);
  }, [neighborhoodName]);

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Recent Reviews for {neighborhoodName}
      </Typography>
      <Typography variant="subtitle2" color="text.secondary" gutterBottom>
        Average Rating: {neighborhoodStats[neighborhoodName]?.avgRating.toFixed(1) || "N/A"}
      </Typography>
      
      <Box sx={{ mt: 2 }}>
        {reviews.map((review, index) => (
          <React.Fragment key={review.id}>
            {index > 0 && <Divider sx={{ my: 3 }} />}
            <Box>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                  {review.author[0]}
                </Avatar>
                <Box>
                  <Typography variant="subtitle1">
                    {review.author}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Rating value={review.rating} precision={0.1} readOnly size="small" />
                    <Typography variant="caption" color="text.secondary">
                      {format(new Date(review.date), 'MMM d, yyyy')}
                    </Typography>
                  </Box>
                </Box>
              </Box>
              
              <Typography variant="body1" sx={{ my: 2 }}>
                {review.content}
              </Typography>
              
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 1 }}>
                {review.tags.map((tag) => (
                  <Chip
                    key={tag}
                    label={tag}
                    size="small"
                    variant="outlined"
                  />
                ))}
              </Box>
              
              <Typography variant="caption" color="text.secondary">
                {review.helpful} people found this helpful
              </Typography>
            </Box>
          </React.Fragment>
        ))}
      </Box>
    </Paper>
  );
};

export default NeighborhoodReviews; 