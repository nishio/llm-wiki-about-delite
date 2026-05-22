# Index

宇田川浩行氏（デライト作者）の思想を整理した Wiki の索引。`/` で区切られたカテゴリは便宜的。実際には多くのページが横断的につながっている。

## ソース要約

- [sources/villagepump-デライト.2hop.md](sources/villagepump-デライト.2hop.md) — 井戸端（Scrapbox `/villagepump`）の「デライト」ページ + 1/2-hop 関連ページ 146件。本人発言が密度高く含まれる。
- [sources/arpla-デライト.2hop.md](sources/arpla-デライト.2hop.md) — Scrapbox `arpla`（アープラ）の「デライト」ページ + 1/2-hop 関連ページ 51件。ほぼすべて **久住哲** 氏による分析・解釈で、設計思想の理論的整理が中心。
- [sources/delite-project.all.md](sources/delite-project.all.md) — Scrapbox `/delite`（[デライト Collabox（仮）](concepts/Collabox.md)）プロジェクト全 43 ページ。zatsma 氏・804C 氏らによるユーザー側の実践知。本人発言はほぼ無いが、輪符の書式・[未公開輪郭](concepts/未公開輪郭.md) の運用比較・[デコ二刀流](concepts/デコ二刀流.md) の実例の供給源。
- [sources/dlt-udagawa-corpus.md](sources/dlt-udagawa-corpus.md) — **デライト本体** (`dlt.kitetu.com`) から K#F85E プロフィールを起点に BFS 取得した **宇田川氏自身の輪郭 505 件**（うち本文あり 234 件）。日記・越省・本人による概念定義文書を含む。`raw/dlt-udagawa/outlines.jsonl` に正規化済み。全公開 19.6 万件のうちのごく一部の試掘段階。

## メタ

- [concepts/先行概念マッピング.md](concepts/先行概念マッピング.md) — 宇田川氏が「新概念」として提示する造語を、既知の先行概念と対応づけた地図。サーベイ不足のケースを明示しつつ、独自性のある部分も区別して示す。
- [concepts/ジェンドリン.md](concepts/ジェンドリン.md) — 宇田川氏の主要概念群（[輪郭](concepts/輪郭.md)・[認知対象](concepts/認知対象.md)・[高度非言語思考](concepts/高度非言語思考.md)・[言語演劇論](concepts/言語演劇論.md)・[FPN](concepts/FPN.md)）と一対一近くで対応する哲学者ユージン・ジェンドリンのハブページ。

---

## concepts/ — 用語集

### A. デライトの基本データモデル

- [輪郭](concepts/輪郭.md) — 投稿1件にあたる情報単位
- [輪郭法](concepts/輪郭法.md) — 輪郭で世界を捉える方法論
- [輪郭構造](concepts/輪郭構造.md) — 視点を含む立体階層構造
- [輪括](concepts/輪括.md) — 引き入れで作られる輪郭同士の関係
- [輪符](concepts/輪符.md) — 輪郭へのリンク表記
- [無番輪符](concepts/無番輪符.md) — 知番なしの輪符
- [輪郭小窓](concepts/輪郭小窓.md) — ホバー時のポップアップ
- [輪注](concepts/輪注.md) — 文中の用語を輪符化する書き方
- [知名](concepts/知名.md) — 輪郭の名前
- [知番](concepts/知番.md) — 認知対象に付与される番号
- [輪郭名](concepts/輪郭名.md) — 知名と区別される、輪郭それ自体の名前
- [認知対象](concepts/認知対象.md) — デライトの基礎単位
- [描出](concepts/描出.md) — 輪郭を新しく作る操作
- [描写](concepts/描写.md) — 輪郭の本文
- [あれ](concepts/あれ.md) — 知名なしの輪郭が自動でこう表示される
- [デライター](concepts/デライター.md) — デライトのユーザー
- [用者](concepts/用者.md) — ユーザーの希哲館訳語
- [用者番号](concepts/用者番号.md) — `K#XXXX` 形式のユーザー ID
- [デライト公式](concepts/デライト公式.md) — `K#1` の公式アカウント

