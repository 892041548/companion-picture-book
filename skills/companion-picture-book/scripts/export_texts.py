#!/usr/bin/env python3
"""Export five UTF-8 texts with pronunciation aids (schema 2); support legacy schema 1.

This checks document structure, not translation quality or rendered images.
Python 3.9+; standard library only.
"""

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile


class ManuscriptError(ValueError):
    pass


def require_text(value, location):
    if not isinstance(value, str) or not value.strip():
        raise ManuscriptError(f"{location}: expected non-empty text")
    if value != value.strip():
        raise ManuscriptError(f"{location}: remove leading/trailing whitespace")
    if any(ord(char) < 32 and char != "\n" for char in value):
        raise ManuscriptError(f"{location}: unsupported control character")
    return value


def validate_manuscript(book):
    if not isinstance(book, dict):
        raise ManuscriptError("manuscript must be a JSON object")
    if type(book.get("schema_version")) is not int or book["schema_version"] not in (1, 2):
        raise ManuscriptError("schema_version must be 1 (legacy) or 2 (with pronunciation aids)")
    require_text(book.get("revision"), "revision")
    if book.get("language_mode") != "zh-en":
        raise ManuscriptError("this exporter supports language_mode='zh-en' only")
    if book.get("mode") not in ("single", "cards", "story"):
        raise ManuscriptError("mode must be single, cards, or story")
    pages = book.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ManuscriptError("pages must be a non-empty array")

    content_count = 0
    for index, page in enumerate(pages):
        location = f"pages[{index}]"
        if not isinstance(page, dict):
            raise ManuscriptError(f"{location}: expected an object")
        kind = page.get("kind")
        if kind == "cover":
            if book["mode"] != "story" or index != 0 or page.get("id") != "00":
                raise ManuscriptError("cover is only allowed first in a story, with id '00'")
        elif kind == "content":
            content_count += 1
            if page.get("id") != f"{content_count:02d}":
                raise ManuscriptError(f"{location}: expected consecutive id '{content_count:02d}'")
        else:
            raise ManuscriptError(f"{location}: kind must be cover or content")

        blocks = page.get("texts")
        if not isinstance(blocks, list):
            raise ManuscriptError(f"{location}.texts: expected an array; use [] for a wordless page")
        block_ids = set()
        for block_index, block in enumerate(blocks):
            block_location = f"{location}.texts[{block_index}]"
            if not isinstance(block, dict):
                raise ManuscriptError(f"{block_location}: expected an object")
            block_id = require_text(block.get("id"), f"{block_location}.id")
            if "\n" in block_id or block_id in block_ids:
                raise ManuscriptError(f"{block_location}.id: must be single-line and unique on the page")
            block_ids.add(block_id)
            for language in ("zh", "en"):
                require_text(block.get(language), f"{block_location}.{language}")
            if book["schema_version"] == 2:
                ipa = require_text(block.get("en_ipa"), f"{block_location}.en_ipa")
                if not (ipa.startswith("/") and ipa.endswith("/") and len(ipa) > 2):
                    raise ManuscriptError(f"{block_location}.en_ipa: wrap reviewed IPA in /.../")
                homophone = require_text(block.get("en_homophone"), f"{block_location}.en_homophone")
                if not any("\u4e00" <= char <= "\u9fff" for char in homophone):
                    raise ManuscriptError(f"{block_location}.en_homophone: expected Chinese pronunciation aid, not romanization")


    if not content_count:
        raise ManuscriptError("at least one content page is required")
    if book["mode"] == "single" and content_count != 1:
        raise ManuscriptError("single mode requires exactly one content page; use cards for a set")
    return book


def render_texts(book):
    """Preserve manuscript text exactly, adding only document separators."""
    validate_manuscript(book)
    annotated = book["schema_version"] == 2
    parallel_pages = []
    aid_pages = {"en_ipa": [], "en_homophone": []}
    reading_pages = {"zh": [], "en": []}
    for page in book["pages"]:
        page_label = "封面" if page["kind"] == "cover" else f"第 {page['id']} 页"
        parallel_lines = [f"【{page_label}】"]
        blocks = page["texts"]
        if not blocks:
            parallel_lines.append("（无朗读正文）")
        for block in blocks:
            parallel_lines.extend([
                f"[{block['id']}]",
                "中文：" + block["zh"],
                "English: " + block["en"],
            ])
            if annotated:
                parallel_lines.extend(["音标：" + block["en_ipa"], "中文谐音：" + block["en_homophone"]])
        parallel_pages.append("\n".join(parallel_lines))
        if annotated:
            for field, label in (("en_ipa", "音标"), ("en_homophone", "中文谐音")):
                lines = [f"【{page_label}】"]
                if not blocks:
                    lines.append("（无朗读正文）")
                for block in blocks:
                    lines.extend([f"[{block['id']}]", "English: " + block["en"], label + "：" + block[field]])
                aid_pages[field].append("\n".join(lines))
        if blocks:
            for language in reading_pages:
                reading_pages[language].append("\n".join(block[language] for block in blocks))

    def document(parts):
        return "\n\n".join(parts) + ("\n" if parts else "")

    ipa_note = "音标为美式参考，| 表示停顿；实际朗读可能有弱读、连读或口音差异。"
    homophone_note = "中文谐音（用户所说的罗马音）仅作近似记忆提示，不是标准发音；请先听英文原声再跟读。"
    documents = {
        "双语对照稿.txt": document(([ipa_note, homophone_note] if annotated else []) + parallel_pages),
        "中文朗读稿.txt": document(reading_pages["zh"]),
        "英文朗读稿.txt": document(reading_pages["en"]),
    }
    if annotated:
        documents["英文朗读稿-音标版.txt"] = document([ipa_note] + aid_pages["en_ipa"])
        documents["英文朗读稿-中文谐音版.txt"] = document([homophone_note] + aid_pages["en_homophone"])
    return documents


def export_texts(book, output_dir, overwrite=False):
    documents = render_texts(book)
    output_dir = Path(output_dir)
    targets = [output_dir / name for name in documents]
    if not overwrite and any(path.exists() or path.is_symlink() for path in targets):
        raise FileExistsError("generated text already exists; use a new output directory or --overwrite")
    if any(path.is_dir() for path in targets):
        raise IsADirectoryError("an output filename is occupied by a directory")
    output_dir.mkdir(parents=True, exist_ok=True)
    # Stage complete files before replacing individual generated outputs.
    with tempfile.TemporaryDirectory(prefix=".texts-", dir=output_dir) as temporary:
        for name, content in documents.items():
            with (Path(temporary) / name).open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(content)
        for name in documents:
            staged = Path(temporary) / name
            destination = output_dir / name
            if overwrite:
                os.replace(staged, destination)
            else:
                # Hard-link creation is exclusive, so a concurrent file is not overwritten.
                os.link(staged, destination)
    return targets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        with args.manuscript.open(encoding="utf-8-sig") as handle:
            book = json.load(handle)
        paths = export_texts(book, args.out, args.overwrite)
    except (OSError, ValueError) as error:
        print(f"Export failed: {error}", file=sys.stderr)
        return 1
    print(f"Exported {len(paths)} text files from revision {book['revision']}:")
    for path in paths:
        print(path.resolve())
    if book["schema_version"] == 1:
        print("Legacy schema 1: pronunciation aids are NOT included. Upgrade to schema 2 for five files.")
    print("Translation, pronunciation, page text, and visual QA still require review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
