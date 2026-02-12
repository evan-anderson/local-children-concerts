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
- [scraper/pipeline.py](scraper/pipeline.py) - Core data processing logic
- [scraper/base_scraper.py](scraper/base_scraper.py) - Concert model and base class
- [scraper/library_events_scraper.py](scraper/library_events_scraper.py) - Generic library scraper (config-driven)
- [scraper/web_search_scraper.py](scraper/web_search_scraper.py) - Generic web scraper (config-driven)
- [main.py](main.py) - Source configurations and pipeline orchestration

## Testing

All tests must pass before merging:
```bash
uv run pytest tests/test_base_scraper.py -v
```

Current test coverage:
- Concert model creation and serialization
- Pipeline deduplication (case-insensitive)
- Pipeline filtering (child-friendly keywords)
- Data persistence (JSON + CSV)
- Town detection from free text
- Empty state handling

## Common Tasks

### Quick verification
```bash
uv run python main.py --use-mock
```
This should:
1. Generate ~150+ mock events
2. Filter to ~100+ child-friendly concerts
3. Save to `data/concerts.json` and `data/concerts.csv`
4. Display summary with town/venue distribution

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