### B. 引き入れ／三景関連

- [引き入れ](concepts/引き入れ.md) — 輪郭をリンクする概念全般
- [引き入れ操作](concepts/引き入れ操作.md) — 操作としての引き入れ
- [引き入れ欄](concepts/引き入れ欄.md) — UI 要素
- [引き外し](concepts/引き外し.md) — 反対操作
- [三景](concepts/三景.md) — 前景・中景・後景の総称
- [前景](concepts/前景.md) / [中景](concepts/中景.md) / [後景](concepts/後景.md) / [前後景](concepts/前後景.md)
- [輪符コピーボタン](concepts/輪符コピーボタン.md) — UI

### C. 公開／非公開・運営原則

- [投稿公開原則](concepts/投稿公開原則.md) — 公開前提のサービス設計
- [未公開輪郭](concepts/未公開輪郭.md) — ゆるい非表示
- [恥を捨てて全部書く](concepts/恥を捨てて全部書く.md) — 宇田川氏のロールモデル宣言
- [デライトのタイムライン](concepts/デライトのタイムライン.md) — 待欄の運用文化
- [無通知設計](concepts/無通知設計.md) — 引き入れに通知が来ない設計

### D. 記法／システム名

- [デルン](concepts/デルン.md) — デライトの前身、ウェブ知識録
- [デライト](concepts/デライト.md) — Deln Lite。本体
- [Cμ](concepts/Cμ.md) — 開発に使われている自作言語
- [デラング](concepts/デラング.md) — デライト向けマークアップ言語
- [パンくず記法](concepts/パンくず記法.md)
- [輪郭を特定する](concepts/輪郭を特定する.md)

### E. 思想体系・希哲館事業

- [希哲館](concepts/希哲館.md) — 宇田川氏が構想する知識機関
- [希哲館事業](concepts/希哲館事業.md) — その総体
- [希哲紀元](concepts/希哲紀元.md) — 独自紀年法
- [希哲館訳語](concepts/希哲館訳語.md) — カタカナ語を漢語／和語に置き換える
- [新現代思想](concepts/新現代思想.md) — 宇田川氏が開拓してきた思想群
- [現代の壁](concepts/現代の壁.md) — 普及を阻む需要不足
- [ジパング計画](concepts/ジパング計画.md) — 希哲館事業の現中心計画
- [大衆知性主義](concepts/大衆知性主義.md) — 万人が希哲者であれるべし
- [メカソクラテス](concepts/メカソクラテス.md) — ソクラテスの機械化
- [言語演劇論](concepts/言語演劇論.md) — 言語ゲームならぬ言語演劇

### F. デライトを位置づけるカテゴリ語

- [KNS](concepts/KNS.md) — knowledge networking service
- [J-IT](concepts/J-IT.md) — 日本の IT 再定義
- [軽やかな IT](concepts/軽やかなIT.md)
- [知能増幅メモサービス](concepts/知能増幅メモサービス.md)
- [FPN](concepts/FPN.md) — first person networker
- [神経目線](concepts/神経目線.md) — FPN の日本語版
- [意味符号化](concepts/意味符号化.md) — 文字コードならぬ意味コード
- [大脳検地](concepts/大脳検地.md) — 内側からの脳科学
- [立体アウトライナー](concepts/立体アウトライナー.md) — 久住によるデライト位置づけ
- [複合的階層構造SNSとしてのデライトの紹介](concepts/複合的階層構造SNSとしてのデライトの紹介.md)
- [SNSとしてのデライト](concepts/SNSとしてのデライト.md)

### G. 設計哲学・キャッチコピー

