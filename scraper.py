import re
from dotenv import load_dotenv
import os
import json
from playwright.sync_api import sync_playwright, Response

load_dotenv()

EMAIL = os.getenv("EDUVULCAN_EMAIL")
PASSWORD = os.getenv("EDUVULCAN_PASSWORD")

def run(playwright):
    def handle_response(response: Response):
        if "PlanZajec?" in response.url:
            try:
                body = response.json()
            except Exception:
                try:
                    body = response.text()
                except Exception:
                    print(f"[!] Could not read body from: {response.url}")
                    return

            filename = response.url.split("?")[-1].replace("&", "_") + ".json"
            filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

            with open(filename, "w", encoding="utf-8") as f:
                json.dump({
                    "url": response.url,
                    "status": response.status,
                    "body": body
                }, f, indent=2, ensure_ascii=False)

            print(f"[✓] Saved: {filename}")

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page() 

    # Attach listener once — it fires for ALL responses throughout the session
    page.on("response", handle_response)

    page.goto("https://eduvulcan.pl/")

    # Accept cookies (if present)
    try:
        frame = page.frame_locator("#respect-privacy-frame")
        frame.get_by_role("button", name="Zgadzam się").click(timeout=3000)
    except:
        pass

    # Login
    page.get_by_role("link", name="Zaloguj się").click()
    page.get_by_role("textbox", name="Login:").fill(EMAIL)
    page.get_by_role("button", name="Dalej").click()
    page.get_by_label("Hasło").wait_for()
    page.get_by_label("Hasło").fill(PASSWORD)
    page.get_by_role("button", name="Zaloguj").click()

    page.wait_for_load_state("networkidle")
    page.get_by_role("link", name=re.compile("Radosław Szafarz")).click()

    # Go to timetable
    page.get_by_role("link", name="Plan zajęć").click()
    with page.expect_response(lambda r: "PlanZajec?" in r.url) as r:
        page.wait_for_load_state("networkidle")
    print(f"[Week 1] Got response: {r.value.url}")

    with page.expect_response(lambda r: "PlanZajec?" in r.url) as r:
        page.get_by_role("button", name="Następny tydzień").click()
    print(f"[Week 2] Got response: {r.value.url}")
    
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)