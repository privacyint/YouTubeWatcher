import logging
import random
from datetime import datetime, timedelta

from selenium.webdriver.remote.webdriver import WebDriver

from src.youtube_shorts import do_search, get_channel_videos, watch_current_video_then_move_to_next


def watch_strategy(driver: WebDriver, search_terms: list, channel_url: str, duration: int = 60):
    """Watches YouTube videos found by searching the provided search_terms and from the given channel_url,
    for a duration in minutes."""

    start_time = datetime.now()
    logging.info(f"== Starting run @ {start_time} ==")

    # Find our starting point, watch the video
    video = video_chooser(driver, search_terms, channel_url)
    driver.get(video.url)

    i = 1

    start_time = datetime.now()  # When we actually start watching videos

    # Not particularly DRY but we can revisit
    if duration == 0:
        logging.info(f"== Watching until the heat death of the universe ==")

        while i > 0:
            try:
                watch_current_video_then_move_to_next(driver=driver, watch_for_seconds=5)

                i += 1

            except Exception as e:
                watched_duration = datetime.now() - start_time
                exception_parser(e, watched_duration, i, driver)
                watch_strategy(driver, search_terms, channel_url, duration)
    else:
        # Watch for the duration
        logging.info(f"Watching for {duration} minutes")

        while datetime.now() < (start_time + timedelta(minutes=duration)):
            try:
                watch_current_video_then_move_to_next(driver=driver)

                i += 1

            except Exception as e:
                watched_duration = datetime.now() - start_time
                exception_parser(e, watched_duration, i, driver)


def exception_parser(e, watched_duration, number_of_videos_watched, driver):
    logging.warning(f"== Watched {number_of_videos_watched} videos for ~{round(watched_duration.total_seconds())} "
                    f"seconds, which is roughly {round(watched_duration.total_seconds() / 60)} minutes. ==")
    logging.error(f"== Caught exception: {e} ==")
    logging.info(f"== Finishing run @ {datetime.now()} ==")

    driver.get_screenshot_as_file(f"looped_screenshots/{driver.current_url}-{datetime.now()}.png")


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
