# 東京女子プロレス スケジュール反映プログラム

## 目的

東京女子プロレスの試合スケジュール(<https://www.ddtpro.com/schedules?teamId=tjpw>)を、カレンダーに反映させ、観戦の予定が組みやすくなるようにしたもの。

### いまできること

- 指定した期間の、東京女子プロレスの「大会情報」をスクレイピングする
- 取得したデータをNotionの「プロレス」に反映


### やりたいができてないこと

- 自身のGoogleカレンダーへ自動で反映させる
  - 標準出力された結果を、手動で反映させる必要がある
- 選手の誕生日の反映

## アーキテクチャ

Dockerコンテナ上で動作。

- app: アプリケーション
  - python3.11
- chrome: seleniarm/standalone-chromiumイメージをベースにした、Chromiumを起動するためのコンテナ
- アプリケーション(appコンテナ)がSelenium(chromeコンテナ)にリモート接続し、Chromiumを操作する

### Selenium採用の理由

スクレイピング対象のページがJavaScriptで動的に生成されるため、Seleniumを採用した。

## システム概要

クラスが少ないため省略。

## テスト

現時点でテストは未実装。

## 使用例

### プログラムの実行

```bash
docker-compose up -d

# start_date, end_dateをイジって実行する
docker-compose exec app python -m src.infrastructure.selenium_scraper
```

### ローカルで実行する

```bash
# .envについて SELENIUM_DOMAIN=http://localhost:4444 にしたうえで実行
python -m src
```

## CLIに組み込む

```shell
# 東京女子のスケジュール更新
function tjpw-update-schedule() {
  cd ~/git/src
  docker-compose down
  docker-compose up -d chrome
  sleep 60
  echo "[TJPW-UPDATE-SCHEDULE] 実行します"
  docker-compose up app

  # 上の処理が失敗した場合はここで終了
  if [ $? -ne 0 ]; then
    slack-post "[TJPW-UPDATE-SCHEDULE] Failed to update TJPW schedule."
    docker-compose down
    cd $OLDPWD
    return 1
  fi

  docker-compose down
  echo "[TJPW-UPDATE-SCHEDULE] 終了しました"
  cd $OLDPWD
}

```
