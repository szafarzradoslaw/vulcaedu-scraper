from playwright.sync_api import sync_playwright
from datetime import datetime
import json
from session import get_session
from api import fetch_week

start = datetime(2026, 3, 1, 23, 0, 0)

with sync_playwright() as playwright:
    cookies, key = get_session(playwright)

data = fetch_week(cookies, key, date_from=start)
with open("classes.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)