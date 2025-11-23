# ドキュメント

このディレクトリには、プロジェクトのドキュメントを配置します。

## Cursor Rulesとの関係

### 業務知識（`.cursor/rules/business/`）
詳細な業務知識や仕様は、以下のファイルに記載されています：

- `business/business-knowledge.mdc`: 業務知識とドメイン知識、ビジネスルール
- `business/business-services.mdc`: 業務サービス（ユースケース）の仕様

### 実装ルール（`.cursor/rules/implementation/`）
実装に関するルールは、以下のファイルに記載されています：

- `implementation/architecture.mdc`: アーキテクチャパターン
- `implementation/python.mdc`: Pythonコーディング規約
- `implementation/usecase.mdc`: ユースケース層の実装ルール
- `implementation/infrastructure.mdc`: インフラストラクチャ層の実装ルール
- `implementation/domain-models.mdc`: ドメインモデルの定義ルール
- `implementation/general.mdc`: プロジェクト全体の一般的なルール

これらのファイルは、Cursorがコード生成や修正を行う際に自動的に参照されます。

## ドキュメントの更新方法

1. 機能変更やビジネスルールの変更があった場合
2. 必要に応じて以下のドキュメントを更新（現在の状態を反映）：
   - `.cursor/rules/business/business-knowledge.mdc`: 業務知識の変更時
   - `.cursor/rules/business/business-services.mdc`: 業務サービスの仕様変更時
   - `.cursor/rules/implementation/`: 実装ルールの変更時
3. コードを修正

**注意**: ドキュメントには変更履歴ではなく、現在の状態のみを記載すること

