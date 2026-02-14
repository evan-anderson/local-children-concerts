# Boston Metro Child-Friendly Concerts

A web application to discover child-friendly concerts in the Boston metropolitan area, including Waltham, Newton, Lexington, Arlington, Somerville, Cambridge, and Boston.

## Features

- **Web UI**: React-based interface with filtering by town and date range
- **REST API**: FastAPI backend serving concert data
- **Data Scraping**: Python-based scrapers to collect concert data from multiple sources
- **Child-Friendly Filtering**: Automatically identifies concerts suitable for children based on keywords
- **Geographic Focus**: Targets Boston metro towns
- **Data Export**: Outputs to both JSON and CSV formats

## Project Structure

```
local-children-concerts/
├── api/                        # FastAPI backend
│   ├── main.py                 # App entry point with CORS
│   ├── routes/concerts.py      # API endpoints
│   └── services/concert_service.py  # Data loading and filtering
├── frontend/                   # React + TypeScript + Vite
│   ├── src/
│   │   ├── components/         # UI components
│   │   ├── hooks/              # Data fetching hooks
│   │   └── types/              # TypeScript interfaces
│   └── package.json
├── scraper/                    # Python scraping modules
│   ├── base_scraper.py         # Base scraper class and Concert model
│   ├── config.py               # Configuration (towns, keywords)
│   ├── pipeline.py             # Data processing pipeline
│   ├── library_events_scraper.py   # Config-driven library scraper
│   └── web_search_scraper.py   # Config-driven web scraper
├── data/                       # Output directory for scraped data
│   ├── concerts.json
│   └── concerts.csv
├── tests/                      # Test suite
├── main.py                     # Scraper entry point
└── pyproject.toml              # Python dependencies (uv)
```

## Setup

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- Node.js 18+ (for frontend)

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd local-children-concerts
```

2. Install Python dependencies:
```bash
uv sync
```

3. Install frontend dependencies:
```bash
cd frontend && npm install
```

## Usage

### Running the Web UI

Start both the API server and frontend dev server:

```bash
# Terminal 1: Start the API server
uv run uvicorn api.main:app --reload --port 8000

# Terminal 2: Start the frontend
cd frontend && npm run dev
```

Open http://localhost:5173 to browse concerts with filtering.

### API Endpoints

- `GET /api/concerts` - List concerts with optional filters:
  - `?towns=Boston&towns=Cambridge` - Filter by towns
  - `?start_date=2025-06-01&end_date=2025-12-31` - Filter by date range
- `GET /api/towns` - List available towns
- `GET /api/health` - Health check

### Running the Scrapers

**Quick Start with Mock Data:**

```bash
uv run python main.py --use-mock
```

**Scrape Real Websites:**

```bash
# Run all scrapers
uv run python main.py

# Run specific scraper groups
uv run python main.py --scrapers boston libraries web

# Available groups:
# - boston: Boston.gov events calendar
# - libraries: Boston & Cambridge Public Library events
# - web: Time Out Boston, Boston.com, BostonCentral
# - eventbrite: Eventbrite API (requires API key)
# - all: Run all scrapers (default)
```

### Running Tests

```bash
# Backend tests (Python)
uv run pytest -v

# Frontend tests (React)
cd frontend && npm test

# Backend with coverage
uv run pytest -v --cov=scraper
```

### Configuring Eventbrite Scraper

The Eventbrite scraper requires an API key:

```bash
export EVENTBRITE_API_KEY='your_api_key_here'
```

## Configuration

Edit `scraper/config.py` to customize:
- **Towns**: Add or remove Boston metro towns
- **Keywords**: Modify child-friendly detection keywords
- **Output paths**: Change where data files are saved

To add new data sources, edit the config dicts in `main.py`:

```python
# Add a library source
LIBRARY_SOURCES.append({
    "name": "Brookline Public Library",
    "base_url": "https://www.brooklinelibrary.org",
    "events_path": "/events/",
    "town": "Brookline",
})

# Add a web source
WEB_SOURCES.append({
    "name": "Boston Magazine",
    "base_url": "https://www.bostonmagazine.com",
    "endpoints": ["/events/"],
    "per_page_limit": 20,
})
```

## Output Data Format

### JSON Format
```json
[
  {
    "title": "Kids Rock Concert",
    "venue": "Symphony Hall",
    "town": "Boston",
    "date": "2025-06-15T14:00:00",
    "url": "https://example.com/event",
    "description": "A fun concert for the whole family",
    "address": "301 Massachusetts Ave, Boston, MA",
    "source": "BostonEvents",
    "scraped_at": "2025-01-15T10:30:00"
  }
]
```

## Contributing

Contributions are welcome! Areas where help is needed:
- Implementing scrapers for additional data sources
- Improving child-friendly keyword detection
- Adding geocoding and map visualization
- Enhancing the web UI

## License

MIT License - feel free to use and modify for your own projects.
