import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        
        # We wrap the PRACTICALS in a file that catches its own syntax errors
        html_code = """
        <script>
        window.addEventListener('error', function(e) {
            console.log('SYNTAX ERRROR AT LINE: ' + e.lineno + ' COL: ' + e.colno + ' MSG: ' + e.message);
        });
        </script>
        <script src="test_syntax.js"></script>
        """
        open("wrap.html", "w").write(html_code)
        
        # We save test_syntax.js separately
        import re
        text = open("index.html.bak").read()
        m = re.search(r'const PRACTICALS = \[.*?\];', text, re.DOTALL)
        open("test_syntax.js", "w").write(m.group(0))
        
        await page.goto("file:///Users/dhruv/Downloads/stitch_dbms_lab_journal_portal/wrap.html")
        await asyncio.sleep(1)
        await browser.close()

asyncio.run(main())
