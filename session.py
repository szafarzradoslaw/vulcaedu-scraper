import re
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("EDUVULCAN_EMAIL")
PASSWORD = os.getenv("EDUVULCAN_PASSWORD")

def get_session(playwright) -> tuple[dict, str]:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://eduvulcan.pl/")

    try:
        frame = page.frame_locator("#respect-privacy-frame")
        frame.get_by_role("button", name="Zgadzam się").click(timeout=3000)
    except:
        pass

    page.get_by_role("link", name="Zaloguj się").click()
    page.get_by_role("textbox", name="Login:").fill(EMAIL)
    page.get_by_role("button", name="Dalej").click()
    page.get_by_label("Hasło").wait_for()
    page.get_by_label("Hasło").fill(PASSWORD)
    page.get_by_role("button", name="Zaloguj").click()

    page.wait_for_load_state("networkidle")
    page.get_by_role("link", name=re.compile("Radosław Szafarz")).click()

    page.get_by_role("link", name="Plan zajęć").click()
    with page.expect_response(lambda r: "PlanZajec?" in r.url) as r:
        page.wait_for_load_state("networkidle")

    key = r.value.url.split("key=")[1].split("&")[0]
    cookies = {c["name"]: c["value"] for c in context.cookies()}

    context.close()
    browser.close()

    return cookies, key