# DECISIONS

## 1. 文書の位置付け

この文書では、プロジェクトにおける重要な判断と、その理由・代替案を記録する。

まだ未決定の項目は確定事項として記録せず、Pending Decisionsとして管理する。

---

## D001: 小さな構成から段階的に発展させる

**Status:** Accepted

### Decision

最初から完成形のインフラ・アーキテクチャを構築せず、MVPを最小構成で作り、実際の問題を確認してから新しい技術を導入する。

### Reason

本プロジェクトはアプリ完成だけでなく、技術を「なぜ必要なのか」まで理解することを目的としているため。

### Rejected / Deferred Alternatives

- 最初からAWSを全面採用する
- 最初からRedis / Queueを導入する
- 最初からMicroservicesに分割する

---

## D002: Monolith First

**Status:** Accepted

### Decision

MVPではFrontendとBackendを分離しても、Backend内部を複数サービスへ分割しない単純なMonolith構成を基本とする。

### Reason

個人開発のMVPであり、Microservicesによる運用・通信・デプロイ複雑性を正当化する要件が現時点では存在しないため。

---

## D003: 原則無料で開発・運用する

**Status:** Accepted

### Decision

MVP完成および初期公開までは無料サービス・無料枠を優先する。

有料サービスを導入する場合は、問題・費用・改善効果を確認してから決める。

### Reason

個人開発であり、現段階では固定費を必要とする要件がないため。

### Notes

独自ドメインや常時稼働サーバー等は将来必要になれば検討する。

---

## D004: 最終的な外部公開を目標とする

**Status:** Accepted with Condition

### Decision

開発初期はローカルで自分だけが利用し、完成度が上がったら外部公開できるWebアプリを目標とする。

### Condition

データソース、API、コンテンツ、名称、画像等の利用規約・公開条件に問題がないこと。

### Fallback

公開条件を満たせない場合は、自分専用システムとして運用する。

---

## D005: Webアプリとして開発する

**Status:** Accepted

### Decision

最終成果物はWebブラウザから利用できるシステムとする。

### Reason

- 自分が複数環境から利用しやすい
- 外部公開と相性が良い
- Frontend / Backend / HTTP / REST等を実践的に学べる
- ポートフォリオとして動く成果物を提示しやすい

---

## D006: MVPは探索機能を中心とする

**Status:** Accepted

### Decision

MVPでは「配信を横断的に探す」という中心課題に集中する。

### Included Direction

- メンバー
- ゲーム / topic
- 期間
- キーワード
- 配信一覧

### Deferred

- アカウント
- お気に入り
- 視聴履歴
- おすすめ
- 高度な検索基盤

---

## D007: Webアプリ本体より先にデータソースPoCを行う

**Status:** Accepted

### Decision

React、FastAPI、DB本実装へ進む前に、必要な配信データを取得できるか確認するPhase 0を行う。

### Reason

本システムの主要価値である「ゲーム横断探索」に必要な具体的ゲーム情報の取得方法が未確定であり、ここが成立しない場合は要件・データモデル・設計が変わるため。

---

## D008: 初期ドキュメントは5ファイルで管理する

**Status:** Accepted

### Decision

現時点では次のファイルを維持する。

- `README.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/REQUIREMENTS.md`
- `docs/DECISIONS.md`
- `docs/PROGRESS.md`

`docs/DESIGN.md` はデータソースPoC後に作成する。

### Reason

設計が未確定な段階で詳細設計を文書化すると、PoC後の書き直しが大きくなるため。

---

# Pending Decisions

以下はまだ決定しない。

## P001: データソース

候補:

- Holodex API
- YouTube Data API v3
- その他の公式・公開手段

Phase 0で決定する。

## P002: game / topicの取得・管理方法

データソースの実データを確認して決定する。

## P003: Frontend技術

第一候補:

- React
- TypeScript
- Vite

Phase 0完了後、MVP設計時に正式決定する。

## P004: Backend技術

第一候補:

- FastAPI
- Python

Phase 0完了後、MVP設計時に正式決定する。

## P005: MVP Database

第一候補:

- SQLite

将来候補:

- PostgreSQL

Phase 0完了後、保存データと更新方式を確認して正式決定する。

## P006: 対象メンバー

第一候補:

- VSPO! JP

対象チャンネルの管理方法も含めてPoC後に決定する。

## P007: 初回取得期間

候補:

- 直近数か月
- 直近1年
- 全期間

データ量とAPI制限を確認して決定する。

## P008: Hosting / Cloud

MVPローカル完成後に検討する。

現時点では特定のクラウドサービスを採用しない。

## Data source for stream metadata

MVPの配信メタデータ取得元には Holodex API v2 を採用する。

YouTube Data API v3 もPoCで比較したが、本番のデータ取得元には使用しない。

### 理由

- Holodexは `topic_id` として具体的なゲーム/トピックを取得できる
- `include=live_info` により実配信の開始・終了日時を取得できる
- PoCでは `start_actual != null` によるライブ配信判定がYouTube Data APIの
  `liveStreamingDetails` と一致した
- `channel_id` + paginationによりチャンネル初期まで遡って取得できた
- YouTube Data API単独では具体的ゲーム名を取得できない
- YouTube APIと外部データを組み合わせる構成はDeveloper Policies上の制約を
  複雑にするため避ける

### 配信判定

Holodexの `type=stream` はライブ配信を意味しない。
Shortsや通常投稿も含まれるため、MVPでは

`start_actual != null`

を配信アーカイブの判定条件とする。

### Topic

`topic_id` は検索用メタデータとして使用するが、
公式または完全に正確なゲーム情報とは扱わない。