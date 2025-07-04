import requests
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

def get_page(url:str,output_path:str):
