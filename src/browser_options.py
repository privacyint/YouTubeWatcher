from selenium import webdriver


def get_firefox_options() -> webdriver.FirefoxOptions:
    """Configure firefox for automated watching"""
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.set_preference("intl.accept_languages", "en-us")
    # Always autoplay videos
    firefox_options.set_preference("media.autoplay.default", 0)
    firefox_options.set_preference("media.volume_scale", "0.0")

    return firefox_options

