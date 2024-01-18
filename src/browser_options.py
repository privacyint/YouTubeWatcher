from selenium import webdriver


def get_firefox_options() -> webdriver.FirefoxOptions:
    """Configure firefox for automated watching"""
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.set_preference("intl.accept_languages", "en-us")
    # Always autoplay videos
    firefox_options.set_preference("media.autoplay.default", 0)
    firefox_options.set_preference("media.volume_scale", "0.0")
    firefox_options.add_argument("-safe-mode")

    return firefox_options


def get_edge_options() -> webdriver.EdgeOptions:
    """Configure Edge for automated watching"""
    edge_options = webdriver.EdgeOptions()

    return edge_options


def get_chromium_options() -> webdriver.ChromeOptions:
    """Configure chromium for automated watching"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/usr/local/bin/chromium"

    return chrome_options
