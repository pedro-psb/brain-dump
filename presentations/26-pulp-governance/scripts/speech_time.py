#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["rich>=13", "watchfiles>=1"]
# ///
"""Estimate spoken duration from the speech sections in a LaTeX draft."""

from __future__ import annotations

import argparse
import math
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from rich.console import Console
from rich.text import Text
from watchfiles import watch


SECTION_RE = re.compile(
    r"^\s*(\d+)\+(\d+)\+\d+\s+\(\d+/\d+/\d+/\d+\)\s+"
    r"(Section|Subsection):\s*(.*?)\s*$"
)
EXCLUDED_SECTIONS = {"revision", "references"}
WORD_RE = re.compile(r"\b[\w]+(?:['’][\w]+)*\b", re.UNICODE)
TEXCOUNT_OPTIONS = Path(__file__).with_name("texcount.opt")


@dataclass
class SectionCount:
    title: str
    words: int
    children: list[SectionCount] = field(default_factory=list)

    def total_words(self) -> int:
        return self.words + sum(child.total_words() for child in self.children)


def read_section_counts(texcount_output: str) -> list[SectionCount]:
    """Return speech word counts, grouped by section and subsection."""
    sections: list[SectionCount] = []
    current_section = None
    for line in texcount_output.splitlines():
        match = SECTION_RE.match(line)
        if not match:
            continue
        body_words, _header_words, level, title = match.groups()
        title = title.strip()
        if level == "Section":
            if title.casefold() in EXCLUDED_SECTIONS:
                current_section = None
                continue
            current_section = SectionCount(title, int(body_words))
            sections.append(current_section)
        elif current_section is not None:
            current_section.children.append(SectionCount(title, int(body_words)))
    return sections


def format_duration(total_seconds: float) -> str:
    total_seconds = round(total_seconds)
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes}:{seconds:02d}"


def render_timing_line(
    console: Console, seconds: float, title: str, *, depth: int = 0
) -> None:
    if depth == 0:
        duration_style = title_style = "bold bright_white"
    elif depth == 1:
        duration_style = title_style = "bold bright_blue"
    else:
        duration_style = title_style = "cyan"
    text = Text()
    text.append(f"{format_duration(seconds):>4}  {'  ' * depth}", style=duration_style)
    text.append(title, style=title_style)
    console.print(text)


def render_tree(
    console: Console,
    node: SectionCount,
    seconds_per_word: float,
    *,
    depth: int = 0,
) -> None:
    render_timing_line(
        console,
        node.total_words() * seconds_per_word,
        node.title,
        depth=depth,
    )
    for child in node.children:
        render_tree(console, child, seconds_per_word, depth=depth + 1)


def count_switches(nodes: list[SectionCount]) -> int:
    """Count transitions between siblings at every hierarchy level."""
    return max(0, len(nodes) - 1) + sum(
        count_switches(node.children) for node in nodes
    )


def parse_seconds(value: str) -> float:
    """Parse a positive duration in seconds."""
    if not value.strip():
        raise argparse.ArgumentTypeError(
            "reference time is required; provide seconds, e.g. 32"
        )
    try:
        elapsed = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "enter the reference duration in seconds (for example, 32)"
        ) from error

    if not math.isfinite(elapsed) or elapsed <= 0:
        raise argparse.ArgumentTypeError(
            "reference time must be a finite number greater than zero"
        )
    return elapsed


def parse_switch_cost(value: str) -> float:
    """Parse a non-negative switching cost in seconds."""
    try:
        cost = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("switch cost must be given in seconds") from error
    if not math.isfinite(cost) or cost < 0:
        raise argparse.ArgumentTypeError(
            "switch cost must be a finite number greater than or equal to zero"
        )
    return cost


def parse_watch(value: str) -> bool:
    if value == "0":
        return False
    if value == "1":
        return True
    raise argparse.ArgumentTypeError("watch must be 0 or 1")


def count_reference_words(path: Path) -> int:
    return len(WORD_RE.findall(path.read_text(encoding="utf-8")))


