import logging
import random
from datetime import datetime, timedelta

from selenium.webdriver.remote.webdriver import WebDriver

from src.youtube_shorts import do_search, get_channel_videos, watch_wait_next


def watch_strategy(driver: WebDriver, search_terms: list, channel_url: str, duration: int = 60):
    """Watches YouTube videos found by searching the provided search_terms and from the given channel_url,
    for a duration in minutes."""

    start_time = datetime.now()
    logging.info(f"Starting @ {start_time}")

    # Find our starting point, watch the video
    video = video_chooser(driver, search_terms, channel_url)
    driver.get(video.url)

    # Not particularly DRY but we can revisit
    if duration == 0:
        logging.info(f"Watching until the heat death of the universe")

        i = 1

        while i > 0:
            last_watched = driver.current_url
            watch_wait_next(driver=driver, wait=15)
            next_up = driver.current_url

            if last_watched == next_up:
                logging.warning(f"We've watched {i} videos. Next video {next_up} appears to be the same as we've just watched ({last_watched})")
                duration = datetime.now() - start_time
                logging.info(f"Watched shorts for {duration.total_seconds()} seconds.")
                video = video_chooser(driver, search_terms, channel_url)
                driver.get(video.url)
                i = 1
                start_time = datetime.now()
            else:
                i += 1
    else:
        # Watch for the duration
        logging.info(f"Watching for {duration} minutes")

        while datetime.now() < (start_time + timedelta(minutes=duration)):
            watch_wait_next(driver=driver)


def video_chooser(driver: WebDriver, search_terms: list, channel_url: str):
    """Return a random video from either the passed channel OR from a randomly chosen search term"""
    return random.choice(
        [
            # Pick a random video from the channel
            # random.choice(get_channel_videos(driver, channel_url)),
            # Pick a random video from a random search term
            random.choice(do_search(driver, random.choice(search_terms))),
        ]
    )
