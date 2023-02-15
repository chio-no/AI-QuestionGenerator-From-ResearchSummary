# AI-QuestionGenerator-From-ResearchSummary
WISS2022で発表した「研究概要を基に質問を生成するAIシステム」のソースコードです

## 使い方
1. Slack Bot用のトークン2つ（アプリレベル、ボットレベル）とDeepl API, Open AI APIのキーを用意してください
（Slack Botの作成とワークスペースのインストールは済んでいる前提です）
2. 用意したトークンとキーを`functions.py`と`SlackAPI.py`に適用してください
3. `SlackAPI.py`を実行

※この実装だとDMで動作しません。DMで動作させたい場合は`SlackAPI.py`に以下のコードを追加してください
```python:SlackAPI.py
@Qapp.message("<@導入したSlack BotのユーザID>")
def message_yoi(event, say):
    QSlackInterface(event["user"], event["channel"], event["text"], bot_token)
```

## ライセンス
MITライセンスに基づいて、このソフトウェアおよび関連するファイル（以下、ソフトウェアと呼びます）を使用、複製、変更、結合、公開、配布、サブライセンス、および/または販売することができます。このソフトウェアは、何らかの保証なしで提供されます。すなわち、このソフトウェアについての暗黙の保証、商業的な適合性、特定の目的への適合性、および非侵害性の保証を含め、限定されません。著作権者または著作権保持者は、いかなる場合においても、いかなる請求、損害賠償、またはその他の義務を負わないものとします。
