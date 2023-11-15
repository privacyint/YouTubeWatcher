from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


def get_current_ip(driver: WebDriver) -> str:
    """Get the browser's current ip by visiting myip.com"""
    driver.get("https://myip.com")
    return driver.find_element(By.CSS_SELECTOR, "#ip").text


def get_firefox_options() -> webdriver.FirefoxOptions:
    """Configure firefox for automated watching"""
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.set_preference("intl.accept_languages", "en-us")
    # Always autoplay videos
    firefox_options.set_preference("media.autoplay.default", 0)
    firefox_options.set_preference("media.volume_scale", "0.0")
    return firefox_options
