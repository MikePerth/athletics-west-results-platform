from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto(
        "https://meets.rosterathletics.com/public/competitions/details/results?id=27216&meId=375360"
    )

    print(
        page.title()
    )

    input(
        "\nPress Enter to close..."
    )

    browser.close()