from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import os

# CSVファイル名
PREVIOUS_CSV = "previous_jobs.csv"  # IDだけ
CURRENT_CSV = "current_jobs.csv"    # 人が見る用

# 前回の案件IDを読み込む
previous_jobs = set()
if os.path.exists(PREVIOUS_CSV):
    with open(PREVIOUS_CSV, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            previous_jobs.add(row[0])

# Chromeのオプション設定
options = Options()
options.add_argument("--headless")  # GUIなし

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 取得したい複数カテゴリURL
urls = [
    "https://crowdworks.jp/public/jobs/search?category_id=226&order=new",
    "https://crowdworks.jp/public/jobs/search?category_id=230&order=new",
]

# 今回取得した案件ID、タイトル、リンクを格納
current_page_jobs = {}

for url in urls:
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # 「新着」 li を探す
    for new_li in soup.find_all("li", string="新着"):
        parent_block = new_li.find_parent("div", class_="UNzN7")
        if parent_block:
            a_tag = parent_block.find("h3").find("a")
            if a_tag:
                title = a_tag.get_text(strip=True)
                link = a_tag["href"]
                if link.startswith("/"):
                    link = "https://crowdworks.jp" + link
                job_id = link.split("/")[-1]
                current_page_jobs[job_id] = (title, link)

driver.quit()

# 新着案件: 前回にない案件だけ
new_jobs = {jid: data for jid, data in current_page_jobs.items() if jid not in previous_jobs}

# ターミナル表示
if new_jobs:
    print(f"新着案件 {len(new_jobs)} 件")

# current_jobs.csv に新着案件を書き出し
with open(CURRENT_CSV, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "タイトル", "リンク"])
    for jid, (title, link) in new_jobs.items():
        writer.writerow([jid, title, link])

# previous_jobs.csv を今回ページの新着案件IDで更新（ラベルが消えた案件は自動で消える）
with open(PREVIOUS_CSV, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    for jid in current_page_jobs.keys():
        writer.writerow([jid])
