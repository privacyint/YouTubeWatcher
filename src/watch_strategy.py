import logging
import random
import time
from datetime import datetime, timedelta

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.youtube_shorts import do_search, get_channel_videos


def watch_strategy(driver: WebDriver, search_terms: list, channel_url: str, duration: int = 60):
    """Watches YouTube videos found by searching the provided search_terms and from the given channel_url,
    for a duration in minutes."""

    start_time = datetime.now()
    logging.info(f"Starting @ {start_time}")

    #Find our starting point, watch the video
    video = video_chooser(driver, search_terms, channel_url)
    driver.get(video.url)

    # Not particularly DRY but we can revisit
    if duration == 0:
        logging.info(f"Watching until the heat death of the universe")

        while True:
            logging.info(f"Watching {driver.title} - {driver.current_url}")
            time.sleep(30)

            WebDriverWait(driver, 20, 1).until(
                EC.element_to_be_clickable((By.ID, 'shorts-container'))
            ).send_keys(Keys.ARROW_DOWN)
    else:
        # Watch for the duration
        while datetime.now() < (start_time + timedelta(minutes=duration)):
            logging.info(f"Watching {video.title}")
            # Watch the video
            driver.get(video.url)
            watch_current_video(driver)


def video_chooser(driver: WebDriver, search_terms: list, channel_url: str):
    """Return a random video from either the passed channel OR from a randomly chosen search term"""
    return random.choice(
        [
            # Pick a random video from the channel
            #random.choice(get_channel_videos(driver, channel_url)),
            # Pick a random video from a random search term
            random.choice(do_search(driver, random.choice(search_terms))),
        ]
    )
