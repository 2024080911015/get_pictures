import asyncio


from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def main():
    async with Stealth().use_async(async_playwright()) as p:
        browse=await p.chromium.launch(headless=False)
        content=await browse.new_context()
        page=await content.new_page()

        await page.goto("https://www.zhihu.com/signin")
        input()
        await content.storage_state(path="cookies.json")
        await browse.close()
if __name__=="__main__":
    asyncio.run(main())