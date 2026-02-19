BrowserStack El País Opinion Scraper

This project is a Selenium-based automation script built as part of the BrowserStack Customer Engineering – Round 2 Technical Assignment.

The script scrapes articles from the Opinion section of El País, verifies that the website is served in Spanish, translates article titles from Spanish to English, performs basic text analysis, and runs cross-browser tests using BrowserStack Automate.

Features

Scrapes up to the first 5 articles from the El País Opinion section

Verifies the website language is Spanish (lang="es")

Extracts:

Article titles (Spanish)

Article content snippets (Spanish)

Cover images (if available)

Translates article titles from Spanish → English

Performs word frequency analysis on translated titles
(words appearing more than 2 times)

Executes:

A local Chrome validation run

BrowserStack Automate runs across desktop and mobile browsers

Marks BrowserStack sessions as Passed / Failed

Uses clear, session-labeled console logs

Handles errors gracefully without interrupting execution

Tech Stack

Python 3.10+

Selenium 4.x

BrowserStack Automate

deep-translator (Google Translate)

NLTK (stopwords and text analysis)

requests (image downloading)

webdriver-manager

concurrent.futures (parallel execution)

BrowserStack Test Matrix

| Session Name       | Platform                               | Browser |
|-------------------|----------------------------------------|---------|
| Win11-Chrome      | Windows 11                             | Chrome (latest) |
| Mac-Firefox       | macOS Monterey                         | Firefox (latest) |
| Win10-Edge        | Windows 10                             | Edge (latest) |
| Android-Chrome    | Samsung Galaxy S23 (Android 13)        | Chrome |
| iPhone-Safari     | iPhone 14 (iOS 16)                     | Safari |

Note:
Parallel execution is implemented in code. Actual concurrency depends on the BrowserStack plan.

Project Structure
browserstack-elpais-assignment/
│
├── elpais_scraper.py   # Main automation script
├── README.md           # Project documentation
└── .gitignore          # Ignored files and folders

Setup & Installation
1. Clone the repository
git clone https://github.com/Aryanv24/browserstack-elpais-assignment.git
cd browserstack-elpais-assignment

2. Create and activate a virtual environment
python -m venv venv

Windows

venv\Scripts\activate

macOS / Linux

source venv/bin/activate

3. Install dependencies
pip install selenium webdriver-manager requests nltk deep-translator
BrowserStack Configuration

Open elpais_scraper.py and update the following variables with your BrowserStack credentials:

BS_USERNAME = "YOUR_BROWSERSTACK_USERNAME"
BS_ACCESS_KEY = "YOUR_BROWSERSTACK_ACCESS_KEY"

You can find these credentials on the BrowserStack Automate Dashboard.

Running the Script
python elpais_scraper.py
Execution Flow
Step 1 — Local Run

Launches Chrome locally

Verifies the page language is Spanish

Scrapes up to 5 articles

Downloads images (if available)

Translates titles

Performs word frequency analysis

Step 2 — BrowserStack Run

Launches BrowserStack sessions

Executes the same logic across desktop and mobile browsers

Marks each session as Passed or Failed on BrowserStack

Output

Console logs show progress for each session

Session labels distinguish parallel BrowserStack runs

If no words repeat more than twice, the script reports:

No repeated words found.
Error Handling

Cookie banners are handled safely

Article loading issues are skipped without crashing the script

Image download failures do not stop execution

BrowserStack session failures are reported with a reason

Mixed logs during parallel execution are expected and handled using session labels

Author

Aryan Gupta

BrowserStack Customer Engineering – Technical Assignment