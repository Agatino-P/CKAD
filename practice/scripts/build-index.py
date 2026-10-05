#!/usr/bin/env python3
# Usage: python3 practice/scripts/build-index.py  (from anywhere; regenerates practice/EXERCISE_INDEX.md, needs pdftotext on PATH)
"""Build practice/EXERCISE_INDEX.md from the exercise sources and practice/scripts/exercise-map.json.

The sources are the three git submodules under practice/sources/ and the Killer Shell results
archive under "Study notes/".
The mechanical part, listing the exercises, is done here.
The hand-written part, one domain, topic and lab-needs entry per exercise id, lives in
exercise-map.json beside this script, so that a re-run reproduces the same index.
An entry also carries "verified", the Kubernetes minor version its reference solution was run on,
once the "Prepare" step of practice/PRACTICE_PLAN.md has run it.
ckad-dojo questions carry their domain in the source, so their map entries hold no domain.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[1]
MAP_FILE = SCRIPT_DIR / "exercise-map.json"
OUTPUT = REPO / "practice" / "EXERCISE_INDEX.md"

DGK_DIR = "practice/sources/dgkanatsios-ckad-exercises"
BM_DIR = "practice/sources/bmuschko-ckad-crash-course/exercises"
DOJO_DIR = "practice/sources/tipunchlabs-ckad-dojo/exams"
KS_PDF = "Study notes/Killer Shell - Exam Simulators - results.pdf"

DGK_FILES = [
    "a.core_concepts.md",
    "b.multi_container_pods.md",
    "c.pod_design.md",
    "d.configuration.md",
    "e.observability.md",
    "f.services.md",
    "g.state.md",
    "h.helm.md",
    "i.crd.md",
    "j.podman.md",
]

DOMAINS = {
    "Application Design and Build",
    "Application Deployment",
    "Application Observability and Maintenance",
    "Application Environment, Configuration and Security",
    "Services and Networking",
}

# ckad-dojo spells one domain with an ampersand in some files; both spellings map to the curriculum name.
DOJO_DOMAIN_SPELLINGS = {
    "application design and build": "Application Design and Build",
    "application deployment": "Application Deployment",
    "application observability and maintenance": "Application Observability and Maintenance",
    "application environment, configuration and security": "Application Environment, Configuration and Security",
    "application environment, configuration & security": "Application Environment, Configuration and Security",
    "services and networking": "Services and Networking",
}

LAB_NEEDS = {"ingress", "metrics", "storage", "netpol", "helm", "image-build", "registry", "crd"}

HEADING_LIMIT = 60
VERSION = re.compile(r"^v\d+\.\d+$")

SOURCES = [
    ("dgk", "dgkanatsios/CKAD-exercises"),
    ("bm", "bmuschko/ckad-crash-course"),
    ("dojo", "TiPunchLabs/ckad-dojo"),
    ("ks", "Killer Shell simulator archive"),
]


def parse_dgk():
    rows = []
    for name in DGK_FILES:
        letter = name[0].upper()
        text = (REPO / DGK_DIR / name).read_text(encoding="utf-8")
        ordinal = 0
        for line in text.splitlines():
            if line.startswith("### "):
                ordinal += 1
                rows.append(
                    {
                        "id": f"DGK-{letter}-{ordinal:02d}",
                        "source": f"{DGK_DIR}/{name} § {truncate(line[4:].strip())}",
                    }
                )
    return rows


def parse_bm():
    rows = []
    base = REPO / BM_DIR
    for directory in sorted(base.iterdir()):
        match = re.match(r"^(\d{2})-", directory.name)
        if not directory.is_dir() or not match:
            continue
        if not (directory / "instructions.md").is_file():
            raise SystemExit(f"{directory} has no instructions.md")
        rows.append({"id": f"BM-{match.group(1)}", "source": f"{BM_DIR}/{directory.name}"})
    return rows


DOJO_HEADING = re.compile(r"^## Question (\d+) \| (.+?)\s*$")
DOJO_DOMAIN = re.compile(r"\*\*CNCF Domain\*\*\s*\|\s*(.+?)\s*\|\s*$")


def parse_dojo():
    rows = []
    base = REPO / DOJO_DIR
    simulations = sorted(
        (int(re.match(r"^ckad-simulation(\d+)$", d.name).group(1)), d)
        for d in base.iterdir()
        if d.is_dir() and re.match(r"^ckad-simulation(\d+)$", d.name)
    )
    for number, directory in simulations:
        path = directory / "questions.md"
        relative = f"{DOJO_DIR}/{directory.name}/questions.md"
        current = None
        for line in path.read_text(encoding="utf-8").splitlines():
            heading = DOJO_HEADING.match(line)
            if heading:
                current = {
                    "id": f"DOJO-{number:02d}-Q{int(heading.group(1)):02d}",
                    "source": f"{relative} § {truncate(line[3:].strip())}",
                    "domain": None,
                }
                rows.append(current)
                continue
            if current is None or current["domain"] is not None:
                continue
            domain = DOJO_DOMAIN.search(line)
            if domain:
                key = re.sub(r"\s+", " ", domain.group(1).strip()).lower()
                if key not in DOJO_DOMAIN_SPELLINGS:
                    raise SystemExit(f"{current['id']}: unknown domain spelling {domain.group(1)!r}")
                current["domain"] = DOJO_DOMAIN_SPELLINGS[key]
    for row in rows:
        if row["domain"] is None:
            raise SystemExit(f"{row['id']} has no CNCF Domain cell")
    return rows


KS_QUESTION = re.compile(r"^Question (\d+) \| (.+?)\s*$")
KS_PREVIEW = re.compile(r"^Preview Question (\d+)\s*$")


def parse_ks():
    pdf = REPO / KS_PDF
    if not pdf.is_file():
        raise SystemExit(f"missing {pdf}")
    with tempfile.NamedTemporaryFile(suffix=".txt") as handle:
        try:
            subprocess.run(["pdftotext", "-layout", str(pdf), handle.name], check=True)
        except FileNotFoundError:
            raise SystemExit("pdftotext is not on PATH; install poppler")
        text = Path(handle.name).read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        question = KS_QUESTION.match(line)
        preview = KS_PREVIEW.match(line)
        if question:
            number = int(question.group(1))
            rows.append({"id": f"KS-{number:02d}", "source": f"{KS_PDF} § Question {number}"})
        elif preview:
            number = int(preview.group(1))
            rows.append({"id": f"KS-P{number}", "source": f"{KS_PDF} § Preview Question {number}"})
    return rows


def truncate(heading):
    if len(heading) <= HEADING_LIMIT:
        return heading
    return heading[:HEADING_LIMIT].rstrip() + "..."


def cell(text):
    return text.replace("|", "\\|")


def load_map():
    return json.loads(MAP_FILE.read_text(encoding="utf-8"))


def merge(rows, mapping, domain_from_source):
    merged = []
    for row in rows:
        entry = mapping.get(row["id"])
        if entry is None:
            raise SystemExit(f"{row['id']} has no entry in {MAP_FILE.name}")
        if domain_from_source:
            if "domain" in entry:
                raise SystemExit(f"{row['id']}: the source states the domain, remove it from {MAP_FILE.name}")
            domain = row["domain"]
        else:
            domain = entry.get("domain")
        if domain not in DOMAINS:
            raise SystemExit(f"{row['id']}: domain {domain!r} is not one of the five curriculum domains")
        topic = entry.get("topic", "")
        if not topic or not topic.endswith("."):
            raise SystemExit(f"{row['id']}: topic must be one sentence ending with a full stop")
        lab = entry.get("lab", [])
        unknown = set(lab) - LAB_NEEDS
        if unknown:
            raise SystemExit(f"{row['id']}: unknown lab needs {sorted(unknown)}")
        verified = entry.get("verified")
        if verified is not None and not VERSION.match(verified):
            raise SystemExit(f"{row['id']}: verified must be a Kubernetes minor version such as v1.37")
        merged.append(
            {
                "id": row["id"],
                "domain": domain,
                "topic": topic,
                "source": row["source"],
                "lab": ", ".join(lab) if lab else "none",
                "state": f"verified on {verified}" if verified else "unverified",
            }
        )
    return merged


def render_table(rows):
    lines = [
        "| Id | Domain | Topic | Source | Lab needs | State |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(cell(row[key]) for key in ("id", "domain", "topic", "source", "lab", "state"))
            + " |"
        )
    return "\n".join(lines)


def render(sections):
    parts = [
        "# CKAD exercise index",
        "",
        "One row is one exercise, holding its id, its exam domain, a one-sentence topic, "
        "the pointer to the question in its source, what the lab must provide, and its verification state.\\",
        "The three repository sources are git submodules under `practice/sources/`, "
        "and every row points at the commit its submodule pins.\\",
        "The Killer Shell rows point at the results archive under `Study notes/`.\\",
        "`practice/scripts/build-index.py` regenerates this file from the sources and from "
        "`practice/scripts/exercise-map.json`, which holds the hand-written domain, topic and lab needs per id, "
        "and the Kubernetes version each reference solution was verified on.",
        "",
        "An id is the source prefix followed by the exercise's position in that source: "
        "`DGK-<file letter>-<ordinal in that file>`, `BM-<exercise number>`, "
        "`DOJO-<simulation number>-Q<question number>`, and `KS-<question number>` "
        "or `KS-P<preview question number>`.",
        "",
    ]
    for title, rows in sections:
        parts.append(f"## {title}")
        parts.append("")
        parts.append(render_table(rows))
        parts.append("")
    parts.append("## Counts")
    parts.append("")
    total = 0
    for title, rows in sections:
        parts.append(f"- {title}: {len(rows)} rows.")
        total += len(rows)
    parts.append(f"- Total: {total} rows.")
    parts.append("")
    return "\n".join(parts)


def main():
    mapping = load_map()
    parsed = {
        "dgk": parse_dgk(),
        "bm": parse_bm(),
        "dojo": parse_dojo(),
        "ks": parse_ks(),
    }
    sections = []
    seen = set()
    for key, title in SOURCES:
        rows = merge(parsed[key], mapping, domain_from_source=(key == "dojo"))
        seen.update(row["id"] for row in rows)
        sections.append((title, rows))
    stale = sorted(set(mapping) - seen)
    if stale:
        raise SystemExit(f"{MAP_FILE.name} has entries for ids that no source produced: {stale}")
    OUTPUT.write_text(render(sections), encoding="utf-8")
    for title, rows in sections:
        print(f"{title}: {len(rows)} rows", file=sys.stderr)
    print(f"wrote {OUTPUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
