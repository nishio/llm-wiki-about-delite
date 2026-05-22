# Log

時系列の ingest / query / lint ログ。各エントリは `## [YYYY-MM-DD] <種別> | <対象>` 形式。

## [2026-05-22] refactor | concepts/ → wiki/{concepts/utagawa, concepts, people, meta}/

ユーザー指示 ([second.txt](second.txt)):

> 現状 /concepts/... という構造になっている。これは指示が悪かった。リファクタリングをするのが良いと思う。
> /wiki/concepts 概念全般
> /wiki/concepts/utagawa 宇多川氏の作った概念
> その他concepts に入れるのが適当でないと思うページに関しては適切に分配せよ

新構造:

```
wiki/
├── concepts/
│   ├── utagawa/    # 宇田川氏の造語・特殊用法 (90 ファイル)
│   └── *.md        # その他の概念 (14 ファイル: 久住派生・Cosense 用語・ユーザー側メタ修辞・接触元)
├── people/         # 人物プロフィール (2 ファイル: デライト開発者, ジェンドリン)
└── meta/           # 編集方針・マッピング (1 ファイル: 先行概念マッピング)
```

実装:

- `git mv` で 98 ファイル移動、残り 7 ファイル（push 後追加分）は手動 mv で対応。
- [tools/refactor_concepts.py](tools/refactor_concepts.py) で 105 ファイルのリンク書き換え（move 辞書ベース）。
- [tools/fix_untracked_links.py](tools/fix_untracked_links.py) で残り 7 ファイルのリンク書き換え。
- [tools/normalize_broken_links.py](tools/normalize_broken_links.py) で元から赤リンクだった 17 件のパス正規化（`../../../concepts/X.md` → `X.md`）。
  - **副作用バグあり**: sources/*.md の `../raw/X.txt`、`../tools/X.py`、`../raw/dlt-udagawa/...` までも一律 `X.md` に潰してしまった。`git checkout HEAD -- sources/` で復元後、`tools/fix_sources_links.py` で正しく適用し直した。教訓: 存在チェックは「対象拡張子で」かつ「実ファイルの存在で」行うべき。
- [CLAUDE.md](CLAUDE.md) の構造説明と ingest フロー記述を新構造に書き直し。
- [tools/verify_links.py](tools/verify_links.py) で内部リンクの健全性チェック。残った broken 22 件は:
  - 元から赤リンクだったページへの参照 (17 件): Markdown としては「同階層赤リンク」になっていて、将来そのページを作れば自動でつながる。仕様。
  - CLAUDE.md 内のサンプルコードブロックの例示リンク (2 件): 仕様。
  - log.md 内の Cosense.md（元から赤リンク）と、修正済みの認知対象.md。

未着手:

- [index.md](index.md) のカテゴリ分類は旧 concepts/ 時代の構造のまま。新構造 (utagawa/ 内 vs 直下) に合わせて再カテゴリ化するとより自然だが、今回は範囲外。
- 元から赤リンクだった 17 件のページを実際に作るかどうかの判断。

## [2026-05-22] ingest | dlt.kitetu.com から宇田川氏輪郭 505 件を BFS 取得

ユーザー指示:

> デライト上の宇多川氏の発言を収集したい。参考資料を読んで考えて

[memo.txt](memo.txt) では「自分のデライトCSVをエクスポートする」前提で書かれていたが、本件は他人（宇田川氏）の公開輪郭の収集なので CSV ルートは使えない。代わりに公開 HTML を直接取得する経路を採用した。

### サイト解析でわかったこと

- robots.txt は一般 UA に許可（`User-Agent: *` / `Disallow: ` 空）。一括 crawler のみ拒否。
- サイトマップ `/see` が 173 ページ分のサブ sitemap を持つ。全公開輪郭 URL は **約 127 万件**。
- 宇田川氏 (`K#F85E` プレフィックス) の公開輪郭は **約 196,000 件**。
- 個別輪郭ページ（例 `https://dlt.kitetu.com/KNo.F85E/0758-4B81`）は **サーバサイド描画** で curl だけで取得可能。
- 一方で listing ページ（`?kw=K%23F85E&pn=N`）は **JavaScript で動的描画** されるため curl では空。ただし1ページ目（`?kw=K%23F85E` パラメタなし）だけは SSR される。
- 各個別輪郭ページには **前景輪符 (fg)** と **後景輪符 (bg)** へのリンクが豊富に埋め込まれている（1ページに ~175 ユニーク KNo）。

### 採用したアプローチ

K#F85E プロフィールおよび直近輪郭を seed として、前景・後景輪符を BFS で辿りながら **K#F85E プレフィックスのものだけ**を収集。listing ページを使わずに完結する。

- 実装: [tools/fetch_udagawa.py](tools/fetch_udagawa.py)（curl + Python の正規表現パーサ）
- 個別ページのパース: ネストした `<div>` を扱うため独自スタック走査（[tools/reparse_udagawa.py](tools/reparse_udagawa.py)）
- レート制限: 1 リクエストあたり 1.5 秒
- 取得件数: 500 件で打ち切り（キューに残り 1,780 件）
- 所要時間: ~13 分

### 取得結果

- 生 HTML: [raw/dlt-udagawa/html/](raw/dlt-udagawa/html) に 505 ファイル（63MB）
- 正規化: [raw/dlt-udagawa/outlines.jsonl](raw/dlt-udagawa/outlines.jsonl)（505 行、各行に kno/title/body/author/ts_drw/ts_rdrw/fg_refs/bg_refs）
- ソースページ: [sources/dlt-udagawa-corpus.md](sources/dlt-udagawa-corpus.md)
- 本文ありの輪郭は 234 件（46%）。残りは分類タグとして機能する空輪郭。

### 内容の傾向（本文ありの 234 件）

- **日記/越省**: 「希哲N年M月D日の日記」「希哲N年M月D日の越省」など、本人の日々の記録。最古 2012-09 から最新 2026-05-22 まで。
- **越省（一日一文）**: 二重鉤括弧『…』で題された本格エッセー。最長は『語るものの価値は語られるものの価値』(1634 字)。
- **概念定義**: 既存の concepts/ ページや Scrapbox ソースに無い本人定義文書を多数発見:
  - 既存概念の本人による定義（[Cosense](wiki/concepts/Cosense.md)？・[デライト](wiki/concepts/utagawa/デライト.md)・[希哲館事業](wiki/concepts/utagawa/希哲館事業.md)・[希哲館訳語](wiki/concepts/utagawa/希哲館訳語.md)・[輪郭小窓](wiki/concepts/utagawa/輪郭小窓.md) など）
  - 未収録の用語: **副日記**, **書了**, **整輪**, **一選万集**, **完全メイト**, **日記準備整輪**, **朝の定時執務**, **侍い**, **本格利用**, **書了**, **「市場施策（^マーケティング）について考える」編** など
- **教育漢字一覧** (小学校 1〜6 学年): 学年別の教育漢字字種を列挙した参照表。

### 4桁プレフィックスと時期の対応（暫定観察）

- **0758**: 2022-11 〜 2026-05（最も活発な現用プレフィックス）
- **4686**: 2017-08 〜 2018-11
- **5B28**: 2019-05 〜 2019 頃
- **E74C**: 2017 頃の旧式
- **E8CA**: 2018-08 頃

宇田川氏の輪郭は知番のプレフィックスでおおまかな時期が掴める。完全な時系列マッピングは未確認。

### 残課題 / 次の選択肢

1. **Wiki への統合**: 234 件の本文ありの輪郭から、既存 [concepts/](wiki/concepts) ページの増補と新規 concept ページ作成（副日記・整輪・書了・越省・一選万集 など 5〜10 個）。
2. **収集範囲の拡張**: 現在キューに 1,780 件残っている。さらに 500 件追加すれば本人定義の網羅性が大幅に上がる。19.6 万件全件は現実的でないため、本文ありの分布をサンプルして取捨選択する戦略が必要。
3. **長文越省の精読**: 『語るものの価値は語られるものの価値』(1634 字) など、本人の思想を直接読める長文エッセーが複数あり、概念ページの本人発言枠に引用すべきもの多数。
4. **日記の時系列整理**: 38 件の日付付き日記が拾えたので、特定時期の開発状況を追える。

## [2026-05-22] ingest (続) | コーパスから Wiki への第一波統合

第一波として、本人輪郭から直接読み取れた **本人の運用概念群** を Wiki に統合した。

### 新規 concept ページ（7 ページ）

- [『希哲日記』](wiki/concepts/utagawa/『希哲日記』.md) — 2018-08-17 開始の生涯規模日記。本人輪郭 [K#F85E/4686-E8CF](https://dlt.kitetu.com/KNo.F85E/4686-E8CF)。
- [副日記](wiki/concepts/utagawa/副日記.md) — 15 種類の生活ログ。本人輪郭 [K#F85E/5B28-5CC0](https://dlt.kitetu.com/KNo.F85E/5B28-5CC0)。
- [整輪](wiki/concepts/utagawa/整輪.md) — 輪郭群の意識的整備（旧称「輪郭整備」）。本人輪郭 [K#F85E/E74C-DB2E](https://dlt.kitetu.com/KNo.F85E/E74C-DB2E)。
- [日記準備整輪](wiki/concepts/utagawa/日記準備整輪.md) — 当日の日記準備としての整輪。本人輪郭 [K#F85E/0758-28EC](https://dlt.kitetu.com/KNo.F85E/0758-28EC)。
- [一日一文](wiki/concepts/utagawa/一日一文.md) — 越省（毎日完成させるエッセー）。長文として『語るものの価値は語られるものの価値』など。
- [書了](wiki/concepts/utagawa/書了.md) — 2026-02-02 に「書き上げ」から置き換え採用。本人輪郭 [K#F85E/0758-0C6C](https://dlt.kitetu.com/KNo.F85E/0758-0C6C)。
- [一選万集](wiki/concepts/utagawa/一選万集.md) — 2019-01-08 考案、「選択と集中」の片面造語。本人輪郭 [K#F85E/4686-9F65](https://dlt.kitetu.com/KNo.F85E/4686-9F65)。

### 既存ページの増補（本人定義の直接引用を追加）

- [希哲館事業](wiki/concepts/utagawa/希哲館事業.md) — 本人輪郭 [K#F85E/7C98](https://dlt.kitetu.com/KNo.F85E/7C98)（2014-06-24）から「日本初の工業化推進事業であった幕末の集成館事業に似ている」を直接引用。
- [輪郭小窓](wiki/concepts/utagawa/輪郭小窓.md) — 本人輪郭 [K#F85E/E74C-7ED7](https://dlt.kitetu.com/KNo.F85E/E74C-7ED7)（2021-07-20）から、輪郭候補窓として閃いた経緯と「描写を書いてもらうインセンティブ設計」の側面を追加。
- [希哲館訳語](wiki/concepts/utagawa/希哲館訳語.md) — 本人輪郭 [K#F85E/4686-E5B8](https://dlt.kitetu.com/KNo.F85E/4686-E5B8)（2017-08-25）から「世界史上最大の外来語翻訳体系」「希哲10年代前半に主要訳語が整った」「3 等級分類」を追加。
- [メカソクラテス](wiki/concepts/utagawa/メカソクラテス.md) — 本人輪郭 [K#F85E/F0A1](https://dlt.kitetu.com/KNo.F85E/F0A1)（2012-08-25）の「ソクラテス」解説と、本人にとっての「希哲」概念との接続を追加。「無知の知」を「哲学（希哲）の本質」と本人が解釈している点。
- [10000ページのぬかるみ](wiki/concepts/utagawa/10000ページのぬかるみ.md) — [一日一文](wiki/concepts/utagawa/一日一文.md) の「[一万葉面（ページ）のぬかるみ」編](https://dlt.kitetu.com/KNo.F85E/0758-D4AF) への発展と題名の段階的変更（2026-04-14, 2026-04-17）を追加。
- [index.md](index.md) — 新カテゴリ「N. 日記・整輪まわり（本人の運用）」を追加、I. 造語論に [一選万集](wiki/concepts/utagawa/一選万集.md) を追加、ソース要約に [dlt-udagawa-corpus](sources/dlt-udagawa-corpus.md) を追加。

### 第二波（並走中）

メモ: バックグラウンドで 2 回目の 500 件 fetch を実行中（resume 機能を [tools/fetch_udagawa.py](tools/fetch_udagawa.py) に追加して再開）。完了後にさらに本文ありの輪郭が増える見込み。残りキューはまだ多いため、第三・第四波も可能。

### 未着手

- 『語るものの価値は語られるものの価値』の本格的な要約と、[希哲館訳語](wiki/concepts/utagawa/希哲館訳語.md)・[造語論](wiki/concepts/utagawa/造語論.md) ページへの引用統合。
- [完全メイト](https://dlt.kitetu.com/KNo.F85E/0758-AE6E)・[侍い](https://dlt.kitetu.com/KNo.F85E/5B28-EC32)・[朝の定時執務](https://dlt.kitetu.com/KNo.F85E/0758-6162)・[本格利用](https://dlt.kitetu.com/KNo.F85E/0758-4DF9) など個別の本人定義の concept 化判断。
- 教育漢字一覧（小1〜小6）を扱うか（概念というより参照表）。
- 『井戸端のソクラテス』宣言（2026-05-22）と井戸端への本格参加との接続。

## [2026-05-22] ingest (続2) | 2 バッチ目 500 件取得・第二波 Wiki 統合

[tools/fetch_udagawa.py](tools/fetch_udagawa.py) に **resume 機能** を追加し（既存 jsonl の fg_refs / bg_refs から未取得の F85E 参照をキューに復元）、追加 500 件を取得。**累計 1,005 件 / 本文あり 437 件 (43%)**。新たに 413 件の本文ありを発見。

最長 9,062 字の越省、宇田川氏が西周由来であることを直接認知している証拠（2013年）など重要な発見が複数。

### 新規 concept ページ（2 ページ）

- [希哲学](wiki/concepts/utagawa/希哲学.md) — 西周由来の「希哲学」の本人輪郭（[K#F85E/9974](https://dlt.kitetu.com/KNo.F85E/9974), 2013-04-13）。**「現代日本語における『哲学』はこれに由来する」「津田真道『性理論』の跋文に西周が書いたものが初出」「希哲学から『希』が抜けて『学』が残ったのが現代の哲学」と本人が明示**。これにより、過去の lint で残されていた「**宇田川氏が西周を意識しているか不明**」という保留状態が解消される。また「希哲学」には宇田川独自の学問体系（英: philosophics、後に「綜学」へ改称）という別用法もあったことが分かった。
- [綜語](wiki/concepts/utagawa/綜語.md) — 宇田川氏が考案した人工言語（本人輪郭 [K#F85E/45E0](https://dlt.kitetu.com/KNo.F85E/45E0), 2012-05-31）。「綜合的日本語（synthetic japanese）」の略から正式名称化。ISO 拡張言語コード `syn_KTK` / `sy_KT`。「言語そのものの改良」層に位置する。

### 既存ページの増補

- [一日一文](wiki/concepts/utagawa/一日一文.md) — 本人輪郭 [K#F85E/5B28-6184](https://dlt.kitetu.com/KNo.F85E/5B28-6184)（2019-05-16）の正式定義を追加。希哲8年（2014年）「一日一章」開始 → 「一日八章」自重荷で挫折 → 希哲13年（2019年）「一日一文」へ簡素化 → 2023-09 から題名に二重鉤括弧、という **12 年の変遷** を記録。本文長 9,062 の [『Collabox 再改称提案』](https://dlt.kitetu.com/KNo.F85E/0758-475D) と 3,160 の [『macOS の字面』](https://dlt.kitetu.com/KNo.F85E/0758-B31E) を主要作品例表に追加。
- [Collabox](wiki/concepts/utagawa/Collabox.md) — 本人越省 [K#F85E/0758-475D](https://dlt.kitetu.com/KNo.F85E/0758-475D)（9,062字）の主要論点を整理:
  - 「Cosense」改称の3つの問題: ①文化的遺伝子の断絶、②意味が直感的に分からない（「最初は違和感あったがしっくり来た」は危険な罠）、③Consense 誤記（公式インタビューにも実例）
  - Collabox 案の優位性: 平易な言葉商標化戦略（LINE / note / Apple と同型）、collabox.io 取得可能性
  - 自己評価: **「言語化に関する知見において私以上の人間はいない」**「私は言語化の鬼」
  - Cosense リブランディングは「ステップで立ち往生」、ジャンプが必要 という総括
- [先行概念マッピング](wiki/meta/先行概念マッピング.md) — 「希哲」項に、**本人が 2013年に西周由来を明示している輪郭の存在** を脚注として追記。「本人が意識しているか不明」という過去の保留状態が解消されたことを記録。

### コーパスインデックスの更新

- [sources/dlt-udagawa-corpus.md](sources/dlt-udagawa-corpus.md) を 1,005 件版に再生成。日記 top30、越省 top25、概念 top60 を表形式で。
- [index.md](index.md) の E. 思想体系・希哲館事業 カテゴリに [希哲学](wiki/concepts/utagawa/希哲学.md)・[綜語](wiki/concepts/utagawa/綜語.md) を追加。ソース要約の件数を 1,005 件に更新。

### 未着手（第二波後）

- 1,005 件の corpus にある 437 本文のうち、本格的に統合できたのは累計約 15 件のみ。残り 420 件以上は jsonl のままで未活用。
- 教育漢字一覧（小1〜小6）など参照表系は引き続き保留。
- 第三バッチ（さらに 500 件）を取るか、現状で十分か判断。残りキュー 2,649 件、全公開 196,000 件。
- 「綜学」「越省」「珠列」「編」「希哲日記の各副日記（睡眠記録ほか14種）」「希哲館事業」のサブ計画群など、概念ページ化候補が依然として多い。
- 本人輪郭の **再描出日時** (ts_rdrw) は parser で取得しているが Wiki 側ではまだ使っていない。「いつ最後に編集されたか」は信頼性の判断に重要。

## [2026-05-22] lint | ジェンドリンの先行概念追加

ユーザー指摘:

> 「輪郭」の概念はユージン・ジェンドリンの「側面」の概念とほぼ同じなのではと思う

確認した結果、**ユージン・ジェンドリン（Eugene Gendlin, 1926-2017）** の哲学が宇田川氏の主要概念群に **横断的かつほぼ一対一で対応している** ことが分かった。

| 宇田川氏 | ジェンドリン |
|---|---|
| [輪郭](wiki/concepts/utagawa/輪郭.md) | aspects / facets / sides（側面） |
| [認知対象](wiki/concepts/utagawa/認知対象.md) | "..." (the implicit) |
| [高度非言語思考](wiki/concepts/utagawa/高度非言語思考.md) | felt sense / Focusing |
| [言語演劇論](wiki/concepts/utagawa/言語演劇論.md) | carrying forward |
| [FPN](wiki/concepts/utagawa/FPN.md) / [神経目線](wiki/concepts/utagawa/神経目線.md) | "from within"（俯瞰せず中から触れる） |

5つもの中核概念が一人の哲学者の体系と並行している、というのは **散発的な並行発想ではなく、領域全体の取りこぼし** に近い。

### 共通祖

宇田川氏が「17歳以降に傾倒した哲学者」として **Whitehead** と **David Bohm** を挙げており、ジェンドリンの 'A Process Model' は **Whitehead のプロセス哲学を直接継承** している。間接的系譜は確実に存在する。にもかかわらず宇田川氏発言の現範囲内ではジェンドリン直接言及は無い。

### 対応:

- [ジェンドリン](wiki/people/ジェンドリン.md) ハブページを新規作成。5概念の対応一覧、共通祖（Whitehead）、直接言及の有無、日本語文献などを整理。
- 個別ページに「## 先行概念」セクションを増補:
  - [輪郭](wiki/concepts/utagawa/輪郭.md): 「特に強い先行: ジェンドリンの側面」節を追加し、対応表を入れた
  - [認知対象](wiki/concepts/utagawa/認知対象.md): ジェンドリンの "..." と implicit intricacy を最強の先行として
  - [高度非言語思考](wiki/concepts/utagawa/高度非言語思考.md): ジェンドリンの felt sense を「特に強い対応」として
  - [言語演劇論](wiki/concepts/utagawa/言語演劇論.md): ジェンドリンの carrying forward を「特に強い対応」として
- [先行概念マッピング](wiki/meta/先行概念マッピング.md) に「特筆: ジェンドリンとの大規模並行」節を追加し、各表にもジェンドリン項目を増補。「独自性」セクションにも「ジェンドリン的 felt sense の哲学を PKM/SNS 実装に落とし込んだ」点を加筆。
- [index.md](index.md) の「メタ」にジェンドリンハブページを追加。

### 編集上の判断

- 「直接影響」とは断定せず、「**共通祖（Whitehead）経由の独立並行発想** か **未調査の先行** か」を両論併記。
- ただし、5つもの中核概念が並行することから、**サーベイ不足の指摘としては明確に成立する**。
- ジェンドリンは日本でも諸富祥彦・池見陽らによって紹介されており、特殊なマイナー哲学者ではない。アクセス可能な範囲だった。

## [2026-05-22] lint | 先行概念マッピングのタイムライン修正

ユーザー指摘:

> 「KNS」 — "knowledge networking" を名乗ったサービスは Twine（2007） が約20年前に存在。
> デライトがいつからあるサービスか知らない

修正内容:

- デルンの **構想は 2002 年**（宇田川氏17歳時）、デルン実用化は2012年、デライト公開は2020年。**Twine（2007）はデルン構想の5年後**であり、「20年前に先行」と書いたのは誤り。
- [先行概念マッピング](wiki/meta/先行概念マッピング.md) に **「タイムラインの目安」** 節を追加し、各先行概念を以下の4区分に整理する方針を明示:
  - **〜2001年**: 明確な先行（Memex, URI, Topic Maps, Polanyi, Vaihinger, 西周 等）
  - **2002〜2012年**: 並行発展（Twine, Tinderbox, Wikidata 等）
  - **2012〜2020年**: 宇田川氏の実装と同時代
  - **2020年〜**: 同時代の比較対象（Roam, Second Brain 等）
- 個別ページの表現も「先行」「並行」「後発」を区別するよう修正:
  - [KNS](wiki/concepts/utagawa/KNS.md): Twine を「先行」から「**並行発展**」に修正
  - [知番](wiki/concepts/utagawa/知番.md): Linked Data 原則化（2006）・Wikidata（2012）は「並行」、DB 代理キー（1970年代-）・URI（1994）・Semantic Web vision（1999-2001）が真の先行
  - [輪郭法](wiki/concepts/utagawa/輪郭法.md): Topic Maps（2000）は明確な先行、Tinderbox（2003）は並行
  - [立体アウトライナー](wiki/concepts/立体アウトライナー.md): TheBrain（1997）は先行、Roam（2020）はデライトと同年
  - [手のひらに大脳を](wiki/concepts/utagawa/手のひらに大脳を.md): Second Brain（2022）は構想より20年後
  - [投稿公開原則](wiki/concepts/utagawa/投稿公開原則.md): Twitter/Reddit/Quantified Self（2005-2007）は構想より後だが原則恒久化より前

教訓:

- **先行概念を主張する前に、宇田川氏の発想時期（2002）と比較対象の時期を必ず突き合わせる**。サーベイ不足を批判するときに自分がサーベイ不足になっていた。
- 「先行」と「並行発展」は別物。並行発展はむしろ「同時期に複数人が独立に同種の発想に到達した」という、発想の妥当性の傍証にもなる。
- 「世界初の KNS」と宇田川氏が主張する場合、Twine が **既に "knowledge networking" を名乗っていた事実** は引き続き重要（並行発展だが、命名としては Twine が先行）。

## [2026-05-22] lint | 先行概念マッピングの編集方針追加

ユーザー指摘:

> 宇多川氏は自分の思想が新規なものであると主張する傾向があるが、しばしば知的生産などに関する既知の概念に対するサーベイ不足だと感じる。彼の主張する「新概念」によりよく知られた過去の概念がある場合はそれを明記したい。

対応:

- [CLAUDE.md](CLAUDE.md) の「編集方針」に **「先行概念との関係を明示する」** セクションを追加。今後の ingest でも同じ方針を継続する。
- [concepts/先行概念マッピング.md](wiki/meta/先行概念マッピング.md) を新規作成。宇田川氏の主要造語を一覧表で先行概念と対応づけ。
- 主要概念ページに **「## 先行概念」セクション** を追加:
  - **基本データモデル**: [知番](wiki/concepts/utagawa/知番.md)、[輪郭](wiki/concepts/utagawa/輪郭.md)、[輪郭法](wiki/concepts/utagawa/輪郭法.md)、[認知対象](wiki/concepts/utagawa/認知対象.md)、[意味符号化](wiki/concepts/utagawa/意味符号化.md)
  - **認知系**: [高度非言語思考](wiki/concepts/utagawa/高度非言語思考.md)、[論理共感覚](wiki/concepts/utagawa/論理共感覚.md)、[FPN](wiki/concepts/utagawa/FPN.md)、[大脳検地](wiki/concepts/utagawa/大脳検地.md)
  - **哲学・社会**: [言語演劇論](wiki/concepts/utagawa/言語演劇論.md)、[希哲館](wiki/concepts/utagawa/希哲館.md)、[希哲館訳語](wiki/concepts/utagawa/希哲館訳語.md)、[大衆知性主義](wiki/concepts/utagawa/大衆知性主義.md)、[メカソクラテス](wiki/concepts/utagawa/メカソクラテス.md)
  - **設計・マーケティング**: [フリーソフィー](wiki/concepts/utagawa/フリーソフィー.md)、[投稿公開原則](wiki/concepts/utagawa/投稿公開原則.md)、[KNS](wiki/concepts/utagawa/KNS.md)、[手のひらに大脳を](wiki/concepts/utagawa/手のひらに大脳を.md)、[セカンドブレイン症候群](wiki/concepts/utagawa/セカンドブレイン症候群.md)
  - **ツール比較**: [立体アウトライナー](wiki/concepts/立体アウトライナー.md)
- [index.md](index.md) に「## メタ」セクションを追加して [先行概念マッピング](wiki/meta/先行概念マッピング.md) を案内。

特に重要な観察:

- **「希哲」**: 西周（明治期の哲学者）が philosophy の訳語として **最初「希哲学」を提案** し、後に「哲学」に改めた。宇田川氏の「希哲」は事実上 **西周の最初の訳語の復活**。本人がこれを意識しているかは現時点不明。
- **「知番」**: 「名前と独立に実体に ID を振る」発想は、Linked Data・Wikidata・データベース理論で半世紀以上前から確立。宇田川氏の「世界初」主張は、Berners-Lee の Semantic Web vision（2001）以降の蓄積を完全に経由していない可能性。
- **「KNS」**: "knowledge networking" を名乗ったサービスは **Twine（2007）** が約20年前に存在した。サーベイ不足の典型例。
- **「高度非言語思考」**: Polanyi の **暗黙知** や Paivio の **二重符号化理論** で既に詳細に論じられている領域。
- **「言語演劇論」**: Vaihinger の **「あたかも（Als Ob）」の哲学**（1911）が「虚構として本気で語る」ほぼ同じテーゼを提示している。

未着手:

- 残りの概念ページ（[マインドクラフト](wiki/concepts/utagawa/マインドクラフト.md)、[ジパング計画](wiki/concepts/utagawa/ジパング計画.md)、[現代の壁](wiki/concepts/utagawa/現代の壁.md)、[フリーソフィー](wiki/concepts/utagawa/フリーソフィー.md) 以外の細々したもの）への先行概念追記。
- 宇田川氏自身が引用するホワイトヘッド・ボームと、ここで対応づけた先行概念群との関係整理。

## [2026-05-22] ingest | delite-project.all.txt

- 対象: `raw/delite-project.all.txt`（21KB、505 行、43 ページ）
- 取得元: <https://scrapbox.io/delite/> を Scrapbox 公開 API 経由で取得し 1 ファイルに統合。
- 内容: `/delite` プロジェクト（「[デライト Collabox（仮）](wiki/concepts/utagawa/Collabox.md)」= デライトユーザー向け井戸端）の全公開ページ。書き手は主に **zatsma 氏（K#FD7E）** と **804C 氏**。宇田川氏本人の `hiro` ページは Cosense デフォルトの自己紹介テンプレートのみ。
- 性格: 既存ソース（villagepump/arpla）に対し **ユーザー側の実践知** を補完する位置づけ。本人発言源としては薄いが、デライトの **記法・運用ノウハウ・ユーザーの読み筋** が拾える。
- 出力:
  - [sources/delite-project.all.md](sources/delite-project.all.md) を新規作成
  - 新しい concept ページ:
    - [用者](wiki/concepts/utagawa/用者.md) — ユーザーの希哲館訳語
    - [用者番号](wiki/concepts/utagawa/用者番号.md) — `K#XXXX` 形式の ID
    - [デライト公式](wiki/concepts/utagawa/デライト公式.md) — `K#1` 公式アカウント
    - [デライト用語ではない](wiki/concepts/デライト用語ではない.md) — ユーザー側メタ用語
    - [のような位置づけ](wiki/concepts/のような位置づけ.md) — ユーザー側メタ用語
    - [ブラケティング](wiki/concepts/ブラケティング.md) — Cosense 用語
    - [輪符をブラケティング](wiki/concepts/輪符をブラケティング.md) — `[{知名 K#.../...}]` という橋渡し記法
  - 既存 concept の更新:
    - [輪符](wiki/concepts/utagawa/輪符.md) — `{知名 K#XXXX/XXXX}` の用者番号 + 連番という構造を明示
    - [無番輪符](wiki/concepts/utagawa/無番輪符.md) — ソース追加
    - [デコ二刀流](wiki/concepts/utagawa/デコ二刀流.md) — zatsma 氏の使い分け実例
    - [未公開輪郭](wiki/concepts/utagawa/未公開輪郭.md) — 公式輪郭の警告文 + zatsma 氏の比較表サマリ
    - [Collabox](wiki/concepts/utagawa/Collabox.md) — `/delite` プロジェクトとして実装された後日談
    - [デライター](wiki/concepts/utagawa/デライター.md) — 用者との区別を追記
  - [index.md](index.md) にカテゴリ M「`/delite` ユーザー側のメタ修辞」を新設、その他は既存カテゴリに追記。
- ingest 中に気付いた事項:
  - **輪符の形式 `{知名 K#XXXX/XXXX}` における前半 `K#XXXX` が [用者番号](wiki/concepts/utagawa/用者番号.md) である** ことが、`/delite` のページ群から明確になった。これは「輪郭は誰の輪郭か」を必ず持つというデライト設計の中核を、記法レベルで可視化している重要な観察。
  - 「[デライト用語ではない](wiki/concepts/デライト用語ではない.md)」「[のような位置づけ](wiki/concepts/のような位置づけ.md)」のような **ユーザー側のメタ修辞** が登場しているのが興味深い。前者は宇田川氏の [造語論](wiki/concepts/utagawa/造語論.md) に対する「学習者の自衛」のような側面があり、希哲館訳語の積極推進と若干テンションがある。
  - [Collabox](wiki/concepts/utagawa/Collabox.md) は宇田川氏が提案を取り下げ気味になった後も、ユーザー側で名前だけ実装された形になった。「優等生過ぎる」と本人は評したが、ユーザーには受け入れられている。
  - zatsma 氏による [未公開輪郭](wiki/concepts/utagawa/未公開輪郭.md) と「プライベートプロジェクト」の比較表は、デライト固有の使用感（「俯瞰したくならない」「縦方向の整理に向く」「あたまのわるい時の私が使う」）を言語化していて、UX 観察として価値が高い。
- 未着手:
  - `/delite` の `自動車教習所` `教習所ふきだしコンテスト` などのオフトピック・ページは無視。
  - `全知検索` という新出語が「[意味符号化](wiki/concepts/utagawa/意味符号化.md) と組み合わせて」と参照されたが、定義は与えられていない。原典での確認待ち。
  - `デライトのRSS` `スマホから書くコセンス` 等の機能・運用ページは concept 化せず、sources 側にメモのみ。
  - 公式輪郭（<https://dlt.kitetu.com/KNo.C7C6/5BFA> 等）の原典確認。

## [2026-05-22] ingest | arpla-デライト.2hop.txt

- 対象: `raw/arpla-デライト.2hop.txt`（156KB、2,429 行、51 ページ）
- 内容: Scrapbox `arpla`（アープラ）の「デライト」ページとその 1/2-hop 関連ページ。ほぼ全て **久住哲** 氏単独の分析・解釈。
- 性格: villagepump（雑談・本人発言中心）に対する補完。**設計思想の理論的整理** が中心。
- 出力:
  - [sources/arpla-デライト.2hop.md](sources/arpla-デライト.2hop.md) を新規作成
  - 新しい concept ページを追加:
    - [神経目線](wiki/concepts/utagawa/神経目線.md)
    - [デライター](wiki/concepts/utagawa/デライター.md)
    - [輪郭名](wiki/concepts/輪郭名.md)
    - [認知パースペクティブ](wiki/concepts/認知パースペクティブ.md)（久住派生概念）
    - [景間距離](wiki/concepts/景間距離.md)（久住派生概念）
    - [立体アウトライナー](wiki/concepts/立体アウトライナー.md)
    - [エンティティとしての投稿](wiki/concepts/エンティティとしての投稿.md)（久住派生概念）
    - [名づけずに語る](wiki/concepts/名づけずに語る.md)
    - [SNSとしてのデライト](wiki/concepts/SNSとしてのデライト.md)
    - [複合的階層構造SNSとしてのデライトの紹介](wiki/concepts/複合的階層構造SNSとしてのデライトの紹介.md)
    - [デライトにコミットするコストとそれへの対策](wiki/concepts/デライトにコミットするコストとそれへの対策.md)
    - [あれ](wiki/concepts/utagawa/あれ.md)
  - 既存ページを更新:
    - [FPN](wiki/concepts/utagawa/FPN.md) — 神経目線・認知パースペクティブへの参照を追加
    - [知名](wiki/concepts/utagawa/知名.md) — 「タイトル」との違い節を追加（久住の整理）
    - [知番](wiki/concepts/utagawa/知番.md) — 単一性の節を追加（久住の整理）
    - [デラング](wiki/concepts/utagawa/デラング.md) — 記法一覧を追加
    - [中景](wiki/concepts/utagawa/中景.md) — 久住の運用論に言及
  - [index.md](index.md) を更新（カテゴリ L. 久住派生概念を追加）
- 気付いた事項:
  - **久住理論と本人理論の関係**: 久住氏は宇田川氏とは独立にデライトの設計思想を再構築している。多くは整合的だが、`SNS としてのデライト` のような「ユーザーの工夫」と本人の意図がずれている可能性を久住自身が指摘している箇所もある。Wiki 側ではこれらの「派生概念」を別カテゴリにして区別。
  - **輪郭名 vs 知名 vs タイトル** という3者関係は、デライト初学者の最大の躓きポイント。これを明示的に整理した久住の論考は教育的価値が高い。
  - **エンティティとしての投稿** という発想（Datalog からの着想）は、宇田川氏の [認知対象を捉える](wiki/concepts/utagawa/認知対象.md) 発想と独立に到達したと久住氏が述べる。同じ場所への二方向からのアプローチとして興味深い。
- 未着手:
  - 久住が言及している宇田川氏の輪郭（[全てのデライターへ](https://dlt.kitetu.com/KNo.F85E/E74C-CA32) 等）の取り込み。
  - 「デライトについて #1〜#15」シリーズで未読のもの（#2, #5, #7, #9, #11〜14）の確認。
  - `単一性`, `個物と現象` の哲学的議論を概念ページ化するか判断。
  - `エディタ＝選り手` のような希哲館訳語の細部追加。

## [2026-05-22] ingest | villagepump-デライト.2hop.txt

- 対象: `raw/villagepump-デライト.2hop.txt`（1MB、14,141 行、146 ページ）
- 内容: Scrapbox/Cosense `villagepump` の「デライト」ページとその 1/2-hop 関連ページ。
- 特筆: 2026年5月、宇田川氏（`[hiro.icon]`）本人が井戸端に本格参加し、設計意図・思想を本人の言葉で大量に書き残している。
- 出力:
  - [sources/villagepump-デライト.2hop.md](sources/villagepump-デライト.2hop.md) を作成
  - [concepts/](wiki/concepts) に 60+ ページを新規作成（カテゴリ別は [index.md](index.md) 参照）
  - [index.md](index.md) を初版作成
  - [CLAUDE.md](CLAUDE.md) を初版作成
- ingest 中に気付いた事項:
  - [init.txt](init.txt) で「宇多川氏」とあるが、ソース内では「**宇田川**浩行」と表記。CLAUDE.md で「宇田川」に統一する旨を明記。
  - 宇田川氏の用語は「片面造語」（既存概念の新名前）と「両面造語」（概念ごと新造）の混在で、後者が圧倒的に多い。本人もそれを自覚しており、[片面造語と両面造語](wiki/concepts/utagawa/片面造語と両面造語.md) という枠組み自体を提示している。
  - デライトを多角的に表現するキャッチコピー群（KNS／知能増幅メモサービス／マインドクラフト／意味符号化／FPN／メカソクラテス／なんでもメモ／手のひらに大脳を）は、いずれも「**全てが本当のデライトの違う一面**」であって、どれが本当のデライトとは言えない、という[高度非言語思考](wiki/concepts/utagawa/高度非言語思考.md) ページの発言が読み解きの鍵。
  - 「[投稿公開原則](wiki/concepts/utagawa/投稿公開原則.md)」と「[未公開輪郭](wiki/concepts/utagawa/未公開輪郭.md)」の関係、および [知番](wiki/concepts/utagawa/知番.md) が「認知対象に付与される番号」（輪郭の ID ではない）という点が、デライト設計の他のあらゆる特徴を生成している中枢概念。
- 未着手:
  - 周辺ページ（多数の日付ページ、`/villagepump` 文化系ページ）から拾える追加発言の収集。
  - 公式輪郭（`dlt.kitetu.com/KNo.xxxx`）の原典との突き合わせ。
  - 希哲館訳語の全リスト作成（[希哲館訳語](wiki/concepts/utagawa/希哲館訳語.md) ページに主要例のみ収録済み）。
  - 言及されているが個別ページ未作成: 描写頭脳, 異子, 輪結, 知能増幅, ニューブレイン, ザナドゥ計画, デコキム以外の細かい派生語, 〇〇を初めて知った場所 など。

