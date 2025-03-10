# flaskとseleniumのサンプルプロジェクト

以下に各ファイルの説明と使い方を記載します。

## ファイル構成
- `http-demo/` ディレクトリ - Webの仕組みを理解するために JavaScript と Flask を利用した最小限のデモアプリケーション。
- `pyproject.toml` - Python プロジェクトの設定ファイル。この内容に基づいて `uv sync` コマンドで環境構築する。
- `flask-demo.py` - Flask を使用したデモアプリケーション。
- `send_calculate.sh` - 計算リクエストを送信するシェルスクリプト。
- `selenium-demo.py` - Selenium を使用したブラウザ自動化のデモスクリプト。
- `flask=selenium.py` - Flask と Selenium を組み合わせたスクリプト。

## 環境構築

1. `uv` をインストールしてください。
2. `uv sync` コマンドを用いて、`pyproject.toml` の内容に 基づいたパッケージインストールを行います。`pip install` に比べて非常に高速なことがわかります。

```bash
uv sync
```

## 各スクリプトの実行方法

### Flask アプリケーションの実行

`flask-demo.py` はシンプルな Flask API サーバーです。Flaskサーバを停止する場合は`ctrl + C` を押してください。

```sh
python flask-demo.py
```

サーバーが起動し、`http://127.0.0.1:5123` でアクセスできます。

### `send_calculate.sh` の実行

このスクリプトは `http://127.0.0.1:5123/calculate` に JSON データを POST します。
Flask サーバーが適切に動作していることを確認してから実行してください。

```sh
./send_calculate.sh
```

シェルスクリプトの権限が不足している場合、上記のコマンドが実行できない可能性があります。
その際は、ユーザーに実行権限を付与してから再実行しましょう。
```sh
chmod +x send_calculate.sh
./send_calculate.sh
```

送信されるデータ例:

```json
{
  "numbers": [1,2,3,4,5]
}
```




### Selenium スクリプトの実行

Selenium を利用したWebスクレイピングのデモンストレーションです。`Python Selenium` と検索してトップに出てくるwebサイトのスクリーンショットを保存します。

```sh
python selenium-demo.py
```

## `flask-selenium.py`について

`flask-selenium.py` は、SeleniumのスクリプトをAPIとして提供するためのスクリプトになっています。
Webスクレイピング機能をAPIとして提供することで、HTTPリクエストをトリガーにしてスクリプトを実行できます。
ただし、外部にこのAPIを公開した場合は、誰もがそのスクレイピング機能にアクセス可能となってしまいます。
実際の運用においては、パスワードを用いた認証機能や、IPアドレスのアクセス制限をかけることが必要です。

また、Chromeの検索欄に `127.0.0.1:5128/selenium` と入力しただけ（エンターを押していない）のに、スクリプトが実行される場合があります。
これはChromeのオートコンプリート機能もしくはプリフェッチ機能が起動していることによるものです。
