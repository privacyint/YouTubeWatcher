import logging
import time

import docker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


def get_current_ip(driver: WebDriver) -> str:
    """Get the browser's current ip by visiting myip.com"""
    driver.get("https://myip.com")
    return driver.find_element(By.CSS_SELECTOR, "#ip").text