- [フリーソフィー](concepts/フリーソフィー.md) — 「無料は品質」
- [KEY 原則](concepts/KEY原則.md) — Keep Enough for You
- [なんでもメモ](concepts/なんでもメモ.md) — 公式キャッチコピー
- [手のひらに大脳を](concepts/手のひらに大脳を.md) — キャッチコピー
- [マインドクラフト](concepts/マインドクラフト.md) — キャッチコピー（旧）
- [高度非言語思考](concepts/高度非言語思考.md) — 開発者の思考法
- [論理共感覚](concepts/論理共感覚.md) — 開発者の認知特性

### H. デコ系（デライト×Cosense）

- [デコ](concepts/デコ.md) — 略語
- [デコ二刀流](concepts/デコ二刀流.md) — 併用スタイル
- [デコサンド](concepts/デコサンド.md) — 実践フロー
- [デコキム理論](concepts/デコキム理論.md) — 大衆性必須論
- [Collabox](concepts/Collabox.md) — Cosense 再改称案。`/delite` プロジェクトの実装あり
- [Cosense 文学](concepts/Cosense文学.md)
- [ブラケティング](concepts/ブラケティング.md) — Cosense 用語
- [輪符をブラケティング](concepts/輪符をブラケティング.md) — `[{知名 K#.../...}]` という橋渡し記法

### I. 造語論

- [造語論](concepts/造語論.md) — 立場の総体
- [造語家](concepts/造語家.md) — 自称ロール
- [片面造語と両面造語](concepts/片面造語と両面造語.md) — 造語の分類
- [貧民的カタカナ外来語](concepts/貧民的カタカナ外来語.md) — 撲滅対象
- [富豪的カタカナ外来語](concepts/富豪的カタカナ外来語.md) — 許容
- [印迫](concepts/印迫.md) — 希哲館訳語の一例
- [待欄](concepts/待欄.md) — 希哲館訳語の一例

### J. 歴史的トピック

- [N10K 騒動](concepts/N10K騒動.md) — 2020年の Twitter 論争
- [10000ページのぬかるみ](concepts/10000ページのぬかるみ.md) — 本来の意図
- [ブルートリンク](concepts/ブルートリンク.md) — update links 批判
- [セカンドブレイン症候群](concepts/セカンドブレイン症候群.md)
- [研究開発十五年説](concepts/研究開発十五年説.md)
- [接触元](concepts/接触元.md) — メタデータ書式

### K. 人物・実践方法

- [デライト開発者](concepts/デライト開発者.md) — 宇田川浩行氏のプロフィール
- [デライトはもう成功している](concepts/デライトはもう成功している.md) — 本人の現状認識
- [デライトにコミットするコストとそれへの対策](concepts/デライトにコミットするコストとそれへの対策.md) — 久住による運用論
- [名づけずに語る](concepts/名づけずに語る.md) — 久住によるデライト実践

### L. 久住哲による派生概念

久住哲氏が arpla 上でデライト分析のために導入した概念。宇田川氏の用語ではない。

- [認知パースペクティブ](concepts/認知パースペクティブ.md)
- [景間距離](concepts/景間距離.md)
- [エンティティとしての投稿](concepts/エンティティとしての投稿.md)
- [輪郭名](concepts/輪郭名.md)

### M. `/delite` ユーザー側のメタ修辞

zatsma 氏・804C 氏らが `/delite` Scrapbox（[Collabox（仮）](concepts/Collabox.md)）で導入した「ユーザー側の自衛的整理タグ」。宇田川氏の用語ではない。

- [デライト用語ではない](concepts/デライト用語ではない.md) — 「覚えなくてよい用語」マーカー
- [のような位置づけ](concepts/のような位置づけ.md) — 「本人公認ではないがそう見える」を婉曲に

---

## 参考資料

- [CLAUDE.md](CLAUDE.md) — Wiki のスキーマと運用ルール
- [init.txt](init.txt) — 初期指示
- [llm-wiki.md](llm-wiki.md) — LLM-Wiki パターン解説
- [log.md](log.md) — ingest / query / lint のログ
