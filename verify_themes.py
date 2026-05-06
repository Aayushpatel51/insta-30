import asyncio
from playwright.async_api import async_playwright
import os
import subprocess
import time

async def verify_themes_and_tabs():
    # Start the backend server
    env = os.environ.copy()
    server_process = subprocess.Popen(
        ["python3", "builds/day-31/backend/main.py"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to start
    time.sleep(5)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})

        try:
            await page.goto("http://localhost:8000")
            await page.wait_for_selector("aside")

            # 1. Capture Dark Mode (Default)
            await page.screenshot(path="/home/jules/verification/dark_mode.png")
            print("Dark mode screenshot saved.")

            # 2. Toggle to Light Mode
            await page.click("#theme-icon")
            await asyncio.sleep(1)
            await page.screenshot(path="/home/jules/verification/light_mode.png")
            print("Light mode screenshot saved.")

            # 3. Switch Tabs (Click 'Projects')
            await page.click("div.sidebar-item:has-text('Projects')")
            await asyncio.sleep(1)
            await page.screenshot(path="/home/jules/verification/tab_projects_light.png")
            print("Projects tab (Light) screenshot saved.")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()
            server_process.terminate()

if __name__ == "__main__":
    asyncio.run(verify_themes_and_tabs())
