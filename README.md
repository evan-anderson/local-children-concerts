# Boston Metro Child-Friendly Concerts

A web application to visualize where child-friendly concerts most frequently occur in the Boston metropolitan area, including Waltham, Newton, Lexington, Arlington, Somerville, Cambridge, and Boston.

## Project Overview

This project scrapes concert data from various sources and generates a heat map showing the geographic distribution of child-friendly concerts across the Boston metro area.

## Features

- **Data Scraping**: Python-based scrapers to collect concert data from multiple sources
- **Child-Friendly Filtering**: Automatically identifies concerts suitable for children based on keywords
- **Geographic Focus**: Targets Boston metro towns (Waltham, Newton, Lexington, Arlington, Somerville, Cambridge, Boston)
- **Data Export**: Outputs to both JSON and CSV formats for easy analysis

## Project Structure

```
local-children-concerts/
├── scraper/                    # Python scraping modules
│   ├── __init__.py
│   ├── base_scraper.py        # Base scraper class and Concert model
│   ├── config.py              # Configuration (towns, keywords)
│   ├── eventbrite_scraper.py  # Eventbrite API scraper
│   └── example_scraper.py     # Template for additional scrapers
├── data/                       # Output directory for scraped data
│   ├── concerts.json          # Concert data in JSON format
│   └── concerts.csv           # Concert data in CSV format
├── main.py                     # Main script to run scrapers
├── pyproject.toml             # Python dependencies (uv)
└── README.md
```

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python dependency management.

### Prerequisites

- Python 3.10+
- uv package manager

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd local-children-concerts
```

2. Install dependencies using uv:
```bash
uv sync
```

This will create a virtual environment and install all required packages.

## Usage

### Running the Scrapers

Run the main scraper script:

```bash
uv run python main.py
```

This will:
1. Generate mock concert data (no API key required)
2. Optionally scrape from Eventbrite (if API key is set)
3. Filter for child-friendly events
4. Save results to `data/concerts.json` and `data/concerts.csv`

**Note**: The scraper works out of the box with mock data - no API keys needed to get started!

### Configuring Eventbrite Scraper

The Eventbrite scraper requires an API key:

1. Create an Eventbrite account at [eventbrite.com](https://www.eventbrite.com)
2. Get an API key at [eventbrite.com/platform/api](https://www.eventbrite.com/platform/api)
3. Set the environment variable:
```bash
export EVENTBRITE_API_KEY='your_api_key_here'
```

### Running Tests

Run the test suite to verify everything works:

```bash
uv run pytest
```

For verbose output with coverage:

```bash
uv run pytest -v --cov=scraper
```

All tests should pass without requiring any API keys.

### Configuration

Edit [scraper/config.py](scraper/config.py) to customize:

- **Towns**: Add or remove Boston metro towns to search
- **Keywords**: Modify keywords used to identify child-friendly concerts
- **Output paths**: Change where data files are saved

## Data Sources

### Currently Implemented
- **Mock Data**: Sample concert data for testing (no API key needed)
- **Eventbrite**: Uses the Eventbrite API to search for family-friendly concerts (optional, requires API key)

### Planned Sources
The project is designed to be extensible. Additional scrapers can be implemented for:
- City/town event calendars
- Public library event pages
- Community center websites
- Venue websites (Symphony Hall, House of Blues, etc.)
- Other ticketing platforms

See [scraper/example_scraper.py](scraper/example_scraper.py) for a template to implement new scrapers.

## Development

### Adding a New Scraper

1. Create a new file in the `scraper/` directory
2. Extend the `BaseScraper` class
3. Implement the `scrape()` method
4. Import and use in [main.py](main.py)

Example:
```python
from scraper.base_scraper import BaseScraper, Concert

class MyCustomScraper(BaseScraper):
    def scrape(self):
        # Your scraping logic here
        concert = Concert(
            title="Example Concert",
            venue="Example Venue",
            town="Boston",
            date="2024-12-31",
            source="MySource"
        )
        self.concerts.append(concert)
        return self.concerts
```

### Child-Friendly Keywords

Events are identified as child-friendly if their title or description contains keywords like:
- kids, children, family
- youth, toddler, preschool
- elementary, young
- all ages

## Output Data Format

### JSON Format
```json
[
  {
    "title": "Concert Title",
    "venue": "Venue Name",
    "town": "Boston",
    "date": "2024-12-31T19:00:00",
    "url": "https://example.com/event",
    "description": "Event description",
    "address": "123 Main St, Boston, MA",
    "source": "Eventbrite",
    "scraped_at": "2024-12-06T19:57:00"
  }
]
```

### CSV Format
Contains the same fields in a comma-separated format suitable for analysis in spreadsheet applications.

## Future Enhancements

- [ ] Web-based heat map visualization
- [ ] Interactive filtering by date range and town
- [ ] Additional data sources (libraries, community centers, venues)
- [ ] Geocoding addresses for precise map coordinates
- [ ] Automated scheduling to update data regularly
- [ ] Frontend web application for browsing events

## Contributing

Contributions are welcome! Areas where help is needed:
- Implementing scrapers for additional data sources
- Improving child-friendly keyword detection
- Building the heat map visualization
- Adding geocoding capabilities

## License

MIT License - feel free to use and modify for your own projects.

## Contact

For questions or suggestions, please open an issue on GitHub.
