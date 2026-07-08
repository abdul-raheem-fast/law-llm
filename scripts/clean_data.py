# Clean and split raw legal HTML documents

import os
import re
import csv
import sys
import html


def strip_html_tags(text):
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<p[^>]*>', '\n\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</p>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<hr[^>]*>', '\n---\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    return text


def clean_whitespace(text):
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        cleaned.append(stripped)
    result = '\n'.join(cleaned)
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip()


def extract_ppc_sections(raw_html):
    """
    Extract individual sections from the Pakistan Penal Code HTML.
    Returns a list of dicts: [{number, title, text, chapter}, ...]
    """
    sections = []
    current_chapter = "INTRODUCTION"
    chapter_pattern = re.compile(
        r'<h4[^>]*>\s*(CHAPTER\s+[IVXLCDM]+)\s*</h4>\s*<h4[^>]*>\s*(.*?)\s*</h4>',
        re.IGNORECASE | re.DOTALL
    )
    section_pattern = re.compile(
        r'<nobr><b>(\d+[A-Z]?)\.</b></nobr>.*?<td[^>]*>(.*?)</td>',
        re.DOTALL | re.IGNORECASE
    )
    chapter_matches = list(chapter_pattern.finditer(raw_html))
    chapter_positions = [(m.start(), m.group(1).strip(), m.group(2).strip())
                         for m in chapter_matches]
    for match in section_pattern.finditer(raw_html):
        sec_num = match.group(1).strip()
        sec_content = match.group(2).strip()
        sec_pos = match.start()
        for i, (cpos, cnum, ctitle) in enumerate(chapter_positions):
            if i + 1 < len(chapter_positions):
                if cpos <= sec_pos < chapter_positions[i + 1][0]:
                    current_chapter = f"{cnum} — {ctitle}"
                    break
            else:
                if cpos <= sec_pos:
                    current_chapter = f"{cnum} — {ctitle}"
        clean_content = strip_html_tags(sec_content)
        clean_content = clean_whitespace(clean_content)
        title_match = re.match(r'^(.*?\.)\s*\n', clean_content)
        title = title_match.group(1).strip() if title_match else f"Section {sec_num}"

        sections.append({
            "number": sec_num,
            "title": title,
            "text": clean_content,
            "chapter": current_chapter,
            "act": "Pakistan Penal Code, 1860"
        })

    return sections


def extract_constitution_articles(raw_html):
    """
    Extract individual articles from the Constitution HTML (Part II, Chapter 1).
    Returns a list of dicts: [{number, title, text}, ...]
    """
    articles = []
    article_pattern = re.compile(
        r'<a\s+name="(\d+[A-Z]?)"\s*></a>.*?'
        r'<nobr><b>(\d+[A-Z]?)\.</b></nobr>.*?<td[^>]*>(.*?)</td>',
        re.DOTALL | re.IGNORECASE
    )
    if not article_pattern.findall(raw_html):
        article_pattern = re.compile(
            r'<nobr><b>(\d+[A-Z]?)\.</b></nobr>.*?<td[^>]*>(.*?)</td>',
            re.DOTALL | re.IGNORECASE
        )
        for match in article_pattern.finditer(raw_html):
            art_num = match.group(1).strip()
            art_content = match.group(2).strip()
            try:
                num_val = int(re.match(r'(\d+)', art_num).group(1))
                if num_val < 8 or num_val > 28:
                    continue
            except (ValueError, AttributeError):
                continue

            clean_content = strip_html_tags(art_content)
            clean_content = clean_whitespace(clean_content)

            title_match = re.match(r'^(.*?\.)\s', clean_content)
            title = title_match.group(1).strip() if title_match else f"Article {art_num}"

            articles.append({
                "number": art_num,
                "title": title,
                "text": clean_content,
                "chapter": "Part II, Chapter 1: Fundamental Rights",
                "act": "Constitution of Pakistan, 1973"
            })
    else:
        for match in article_pattern.finditer(raw_html):
            art_num = match.group(2).strip() if match.lastindex >= 2 else match.group(1).strip()
            art_content = match.group(match.lastindex).strip()

            try:
                num_val = int(re.match(r'(\d+)', art_num).group(1))
                if num_val < 8 or num_val > 28:
                    continue
            except (ValueError, AttributeError):
                continue

            clean_content = strip_html_tags(art_content)
            clean_content = clean_whitespace(clean_content)

            title_match = re.match(r'^(.*?\.)\s', clean_content)
            title = title_match.group(1).strip() if title_match else f"Article {art_num}"

            articles.append({
                "number": art_num,
                "title": title,
                "text": clean_content,
                "chapter": "Part II, Chapter 1: Fundamental Rights",
                "act": "Constitution of Pakistan, 1973"
            })

    return articles


