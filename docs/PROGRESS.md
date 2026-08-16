# PROGRESS

Last Updated: 2026-08-15

## Current Phase

**Phase 0: Data Source Feasibility Study / PoC - Ready to Start**\
→ **Phase 0 Completed / MVP Design**

## Completed

### Project Planning

- 開発背景を整理した
- 中心となるユーザー課題を整理した
- 「複数メンバーを横断した配信探索」を中心価値と定義した
- MVP候補とMVP外の機能を整理した
- 小さな構成から段階的に発展させる方針を決めた
- Monolith First方針を決めた
- テスト可能な設計を目指す方針を決めた
- Git / GitHubを積極的に利用する方針を決めた

### Cost / Publication Policy

- 原則無料で開発・運用する方針を決めた
- 有料サービスは必要性と費用対効果を確認してから導入する方針を決めた
- 初期はローカル利用とする
- 規約上問題がなければ最終的に外部公開することを目標とした

### MVP Direction

MVPでは次の探索を中心とする方針を整理した。

- メンバー
- ゲーム / topic
- 配信期間
- タイトルキーワード

MVPでは次を原則含めない。

- Authentication / Authorization
- お気に入り
- 視聴履歴
- おすすめ
- Redis
- Queue / Worker
- Search Engine
- Microservices
- Kubernetes

### Documentation

初期ドキュメントを作成した。

- `README.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/REQUIREMENTS.md`
- `docs/DECISIONS.md`
- `docs/PROGRESS.md`

`docs/DESIGN.md` はPhase 0完了後に作成する。

## Phase 0: Data source PoC

Completed.

- YouTube Data API v3とHolodex API v2を比較
- VALORANT / Minecraft / Apex Legends / League of Legendsを実データで検証
- Holodex `topic_id` が代表4ゲームで一致
- 4チャンネル200動画を調査
- ライブ配信185件中183件にtopicあり（98.9%）
- `start_actual != null` とYouTube `liveStreamingDetails` の整合を確認
- Shorts / 通常動画がHolodex `type=stream` に含まれることを確認
- channel ID単位でチャンネル初期まで遡れることを確認
- paginationを実測し、50件×2ページで重複0件を確認
- MVPデータソースをHolodex API v2に決定

## Next Task

親チャットへ結果を戻し、次を行う。

1. `REQUIREMENTS.md` を更新してMVP要件を正式化する
2. `DECISIONS.md` にデータソース選定を記録する
3. `docs/DESIGN.md` を新規作成する
4. データモデルを設計する
5. MVP技術スタックを正式決定する
6. GitHubリポジトリ構成を確定する
7. Backend / DB実装フェーズへ進む

## Not Started

- DB設計
- Backend実装
- Frontend実装
- Docker
- CI/CD
- Cloud deployment
- 外部公開