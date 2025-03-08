import time
import os
import base64
import numpy as np
from flask import Flask, request, jsonify, render_template_string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

os.environ["WDM_LOCAL"] = "1" # プロジェクト内にWebDriverをダウンロード

app = Flask(__name__)

def setup_driver():
    """ SeleniumのWebDriverをセットアップ """
    service = Service(ChromeDriverManager().install())
    options = Options()
    # options.add_argument("--headless") # ヘッドレスモードを有効にする場合
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(service=service, options=options)

def google_search(driver, query):
    """ Google検索を実行し、最初の検索結果のタイトルとURLを取得 """
    driver.get("https://www.google.com")
    
    # 検索ボックスを取得し、キーワードを入力
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(3)
    
    # reCAPTCHAが表示されたら手動で解除を待つ
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
        ))
        print("reCAPTCHA検出！手動で解除してください...")
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, "search")))
        print("reCAPTCHA解除完了！")
    except:
        print("reCAPTCHAは表示されませんでした")
    
    # 最初の検索結果を取得
    try:
        first_result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='search']//a/h3"))
        )
        title = first_result.text
        url = first_result.find_element(By.XPATH, "./ancestor::a").get_attribute("href")
        print(f"タイトル: {title}\nURL: {url}")
        return title, url
    except:
        print("検索結果を取得できませんでした")
        return "タイトル取得失敗", "#"

def take_screenshot(driver):
    """ 現在のページのスクリーンショットを取得し、Base64エンコードして返す """
    time.sleep(3)
    screenshot = driver.get_screenshot_as_png()
    return base64.b64encode(screenshot).decode("utf-8")

@app.route("/calculate", methods=["POST"])
def calculate():
    """ 数値配列の合計と平均を計算するAPI """
    data = request.json
    arr = np.array(data.get('numbers', []))
    return jsonify({'total': float(np.sum(arr)), 'average': float(np.mean(arr))})

@app.route("/selenium", methods=["GET"])
def run_selenium():
    """ Seleniumを使ってGoogle検索し、結果を取得してHTMLとして表示 """
    driver = setup_driver()
    try:
        query = "Selenium Python"
        title, url = google_search(driver, query)
        driver.get(url)  # 検索結果のページに遷移
        screenshot = take_screenshot(driver)
    finally:
        driver.quit()
    
    # HTMLページとして表示
    html_template = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>検索結果のスクリーンショット</title>
    </head>
    <body>
        <h1>検索結果のスクリーンショット</h1>
        <p><strong>タイトル:</strong> {{ title }}</p>
        <p><strong>URL:</strong> <a href="{{ url }}" target="_blank">{{ url }}</a></p>
        <h2>スクリーンショット</h2>
        <img src="data:image/png;base64,{{ screenshot }}" alt="スクリーンショット">
    </body>
    </html>
    """
    return render_template_string(html_template, title=title, url=url, screenshot=screenshot)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5123)
