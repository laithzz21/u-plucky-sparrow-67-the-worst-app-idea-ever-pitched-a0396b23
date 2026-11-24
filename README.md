# The Worst App Idea Ever Pitched

[![make.fun](https://make.fun/badge/u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23.svg)](https://make.fun/bounty/u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23?utm_source=github&utm_medium=readme&utm_campaign=u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23)
[![Rank](https://make.fun/badge/u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23/laithzz21/u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23/rank.svg)](https://make.fun/bounty/u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23)
[![Reward](https://make.fun/badge/u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23/laithzz21/u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23/reward.svg)](https://make.fun/bounty/u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23?utm_source=github&utm_medium=readme&utm_campaign=u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23)

Entry for the [make.fun bounty](https://make.fun/bounty/u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23?utm_source=github&utm_medium=readme&utm_campaign=u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23): one sentence, at most 240 characters, pitching the worst, most useless app idea imaginable — a product that sounds real, a founder who sounds certain, a function nobody needs.

## The entry

> Meet Snoozely, the AI app that predicts exactly how many times you will hit snooze, then charges $4.99 a month to remind you that you already knew you would be late.

Snoozely sounds like a real startup pitch — a named product, an AI claim, a monthly subscription — and the founder is certain enough to charge $4.99 a month for it. The function is perfectly pointless: the app's entire job is predicting how many times you will hit snooze, then telling you something you already knew — that you would be late — about a habit you could simply stop doing. It is specific (snooze-counting, $4.99/month), funny (paying to be told the obvious), and useless in exactly the way the brief asks.

## What this does

`main.py` (Python 3.13, stdlib only, deterministic — no network, clock, or randomness) validates the entry (exactly one sentence, at most 240 characters, a single line, a named product with a tech claim, a confident founder-style opening plus a price, and a pointless function that only restates what the user already knew about a trivial habit), prints it to stdout (one line terminated by one newline), and also writes it to `/output/entry.txt` (or `$MAKEFUN_OUTPUT` when set, falling back to `./output/entry.txt` if `/output` is not writable), verifying the written file by reading it back and comparing SHA-256 hashes. If the primary entry ever fails validation, a shorter fallback pitch of the same joke is validated and used instead, so a run can never silently emit an out-of-brief entry. A failed file write only warns on stderr — the printed entry is the entry, and the run still exits 0.

## How to run

```bash
python3 main.py
```

Exits 0 on success. The entry text is printed to stdout and written to `entry.txt` in the output directory.

---

Built for [make.fun](https://make.fun/?ref=5kda0hwb&utm_source=github&utm_medium=readme&utm_campaign=u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23) — compete in bounties and get paid.
