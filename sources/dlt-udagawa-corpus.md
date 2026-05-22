# デライト本体から収集した宇田川氏輪郭コーパス

- **取得日**: 2026-05-22
- **収集元**: https://dlt.kitetu.com/ （公開輪郭のみ）
- **対象 KNo**: K#F85E 配下（宇田川（希哲）浩行＝デライト開発者の輪郭群）
- **収集方法**: K#F85E プロフィール輪郭を起点に前景・後景輪符を BFS 取得（[tools/fetch_udagawa.py](../tools/fetch_udagawa.py)）
- **取得件数**: 2005 輪郭 / 本文ありは 758 件 (37%)
- **生データ**: [raw/dlt-udagawa/outlines.jsonl](../raw/dlt-udagawa/outlines.jsonl) + 個別 HTML in [raw/dlt-udagawa/html/](../raw/dlt-udagawa/html)

## 取得バッチ

- 第1バッチ (2026-05-22 初回): 505 件
- 第2バッチ (2026-05-22): 500 件追加（resume 機能で前回キューから継続）
- 第3バッチ (2026-05-22): 500 件追加
- 第4バッチ (2026-05-22): 500 件追加
- 現在のキュー残り: 約 4,249 件（全公開 ~196,000 件）

## サイト構造の理解

- 各輪郭は **K#XXXX** （4桁知番、古いもの）または **K#XXXX/YYYY-ZZZZ** （所有者プレフィックス + サブ知番）の形式
- 宇田川氏所有の輪郭は **K#F85E** プレフィックス（全公開で約 196,000 件）
- 多くの輪郭は本文（描写）が空で、純粋にタグ／分類用 — 本文を持つのは全体の 4 割弱
- 各ページは前景輪符（fg、その輪郭から指す先）と後景輪符（bg、その輪郭を指す元）でつながる有向グラフ

## 4桁プレフィックスと時期の対応（暫定）

観察された主要プレフィックスと最古／最新の描出日（本文ありの輪郭のみ集計）:

- **0758** (364件): 2023-07-29 12:24 〜 2026-05-22 06:45
- **2510** (19件): 2016-02-28 23:47 〜 2016-08-27 12:42
- **4686** (44件): 2017-05-19 22:54 〜 2019-02-17 04:25
- **5B28** (32件): 2019-04-10 20:39 〜 2020-10-22 14:33
- **7311** (6件): 2017-04-01 22:24 〜 2017-04-05 22:20
- **E74C** (52件): 2021-02-15 20:42 〜 2023-01-29 03:51
- **E8CA** (66件): 2015-06-26 23:33 〜 2015-12-31 01:48

## カテゴリ別収録

### 日記・越省・つぶがき（希哲X年Y月Z日の…）

本人が日々の生活・思考・開発進捗を記録した文書。118件収録。

