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

# Keywords to identify child-friendly concerts.
# "young" alone is intentionally excluded — it matches "young adult".
CHILD_FRIENDLY_KEYWORDS = [
    "kids",
    "children",
    "family",
    "youth",
    "toddler",
    "preschool",
    "elementary",
    "young people",
    "all ages",
    "sing along",
    "sing-along",
    "baby",
    "infant",
    "parent and child",
]

# Output file paths
OUTPUT_DIR = "data"
CONCERTS_JSON = f"{OUTPUT_DIR}/concerts.json"
CONCERTS_CSV = f"{OUTPUT_DIR}/concerts.csv"
