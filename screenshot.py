"""
Playwright screenshot collector for the Best Cars Capstone submission.
Collects all required screenshots for Tasks 12-22.

Usage:
  pip3 install playwright
  playwright install chromium
  python3 screenshot.py
"""

import asyncio
from playwright.async_api import async_playwright

BASE_URL = "https://theia-rishikananda-8000.theiadocker-1-labs-prod-theiak8s-3-tor01.proxy.cognitiveclass.ai"

# Set your superuser credentials here
ADMIN_USER = "admin"
ADMIN_PASS = "admin"   # <-- change to your superuser password

# Test user for login screenshots (will be registered if not exists)
TEST_USER = "testuser"
TEST_PASS = "testpass123"

async def setup_car_data(page):
    """Add CarMake and CarModel data via admin for Task 14/15"""
    print("Setting up car data...")
    await page.goto(f"{BASE_URL}/admin/djangoapp/carmake/add/")
    await page.wait_for_load_state("networkidle")

    makes = [
        {"name": "Toyota", "description": "Japanese car manufacturer"},
        {"name": "Honda", "description": "Japanese car manufacturer"},
        {"name": "Ford", "description": "American car manufacturer"},
    ]

    for make in makes:
        await page.goto(f"{BASE_URL}/admin/djangoapp/carmake/add/")
        await page.wait_for_load_state("networkidle")
        await page.fill("#id_name", make["name"])
        await page.fill("#id_description", make["description"])
        # Add one car model inline
        await page.fill("#id_carmodel_set-0-name", f"{make['name']} Corolla" if make['name']=='Toyota' else f"{make['name']} Civic" if make['name']=='Honda' else f"{make['name']} F-150")
        try:
            await page.select_option("#id_carmodel_set-0-type", "Sedan")
        except Exception:
            pass
        try:
            await page.fill("#id_carmodel_set-0-year", "2022")
        except Exception:
            pass
        await page.click("input[value='Save']")
        await page.wait_for_load_state("networkidle")
        print(f"  Added CarMake: {make['name']}")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()

        # ── Task 12: Admin Login screenshot ──────────────────────────────────
        print("Task 12: Admin login...")
        await page.goto(f"{BASE_URL}/admin/login/")
        await page.wait_for_load_state("networkidle")
        await page.fill("#id_username", ADMIN_USER)
        await page.fill("#id_password", ADMIN_PASS)
        await page.screenshot(path="admin_login.png")
        print("  Saved: admin_login.png")

        # Submit login
        await page.click("input[value='Log in']")
        await page.wait_for_load_state("networkidle")

        # Set up car data (needed for Tasks 14/15)
        await setup_car_data(page)

        # ── Task 13: Admin Logout screenshot ─────────────────────────────────
        print("Task 13: Admin logout...")
        await page.goto(f"{BASE_URL}/admin/")
        await page.wait_for_load_state("networkidle")
        await page.click("a:has-text('Log out')")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path="admin_logout.png")
        print("  Saved: admin_logout.png")

        # ── Task 17: Dealers on home page BEFORE login ───────────────────────
        print("Task 17: Home page before login...")
        await page.goto(BASE_URL)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)
        await page.screenshot(path="get_dealers.png")
        print("  Saved: get_dealers.png")

        # ── Register test user ────────────────────────────────────────────────
        print("Registering test user...")
        await page.goto(f"{BASE_URL}/register")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(2000)
        try:
            await page.fill("input[placeholder='Username']", TEST_USER)
            await page.fill("input[placeholder='First Name']", "Test")
            await page.fill("input[placeholder='Last Name']", "User")
            await page.fill("input[placeholder='Email']", "test@example.com")
            await page.fill("input[placeholder='Password']", TEST_PASS)
            await page.click("input[type='submit']")
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(2000)
            print("  Test user registered")
        except Exception as e:
            print(f"  Register skipped: {e}")

        # ── Task 18: Home page AFTER login ───────────────────────────────────
        print("Task 18: Home page after login...")
        await page.goto(f"{BASE_URL}/login")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(2000)
        try:
            await page.fill("input[name='username']", TEST_USER)
            await page.fill("input[name='psw']", TEST_PASS)
            await page.click("input[value='Login']")
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(3000)
        except Exception as e:
            print(f"  Login attempt: {e}")

        await page.goto(BASE_URL)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)
        await page.screenshot(path="get_dealers_loggedin.png")
        print("  Saved: get_dealers_loggedin.png")

        # ── Task 19: Filter dealers by state ─────────────────────────────────
        print("Task 19: Filter by state...")
        await page.goto(BASE_URL)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)
        try:
            await page.select_option("select#state", "Kansas")
            await page.wait_for_timeout(2000)
        except Exception:
            try:
                await page.select_option("select[name='state']", "Kansas")
                await page.wait_for_timeout(2000)
            except Exception as e:
                print(f"  State filter: {e}")
        await page.screenshot(path="dealersbystate.png")
        print("  Saved: dealersbystate.png")

        # ── Task 20: Dealer details with reviews ─────────────────────────────
        print("Task 20: Dealer details with reviews...")
        await page.goto(f"{BASE_URL}/dealer/2")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(4000)
        await page.screenshot(path="dealer_id_reviews.png")
        print("  Saved: dealer_id_reviews.png")

        # ── Task 21: Post review page (before submit) ─────────────────────────
        print("Task 21: Post review page...")
        await page.goto(f"{BASE_URL}/postreview/2")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)
        try:
            await page.fill("textarea#review", "Excellent service and great selection of cars!")
            await page.fill("input[type='date']", "2026-03-23")
            await page.select_option("select#cars", index=1)
            await page.fill("input[type='int']", "2022")
        except Exception as e:
            print(f"  Fill review form: {e}")
        await page.screenshot(path="dealership_review_submission.png")
        print("  Saved: dealership_review_submission.png")

        # ── Task 22: Submit review and screenshot ─────────────────────────────
        print("Task 22: Submit review...")
        try:
            await page.click("button.postreview")
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(3000)
            await page.screenshot(path="added_review.png")
            print("  Saved: added_review.png")
        except Exception as e:
            print(f"  Submit review: {e}")
            await page.screenshot(path="added_review.png")

        await browser.close()
        print("\nAll screenshots collected!")
        print("Files: admin_login.png, admin_logout.png, get_dealers.png,")
        print("       get_dealers_loggedin.png, dealersbystate.png,")
        print("       dealer_id_reviews.png, dealership_review_submission.png, added_review.png")


if __name__ == "__main__":
    asyncio.run(main())
