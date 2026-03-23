"""
Playwright debug script - checks each page and reports errors.
Run: python3 debug.py
"""
import asyncio
from playwright.async_api import async_playwright

BASE_URL = "https://rishikananda-8000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai"
ADMIN_USER = "admin"
ADMIN_PASS = "admin"  # <-- update this

async def check(page, label, url, screenshot_path):
    print(f"\n{'='*50}")
    print(f"Checking: {label}")
    print(f"URL: {url}")
    try:
        response = await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        status = response.status if response else "no response"
        title = await page.title()
        content = await page.content()
        print(f"  Status : {status}")
        print(f"  Title  : {title}")
        print(f"  Body snippet: {content[:300]}")
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"  Screenshot: {screenshot_path}")
    except Exception as e:
        print(f"  ERROR: {e}")
        try:
            await page.screenshot(path=screenshot_path)
        except Exception:
            pass

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            ignore_https_errors=True
        )
        page = await context.new_page()

        # 1. Check home page
        await check(page, "Home page", BASE_URL, "debug_home.png")

        # 2. Check admin page
        await check(page, "Admin login page", f"{BASE_URL}/admin/login/", "debug_admin.png")

        # 3. Try admin login
        print(f"\n{'='*50}")
        print("Attempting admin login...")
        await page.goto(f"{BASE_URL}/admin/login/", wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        try:
            await page.fill("#id_username", ADMIN_USER)
            await page.fill("#id_password", ADMIN_PASS)
            await page.screenshot(path="debug_admin_filled.png")
            await page.click("input[value='Log in']")
            await page.wait_for_timeout(3000)
            title = await page.title()
            url = page.url
            print(f"  After login - Title: {title}")
            print(f"  After login - URL: {url}")
            await page.screenshot(path="debug_admin_after_login.png")
        except Exception as e:
            print(f"  ERROR: {e}")

        # 4. Check React routes
        await check(page, "React home /", BASE_URL + "/", "debug_react_home.png")
        await check(page, "Login page", BASE_URL + "/login", "debug_login.png")
        await check(page, "Register page", BASE_URL + "/register", "debug_register.png")

        # 5. Check API endpoints
        await check(page, "Get dealers API", BASE_URL + "/djangoapp/get_dealers", "debug_api_dealers.png")

        await browser.close()
        print("\n\nDebug screenshots saved. Check debug_*.png files.")

if __name__ == "__main__":
    asyncio.run(main())
