## Stream data collection

VSPO! JPメンバーとYouTube channel IDはアプリ側でmaster管理する。

各channel IDについてHolodex `/videos` を取得する。

- `type=stream`
- `status=past`
- `include=live_info`
- `limit=50`
- `offset` によるpagination

初回は全履歴をbackfillする。
通常更新では直近の動画を再取得し、YouTube video IDをキーにupsertする。

`start_actual == null` の動画はMVPの配信アーカイブ対象外とする。

Holodex API KeyはBackend/collectorのみで使用し、Frontendへ公開しない。