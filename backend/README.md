# IPL Stats Backend API

FastAPI application serving IPL player statistics derived from ball-by-ball datasets.

## Setup & Running

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --port 8000
```

## Health Check
- GET `http://localhost:8000/health`
