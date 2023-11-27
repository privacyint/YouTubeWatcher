import logging
import time
from typing import List

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.video_element import ClickableVideoElement


def close_cookie_popup(driver: WebDriver) -> None:
    """Closes the annoying cookie modal so we can interact with YouTube"""
    driver.get("https://www.youtube.com/")
    try:
        reject_all_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label^="Reject"]'))
        )
        reject_all_btn.click()
        logging.info("Rejected all cookies")
    except:
        logging.info("No cookie pop up found by close_privacy_popup")


def is_livestream(video_element: WebElement) -> bool:
    """Checks if the given video_element is a livestream instead of a regular video"""
    try:
        badge = video_element.find_element(By.XPATH, "div[1]/div/ytd-badge-supported-renderer/div[1]/span")
        return badge.get_attribute("innerText") == "LIVE NOW"
    except:
        return False


def watch_wait_next(driver: WebDriver, wait: int=30):
    logging.info(f"Watching {driver.title} - {driver.current_url} for {wait} seconds")

    time.sleep(wait)

    WebDriverWait(driver, 20, 1).until(
        EC.element_to_be_clickable((By.ID, 'shorts-container'))
    ).send_keys(Keys.ARROW_DOWN)

    time.sleep(2)


def do_search(driver: WebDriver, search_term: str) -> List[ClickableVideoElement]:
    """ Search youtube for the search_term and return the results """
    videos = []

    try:
        time.sleep(5)
        logging.info(f'Searching for {search_term}')

        # Input the search term and confirm
        search_box = WebDriverWait(driver, 20, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#search")))
        assert "Search" in search_box.get_attribute("placeholder")
        search_box.clear()
        search_box.send_keys(search_term)
        time.sleep(3)
        WebDriverWait(driver, 20, 1).until(
            EC.element_to_be_clickable((By.ID, 'search-icon-legacy'))
        ).click()
    except:
        logging.warning(f'Unable to search for {search_term}')
        exit(1)

    try:
        time.sleep(5)
        # Wait for results page to load with a clickable "shorts" filter
        WebDriverWait(driver, 20, 1).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'yt-chip-cloud-chip-renderer.yt-chip-cloud-renderer:nth-child(2) > yt-formatted-string:nth-child(1)'))
        ).click()
    except:
        logging.warning("Couldn't click the shorts filter button")
        exit(1)

    try:
        time.sleep(5)
        # Wait until they're rendered, then get all results
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.TAG_NAME, "ytd-video-renderer")))
        video_title_elems = driver.find_elements(By.TAG_NAME, "ytd-video-renderer")

        for element in video_title_elems:
            if not is_livestream(element):
                videos.append(ClickableVideoElement(element))
    except:
        exit(1)

    logging.info(f'Got {len(videos)} results returned')

    return videos


def get_video_suggestions(driver: WebDriver, suggestion_count: int = 1) -> List[ClickableVideoElement]:
    """ Get suggestion_count number of video suggestions from the sidebar of the current video. """
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "ytd-compact-video-renderer.ytd-watch-next-secondary-results-renderer",
            )
        )
    )

    yt_app = driver.find_element(By.TAG_NAME, "ytd-app")

    suggestions = []
    prev_suggestion_count = -1

    # Video suggestions are generated lazily while scrolling.
    # So we need to scroll far enough to get the number of suggestions we want.
    while suggestion_count > len(suggestions) > prev_suggestion_count:
        driver.execute_script(f'window.scrollTo(0, {int(yt_app.get_attribute("scrollHeight"))});')
        # Give YouTube a bit of time to load suggestions
        time.sleep(1)
        try:
            WebDriverWait(driver, 20).until_not(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "paper-spinner.yt-next-continuation#spinner"))
            )
        except:
            logging.warning("Suggestion scroller failed to detect spinner")
        prev_suggestion_count = len(suggestions)
        # Suggestions are not recycled, the total amount of elements is accurate
        suggestions = driver.find_elements(By.CSS_SELECTOR,
            "ytd-compact-video-renderer.ytd-watch-next-secondary-results-renderer"
        )

    # Enough suggestions are displayed, we can collect them
    videos = []
    for element in suggestions[0:suggestion_count]:
        if not is_livestream(element):
            videos.append(ClickableVideoElement(element))
    return videos


def get_channel_videos(driver: WebDriver, channel_url: str) -> List[ClickableVideoElement]:
    """ Navigates to channel_url and gets videos from the channel page. """
    try:
        driver.get(f"{channel_url}/videos")
        # Wait for results page to load
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.TAG_NAME, "ytd-rich-item-renderer")))
        channel_name = driver.find_element(By.CSS_SELECTOR,
            "ytd-channel-name.ytd-c4-tabbed-header-renderer > div:nth-child(1) > div:nth-child(1) > "
            "yt-formatted-string:nth-child(1) "
        ).text
        time.sleep(5)
    # Get all results
        video_title_elems = driver.find_elements(By.TAG_NAME, "ytd-rich-item-renderer")
        logging.info(f"Found {len(video_title_elems)} videos on {channel_name}")
        time.sleep(5)
        videos = []
        for element in video_title_elems:
            if not is_livestream(element):
                videos.append(ClickableVideoElement(element, channel_name))
        return videos
    except:
        logging.error("I was unable to retrieve any videos from the channel")
