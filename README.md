# IPL Player Stats Dashboard

A full-stack portfolio application for visualizing aggregated IPL (Indian Premier League) player performance metrics derived from ball-by-ball data.

## Features
- **Phase-wise Batting Strike Rates**: Powerplay (1-6), Middle (7-15), Death (16-20)
- **Bowling Metrics**: Death-over economy, overall economy, dot ball percentage
- **FastAPI Backend**: Serves cleaned CSV data with filtering, sorting, and pagination options
- **React Frontend**: Modern, responsive single-page application with search, season/role filters, and sortable tables

## Project Structure
- `backend/`: FastAPI application, endpoints, and unit tests
- `frontend/`: React + Vite single-page application
- `backend/data/`: Aggregated IPL player stats dataset
