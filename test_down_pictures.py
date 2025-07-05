import requests
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import asyncio
import time
import aiofiles
import aiohttp

async def download_page(url:str):
    async  with Stealth().use_async(async_playwright()) as p:
        browser=await p.chromium.launch(headless=True)
        content=await browser.new_context(storage_state="cookies.json")
        page=await content.new_page()
        await page.goto(url=url,timeout=6000)
        await page.wait_for_load_state("networkidle")
        last_height=await page.evaluate("document.body.scrollHeight")
        button_locator=page.locator(".ViewAll-QuestionMainAction").first
        if await button_locator.count()>0:
            await button_locator.click()
        else:
            print("没有找到按钮")
        for i in range(100):
            next_button_locator=page.locator(".ContentItem-more").first
            if await next_button_locator.count()>0:
                await next_button_locator.click()
            await page.keyboard.press("PageDown")
            await asyncio.sleep(1)
        all_pictures=[]
        src_locator=page.locator(".RichContent-inner img[src^='https']")
        count=await src_locator.count()
        if count>0:
            for i in range(count):
                locator=src_locator.nth(i)
                picture=await locator.get_attribute("src")
                all_pictures.append(picture)
                await asyncio.sleep(1)
        else:
            print("没有找到")
    return all_pictures
async def main():
    url="https://www.zhihu.com/search?q=%E5%85%AB%E9%87%8D%E7%A5%9E%E5%AD%90%E7%BE%8E%E5%9B%BE&search_source=Suggestion&utm_content=search_suggestion&type=content"
    all_output_path="C:/Users/iiijj/Desktop/shenzi"
    all_pictures=await download_page(url)
    async with aiohttp.ClientSession() as session:
        for i, pictures in enumerate(all_pictures):
            async with session.get(pictures) as response:
                content=await response.read()
                output_path=f"{all_output_path}/{i}.jpg"
                async with aiofiles.open(output_path, "wb") as f:
                    await f.write(content)
                    print("第"+str(i+1)+"张照片下载成功")




if __name__=="__main__":
    asyncio.run(main())