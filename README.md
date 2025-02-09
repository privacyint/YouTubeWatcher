<p align="center">
    <a href="https://github.com/ContentAutomation"><img src="https://contentautomation.s3.eu-central-1.amazonaws.com/logo.png" alt="Logo" width="150"/></a>
    <br />
    <br />
    <a href="http://choosealicense.com/licenses/mit/"><img src="https://img.shields.io/badge/license-MIT-3C93B4.svg?style=flat" alt="MIT License"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
    <br />
    <a href="https://www.youtube.com/channel/UCqq27nknJ3fe5IvrAbfuEwQ"><img src="https://img.shields.io/badge/YouTube-FF0000.svg?style=flat&logo=youtube" alt="Platform: YouTube"></a>
        <a href="https://www.selenium.dev/documentation/en/"><img src="https://img.shields.io/badge/Selenium-43B02A.svg?logo=Selenium&logoColor=white&labelColor=43B02A" alt="Automation supporting Firefox and Chrome"></a>
    <br />
         <a href="https://www.mozilla.org/en-US/firefox/new/"><img src="https://img.shields.io/badge/Firefox-FF7139.svg?logo=Firefox-Browser&logoColor=white" alt="Firefox supported"></a>
         <a href="https://www.google.com/chrome/"><img src="https://img.shields.io/badge/Chrome-4285F4.svg?logo=Google-Chrome&logoColor=white" alt="Chrome supported"></a>
    <br />
    <br />
    <i>An automated, headless YouTube Shorts Watcher and Scraper</i>
    <br />
<br />
    <i><b>Original Authors</b>:
        <a href="https://github.com/ChristianCoenen">Christian C.</a>,
        <a href="https://github.com/MorMund">Moritz M.</a>,
        <a href="https://github.com/lucaSchilling">Luca S. </a>
    </i>
    <br />
    <i><b>Related Projects</b>:
        <a href="https://github.com/ContentAutomation/YouTubeUploader">YouTube Uploader</a>,
        <a href="https://github.com/ContentAutomation/TwitchCompilationCreator">Twitch Compilation Creator</a>,
        <a href="https://github.com/ContentAutomation/NeuralNetworks">Neural Networks</a>
    </i>
   <br />
    <i><b>Adapted for PI by</b>:
        <a href="https://github.com/EdGeraghty">Ed Geraghty</a>
    </i>

</p>

<hr />

## About

Searches YouTube shorts, queries recommended videos and watches them. All fully automated.

## Setup

### YouTube Automation

This project requires [Poetry](https://python-poetry.org/) to install the required dependencies.
Check out [this link](https://python-poetry.org/docs/) to install Poetry on your operating system.

Make sure you have installed [Python](https://www.python.org/downloads/) 3.8 or later! Otherwise Step 3 will let you know that you have no compatible Python version installed.

1. Clone/Download this repository
2. Navigate to the root of the repository
3. Run ```poetry install``` to create a virtual environment with Poetry
4. Ensure the browser you wish to use is installed on the machine.
5. Run ```poetry run python main.py``` to run the program. Alternatively you can run ```poetry shell``` followed by ```python main.py```. By default this connects to MS Edge Browser. To automate a different Browser use the `--browser [chrome/firefox/edge]` command line option.

## Run Parameters
All of these parameters are optional and a default value will be used if they are not defined. 
You can also get these definitions by running ```main.py --help```

```
usage: main.py [-h] [-H] [-B {chromium,firefox,edge}] -s SEARCH_TERMS [-c CHANNEL_URL]

optional arguments:
  -h, --help            show this help message and exit
  -H, --headless        run the browser headlessly
  -B {chromium,firefox,edge}, --browser {chromium,firefox,edge}
                        Select the driver/browser to use for executing the script. Defaults to Edge.
  -s SEARCH_TERMS, --search-terms SEARCH_TERMS
                        This argument declares a list of search terms which get viewed.
  -c CHANNEL_URL, --channel-url CHANNEL_URL
                        Channel URL if not declared it uses Privacy International's channel URL as default.
```
