# Neighborhood Insights API

This is a Flask-based API that provides insights about neighborhoods, including crime data, real estate trends, and resident complaints.

## Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
- On macOS/Linux:
```bash
source venv/bin/activate
```
- On Windows:
```bash
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

1. Start the Flask server:
```bash
python app.py
```

The server will start at `http://127.0.0.1:5000`

## API Endpoints

### Health Check
- **GET** `/health`
- Returns the API health status

### Get Neighborhood Insights
- **POST** `/get_insights`
- Request body:
```json
{
    "address": "San Francisco, CA"
}
```
- Returns neighborhood insights including:
  - Crime analysis
  - Real estate trends
  - Resident complaints

## Example Usage

```bash
curl -X POST http://127.0.0.1:5000/get_insights \
  -H "Content-Type: application/json" \
  -d '{"address": "San Francisco, CA"}'
```

## Note
This is a demo implementation with mock data. In a production environment, you would need to:
1. Replace mock data with real API integrations
2. Add proper error handling and validation
3. Implement security measures
4. Add rate limiting
5. Set up proper logging 