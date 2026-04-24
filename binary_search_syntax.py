import asyncio
from playwright.async_api import async_playwright

async def check_syntax(code_str):
    open("test_bs.js", "w").write(code_str)
    html = "<script src='test_bs.js'></script>"
    open("test_bs.html", "w").write(html)
    
    error_msg = None
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page()
        def on_err(err):
            nonlocal error_msg
            error_msg = err.message
        page.on("pageerror", on_err)
        await page.goto("file:///Users/dhruv/Downloads/stitch_dbms_lab_journal_portal/test_bs.html")
        await b.close()
    return error_msg

async def main():
    import re
    text = open("index.html.bak").read()
    m = re.search(r'const PRACTICALS = \[.*?\];', text, re.DOTALL)
    code = m.group(0)
    lines = code.split('\n')
    
    # Verify the whole thing fails
    fail_all = await check_syntax(code)
    if not fail_all:
        print("Wait, the whole string is fine??")
        return
        
    low = 0
    high = len(lines)
    while low < high:
        mid = (low + high) // 2
        # To test a partial slice, we must make it syntactically valid by appending whatever brackets.
        # But if it's truncated, it will throw "Unexpected end of input", NOT "Unexpected token ':'".
        # So we look for specifically "Unexpected token ':'".
        test_code = '\n'.join(lines[:mid])
        msg = await check_syntax(test_code)
        
        # If msg contains "Unexpected token ':'", then the colon is IN the slice!
        if msg and "Unexpected token ':'" in msg:
            high = mid
        else:
            low = mid + 1
            
    print(f"Error is at line {low}")
    print(f"Line content: {lines[low-1]}")

asyncio.run(main())
