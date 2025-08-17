# CrowdWorks New Jobs Scraper

## 概要
このPythonスクリプトは、クラウドワークスの指定カテゴリの新着案件をスクレイピングして取得します。  
前回取得した案件と比較して、新規案件のみを `current_jobs.csv` に出力し、全案件IDを `previous_jobs.csv` に保存します。

- `previous_jobs.csv`：比較用。案件IDのみ保存
- `current_jobs.csv`：今回の新着案件。案件IDとURLを保存
- ターミナルには今回の新着案件数を表示

## 特徴
- 複数カテゴリURLに対応
- 「新着」ラベル付き案件のみ抽出
- CSVファイルで簡単に管理可能
- ヘッドレスモードでGUIなしで実行可能

## 必要なライブラリ
```bash
pip install -r requirements.txt
```

## 使い方
1. urlsリストに取得したいカテゴリURLを追加します．
2. ターミナルでスクリプトを実行します．
```bash
python get_new_works.py
```
3. 新着案件があれば current_jobs.csv に出力され、previous_jobs.csv は自動で更新されます。
