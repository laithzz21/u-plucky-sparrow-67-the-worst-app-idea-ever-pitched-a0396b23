#!/usr/bin/env python3
"""Entry for make.fun bounty u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23:
the worst app idea ever pitched.

The brief: ONE sentence, at most 240 characters, pitching the worst, most
useless app idea imaginable -- a product that sounds real, a founder who
sounds certain, a function nobody needs. The judge wants it specific,
funny, and perfectly pointless.

The pitch: Snoozely, an AI app that predicts exactly how many times you
will hit snooze, then charges $4.99 a month to remind you that you already
knew you would be late. It sounds like a real startup pitch (AI! a
subscription! a named product!), the founder is certain enough to charge
for it, and the function is perfectly pointless: the only thing it tells
you is something you already knew, about a habit you could simply stop.

Prints the one-sentence entry to stdout (terminated by a single newline)
and also writes it to the output directory (``/output/entry.txt`` by
default, or ``$MAKEFUN_OUTPUT`` when set), verifying the written file by
reading it back.

Python 3.13, stdlib only, deterministic: no network, clock, or randomness.
"""

import hashlib
import os
import re
import sys

# The entry: exactly one sentence, 165 characters (limit 240).
ENTRY = (
    "Meet Snoozely, the AI app that predicts exactly how many times you "
    "will hit snooze, then charges $4.99 a month to remind you that you "
    "already knew you would be late."
)

MAX_CHARS = 240

# Fallback pitch, used only if the primary entry ever fails validation
# (for example after a future edit): a shorter version of the same joke,
# same product, same pointless function, still inside every limit. It is
# validated by the same checks before it is ever printed, so the run can
# never silently emit an entry that breaks the brief.
FALLBACK_ENTRY = (
    "Meet Snoozely, the AI app that counts how many times you hit snooze "
    "and charges $4.99 a month to tell you what you already knew."
)

# A sentence terminator is one of . ! ? at the end of the text. The brief
# demands exactly one sentence, so the entry must carry exactly one
# terminator and it must be the last character.
TERMINATOR_RE = re.compile(r"[.!?]$")

# The pitch must sound like a real product: it needs a product name and
# a technology claim (here, AI) so it reads as a startup pitch, not a
# random complaint.
PRODUCT_MARKERS = ("snoozely",)
TECH_MARKERS = ("ai", "artificial intelligence", "machine learning")

# The founder must sound certain: a confident launch verb ("Meet",
# "Introducing", "We built") plus a definite price, so the pitch reads as
# a founder who genuinely believes in the product.
FOUNDER_MARKERS = ("meet ", "introducing", "we built", "we made")
PRICE_RE = re.compile(r"\$\d+(\.\d{2})?")

# The function must be one nobody needs: the app only restates something
# the user already knows ("already knew"), about a trivial habit, and it
# charges for that restatement.
POINTLESS_MARKERS = ("already knew", "already know", "you knew")

# The pointless function must be about a trivial, everyday habit -- here
# hitting snooze -- so the uselessness is concrete, not abstract. A pitch
# about a vague "productivity" feature could accidentally sound useful.
HABIT_MARKERS = ("snooze", "alarm", "nap", "sleep in")

# One sentence capped at 240 characters cannot hold many words; a word
# count far above the expected range would mean the sentence is crammed
# with extra clauses and is no longer a clean single pitch.
MAX_WORDS = 45


def count_sentences(text: str) -> int:
    """Count sentence-ending terminators in the entry.

    A terminator counts only when it is followed by a space or the end of
    the text, so the decimal point in a price such as "$4.99" (period
    followed by a digit) is not miscounted as a sentence end.
    """
    count = 0
    for match in re.finditer(r"[.!?]", text):
        after = text[match.end():]
        if after == "" or after[0] in " \t":
            count += 1
    return count