| 日付 | 知名 | KNo | 本文長 |
|---|---|---|---|
| 2026-05-22 | 希哲20年5月22日の進捗 | [K#F85E/0758-793B](https://dlt.kitetu.com/KNo.F85E/0758-793B) | 53 |
| 2026-05-22 | 希哲20年5月22日の越省 | [K#F85E/0758-6A32](https://dlt.kitetu.com/KNo.F85E/0758-6A32) | 88 |
| 2026-05-22 | 希哲20年5月22日の副日記 | [K#F85E/0758-19D3](https://dlt.kitetu.com/KNo.F85E/0758-19D3) | 126 |
| 2026-05-22 | 希哲20年5月22日の日記 | [K#F85E/0758-FEBC](https://dlt.kitetu.com/KNo.F85E/0758-FEBC) | 58 |
| 2026-05-03 | 希哲20年5月3日の入浴 | [K#F85E/0758-80A7](https://dlt.kitetu.com/KNo.F85E/0758-80A7) | 156 |
| 2026-05-03 | 希哲20年5月3日の飲食 | [K#F85E/0758-81E8](https://dlt.kitetu.com/KNo.F85E/0758-81E8) | 505 |
| 2026-05-03 | 希哲20年5月3日の執務 | [K#F85E/0758-82EC](https://dlt.kitetu.com/KNo.F85E/0758-82EC) | 63 |
| 2026-05-03 | 希哲20年5月3日の越省 | [K#F85E/0758-CC8F](https://dlt.kitetu.com/KNo.F85E/0758-CC8F) | 149 |
| 2026-05-03 | 希哲20年5月3日の副日記 | [K#F85E/0758-F6EB](https://dlt.kitetu.com/KNo.F85E/0758-F6EB) | 128 |
| 2026-05-03 | 希哲20年5月3日の日記 | [K#F85E/0758-8EE1](https://dlt.kitetu.com/KNo.F85E/0758-8EE1) | 118 |
| 2026-05-02 | 希哲20年5月2日の飲食 | [K#F85E/0758-E4EE](https://dlt.kitetu.com/KNo.F85E/0758-E4EE) | 507 |
| 2026-05-02 | 希哲20年5月2日の越省 | [K#F85E/0758-D495](https://dlt.kitetu.com/KNo.F85E/0758-D495) | 121 |
| 2026-05-02 | 希哲20年5月2日の日記 | [K#F85E/0758-2717](https://dlt.kitetu.com/KNo.F85E/0758-2717) | 176 |
| 2026-05-02 | 希哲20年5月2日の副日記 | [K#F85E/0758-6B28](https://dlt.kitetu.com/KNo.F85E/0758-6B28) | 128 |
| 2026-05-01 | 希哲20年5月1日の睡眠 | [K#F85E/0758-93D4](https://dlt.kitetu.com/KNo.F85E/0758-93D4) | 155 |
| 2026-05-01 | 希哲20年5月1日の飲食 | [K#F85E/0758-4CCC](https://dlt.kitetu.com/KNo.F85E/0758-4CCC) | 512 |
| 2026-05-01 | 希哲20年5月1日の副日記 | [K#F85E/0758-00D0](https://dlt.kitetu.com/KNo.F85E/0758-00D0) | 129 |
| 2026-05-01 | 希哲20年5月1日の越省 | [K#F85E/0758-D1F0](https://dlt.kitetu.com/KNo.F85E/0758-D1F0) | 140 |
| 2026-05-01 | 希哲20年5月1日の日記 | [K#F85E/0758-F148](https://dlt.kitetu.com/KNo.F85E/0758-F148) | 276 |
| 2026-04-30 | 希哲20年4月30日の睡眠 | [K#F85E/0758-039E](https://dlt.kitetu.com/KNo.F85E/0758-039E) | 215 |
| 2026-04-30 | 希哲20年4月30日の越省 | [K#F85E/0758-5EB3](https://dlt.kitetu.com/KNo.F85E/0758-5EB3) | 320 |
| 2026-04-30 | 希哲20年4月30日の日記 | [K#F85E/0758-524B](https://dlt.kitetu.com/KNo.F85E/0758-524B) | 710 |
| 2026-04-30 | 希哲20年4月30日の副日記 | [K#F85E/0758-7A8E](https://dlt.kitetu.com/KNo.F85E/0758-7A8E) | 130 |
| 2026-04-29 | 希哲20年4月29日の副日記 | [K#F85E/0758-8291](https://dlt.kitetu.com/KNo.F85E/0758-8291) | 131 |
| 2026-04-29 | 希哲20年4月29日の越省 | [K#F85E/0758-A561](https://dlt.kitetu.com/KNo.F85E/0758-A561) | 313 |
| 2026-04-29 | 希哲20年4月29日の日記 | [K#F85E/0758-F44F](https://dlt.kitetu.com/KNo.F85E/0758-F44F) | 68 |
| 2026-04-28 | 希哲20年4月28日の副日記 | [K#F85E/0758-1BD8](https://dlt.kitetu.com/KNo.F85E/0758-1BD8) | 131 |
| 2026-04-28 | 希哲20年4月28日の越省 | [K#F85E/0758-C775](https://dlt.kitetu.com/KNo.F85E/0758-C775) | 258 |
| 2026-04-28 | 希哲20年4月28日の日記 | [K#F85E/0758-5C40](https://dlt.kitetu.com/KNo.F85E/0758-5C40) | 103 |
| 2026-04-27 | 希哲20年4月27日の睡眠 | [K#F85E/0758-B2E5](https://dlt.kitetu.com/KNo.F85E/0758-B2E5) | 155 |
| … | 残り 88 件は jsonl 参照 | | |

### 越省・一日一文（思想的エッセー）

二重鉤括弧 `『…』` を冠した本格的な文章。13件収録。

| 日付 | 題名 | KNo | 本文長 |
|---|---|---|---|
| 2025-07-28 | 『Cosense（（旧 Scrapbox））は「Collabox」に再改称してはどうか』 | [K#F85E/0758-475D](https://dlt.kitetu.com/KNo.F85E/0758-475D) | 9062 |
| 2026-02-09 | 『あえて政治を語ることの大切さ』 | [K#F85E/0758-0957](https://dlt.kitetu.com/KNo.F85E/0758-0957) | 3338 |
| 2025-07-23 | 『macOS の字面が気持ち悪い』 | [K#F85E/0758-B31E](https://dlt.kitetu.com/KNo.F85E/0758-B31E) | 3160 |
| 2026-02-19 | 『語るものの価値は語られるものの価値』 | [K#F85E/0758-EF77](https://dlt.kitetu.com/KNo.F85E/0758-EF77) | 1634 |
| 2019-05-16 | 一日一文 | [K#F85E/5B28-6184](https://dlt.kitetu.com/KNo.F85E/5B28-6184) | 541 |
| 2018-08-17 | 『希哲日記』 | [K#F85E/4686-E8CF](https://dlt.kitetu.com/KNo.F85E/4686-E8CF) | 518 |
| 2026-01-15 | 『越省（＾エッセー）としての一日一文』 | [K#F85E/0758-E363](https://dlt.kitetu.com/KNo.F85E/0758-E363) | 395 |
| 2026-05-04 | 『デライト半公式 Collabox』 | [K#F85E/0758-CDE5](https://dlt.kitetu.com/KNo.F85E/0758-CDE5) | 114 |
| 2026-05-22 | 『井戸端のソクラテス』 | [K#F85E/0758-352C](https://dlt.kitetu.com/KNo.F85E/0758-352C) | 77 |
| 2025-07-29 | 『300万輪達成によせて』 | [K#F85E/0758-B2D5](https://dlt.kitetu.com/KNo.F85E/0758-B2D5) | 76 |
| 2026-04-23 | 『アープラノート』 | [K#F85E/0758-5EBB](https://dlt.kitetu.com/KNo.F85E/0758-5EBB) | 57 |
| 2026-02-02 | 書了一日一文 | [K#F85E/0758-F8FE](https://dlt.kitetu.com/KNo.F85E/0758-F8FE) | 32 |
| 2025-11-28 | 新生一日一文 | [K#F85E/0758-2BDE](https://dlt.kitetu.com/KNo.F85E/0758-2BDE) | 11 |

### 概念・用語・固有名（本人による定義）

既存の concepts/ ページや Scrapbox には無い、宇田川氏自身による定義文書。616件収録。本文の長いものほど、概念解説として価値が高い。

| 用語 | 本文長 | 描出日 | KNo |
|---|---|---|---|
| Cosense | 793 | 2018-11-27 | [K#F85E/4686-7AE6](https://dlt.kitetu.com/KNo.F85E/4686-7AE6) |
| 漢字 | 725 | 2012-09-23 | [K#F85E/32D9](https://dlt.kitetu.com/KNo.F85E/32D9) |
| 文字 | 715 | 2012-09-23 | [K#F85E/A81F](https://dlt.kitetu.com/KNo.F85E/A81F) |
| 希哲学 | 558 | 2013-04-13 | [K#F85E/9974](https://dlt.kitetu.com/KNo.F85E/9974) |
| 自由 | 512 | 2012-08-24 | [K#F85E/046C](https://dlt.kitetu.com/KNo.F85E/046C) |
| 綜語 | 474 | 2012-05-31 | [K#F85E/45E0](https://dlt.kitetu.com/KNo.F85E/45E0) |
| 副日記 | 471 | 2019-05-21 | [K#F85E/5B28-5CC0](https://dlt.kitetu.com/KNo.F85E/5B28-5CC0) |
| 睡眠記録 | 440 | 2018-07-27 | [K#F85E/4686-71BC](https://dlt.kitetu.com/KNo.F85E/4686-71BC) |
| 希哲館訳語 | 440 | 2017-08-25 | [K#F85E/4686-E5B8](https://dlt.kitetu.com/KNo.F85E/4686-E5B8) |
| 書了 | 437 | 2026-02-02 | [K#F85E/0758-0C6C](https://dlt.kitetu.com/KNo.F85E/0758-0C6C) |
| 2月 | 410 | 2014-09-21 | [K#F85E/C341](https://dlt.kitetu.com/KNo.F85E/C341) |
| 3月 | 399 | 2014-09-21 | [K#F85E/C7B3](https://dlt.kitetu.com/KNo.F85E/C7B3) |
| ソクラテス | 395 | 2012-08-25 | [K#F85E/F0A1](https://dlt.kitetu.com/KNo.F85E/F0A1) |
| デライト市場戦略 | 383 | 2020-05-16 | [K#F85E/5B28-3631](https://dlt.kitetu.com/KNo.F85E/5B28-3631) |
| 黄金朝食 | 354 | 2025-02-17 | [K#F85E/0758-181A](https://dlt.kitetu.com/KNo.F85E/0758-181A) |
| 整輪 | 349 | 2021-05-30 | [K#F85E/E74C-DB2E](https://dlt.kitetu.com/KNo.F85E/E74C-DB2E) |
| 希哲13年1月8日 | 338 | 2019-01-08 | [K#F85E/4686-0AC8](https://dlt.kitetu.com/KNo.F85E/4686-0AC8) |
| ウィキ | 316 | 2013-06-08 | [K#F85E/C358](https://dlt.kitetu.com/KNo.F85E/C358) |
| 主力機 | 313 | 2017-05-19 | [K#F85E/4686-8EC0](https://dlt.kitetu.com/KNo.F85E/4686-8EC0) |
| 大整輪 | 295 | 2022-03-05 | [K#F85E/E74C-2091](https://dlt.kitetu.com/KNo.F85E/E74C-2091) |
| 我由 | 274 | 2012-05-20 | [K#F85E/C1BC](https://dlt.kitetu.com/KNo.F85E/C1BC) |
| デライト広告収益の漸増 | 264 | 2026-02-11 | [K#F85E/0758-9A7D](https://dlt.kitetu.com/KNo.F85E/0758-9A7D) |
| 9月 | 263 | 2014-09-21 | [K#F85E/1230](https://dlt.kitetu.com/KNo.F85E/1230) |
| 12月 | 259 | 2014-09-21 | [K#F85E/6DF2](https://dlt.kitetu.com/KNo.F85E/6DF2) |
| 7月 | 259 | 2014-09-21 | [K#F85E/EE6A](https://dlt.kitetu.com/KNo.F85E/EE6A) |
| 6月 | 257 | 2014-09-21 | [K#F85E/E518](https://dlt.kitetu.com/KNo.F85E/E518) |
| 表外漢字 | 256 | 2015-04-22 | [K#F85E/0DF3](https://dlt.kitetu.com/KNo.F85E/0DF3) |
| 仮名 | 254 | 2014-03-18 | [K#F85E/1267](https://dlt.kitetu.com/KNo.F85E/1267) |
| 整清 | 252 | 2018-07-24 | [K#F85E/4686-193C](https://dlt.kitetu.com/KNo.F85E/4686-193C) |
| 黄金 | 249 | 2025-02-13 | [K#F85E/0758-450D](https://dlt.kitetu.com/KNo.F85E/0758-450D) |
| 日 | 243 | 2014-09-21 | [K#F85E/521C](https://dlt.kitetu.com/KNo.F85E/521C) |
| デライト | 240 | 2018-11-23 | [K#F85E/4686-182F](https://dlt.kitetu.com/KNo.F85E/4686-182F) |
| 輪郭小窓 | 230 | 2021-07-20 | [K#F85E/E74C-7ED7](https://dlt.kitetu.com/KNo.F85E/E74C-7ED7) |
| 「一万 葉面（＾ページ）のぬかるみ」編 | 224 | 2025-10-24 | [K#F85E/0758-D4AF](https://dlt.kitetu.com/KNo.F85E/0758-D4AF) |
| 熟語 | 215 | 2014-10-20 | [K#F85E/E752](https://dlt.kitetu.com/KNo.F85E/E752) |
| XWA | 214 | 2025-09-02 | [K#F85E/0758-73C4](https://dlt.kitetu.com/KNo.F85E/0758-73C4) |
| 希哲19年7月 | 213 | 2025-01-23 | [K#F85E/0758-99F4](https://dlt.kitetu.com/KNo.F85E/0758-99F4) |
| デライト宣伝 | 208 | 2020-06-29 | [K#F85E/5B28-49C7](https://dlt.kitetu.com/KNo.F85E/5B28-49C7) |
| 【候り】 | 203 | 2025-06-10 | [K#F85E/0758-0CDB](https://dlt.kitetu.com/KNo.F85E/0758-0CDB) |
| 希哲19年5月 | 203 | 2025-01-23 | [K#F85E/0758-2FBE](https://dlt.kitetu.com/KNo.F85E/0758-2FBE) |
| 希哲19年8月 | 203 | 2025-01-23 | [K#F85E/0758-57C5](https://dlt.kitetu.com/KNo.F85E/0758-57C5) |
| 希哲館 | 201 | 2012-06-18 | [K#F85E/6013](https://dlt.kitetu.com/KNo.F85E/6013) |
| 哲学者 | 197 | 2012-09-18 | [K#F85E/38C8](https://dlt.kitetu.com/KNo.F85E/38C8) |
| 一選万集 | 195 | 2019-01-08 | [K#F85E/4686-9F65](https://dlt.kitetu.com/KNo.F85E/4686-9F65) |
| 希哲19年6月 | 194 | 2025-01-23 | [K#F85E/0758-9B38](https://dlt.kitetu.com/KNo.F85E/0758-9B38) |
| 輪郭填範 | 191 | 2026-04-04 | [K#F85E/0758-0C80](https://dlt.kitetu.com/KNo.F85E/0758-0C80) |
| 希哲19年9月 | 187 | 2025-01-23 | [K#F85E/0758-1EF0](https://dlt.kitetu.com/KNo.F85E/0758-1EF0) |
| 上 | 181 | 2015-08-19 | [K#F85E/E8CA-4A64](https://dlt.kitetu.com/KNo.F85E/E8CA-4A64) |
| 出理 | 178 | 2026-01-22 | [K#F85E/0758-F528](https://dlt.kitetu.com/KNo.F85E/0758-F528) |
| 希哲19年12月 | 177 | 2025-01-23 | [K#F85E/0758-8887](https://dlt.kitetu.com/KNo.F85E/0758-8887) |
| 才 | 175 | 2015-05-23 | [K#F85E/45EB](https://dlt.kitetu.com/KNo.F85E/45EB) |
| 日記準備整輪 | 171 | 2025-06-16 | [K#F85E/0758-28EC](https://dlt.kitetu.com/KNo.F85E/0758-28EC) |
| 完全メイト | 171 | 2025-03-01 | [K#F85E/0758-AE6E](https://dlt.kitetu.com/KNo.F85E/0758-AE6E) |
| 歯ブラシの交換 | 167 | 2025-12-08 | [K#F85E/0758-6708](https://dlt.kitetu.com/KNo.F85E/0758-6708) |
| 陶練 | 163 | 2018-08-02 | [K#F85E/4686-0DA3](https://dlt.kitetu.com/KNo.F85E/4686-0DA3) |
| 閃き | 163 | 2017-03-10 | [K#F85E/7309-F77C](https://dlt.kitetu.com/KNo.F85E/7309-F77C) |
| 大脱皮 | 161 | 2025-05-30 | [K#F85E/0758-822F](https://dlt.kitetu.com/KNo.F85E/0758-822F) |
| 黄金大整輪 | 160 | 2025-02-13 | [K#F85E/0758-3AD7](https://dlt.kitetu.com/KNo.F85E/0758-3AD7) |
| 「市場施策（＾マーケティング）について考える」編 | 156 | 2026-03-20 | [K#F85E/0758-B628](https://dlt.kitetu.com/KNo.F85E/0758-B628) |
| 過 | 153 | 2015-08-21 | [K#F85E/E8CA-80D0](https://dlt.kitetu.com/KNo.F85E/E8CA-80D0) |
| 見 | 153 | 2015-08-23 | [K#F85E/E8CA-822B](https://dlt.kitetu.com/KNo.F85E/E8CA-822B) |
| 記 | 152 | 2015-05-29 | [K#F85E/941C](https://dlt.kitetu.com/KNo.F85E/941C) |
| 納 | 152 | 2015-10-02 | [K#F85E/E8CA-2350](https://dlt.kitetu.com/KNo.F85E/E8CA-2350) |
| 朝の定時執務 | 150 | 2026-02-04 | [K#F85E/0758-6162](https://dlt.kitetu.com/KNo.F85E/0758-6162) |
| 開 | 149 | 2015-04-20 | [K#F85E/C20E](https://dlt.kitetu.com/KNo.F85E/C20E) |
| 画数 | 148 | 2016-05-09 | [K#F85E/2510-960A](https://dlt.kitetu.com/KNo.F85E/2510-960A) |
| 提 | 148 | 2015-08-25 | [K#F85E/E8CA-BBD8](https://dlt.kitetu.com/KNo.F85E/E8CA-BBD8) |
| 散歩記録 | 147 | 2019-09-30 | [K#F85E/5B28-5E73](https://dlt.kitetu.com/KNo.F85E/5B28-5E73) |
| 自 | 146 | 2015-06-08 | [K#F85E/0377](https://dlt.kitetu.com/KNo.F85E/0377) |
| 希哲館黄金期 | 146 | 2018-11-04 | [K#F85E/4686-3606](https://dlt.kitetu.com/KNo.F85E/4686-3606) |
| 希哲20年1月 | 145 | 2025-09-09 | [K#F85E/0758-FBA1](https://dlt.kitetu.com/KNo.F85E/0758-FBA1) |
| 希哲館事業 | 145 | 2014-06-24 | [K#F85E/7C98](https://dlt.kitetu.com/KNo.F85E/7C98) |
| 希哲19年11月 | 144 | 2025-01-23 | [K#F85E/0758-E637](https://dlt.kitetu.com/KNo.F85E/0758-E637) |
| 侍い | 140 | 2020-02-12 | [K#F85E/5B28-EC32](https://dlt.kitetu.com/KNo.F85E/5B28-EC32) |
| 累新 | 140 | 2015-03-30 | [K#F85E/C038](https://dlt.kitetu.com/KNo.F85E/C038) |
| 利 | 139 | 2015-04-30 | [K#F85E/30F1](https://dlt.kitetu.com/KNo.F85E/30F1) |
| 語 | 138 | 2014-09-26 | [K#F85E/C891](https://dlt.kitetu.com/KNo.F85E/C891) |
| 現 | 138 | 2015-08-23 | [K#F85E/E8CA-3683](https://dlt.kitetu.com/KNo.F85E/E8CA-3683) |
| 省 | 138 | 2015-09-07 | [K#F85E/E8CA-998D](https://dlt.kitetu.com/KNo.F85E/E8CA-998D) |
| 知能増幅 | 137 | 2014-11-07 | [K#F85E/32AD](https://dlt.kitetu.com/KNo.F85E/32AD) |

（536件は jsonl 参照）

### 漢字関連（教育漢字一覧）

学年別の教育漢字を列挙した参照表。8件。

### 年単位（希哲N年）

特定年の総説的な輪郭。3件。

## 引用上の注意

- すべての輪郭の作者は「宇田川（希哲）浩行」と表示される（本人発言として扱える）
- ただし本人が後年に編集した可能性はある（再描出日時 ts_rdrw が記録されている）
- 「希哲N年」は希哲館の独自年号（希哲元年=2007年）
- 引用時は原 URL（dlt.kitetu.com の KNo.XXXX）と取得日を併記すること

## 関連
- [Scrapbox 井戸端側の発言整理](villagepump-デライト.2hop.md)
- 概念ページ群: [wiki/concepts/](../wiki/concepts) / [wiki/concepts/utagawa/](../wiki/concepts/utagawa)
- メタページ: [wiki/meta/先行概念マッピング.md](../wiki/meta/先行概念マッピング.md)
