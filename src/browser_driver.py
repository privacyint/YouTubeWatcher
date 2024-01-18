from argparse import ArgumentError

from selenium import webdriver
# MS Edge driver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
# FireFox driver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
# Chromium driver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

from src.browser_options import get_firefox_options, get_chromium_options, get_edge_options


def get_browser_driver(browser: str) -> webdriver:
        case "firefox":
            return (
                webdriver.Firefox(
                    service=FirefoxService(
                        GeckoDriverManager().install(),
                    ),
                    options=get_firefox_options(),
                )
            )
        case "chromium":
            return (
                webdriver.Chrome(
                    service=ChromiumService(
                        ChromeDriverManager(
                            chrome_type=ChromeType.CHROMIUM,
                        )
                        .install(),
                    ),
                    options=get_chromium_options(),
                )
            )
        case "edge":
            return (
                webdriver.Edge(
                    service=EdgeService(
                        EdgeChromiumDriverManager().install(),
                    ),
                    options=get_edge_options(),
                )
            )
        case _:
            raise ArgumentError(
                message=f"Unknown driver '{browser}'",
                argument=browser,
            )
