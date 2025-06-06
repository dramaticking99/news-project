import re
from dateutil import parser as dateparser

def clean_whitespace(text):
    return re.sub(r"\s+", " ", text).strip()

def parse_datestring(dt_str):
    # NDTV often uses ISO‐like strings; if some site uses “June 6, 2025” format:
    return dateparser.parse(dt_str)
