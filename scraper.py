import re
from dotenv import load_dotenv
import os
import json
from playwright.sync_api import sync_playwright

load_dotenv()

EMAIL = os.getenv("EDUVULCAN_EMAIL")
PASSWORD = os.getenv("EDUVULCAN_PASSWORD")

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()


    def capture_plan(response):
            if "PlanZajec" in response.url:
                print("Captured PlanZajec response!")
                data = response.json()
                with open("timetable.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                print("Timetable saved")

    page.on("response", capture_plan)
    
    page.goto("https://eduvulcan.pl/")

    # Accept cookies (if present)
    try:
        frame = page.frame_locator("#respect-privacy-frame")
        frame.get_by_role("button", name="Zgadzam się").click(timeout=3000)
    except:
        pass  # Cookie banner not present)

    # Login
    page.get_by_role("link", name="Zaloguj się").click()
    
    page.get_by_role("textbox", name="Login:").fill(EMAIL)
    page.get_by_role("button", name="Dalej").click()

    # Wait for step 2 to appear
    page.get_by_label("Hasło").wait_for()

    # Step 2: Password
    page.get_by_label("Hasło").fill(PASSWORD)
    page.get_by_role("button", name="Zaloguj").click()

    page.wait_for_load_state("networkidle")

    # Select student
    page.get_by_role("link", name=re.compile("Radosław Szafarz")).click()

    # Go to timetable
    page.get_by_role("link", name="Plan zajęć").click()

    page.wait_for_load_state("networkidle")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)