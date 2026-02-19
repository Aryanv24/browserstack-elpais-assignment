# BrowserStack El País Opinion Scraper

This repository contains a Selenium-based automation script created as part of the **BrowserStack Customer Engineering – Round 2 Technical Assignment**.

The script scrapes articles from the **Opinion** section of *El País*, verifies that the website is displayed in Spanish, translates article titles to English, performs text analysis, and runs cross-browser tests using **BrowserStack Automate**.

---

## Features

- Scrapes the first **5 articles** from the El País Opinion section
- Verifies the website language is **Spanish** (`lang="es"`)
- Extracts:
  - Article titles (Spanish)
  - Article content snippets (Spanish)
  - Cover images (if available)
- Translates article titles from **Spanish → English**
- Performs **word frequency analysis** on translated titles  
  (words appearing more than 2 times)
- Executes:
  - A **local Chrome run**
  - **BrowserStack Automate runs** across multiple browsers/devices
- Marks BrowserStack sessions as **Passed / Failed**
- Handles failures gracefully without stopping execution

---

## Project Structure
browserstack-elpais-assignment/
│
├── elpais_scraper.py # Main automation script
├── README.md # Project documentation
└── .gitignore # Ignored files and folders

## Setup & Installation

### 1. Clone the repository

```bash
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

Open elpais_scraper.py and update the following variables:

BS_USERNAME = "YOUR_BROWSERSTACK_USERNAME"
BS_ACCESS_KEY = "YOUR_BROWSERSTACK_ACCESS_KEY"

You can find these credentials on the BrowserStack Automate Dashboard.

Running the Script
python elpais_scraper.py
Execution Flow
Step 1 — Local Run

Launches Chrome locally

Confirms the website language is Spanish

Scrapes up to 5 articles

Downloads images (if available)

Translates article titles

Performs word frequency analysis

Step 2 — BrowserStack Run

Launches BrowserStack sessions

Runs the same logic across desktop and mobile browsers

Marks each session as Passed or Failed on BrowserStack

Note: Parallel execution is implemented in code. Actual concurrency depends on the BrowserStack plan.

Output

Console logs display progress for each session

Session labels identify BrowserStack runs

If no words repeat more than twice, the script reports:

No repeated words found.
Error Handling

Cookie banners are handled safely

Article loading failures are skipped

Image download failures do not stop execution

BrowserStack session failures are reported with a reason

Mixed logs during parallel execution are expected

Author

Aryan Gupta
BrowserStack Customer Engineering – Technical Assignment