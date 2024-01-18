from selenium import webdriver


def get_firefox_options(headless: bool) -> webdriver.FirefoxOptions:
    """Configure firefox for automated watching"""
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.set_preference("intl.accept_languages", "en-us")
    # Always autoplay videos
    firefox_options.set_preference("media.autoplay.default", 0)
    firefox_options.set_preference("media.volume_scale", "0.0")
    firefox_options.add_argument("-safe-mode")

    if headless:
        firefox_options.add_argument('--headless')

    return firefox_options


def get_edge_options(headless: bool) -> webdriver.EdgeOptions:
    """Configure Edge for automated watching"""
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument('−−mute−audio')

    if headless:
        edge_options.add_argument('--headless')

    return edge_options


def get_chromium_options(headless: bool) -> webdriver.ChromeOptions:
    """Configure chromium for automated watching"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('−−mute−audio')

    if headless:
        chrome_options.add_argument('--headless')

    return chrome_options
