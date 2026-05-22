#!/usr/bin/env python3
"""Re-parse already-fetched HTML in raw/dlt-udagawa/html/ → outlines.jsonl

正しい dln 抽出（div ネスト対応）。
"""
import re, json, os, glob
from html import unescape

ROOT = "/Users/nishio/delite/raw/dlt-udagawa"


def kno_from_safe(safe: str) -> str:
    return "K#" + safe.replace("_", "/")


def find_matching_close_div(html: str, start: int) -> int:
    """start = index right after a <div ...> opening tag.
    Return index of matching </div>'s '<'."""
    depth = 1
    i = start
    L = len(html)
    while i < L:
        no = html.find("<div", i)
        nc = html.find("</div>", i)
        if nc == -1:
            return -1
        if no != -1 and no < nc:
            # next char must be space or '>' to be a div tag, not divider etc.
            if no + 4 < L and html[no + 4] in " \t\n\r>":
                depth += 1
            i = no + 4
        else:
            depth -= 1
            if depth == 0:
                return nc
            i = nc + 6
    return -1


def extract_dln(html: str, kno: str) -> tuple[str, str]:
    """Return (dln_html, dln_text)."""
    # locate the article for this kno
    art_re = re.compile(
        r'<article[^>]*data-kno="' + re.escape(kno) + r'"[^>]*>',
    )
    am = art_re.search(html)
    if not am:
        return "", ""
    # find dln tag within first ~30KB after article start (entire article block)
    art_pos = am.end()
    # also bound by next </article>
    art_end = html.find("</article>", art_pos)
    if art_end == -1:
        art_end = art_pos + 30000
    region = html[art_pos:art_end]
    dm = re.search(
        r'<div class="dln"[^>]*itemprop="articleBody"[^>]*>', region,
    )
    if not dm:
        return "", ""
    start_in_region = dm.end()
    # convert to absolute index
    start = art_pos + start_in_region
    end = find_matching_close_div(html, start)
    if end == -1:
        return "", ""
    inner = html[start:end]
    text = unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", inner))).strip()
    return inner.strip(), text


def parse(kno: str, html: str) -> dict:
    # title
    art_re = re.compile(
        r'<article[^>]*data-kno="' + re.escape(kno) + r'"[^>]*>(.*?)</article>',
        re.DOTALL,
    )
    am = art_re.search(html)
    main_body = am.group(1) if am else ""

    title_m = re.search(r'<span class="knm"[^>]*data-src="([^"]*)"', main_body) \
        or re.search(r'<meta property="og:title" content="([^"]*)"', html)
    title = unescape(title_m.group(1)) if title_m else ""

    dln_html, dln_text = extract_dln(html, kno)

    auth_m = re.search(
        r'<address class="ego"[^>]*>.*?<span itemprop="name">([^<]+)</span>',
        main_body, re.DOTALL,
    )
    author = unescape(auth_m.group(1)) if auth_m else ""

    ts_drw_m = re.search(
        r'<time class="ts_drw"[^>]*>(?:<[^>]+>)*([^<]+)</time>', main_body,
    )
    ts_drw = ts_drw_m.group(1).strip() if ts_drw_m else ""
    ts_rdrw_m = re.search(
        r'<time class="ts_rdrw"[^>]*>(?:<[^>]+>)*([^<]+)</time>', main_body,
    )
    ts_rdrw = ts_rdrw_m.group(1).strip() if ts_rdrw_m else ""

    if am:
        before = html[: am.start()]
        after = html[am.end():]
    else:
        before, after = "", ""
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
        "url": f"https://dlt.kitetu.com/" + kno.replace("K#", "KNo."),
        "title": title,
        "author": author,
        "ts_drw": ts_drw,
        "ts_rdrw": ts_rdrw,
        "body": dln_text,
        "body_html": dln_html,
        "fg_refs": fg_refs,
        "fg_names": fg_names,
        "bg_refs": bg_refs,
        "bg_names": bg_names,
    }


def main():
    out = open(f"{ROOT}/outlines.jsonl", "w", encoding="utf-8")
    n = 0
    for f in sorted(glob.glob(f"{ROOT}/html/*.html")):
        safe = os.path.splitext(os.path.basename(f))[0]
        kno = kno_from_safe(safe)
        with open(f) as fh:
            html = fh.read()
        data = parse(kno, html)
        out.write(json.dumps(data, ensure_ascii=False) + "\n")
        n += 1
    out.close()
    print(f"reparsed: {n}")


if __name__ == "__main__":
    main()
