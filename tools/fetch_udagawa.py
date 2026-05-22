#!/usr/bin/env python3
"""BFS-fetch 宇田川氏 (F85E) の輪郭ページを取得して JSONL に整形する。

入口: 既知の起点 KNo を seeds に与える。
取り出し: fg/bg リンクのうち K#F85E/* のものをキューに追加。
レート制限: 1.5 秒間隔。
出力:
  raw/dlt-udagawa/html/<KNO>.html  (生 HTML)
  raw/dlt-udagawa/outlines.jsonl   (1 輪郭 1 行)
  raw/dlt-udagawa/fetch.log        (取得ログ)
"""
import sys, os, re, json, time, urllib.parse
from collections import deque
from html import unescape
import urllib.request

BASE = "https://dlt.kitetu.com"
ROOT = "/Users/nishio/delite/raw/dlt-udagawa"
UA = "Mozilla/5.0 wiki-builder/0.1 (contact:nishio.hirokazu@gmail.com)"
SLEEP = 1.5

SEEDS = [
    "K#F85E",
    # recent (from listing page 1, snapshot 2026-05-22)
    "K#F85E/0758-3F4F", "K#F85E/0758-36B9", "K#F85E/0758-3561", "K#F85E/0758-9649",
    "K#F85E/0758-352C", "K#F85E/0758-4DF9", "K#F85E/0758-CC01", "K#F85E/0758-0EE6",
    "K#F85E/0758-DE2E", "K#F85E/0758-FD3B",
    # one known dev log
    "K#F85E/0758-4B81",
]


def kno_to_safe(kno: str) -> str:
    """K#F85E/0758-4B81 -> F85E_0758-4B81  (ファイル名用)"""
    return kno.replace("K#", "").replace("/", "_")


def kno_to_url(kno: str) -> str:
    """K#F85E/0758-4B81 -> https://dlt.kitetu.com/KNo.F85E/0758-4B81"""
    path = kno.replace("K#", "KNo.")
    return f"{BASE}/{path}"


def fetch(url: str) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
            return data.decode("utf-8", errors="replace")
    except Exception as e:
        return None


def parse(kno: str, html: str) -> dict:
    """主輪郭の各フィールドを抽出。"""
    # main article block
    art_re = re.compile(
        r'<article[^>]*data-kno="(' + re.escape(kno) + r')"[^>]*>(.*?)</article>',
        re.DOTALL,
    )
    m = art_re.search(html)
    main_body = m.group(2) if m else ""

    title_m = re.search(r'<span class="knm"[^>]*data-src="([^"]*)"', main_body) \
        or re.search(r'<meta property="og:title" content="([^"]*)"', html)
    title = unescape(title_m.group(1)) if title_m else ""

    # description body (articleBody)
    dln_m = re.search(
        r'<div class="dln"[^>]*itemprop="articleBody"[^>]*>(.*?)</div>',
        main_body, re.DOTALL,
    )
    dln_html = dln_m.group(1) if dln_m else ""
    dln_text = unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", dln_html))).strip()

    # author
    auth_m = re.search(
        r'<address class="ego"[^>]*>.*?<span itemprop="name">([^<]+)</span>',
        main_body, re.DOTALL,
    )
    author = unescape(auth_m.group(1)) if auth_m else ""

    # ts_drw, ts_rdrw
    ts_drw_m = re.search(
        r'<time class="ts_drw"[^>]*>(?:<[^>]+>)*([^<]+)</time>', main_body,
    )
    ts_drw = ts_drw_m.group(1).strip() if ts_drw_m else ""
    ts_rdrw_m = re.search(
        r'<time class="ts_rdrw"[^>]*>(?:<[^>]+>)*([^<]+)</time>', main_body,
    )
    ts_rdrw = ts_rdrw_m.group(1).strip() if ts_rdrw_m else ""

    # foreground / background outline refs (parent of main article)
    # fg block is BEFORE the main article (top), bg block is AFTER (bottom).
    # Locate by class "fg" and "bg" enclosing spans with data-kno.
    fg_refs, bg_refs = [], []
    # Find article position
    if m:
        before = html[:m.start()]
        after = html[m.end():]
    else:
        before, after = "", ""
    # Take last <div class="*fg*"> open before article, and first <div class="*bg*"> after article
    # Heuristic: search the closest fg/bg wrappers
    # Simpler: gather refs from outermost "bln top fg" and "bg" containers around the article
    # Just gather data-kno from before/after blocks limited to ~2000 chars window
    fg_window = before[-3000:] if before else ""
    bg_window = after[:3000] if after else ""
    fg_refs = re.findall(r'<span[^>]*class="oln[^"]*"[^>]*data-kno="(K#[^"]+)"', fg_window)
    fg_names = re.findall(
        r'<span[^>]*class="oln[^"]*"[^>]*data-kno="K#[^"]+"[^>]*>.*?<a class="knm"[^>]*data-src="([^"]*)"',
        fg_window, re.DOTALL,
    )
    bg_refs = re.findall(r'<span[^>]*class="oln[^"]*"[^>]*data-kno="(K#[^"]+)"', bg_window)
    bg_names = re.findall(
        r'<span[^>]*class="oln[^"]*"[^>]*data-kno="K#[^"]+"[^>]*>.*?<a class="knm"[^>]*data-src="([^"]*)"',
        bg_window, re.DOTALL,
    )

    return {
        "kno": kno,
        "url": kno_to_url(kno),
        "title": title,
        "author": author,
        "ts_drw": ts_drw,
        "ts_rdrw": ts_rdrw,
        "body": dln_text,
        "body_html": dln_html.strip(),
        "fg_refs": fg_refs,
        "fg_names": fg_names,
        "bg_refs": bg_refs,
        "bg_names": bg_names,
    }


