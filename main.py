import argparse
import logging
import sys
from datetime import datetime

from selenium.common.exceptions import TimeoutException

from src.browser_driver import get_browser_driver
from src.watch_strategy import watch_strategy, get_current_ip
from src.youtube_shorts import close_cookie_popup


def main():
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(filename=f'yt-shorts-{datetime.now()}.log', encoding='utf-8')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))  # We also want it to stdout

    # Setup Selenium web driver
    parser = get_arg_parser()
    args = parser.parse_args()
    driver = get_browser_driver(args.browser)

    try:
        # Log our current ip
        ip = get_current_ip(driver)
        logging.info(f"Current IP: {ip}")

        if ":" not in ip:
            logging.error(f"We're connecting over IPv4. Quitting.")
            raise ConnectionError()

        # Start watching videos
        while True:
            try:
                # Reject YouTube's cookies
                close_cookie_popup(driver)
                watch_strategy(driver, args.search_terms, args.channel_url, duration=0)
            except TimeoutException:
                logging.warning("Got a timeout. This is probably a CAPTCHA. Exiting.")
                driver.quit()
                raise
            except Exception as e:
                logging.error(repr(e))
                pass
    except:
        # Make sure the driver doesn't leak no matter what
        driver.quit()
        raise


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-B",
        "--browser",
        choices=["chrome", "firefox", "edge"],
        default="edge",
        type=str,
        help="Select the driver/browser to use for executing the script.",
    )
    parser.add_argument(
        "-s",
        "--search-terms",
        dest="search_terms",
        action="append",
        help="This argument declares a list of search terms which get viewed.",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--channel-url",
        default="https://www.youtube.com/@PrivacyInternational",
        dest="channel_url",
        type=str,
        help="Channel URL if not declared it uses Privacy International's channel URL as default.",
        required=False,
    )
    return parser


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Quitting watcher")
