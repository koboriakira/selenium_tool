# 東京女子プロレス スケジュール反映プログラム

## 目的

東京女子プロレスの試合スケジュール(<https://www.ddtpro.com/schedules?teamId=tjpw>)を、自身のGoogleカレンダーに反映させ、観戦の予定が組みやすくなるようにしたもの。

### いまできること

- プログラムを実行すると、スケジュールが標準出力される

### やりたいができてないこと

- 自身のGoogleカレンダーへ自動で反映させる
  - 標準出力された結果を、手動で反映させる必要がある
- 選手の誕生日の反映

## アーキテクチャ

- Dockerコンテナ上で動作
  - app: アプリケーション
    - python3.11
  - chrome: seleniarm/standalone-chromiumイメージをベースにした、Chromiumを起動するためのコンテナ
  - アプリケーション(appコンテナ)がSelenium(chromeコンテナ)にリモート接続し、Chromiumを操作する

### Selenium採用の理由

BeautifulSoupなどのHTMLパーサーを使っても良いが、スクレイピング対象のページがJavaScriptで動的に生成されるため、Seleniumを採用した。

## システム概要

クラスが少ないため省略。

## テスト

現時点でテストは未実装。

## 使用例

### プログラムの実行

```bash
docker-compose up
docker-compose exec app python -m tjpw_schedule.scraping
```