def main(limit: int = 500):
    os.makedirs(f"{ROOT}/html", exist_ok=True)
    jsonl_path = f"{ROOT}/outlines.jsonl"
    log_path = f"{ROOT}/fetch.log"

    # resume: load already-fetched knos AND rebuild pending queue from their refs
    done = set()
    pending_from_existing = []
    if os.path.exists(jsonl_path):
        with open(jsonl_path) as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                    done.add(r["kno"])
                    for ref in r.get("fg_refs", []) + r.get("bg_refs", []):
                        if ref.startswith("K#F85E"):
                            pending_from_existing.append(ref)
                except Exception:
                    pass
        print(f"resume: {len(done)} already fetched, {len(pending_from_existing)} ref candidates from existing data")

    queue = deque()
    queued = set()
    for s in SEEDS:
        if s not in done and s not in queued:
            queue.append(s); queued.add(s)
    # then add pending refs gathered from previously-fetched outlines
    for s in pending_from_existing:
        if s not in done and s not in queued:
            queue.append(s); queued.add(s)
    print(f"queue size on start: {len(queue)}")

    out_jsonl = open(jsonl_path, "a", encoding="utf-8")
    out_log = open(log_path, "a", encoding="utf-8")

    fetched = 0
    while queue and fetched < limit:
        kno = queue.popleft()
        if kno in done:
            continue
        url = kno_to_url(kno)
        html = fetch(url)
        if html is None:
            out_log.write(f"FAIL {kno}\n"); out_log.flush()
            print(f"  FAIL {kno}")
            time.sleep(SLEEP)
            continue

        safe = kno_to_safe(kno)
        with open(f"{ROOT}/html/{safe}.html", "w", encoding="utf-8") as fh:
            fh.write(html)

        data = parse(kno, html)
        out_jsonl.write(json.dumps(data, ensure_ascii=False) + "\n")
        out_jsonl.flush()
        done.add(kno)
        fetched += 1

        # enqueue F85E refs
        for ref in data["fg_refs"] + data["bg_refs"]:
            if ref.startswith("K#F85E") and ref not in done and ref not in queued:
                queue.append(ref); queued.add(ref)

        out_log.write(
            f"OK {kno} | title={data['title'][:30]} | body_len={len(data['body'])} | queue={len(queue)}\n"
        )
        out_log.flush()
        if fetched % 10 == 0:
            print(f"  {fetched} fetched, queue={len(queue)}, last={kno}")
        time.sleep(SLEEP)

    out_jsonl.close()
    out_log.close()
    print(f"done. fetched={fetched}, total done={len(done)}, queue remaining={len(queue)}")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    main(limit=n)