def process_raw_text_fallback(raw_html, act_name, prefix):
    """
    Fallback: if HTML parsing doesn't work well, just do basic
    text extraction and split by Section/Article markers.
    """
    text = strip_html_tags(raw_html)
    text = clean_whitespace(text)

    sections = []
    parts = re.split(r'\n(?=\d+[A-Z]?\.\s+[A-Z])', text)

    for part in parts:
        part = part.strip()
        if not part:
            continue
        sec_match = re.match(r'^(\d+[A-Z]?)\.\s+(.*?)(?:\.\s|\n)', part, re.DOTALL)
        if sec_match:
            sec_num = sec_match.group(1)
            title = sec_match.group(2).strip()
            sections.append({
                "number": sec_num,
                "title": f"{title}.",
                "text": part,
                "chapter": "",
                "act": act_name
            })

    return sections


def save_sections(sections, output_dir, prefix):
    """Save each section/article as an individual .txt file."""
    os.makedirs(output_dir, exist_ok=True)
    saved = []

    for sec in sections:
        num = sec["number"]
        filename = f"{prefix}_{num}.txt"
        filepath = os.path.join(output_dir, filename)
        content = (
            f"ACT: {sec['act']}\n"
            f"SECTION/ARTICLE: {num}\n"
            f"TITLE: {sec['title']}\n"
            f"CHAPTER: {sec['chapter']}\n"
            f"{'=' * 60}\n\n"
            f"{sec['text']}\n"
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        word_count = len(sec["text"].split())
        saved.append({
            "filename": filename,
            "act": sec["act"],
            "section_article": num,
            "title": sec["title"],
            "chapter": sec["chapter"],
            "word_count": word_count
        })

    return saved


def main():
    print("Cleaning legal data pipeline...")

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)

    clean_dir = "data/clean"
    os.makedirs(clean_dir, exist_ok=True)

    all_records = []
    ppc_files = [
        os.path.join("data", "raw", "ppc", f)
        for f in os.listdir(os.path.join("data", "raw", "ppc"))
        if f.endswith((".html", ".htm", ".txt"))
    ] if os.path.isdir(os.path.join("data", "raw", "ppc")) else []

    if ppc_files:
        print("\n  Processing Pakistan Penal Code...")
        for fpath in ppc_files:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                raw = f.read()
            sections = extract_ppc_sections(raw)
            if not sections:
                print(f"    [WARN] HTML parsing found 0 sections, trying fallback...")
                sections = process_raw_text_fallback(raw, "Pakistan Penal Code, 1860", "ppc")
            records = save_sections(sections, clean_dir, "ppc_section")
            all_records.extend(records)
            print(f"    [OK] Extracted {len(records)} PPC sections")
    else:
        print("\n  [WARN] No PPC files found in data/raw/ppc/")
        print("     Run: python scripts/download_sources.py first")
    crpc_files = [
        os.path.join("data", "raw", "crpc", f)
        for f in os.listdir(os.path.join("data", "raw", "crpc"))
        if f.endswith((".html", ".htm", ".txt"))
    ] if os.path.isdir(os.path.join("data", "raw", "crpc")) else []

    if crpc_files:
        print("\n  Processing Code of Criminal Procedure...")
        for fpath in crpc_files:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                raw = f.read()
            sections = process_raw_text_fallback(raw, "Code of Criminal Procedure, 1898", "crpc")
            records = save_sections(sections, clean_dir, "crpc_section")
            all_records.extend(records)
            print(f"    [OK] Extracted {len(records)} CrPC sections")
    else:
        print("\n  [WARN] No CrPC files found in data/raw/crpc/")
        print("     Please download CrPC manually (see download_sources.py)")
    const_files = [
        os.path.join("data", "raw", "constitution", f)
        for f in os.listdir(os.path.join("data", "raw", "constitution"))
        if f.endswith((".html", ".htm", ".txt"))
    ] if os.path.isdir(os.path.join("data", "raw", "constitution")) else []

    if const_files:
        print("\n  Processing Constitution (Fundamental Rights)...")
        for fpath in const_files:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                raw = f.read()
            articles = extract_constitution_articles(raw)
            if not articles:
                print(f"    [WARN] HTML parsing found 0 articles, trying fallback...")
                articles = process_raw_text_fallback(
                    raw, "Constitution of Pakistan, 1973", "constitution"
                )
            records = save_sections(articles, clean_dir, "constitution_article")
            all_records.extend(records)
            print(f"    [OK] Extracted {len(records)} Constitutional articles")
    else:
        print("\n  [WARN] No Constitution files found in data/raw/constitution/")
        print("     Run: python scripts/download_sources.py first")
    if all_records:
        index_path = os.path.join("data", "data_index.csv")
        with open(index_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                "filename", "act", "section_article", "title", "chapter", "word_count"
            ])
            writer.writeheader()
            writer.writerows(all_records)

        print(f"\n  Data index saved: {index_path}")
        print(f"     Total records: {len(all_records)}")
        total_words = sum(r["word_count"] for r in all_records)
        print(f"     Total word count: {total_words:,}")
    else:
        print("\n  [FAIL] No records to write. Ensure raw data is present.")

    print()
    return 0 if all_records else 1


if __name__ == "__main__":
    sys.exit(main())
