"""Configuration for the concert scraper."""

# Boston metro area towns to search
BOSTON_METRO_TOWNS = [
    "Waltham",
    "Newton",
    "Lexington",
    "Arlington",
    "Somerville",
    "Cambridge",
    "Boston",
]

# Keywords to identify child-friendly concerts
CHILD_FRIENDLY_KEYWORDS = [
    "kids",
    "children",
    "family",
    "youth",
    "toddler",
    "preschool",
    "elementary",
    "young",
    "all ages",
]

# Output file paths
OUTPUT_DIR = "data"
CONCERTS_JSON = f"{OUTPUT_DIR}/concerts.json"
CONCERTS_CSV = f"{OUTPUT_DIR}/concerts.csv"