def validate(text: str) -> None:
    """The entry must be exactly one sentence, at most 240 characters,
    naming a real-sounding product with a confident founder voice and a
    perfectly pointless function. Raises ValueError on any violation so
    the failure is loud, not silent."""
    if not text or text != text.strip():
        raise ValueError("entry must be non-empty with no surrounding whitespace")
    if "\r" in text:
        raise ValueError("entry must use LF line endings only, no CR characters")
    if "\n" in text:
        raise ValueError("entry must be a single line: one sentence, no newlines")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry must be at most {MAX_CHARS} characters, got {len(text)}"
        )
    if len(text) < 40:
        raise ValueError(
            "entry is too short to pitch a product, a founder, and a function"
        )
    words = text.split()
    if len(words) > MAX_WORDS:
        raise ValueError(
            f"entry must be at most {MAX_WORDS} words for one clean sentence, "
            f"got {len(words)}"
        )
    if count_sentences(text) != 1:
        raise ValueError(
            f"entry must be exactly one sentence, "
            f"got {count_sentences(text)} sentence terminators"
        )
    if not TERMINATOR_RE.search(text):
        raise ValueError("entry must end with a sentence terminator")
    lower = text.lower()
    # It must sound like a real product: a named app plus a tech claim.
    if not any(marker in lower for marker in PRODUCT_MARKERS):
        raise ValueError("entry must name the app it is pitching")
    if not any(marker in lower for marker in TECH_MARKERS):
        raise ValueError("entry must sound like a real tech product pitch")
    # The founder must sound certain: a confident launch verb and a price.
    if not any(marker in lower for marker in FOUNDER_MARKERS):
        raise ValueError("entry must open with a confident founder-style pitch")
    if not PRICE_RE.search(text):
        raise ValueError("entry must include a price: the founder charges for it")
    # The function must be perfectly pointless: it only tells the user
    # something they already knew, about a trivial habit.
    if not any(marker in lower for marker in POINTLESS_MARKERS):
        raise ValueError(
            "entry must show the function is pointless: "
            "it only restates what the user already knew"
        )
    if not any(marker in lower for marker in HABIT_MARKERS):
        raise ValueError(
            "entry must name the trivial habit the app is built around "
            "(hitting snooze), so the uselessness is concrete"
        )


def select_entry() -> str:
    """Return the entry to print: the primary pitch when it validates,
    otherwise the fallback pitch (itself validated). The fallback exists
    so a bad edit to ENTRY can never turn a run into a crash or an
    out-of-brief submission; if both fail, the error is raised loudly.
    """
    try:
        validate(ENTRY)
        return ENTRY
    except ValueError as exc:
        print(f"warning: primary entry failed validation: {exc}", file=sys.stderr)
        validate(FALLBACK_ENTRY)
        print("warning: using fallback entry", file=sys.stderr)
        return FALLBACK_ENTRY


def resolve_out_dir() -> str:
    """Return the first writable output directory.

    Tries $MAKEFUN_OUTPUT, then /output, then ./output in turn, probing
    each with a throwaway write; a directory that cannot be created or
    written is skipped instead of failing the run outright.
    """
    requested = os.environ.get("MAKEFUN_OUTPUT") or "/output"
    candidates = [requested, "/output", os.path.join(os.getcwd(), "output")]
    seen: set[str] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write_probe")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    # Last resort: the current directory itself, which must be writable
    # for the process to be running at all.
    return os.getcwd()


def main() -> int:
    entry = select_entry()
    # The stdout write is the entry; it must succeed before anything else.
    # Written explicitly as bytes so the byte count can be verified: the
    # entry is one line terminated by one newline.
    payload = (entry + "\n").encode("utf-8")
    written_bytes = sys.stdout.buffer.write(payload)
    sys.stdout.buffer.flush()
    if written_bytes != len(payload):
        raise RuntimeError(
            f"stdout write incomplete: wrote {written_bytes} of {len(payload)} bytes"
        )
    try:
        out_dir = resolve_out_dir()
        path = os.path.join(out_dir, "entry.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(entry)
            f.write("\n")
        # Verify the written file by reading it back and comparing both
        # the text and its SHA-256 digest against the entry.
        with open(path, "r", encoding="utf-8") as f:
            written = f.read()
        if written != entry + "\n":
            raise RuntimeError("verification failed: written entry does not match")
        expected_hash = hashlib.sha256((entry + "\n").encode("utf-8")).hexdigest()
        actual_hash = hashlib.sha256(written.encode("utf-8")).hexdigest()
        if actual_hash != expected_hash:
            raise RuntimeError("verification failed: SHA-256 mismatch on entry.txt")
    except OSError as exc:
        # File output is a convenience copy only; the printed entry is
        # already out, so a failed write must not fail the run.
        print(f"warning: could not write entry.txt: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
