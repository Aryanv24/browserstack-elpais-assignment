

import os
import re
import time
import requests
import nltk

from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from deep_translator import GoogleTranslator
from nltk.corpus import stopwords

# Download stopwords once
nltk.download("stopwords")


BASE_URL = "https://elpais.com/opinion/"
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# 🔴 REPLACE WITH YOUR CREDENTIALS
BS_USERNAME = "aryangupta_pgQrR8"
BS_ACCESS_KEY = "UGhHhNXEKaAzwfy5Pvqz"


def download_image(url, path):
    try:
        r = requests.get(url, timeout=5)
        with open(path, "wb") as f:
            f.write(r.content)
    except:
        pass


def set_bs_status(driver, status, reason):
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", '
        '"arguments": {"status": "%s", "reason": "%s"}}'
        % (status, reason[:200])
    )



def scrape_articles(driver, label="LOCAL"):
    wait = WebDriverWait(driver, 15)

    def log(msg):
        print(f"[{label}] {msg}")

    driver.get(BASE_URL)

    # Accept cookies if present
    try:
        cookie_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceptar')]"))
        )
        cookie_btn.click()
        log("Cookie banner accepted")
    except:
        pass

    # Verify Spanish
    lang = driver.find_element(By.TAG_NAME, "html").get_attribute("lang")
    log(f"Language detected: {lang}")

    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article")))

    # Collect up to 5 article links
    article_elements = driver.find_elements(By.CSS_SELECTOR, "h2 a, h3 a")

    links = []
    for elem in article_elements:
        if len(links) == 5:
            break
        title = elem.text.strip()
        link = elem.get_attribute("href")
        if title and link:
            links.append(link)

    log(f"Collected {len(links)} article links")

    final_titles = []

    for i, link in enumerate(links):
        try:
            driver.get(link)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))

            title = driver.find_element(By.TAG_NAME, "h1").text.strip()
            log(f"Article {i+1} Title (Spanish): {title}")

            paragraphs = driver.find_elements(By.CSS_SELECTOR, "article p")
            content = ""
            for p in paragraphs:
                if len(p.text.strip()) > 50:
                    content = p.text.strip()
                    break

            log(f"Content (Spanish): {content[:120]}...")

            images = driver.find_elements(By.CSS_SELECTOR, "article img")
            for img in images:
                img_url = img.get_attribute("src")
                if img_url and img_url.startswith("http"):
                    download_image(img_url, f"{IMAGE_DIR}/{label}_{i+1}.jpg")
                    log("Image downloaded")
                    break

            final_titles.append(title)

        except Exception:
            log(f"Handled Article {i+1} safely")

    return final_titles



def translate_titles(titles):
    translator = GoogleTranslator(source="es", target="en")
    translated = []

    print("\nTranslating Titles...\n")
    for t in titles:
        try:
            en = translator.translate(t)
            translated.append(en)
            print("English:", en)
        except:
            translated.append(t)

    return translated



def analyze_words(titles):
    stop_words = set(stopwords.words("english"))

    text = " ".join(titles).lower()
    text = re.sub(r"[^a-z ]", "", text)

    words = [w for w in text.split() if w not in stop_words]
    counts = Counter(words)

    print("\nRepeated Words (>2 times):")
    found = False
    for w, c in counts.items():
        if c > 2:
            print(w, c)
            found = True

    if not found:
        print("No repeated words found.")



def run_local():
    print("\n========== LOCAL RUN ==========\n")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )

    start = time.time()
    titles = scrape_articles(driver, label="LOCAL")
    driver.quit()

    translated = translate_titles(titles)
    analyze_words(translated)

    print("\nLocal Runtime:", round(time.time() - start, 2), "seconds")



def run_browserstack():
    print("\n========== BROWSERSTACK RUN ==========\n")

    environments = [
        {
            "browserName": "Chrome",
            "browserVersion": "latest",
            "bstack:options": {
                "os": "Windows",
                "osVersion": "11",
                "sessionName": "Win11-Chrome"
            }
        },
        {
            "browserName": "Firefox",
            "browserVersion": "latest",
            "bstack:options": {
                "os": "OS X",
                "osVersion": "Monterey",
                "sessionName": "Mac-Firefox"
            }
        },
        {
            "browserName": "Edge",
            "browserVersion": "latest",
            "bstack:options": {
                "os": "Windows",
                "osVersion": "10",
                "sessionName": "Win10-Edge"
            }
        },
        {
            "browserName": "Chrome",
            "bstack:options": {
                "deviceName": "Samsung Galaxy S23",
                "osVersion": "13.0",
                "realMobile": "true",
                "sessionName": "Android-Chrome"
            }
        },
        {
            "browserName": "Safari",
            "bstack:options": {
                "deviceName": "iPhone 14",
                "osVersion": "16",
                "realMobile": "true",
                "sessionName": "iPhone-Safari"
            }
        }
    ]

    def run_env(cap):
        options = webdriver.ChromeOptions()
        for k, v in cap.items():
            options.set_capability(k, v)

        driver = webdriver.Remote(
            command_executor=f"https://{BS_USERNAME}:{BS_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
            options=options
        )

        label = cap["bstack:options"]["sessionName"]

        try:
            scrape_articles(driver, label=label)
            set_bs_status(driver, "passed", "El Pais scraping completed successfully")
        except Exception as e:
            set_bs_status(driver, "failed", str(e))
        finally:
            driver.quit()

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(run_env, environments)



if __name__ == "__main__":
    run_local()
    run_browserstack()