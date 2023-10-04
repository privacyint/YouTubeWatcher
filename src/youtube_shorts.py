import logging
import time
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.video_element import ClickableVideoElement


def watch_current_video(driver: WebDriver, max_time: int = 420) -> None:
    """Watches the YouTube short video on the currently selected page.
    Arguments:
    driver - The webdriver, it has to be navigated to a YouTube video before calling this function.
    with_progress - If true, periodically print the watch progress.
    max_time - Maximum time spent watching this video before aborting.
    """

    # Wait for YouTube to finish loading the player
    player_div = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div#player.ytd-watch-flexy"))
    )
    start_time = time.time()
    logging.info("Started watching")
    current_time_elem = driver.find_element(By.CSS_SELECTOR, "span.ytp-time-current")
    duration_time_elem = driver.find_element(By.CSS_SELECTOR, "span.ytp-time-duration")

    # The watch next video button gets created later I guess ¯\_(ツ)_/¯
    up_next_button_elem = None

    # We wiggle the virtual mouse to prevent YouTube from hiding the player controls,
    # because we read the watched time from there
    move_to_player = webdriver.ActionChains(driver)
    move_to_player.move_to_element_with_offset(player_div, 100, 100)
    wiggle_mouse = webdriver.ActionChains(driver)
    wiggle_mouse.move_by_offset(10, 0)
    wiggle_mouse.pause(1)
    wiggle_mouse.move_by_offset(-10, 0)
    move_to_player.perform()
    while True:
        # The buttom time bar won't update if it is not visible so move the mouse to show it
        wiggle_mouse.perform()
        logging.info(
            f'{current_time_elem.get_attribute("textContent")} of {duration_time_elem.get_attribute("textContent")}'
        )

        # Resting is important
        time.sleep(5)

        # If the 'Up next' screen is showing, we are done watching this video
        try:
            if up_next_button_elem:
                if up_next_button_elem.is_displayed():
                    break
            else:
                up_next_button_elem = driver.find_element(By.CLASS_NAME, "ytp-autonav-endscreen-upnext-button")
        except:
            # The next button is created lazily, so sometimes its missing
            logging.warning("No next button found while watching video")

        if time.time() - start_time >= max_time:
            break

    logging.info("finished watching video")


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
        logging.warning("No cookie pop up found by close_privacy_popup")


def is_livestream(video_element: WebElement) -> bool:
    """Checks if the given video_element is a livestream instead of a regular video"""
    try:
        badge = video_element.find_element(By.XPATH, "div[1]/div/ytd-badge-supported-renderer/div[1]/span")
        return badge.get_attribute("innerText") == "LIVE NOW"
    except:
        return False


def do_search(driver: WebDriver, search_term: str) -> List[ClickableVideoElement]:
    """ Search youtube for the search_term and return the results """
    videos = []

    try:
        # Input the search term and confirm
        search_box = WebDriverWait(driver, 20, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#search")))
        assert "Search" in search_box.get_attribute("placeholder")
        search_box.clear()
        search_box.send_keys(search_term)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'search-icon-legacy'))
        ).click()
    except:
        logging.warning(f'Unable to search for {search_term}')
        exit(1)

    try:
        # Wait for results page to load with a clickable "shorts" filter
        WebDriverWait(driver, 20, 1).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'yt-chip-cloud-chip-renderer.style-scope:nth-child(2) > yt-formatted-string:nth-child(1)'))
        ).click()
    except:
        logging.warning("Couldn't click the shorts filter button")
        exit(1)

    try:
        # Wait until they're rendered, then get all results
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.TAG_NAME, "ytd-video-renderer")))
        video_title_elems = driver.find_elements(By.TAG_NAME, "ytd-video-renderer")

        for element in video_title_elems:
            if not is_livestream(element):
                videos.append(ClickableVideoElement(element))
    except:
        exit(1)

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
