from argparse import ArgumentError, Namespace

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


def get_browser_driver(args: Namespace) -> webdriver:
    """ Downloads the required driver software - if needed - and returns the correct webdriver based on {browser} """
    match args.browser:
        case "firefox":
            return (
                webdriver.Firefox(
                    service=FirefoxService(
                        GeckoDriverManager().install(),
                    ),
                    options=get_firefox_options(args.headless),
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
                    options=get_chromium_options(args.headless),
                )
            )
        case "edge":
            return (
                webdriver.Edge(
                    service=EdgeService(
                        EdgeChromiumDriverManager().install(),
                    ),
                    options=get_edge_options(args.headless),
                )
            )
        case _:
            raise ArgumentError(
                message=f"Unknown driver '{args.browser}'",
                argument=None,
            )
