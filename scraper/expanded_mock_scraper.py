"""Expanded mock scraper generating 100+ realistic historical concert events.

This generates a comprehensive dataset for building the heatmap visualization.
"""

import logging
import random
from datetime import datetime, timedelta
from typing import List

from scraper.base_scraper import BaseScraper, Concert

logger = logging.getLogger(__name__)


class ExpandedMockScraper(BaseScraper):
    """Generates 100+ realistic concert events across Boston metro area."""

    def __init__(self):
        super().__init__()

    def scrape(self) -> List[Concert]:
        """Generate comprehensive mock dataset."""
        logger.info("Generating expanded mock concert dataset...")

        # Venues by town
        venues = {
            "Boston": [
                ("Symphony Hall", "301 Massachusetts Ave"),
                ("House of Blues Boston", "15 Lansdowne St"),
                ("Boston Children's Museum", "308 Congress St"),
                ("Boston Public Library - Central", "700 Boylston St"),
                ("Berklee Performance Center", "136 Massachusetts Ave"),
                ("TD Garden", "100 Legends Way"),
                ("Agganis Arena", "925 Commonwealth Ave"),
                ("Paradise Rock Club", "967 Commonwealth Ave"),
            ],
            "Cambridge": [
                ("Sanders Theatre", "45 Quincy St"),
                ("MIT Kresge Auditorium", "48 Massachusetts Ave"),
                ("The Sinclair", "52 Church St"),
                ("Club Passim", "47 Palmer St"),
                ("Cambridge Public Library", "449 Broadway"),
            ],
            "Somerville": [
                ("Somerville Theatre", "55 Davis Sq"),
                ("Arts at the Armory", "191 Highland Ave"),
                ("ONCE Ballroom", "156 Highland Ave"),
                ("Somerville Arts Center", "143 Highland Ave"),
            ],
            "Newton": [
                ("Newton Community Music School", "321 Chestnut St"),
                ("Newton Free Library", "330 Homer St"),
                ("Burr Performing Arts Center", "500 Lowell Ave"),
            ],
            "Waltham": [
                ("Waltham High School Auditorium", "617 Lexington St"),
                ("Charles River Museum", "154 Moody St"),
                ("Waltham Public Library", "735 Main St"),
            ],
            "Arlington": [
                ("Arlington Town Hall", "730 Massachusetts Ave"),
                ("Robbins Library", "700 Massachusetts Ave"),
                ("Regent Theatre", "7 Medford St"),
            ],
            "Lexington": [
                ("Cary Memorial Hall", "1605 Massachusetts Ave"),
                ("Lexington Public Library", "1625 Massachusetts Ave"),
                ("Lexington High School", "251 Waltham St"),
            ],
        }

        # Event types
        child_friendly_events = [
            ("Kids Rock Concert", "High-energy rock music for children and families"),
            ("Children's Chorus Performance", "Young voices perform classical and contemporary pieces"),
            ("Family Folk Festival", "Traditional folk music with sing-alongs for all ages"),
            ("Youth Orchestra Concert", "Young musicians showcase their talents"),
            ("Toddler Music Class Performance", "Interactive music for preschool children"),
            ("Disney Sing-Along", "Sing your favorite Disney songs"),
            ("Kidz Bop Live", "Today's biggest hits performed for kids"),
            ("Family Music Workshop", "Interactive music-making for families"),
            ("Children's Theater Musical", "Family-friendly musical performance"),
            ("Young People's Symphony", "Introduction to orchestral music for kids"),
            ("Elementary School Band Concert", "Student musicians perform"),
            ("Family Jazz Afternoon", "Jazz music in a family-friendly setting"),
            ("Preschool Music Hour", "Music and movement for young children"),
            ("Kids' World Music Festival", "Music from around the world for families"),
            ("All Ages Acoustic Show", "Acoustic music suitable for all ages"),
        ]

        adult_events = [
            ("Jazz Night", "Evening of sophisticated jazz"),
            ("Rock Concert", "Live rock performance"),
            ("Classical Recital", "Professional classical performance"),
            ("Indie Band Showcase", "Local indie music"),
        ]

        # Generate events over past year
        base_date = datetime.now() - timedelta(days=365)

        for day_offset in range(0, 365, 3):  # Event every 3 days = ~120 events
            current_date = base_date + timedelta(days=day_offset)

            # Random town weighted by size
            town_weights = {
                "Boston": 0.35,
                "Cambridge": 0.20,
                "Somerville": 0.15,
                "Newton": 0.10,
                "Waltham": 0.08,
                "Arlington": 0.07,
                "Lexington": 0.05,
            }
            town = random.choices(list(town_weights.keys()), weights=town_weights.values())[0]
            venue_info = random.choice(venues[town])
            venue_name, venue_address = venue_info

            # 70% child-friendly, 30% adult
            if random.random() < 0.7:
                event_info = random.choice(child_friendly_events)
            else:
                event_info = random.choice(adult_events)

            title, description = event_info

            # Add time
            hour = random.randint(10, 19)
            minute = random.choice([0, 30])
            event_datetime = current_date.replace(hour=hour, minute=minute)

            concert = Concert(
                title=title,
                venue=venue_name,
                town=town,
                date=event_datetime.isoformat(),
                url=f"https://example.com/event-{day_offset}",
                description=description,
                address=f"{venue_address}, {town}, MA",
                source="ExpandedMockData",
            )
            self.concerts.append(concert)

        # Add some recurring monthly events
        for month_offset in range(12):
            month_date = base_date + timedelta(days=month_offset * 30)

            # Monthly children's concerts in each major town
            for town in ["Boston", "Cambridge", "Somerville"]:
                venue_info = random.choice(venues[town])
                venue_name, venue_address = venue_info

                concert = Concert(
                    title="Monthly Family Concert Series",
                    venue=venue_name,
                    town=town,
                    date=month_date.replace(day=15, hour=14, minute=0).isoformat(),
                    url=f"https://example.com/monthly-{town}-{month_offset}",
                    description="Monthly concert series featuring family-friendly music and performances for children of all ages",
                    address=f"{venue_address}, {town}, MA",
                    source="ExpandedMockData",
                )
                self.concerts.append(concert)

        logger.info(f"Generated {len(self.concerts)} mock concert events")
        return self.concerts
