# FHE study log

The daily Routine (`Daily FHE fundamentals`, 14:27 UTC) reads this file as its **only**
memory of previous sessions. Append one entry per session, newest at the bottom, and push.
If the push fails the day is lost — see the note at the end.

Format for each entry:

```
## YYYY-MM-DD — Chapter N: <title>
Exercise assigned: <tier>/<file>
Answers: <what was asked, what was right, what was wrong>
Weak spots: <specific, e.g. "confuses rescaling with modulus switching">
Revisit next time: <or "nothing">
```

---

## 2026-08-18 — log seeded, no session content

Created because the file was missing and every prior session had therefore begun at
Chapter 1 with no record. Nothing is known about which chapters have actually been
covered between 2026-08-07 and 2026-08-18, so the next session should **ask Parth what
he has already covered** rather than assuming Chapter 1, and record the answer here.

Reading order for reference: `fhe-book.html` has 28 chapters plus Appendices A–D.
Exercise pairing lives in `fhe-foundations/`: `tier0_math/ex01-05` for Chapters 1–5,
`tier1_ckks/ex06-09` for CKKS basics and depth limits, `tier2_engineering/ex10-12` for
OpenFHE level management and rotations, `tier3_ml/ex13-16` for encrypted ML and Chebyshev
activations, `tier4_fherma/ex17-18` for challenge preparation.

---

### If the push fails

This file is only useful if it is pushed. A session that cannot push must not end
quietly: it should say so plainly and send the updated log back through the chat so the
day's record survives outside the repository.