def render_estimate(args: argparse.Namespace, console: Console) -> bool:
    result = subprocess.run(
        [
            args.texcount,
            f"-opt={TEXCOUNT_OPTIONS}",
            "-sub=subsection",
            str(args.source),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        console.print(f"TeXcount failed: {detail}", style="bold red")
        return False

    sections = read_section_counts(result.stdout)
    if not sections:
        console.print("No speech sections found", style="bold red")
        return False

    reference_words = count_reference_words(args.reference_speech)
    if reference_words == 0:
        console.print("Reference speech contains no words", style="bold red")
        return False

    presentation = SectionCount("Presentation", 0, sections)
    total_words = presentation.total_words()
    words_per_minute = reference_words * 60 / args.reference_time
    seconds_per_word = args.reference_time / reference_words
    header = Text("Speech time estimate", style="bold bright_white")
    header.append(f" ({total_words} words)", style="bold bright_cyan")
    console.print(header)
    console.print("Excluded: abstract, Revision, References", style="dim")
    console.print(
        f"Calibration: {reference_words} words in "
        f"{format_duration(args.reference_time)} "
        f"({words_per_minute:.1f} words per minute)",
        style="dim",
    )
    render_tree(console, presentation, seconds_per_word)

    switch_count = count_switches(sections)
    total_seconds = total_words * seconds_per_word
    total_seconds += switch_count * args.switch_cost_seconds
    console.print(Text("---", style="dim"))
    console.print(
        Text.assemble(
            (
                f"{format_duration(total_seconds):>4}  ",
                "bold yellow",
            ),
            ("Total (with overhead estimate)", "bold yellow"),
        )
    )
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        usage=(
            "make speech-time REFERENCE_SECONDS=<seconds> "
            "[SWITCH_COST_SECONDS=5] [WATCH=0|1]"
        ),
        description=(
            "Estimate speech time from draft.tex. The abstract, Revision, and "
            "References are excluded. Calibrate the estimate with a timed "
            "reference speech."
        )
    )
    parser.add_argument(
        "source", nargs="?", type=Path, default=Path("draft.tex"),
        help="LaTeX draft to count (default: draft.tex)",
    )
    parser.add_argument(
        "--reference-time", required=True, type=parse_seconds,
        help="time spent delivering the reference speech, in seconds",
    )
    parser.add_argument(
        "--reference-speech", type=Path,
        default=Path("references/reference-speech.txt"),
        help="plain-text calibration speech (default: %(default)s)",
    )
    parser.add_argument(
        "--switch-cost-seconds", type=parse_switch_cost, default=5.0,
        help="cost for each section/subsection transition in seconds (default: 5)",
    )
    parser.add_argument(
        "--force-color", action="store_true",
        help="emit terminal colors even when stdout is not a terminal",
    )
    parser.add_argument(
        "--watch", type=parse_watch, default=False, metavar="0|1",
        help="recalculate when the draft or reference speech changes",
    )
    parser.add_argument(
        "--texcount", default="texcount",
        help="TeXcount executable (default: texcount)",
    )
    args = parser.parse_args()

    if not args.source.is_file():
        parser.error(f"source file not found: {args.source}")
    if not args.reference_speech.is_file():
        parser.error(f"reference speech not found: {args.reference_speech}")
    if not shutil.which(args.texcount):
        print(
            f"error: cannot find TeXcount executable: {args.texcount}",
            file=sys.stderr,
        )
        return 2

    console = Console(force_terminal=True if args.force_color else None)
    console.clear()
    if not render_estimate(args, console):
        return 2

    if not args.watch:
        return 0

    def show_watching_message() -> None:
        console.print(
            "Watching draft and reference speech; press Ctrl-C to stop.",
            style="dim",
        )

    show_watching_message()
    watched_files = {
        args.source.resolve(),
        args.reference_speech.resolve(),
    }
    watch_roots = sorted({path.parent for path in watched_files})
    try:
        for changes in watch(*watch_roots, debounce=500):
            changed_files = {
                Path(path).resolve()
                for _change, path in changes
            }
            if not watched_files.intersection(changed_files):
                continue
            console.clear()
            render_estimate(args, console)
            show_watching_message()
    except KeyboardInterrupt:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
