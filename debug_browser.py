import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        page.on("pageerror", lambda err: print(f"ERROR: {err.message} \nSTACK: {err.stack}"))
        
        print("Navigating...")
        await page.goto("http://localhost:8000/index.html")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
