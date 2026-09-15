#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern browser automation module using pyppeteer
"""

import asyncio
import pyppeteer
from pyppeteer import launch
import fake_useragent
import os
import shutil
import logging
from typing import Optional, Dict, Any
from config import BROWSER_TIMEOUT, BROWSER_HEADLESS, BROWSER_WIDTH, BROWSER_HEIGHT, DEFAULT_PASSWORD, DEFAULT_PIN

logger = logging.getLogger(__name__)

class BrowserAutomation:
    """Modern browser automation for student email registration"""
    
    def __init__(self, user_detail: Dict[str, Any]):
        self.user_detail = user_detail
        self.browser = None
        self.psd = DEFAULT_PASSWORD
        self.pin = DEFAULT_PIN
    
    async def initialize_browser(self) -> bool:
        """Initialize and configure browser"""
        try:
            self.browser = await launch({
                'executablePath': pyppeteer.launcher.executablePath(),
                'headless': BROWSER_HEADLESS,
                'dumpio': True,
                'args': [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-infobars',
                    '--disable-extensions',
                    '--disable-web-security',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--lang=en-US',
                ]
            }, userDataDir=f'./browser_cache/{self.user_detail["email"]}')
            logger.info(f"Browser initialized for {self.user_detail['email']}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            return False
    
    async def setup_page(self, page) -> None:
        """Setup page with anti-detection measures"""
        try:
            # Remove webdriver detection
            await page.evaluateOnNewDocument("""() => {
                delete navigator.__proto__.webdriver;
            }""")
            
            # Set user agent
            ua = fake_useragent.UserAgent()
            await page.setUserAgent(ua.chrome)
            
            # Set language
            await page.evaluateOnNewDocument('''data => {
                Object.defineProperty(navigator, 'language', { get: () => data });
            }''', 'en-US')
            
            # Set notifications permission
            await page.evaluateOnNewDocument("""() => {
                Object.defineProperty(Notification, 'permission', { get: () => 'default' })
            }""")
            
            logger.info("Page setup completed")
        except Exception as e:
            logger.error(f"Failed to setup page: {e}")
    
    async def navigate_to_url(self, url: str, timeout: int = BROWSER_TIMEOUT) -> bool:
        """Navigate to URL with error handling"""
        try:
            page = await self.browser.newPage()
            await page.setViewport({'width': BROWSER_WIDTH, 'height': BROWSER_HEIGHT})
            await self.setup_page(page)
            page.setDefaultNavigationTimeout(timeout)
            
            await page.goto(url, {'waitUntil': 'domcontentloaded'})
            logger.info(f"Navigated to {url}")
            return True
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            return False
    
    async def close(self) -> None:
        """Close browser and cleanup"""
        try:
            if self.browser:
                await self.browser.close()
                logger.info(f"Browser closed for {self.user_detail['email']}")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
    
    async def __aenter__(self):
        """Async context manager entry"""
        if await self.initialize_browser():
            return self
        raise Exception("Failed to initialize browser")
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
