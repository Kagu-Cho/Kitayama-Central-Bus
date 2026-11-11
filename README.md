# 北山中央バス発車案内 — Render公開用

最新版Ver.10（画面内に自動縮小）をベースにした、Render Web Service公開用ファイルです。
データ表示・地図案内・運行終了表示は元のままです。

## 重要: 公開前に確認してください

本アプリは非公式で、京阪バスのバスロケページから情報を取得します。
京阪バス公式サイトの利用規約には、権利者の承諾なく私的使用の範囲を超えて
サイトの著作物等を使用・公開できない旨の記載があります。
外部公開・不特定多数への提供を行う前に、データの利用・再配信について許諾を得るか、
公式に許可されたデータソースへ変更することをおすすめします。
https://www.keihanbus.jp/terms/

## Renderでの公開手順（GitHub経由）

1. このZIPを解凍します。
2. GitHubで新規リポジトリを作成します（公開・非公開のどちらでも可）。
3. 解凍した `app.py`、`web_app.py`、`requirements.txt`、
   `.python-version`、`render.yaml`、必要ならREADMEをリポジトリ直下へアップロードします。
4. Renderの https://dashboard.render.com/ で `New` → `Web Service`。
5. GitHubの該当リポジトリを選択します。
6. 画面の入力項目は以下に設定します。

   - Language: `Python 3`
   - Region: `Singapore`
   - Instance: `Free`（常時稼働には有料プランが必要）
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 60 web_app:app`

7. `Deploy Web Service` を選択します。
8. `https://<サービス名>.onrender.com/` 形式のアドレスが発行されます。
9. 画面が表示されたら `/api/sources` で取得状況を確認できます。

`render.yaml` があるため、Renderの `New` → `Blueprint` から作成することもできます。

## インターネット版で変更した点

- UTCで動くサーバーでも必ず日本時間で取得・並び替え・表示します。
- WindowsのBATではなく、GunicornでWebアプリを起動します。
- データ更新はサーバー側で1分間隔とし、閲覧者が増えても取得先へのアクセスを増やしません。
- 更新スレッドが二重にならないようGunicornを1ワーカーに制限します。
- 画面の自動縮小、案内地図、遅延表示、運行終了時の表示は維持します。

## 無料プランの注意

Renderの無料Webサービスは15分間アクセスがないと停止し、
再アクセス時に起動するまで約1分かかる場合があります。
停止・再起動後は新しい情報を再取得するため、一時的に「取得中…」と表示されます。
常時表示端末で使うときは有料のWeb Serviceの利用を検討してください。

## ローカルで試す場合

```
python -m pip install -r requirements.txt
python app.py --demo
```

http://127.0.0.1:5000/ を開きます。`--demo` は架空の便の表示確認用です。
データ取得を行う本番モードは `python app.py` です。

## うまく動かない場合

- Renderの Logs に `ModuleNotFoundError` が出ていないか確認してください。
- `/api/sources` の `ok` がすべて `false` のときは上流サイトへの通信失敗や仕様変更が考えられます。
- 外部公開先から京阪バス側のページへ接続できるかは未確認です。
- このアプリは京阪バスの公式サービスではありません。
