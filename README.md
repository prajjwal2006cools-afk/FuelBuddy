# FUEL BUDDY

FUEL BUDDY is a production-quality web app built to help users fuel smarter and drive further. It provides tools for finding the cheapest fuel stations, locating EV chargers, planning cost-efficient trips, and predicting fuel consumption using machine learning.

## Tech Stack
- **Frontend**: Pure HTML5, CSS3 (with CSS variables), and vanilla JavaScript.
- **Backend**: Python 3.11+ with FastAPI.
- **Database**: SQLite via SQLAlchemy.
- **AI / ML**: scikit-learn models.
- **Auth**: Phone number + OTP login using JWT.
- **Maps**: Leaflet.js with OpenStreetMap.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Copy the example environment file and customize it if needed.
   ```bash
   cp .env.example .env
   ```

3. **Train ML Models**:
   The application relies on ML models for fuel consumption prediction.
   ```bash
   python backend/ml/train.py
   ```

4. **Run the Application**:
   Start the FastAPI development server:
   ```bash
   uvicorn backend.main:app --reload
   ```

5. **Access the App**:
   Open your browser and navigate to `http://127.0.0.1:8000`.

## Testing
To run the automated test suite using pytest:
```bash
PYTHONPATH=. pytest backend/tests/
```

## Features Complete
- OTP Auth (Dev mode fallback included)
- Vehicle profile management
- Fuel guide and unit converter
- Station and EV Charger locators with Leaflet Maps
- Trip Planner for calculating fuel costs and CO2 emissions
- Dashboard with ML insights
