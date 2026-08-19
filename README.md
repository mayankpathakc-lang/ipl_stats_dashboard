# 🏏 IPL Player Stats Dashboard

A full-stack portfolio application that aggregates and visualizes Indian Premier League (IPL) player performance metrics derived from ball-by-ball datasets, featuring phase-wise batting strike rates and death-over bowling economy rates.

![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18+-61DAFB.svg?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-8+-646CFF.svg?logo=vite&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/pytest-24%20passed-success.svg)

---

## ✨ Features

- **Phase-Wise Batting Insights**:
  - **Powerplay SR (Overs 1–6)**: Measure top-order explosion and fielding restriction exploitation
  - **Middle Overs SR (Overs 7–15)**: Assess spin handling and strike rotation
  - **Death Overs SR (Overs 16–20)**: Highlight explosive finish capabilities
- **Critical Bowling Metrics**:
  - **Death-Over Economy (Overs 16–20)**: Identify clutch death bowlers
  - **Overall Bowling Economy & Dot Ball %**: Comprehensive bowler efficiency
- **Interactive Single-Page UI**:
  - Instant debounced search by player name
  - Multi-criteria filtering by **Season** (2021–2024), **Role** (*Batsman, Bowler, All-Rounder, Wicket-Keeper*), and **Team** (*RCB, CSK, MI, KKR, SRH, etc.*)
  - Bi-directional table column sorting with active indicators
  - Dynamic KPI highlight cards (Top Run Scorer, Top Wicket-Taker, Best Strike Rate, Best Death Economy)
  - Responsive pagination and skeleton loading states
- **Production-Hardened Security**:
  - Strict CORS allowlists, TrustedHost middleware, Security HTTP Headers
  - Parameter sanitation, sort column allowlists, regex path parameter validation

---

## 🏗️ Architecture & Project Structure

```
ipl-project/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, security middleware, CORS & error handling
│   │   ├── routes/
│   │   │   └── players.py       # REST endpoints (/api/players, /filters, /summary, /{id})
│   │   ├── services/
│   │   │   └── stats.py         # Pandas-based filtering, sorting, pagination & caching
│   │   └── models/
│   │       └── schemas.py       # Pydantic models & response envelopes
│   ├── data/
│   │   └── ipl_player_stats.csv # Aggregated IPL ball-by-ball dataset
│   ├── tests/
│   │   ├── test_routes.py       # Route & security test suite (TestClient)
│   │   └── test_services.py     # Statistics service unit tests
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SearchBar.jsx    # Debounced search bar with clear button
│   │   │   ├── FilterPanel.jsx  # Season, Role & Team dropdown filters + Reset
│   │   │   ├── StatCard.jsx     # Glassmorphic summary metric cards
│   │   │   ├── PlayerTable.jsx  # Sortable data table with role badges & empty state
│   │   │   └── Pagination.jsx   # Smart pagination with ellipsis navigation
│   │   ├── hooks/
│   │   │   └── usePlayers.js    # Custom hook managing filter, sort, debounce & pagination state
│   │   ├── utils/
│   │   │   └── api.js           # Axios API utility
│   │   ├── App.jsx              # Main dashboard shell
│   │   └── App.css / index.css  # Dark theme design system with glassmorphism & gradients
│   └── vite.config.js           # Vite dev server with /api proxy to FastAPI
│
└── README.md
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create & activate a virtual environment (optional but recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend test suite (24 tests)
python -m pytest tests/ -v

# Start FastAPI development server
uvicorn app.main:app --reload --port 8000
```
Backend API will be running at `http://localhost:8000` (Health check: `http://localhost:8000/health`).

---

### 2. Frontend Setup

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
Open **`http://localhost:3000`** in your browser to view the dashboard!

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Service health check |
| `GET` | `/api/players` | Query paginated players with `search`, `season`, `role`, `team`, `sort_by`, `sort_order`, `page`, `page_size` |
| `GET` | `/api/players/filters` | Distinct available filter values (`seasons`, `roles`, `teams`) |
| `GET` | `/api/players/summary` | Top metrics highlights (`highest_runs`, `highest_wickets`, `best_strike_rate`, `best_death_economy`) |
| `GET` | `/api/players/{player_id}` | Multi-season performance history for a specific player |

---

## 🧪 Testing

```bash
cd backend
python -m pytest tests/ -v
```

All 24 automated unit and integration tests verify:
- Dataset loading and fallback handling
- Multi-criteria filtering (search, season, role, team)
- Ascending and descending column sorting
- Pagination slicing and boundaries
- Summary metric calculations
- Security headers presence
- Parameter length, range, and format validation
- Directory traversal & injection protection

---

## 📄 License
MIT License. Built for portfolio demonstration.
