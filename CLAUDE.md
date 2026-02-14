# Claude Code Assistant Guide

This file contains important context for AI assistants working on this project.

## Package Management

**IMPORTANT: This project uses `uv` for dependency management, NOT pip.**

### Installing Dependencies
```bash
uv sync
```

### Running Commands
Always prefix Python commands with `uv run`:

```bash
# Running tests
uv run pytest
uv run pytest -v
uv run pytest -v --cov=scraper

# Running the application
uv run python main.py --use-mock
uv run python main.py --scrapers libraries web
```

## Project Architecture

This project was recently refactored (see commit `32ce211`) to a **pipeline-first, config-driven architecture**:

- **Scrapers**: Data collection only (no filtering, no persistence)
- **Pipeline** ([scraper/pipeline.py](scraper/pipeline.py)): All data transformations (deduplicate, filter, save, summarize)
- **Main** ([main.py](main.py)): Source configuration as data, not classes
- **Adding sources**: Edit config dicts in [main.py](main.py), don't create new classes

### Key Files
- [main.py](main.py) - Source configurations and pipeline orchestration
- [scraper/pipeline.py](scraper/pipeline.py) - Core data processing logic
- [scraper/base_scraper.py](scraper/base_scraper.py) - Concert model and base class
- [scraper/library_events_scraper.py](scraper/library_events_scraper.py) - Generic library scraper (config-driven)
- [scraper/web_search_scraper.py](scraper/web_search_scraper.py) - Generic web scraper (config-driven)
- [scraper/boston_events_scraper.py](scraper/boston_events_scraper.py) - Boston.gov events scraper
- [scraper/eventbrite_scraper.py](scraper/eventbrite_scraper.py) - Eventbrite API scraper
- [scraper/expanded_mock_scraper.py](scraper/expanded_mock_scraper.py) - Mock data generator for testing
- [api/main.py](api/main.py) - FastAPI app entry point
- [api/routes/concerts.py](api/routes/concerts.py) - API endpoints
- [api/services/concert_service.py](api/services/concert_service.py) - Data loading and filtering

## Web UI

The project includes a web interface for browsing concerts:

- **Backend**: FastAPI serving concert data from `data/concerts.json`
- **Frontend**: React + TypeScript + Vite

### Running the Web UI

```bash
# Terminal 1: Start the API server
uv run uvicorn api.main:app --reload --port 8000

# Terminal 2: Start the frontend dev server
cd frontend && npm run dev
```

Then open http://localhost:5173

### API Endpoints
- `GET /api/concerts` - List concerts (supports `?towns=Boston&start_date=...&end_date=...`)
- `GET /api/towns` - List available towns for filtering
- `GET /api/health` - Health check

### Frontend Structure
```
frontend/src/
├── components/
│   ├── ConcertCard.tsx      # Individual concert display
│   ├── ConcertList.tsx      # List with loading/error states
│   ├── TownFilter.tsx       # Multi-select town filter
│   └── DateRangeFilter.tsx  # Date range picker
├── hooks/
│   └── useConcerts.ts       # Data fetching hooks
└── types/
    └── concert.ts           # TypeScript interfaces
```

## Testing

All tests must pass before merging:
```bash
# Backend tests (Python)
uv run pytest -v

# Frontend unit tests (React)
cd frontend && npm test

# Frontend E2E tests (Playwright)
cd frontend && npm run test:e2e
```

### Backend test coverage (19 tests)
- Concert model creation and serialization
- Pipeline deduplication (case-insensitive)
- Pipeline filtering (child-friendly keywords)
- Data persistence (JSON + CSV)
- Town detection from free text
- Empty state handling
- API endpoints (concerts, towns, health)
- API filtering (by town, by date range)

### Frontend unit test coverage (20 tests)
- ConcertCard rendering (title, venue, description, links)
- ConcertList states (loading, error, empty, populated)
- TownFilter interactions (checkbox selection/deselection)
- DateRangeFilter interactions (date input changes)

### Frontend E2E test coverage (10 tests)
- Page load (title, header, concerts display)
- Concert card content (title, date, venue)
- Town filter checkboxes (display and interaction)
- Date filter inputs (display and filtering)
- Empty state when no concerts match filters
- Loading state on initial page load

## Common Tasks

### Quick verification (scraper)
```bash
uv run python main.py --use-mock
```
This should:
1. Generate ~150+ mock events
2. Filter to ~100+ child-friendly concerts
3. Save to `data/concerts.json` and `data/concerts.csv`
4. Display summary with town/venue distribution

### Quick verification (web UI)
```bash
# In separate terminals:
uv run uvicorn api.main:app --reload --port 8000
cd frontend && npm run dev
```
Open http://localhost:5173 - should show concert list with filters

### Adding a new library source
Edit `LIBRARY_SOURCES` in [main.py](main.py):
```python
LIBRARY_SOURCES.append({
    "name": "Brookline Public Library",
    "base_url": "https://www.brooklinelibrary.org",
    "events_path": "/events/",
    "town": "Brookline",
})
```

### Adding a new web source
Edit `WEB_SOURCES` in [main.py](main.py):
```python
WEB_SOURCES.append({
    "name": "Boston Magazine",
    "base_url": "https://www.bostonmagazine.com",
    "endpoints": ["/events/", "/things-to-do/"],
    "per_page_limit": 20,
    "title_filter": ["concert", "music", "show"],  # optional
})
```

## Design Principles

1. **No class proliferation** - Use parameterized classes, not inheritance
2. **Configuration as data** - Sources are dicts, not classes
3. **Single responsibility** - Pipeline stages are independent functions
4. **DRY** - If you see duplicate code, extract it
5. **Fail fast** - Validate at boundaries, trust internal contracts
