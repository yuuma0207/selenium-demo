import time
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.environ["WDM_LOCAL"] = "1" # プロジェクト内にWebDriverをダウンロードする設定

# 1. ChromeDriver を使ってブラウザを立ち上げる
service = Service(ChromeDriverManager().install())
options = Options()
# options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=service, options=options,)

try:
    # 2. 指定したURLを開く
    driver.get("https://www.google.com")

    time.sleep(3)

    # 3. 要素を探す（検索ボックスの要素を取得）
    search_box = driver.find_element(By.NAME, "q")

    # 4. キーワードを入力して Enter を押す
    search_box.send_keys("Selenium Python")
    search_box.send_keys(Keys.RETURN)

    # 検索結果が表示されるのを待つ
    time.sleep(3)
    try:
        # reCAPTCHA iframe の存在を確認
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'recaptcha')]"))
        )
        print("reCAPTCHA検出！手動で解除してください...")

        # reCAPTCHA解除を待つ → Google検索結果が表示されるまで待機
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.ID, "search"))  # Googleの検索結果が表示されるID
        )
        print("reCAPTCHA解除完了！")

    except:
        print("reCAPTCHAは表示されませんでした")
    # 最初の検索結果のタイトルとURLを取得
    # 検索結果の最初の記事を取得
    try:
        first_result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='search']//a/h3"))
        )
        article_title = first_result.text
        article_url = first_result.find_element(By.XPATH, "./ancestor::a").get_attribute("href")

        print("検索結果を取得しました！")
        print(f"タイトル: {article_title}")
        print(f"URL: {article_url}")
        time.sleep(3)

        # 取得したURLへ遷移
        driver.get(article_url)
        print("遷移完了！")
        print("終了するには何かキーを押してください...")
        input()
        print("終了しました！")


    except:
        print("検索結果を取得できませんでした")

    # 6. スクリーンショットを保存（確認用）
    print("スクリーンショット保存中...")
    time.sleep(3)
    driver.save_screenshot("search_result.png")

finally:
    # 7. ブラウザを閉じる
    driver.quit()