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

## 2026-08-21 — Chapter 1: Modular Arithmetic and Algebraic Structures
Exercise assigned: tier0_math/ex01_modular_arith.py (reference solutions present; task = blank and re-derive ntt(), watch the psi=2 rejection test and the schoolbook-convolution cross-check)
Answers: pending — three checking questions posed (RNS vs comparison; why omega^(N/2)=-1 is needed in the butterfly; discrete Gaussian vs bounded-uniform noise). Parth had not yet answered when the day's Routine fired.
Weak spots: unknown yet — first recorded session. Parth confirmed starting from Chapter 1 (no reliable coverage from the lost 2026-08-07..18 sessions).
Revisit next time: open with his answers to the three Ch1 questions before starting Chapter 2 (Polynomial Rings and Cyclotomic Fields).

## 2026-08-22 — Chapter 2: Polynomial Rings and Cyclotomic Fields
Exercise assigned: tier0_math/ex02_ring_poly.py (re-derive poly_mul_ntt; watch the negacyclic-wrap test and the random NTT-vs-schoolbook cross-check)
Answers: pending — 3 new questions (NTT domain vs plaintext slots; canonical vs coefficient norm; psi-twist sign mechanism). Ch1's 3 questions still open, carried forward.
Weak spots: none observable yet (no answers received in two sessions).
Revisit next time: all six open questions (Ch1 Q1-3, Ch2 Q1-3) before starting Ch3 (Lattices and Hard Problems).

## 2026-08-23 — Chapter 3: Lattices and Hard Problems
Exercise assigned: implement LLL from scratch (book Artifact 3.1) — verify reduced norms ~33.3/59.7 and det 1957 on bad basis [(1731,512),(1264,375)]. Note: ex03_lwe.py is Ch4 material, deferred to next session.
Answers: pending — day 3, no answers received. Nine questions open (Ch1 Q1-3, Ch2 Q1-3, Ch3 Q1-3).
Weak spots: none observable (no responses yet).
Revisit next time: if still no answers, pause new material and run a consolidated Ch1-3 review instead of teaching Ch4.

## 2026-08-24 — Consolidated review of Ch1-3 (no new chapter)
Exercise assigned: none new; invited pushing partial ex01/ex02/LLL work for code review.
Answers: pending, day 4. Nine open questions compressed into a six-item quick-reply check in chat.
Weak spots: engagement is the risk; no misconception observable yet.
Revisit next time: the six-item check. Resume Ch4 (LWE, ex03_lwe.py) once any answers arrive; if silence persists two more sessions, propose restructuring the format (weekly quiz / exercises-only / teach-only) before continuing.

## 2026-08-25 — Chapter 4: Learning With Errors
Exercise assigned: tier0_math/ex03_lwe.py (re-derive encrypt_lwe/decrypt_lwe; watch the 100/100 safe-regime test and the 39% broken-regime demo; try the wrong number-line decryption once deliberately)
Answers: pending — day 5 of silence. Open: six-item Ch1-3 consolidated check + Ch4 Q1-3.
Weak spots: none observable (no responses yet).
Revisit next time: all open items. If next session is also silent, propose format restructuring (weekly quiz / exercises-only / teach-only) before teaching Ch5 (Ring-LWE).

## 2026-08-26 — Catch-up review of Ch1-4 (Parth chose "catch up now, then continue")
Format decision: Parth selected a live interactive catch-up over restructuring. Daily chapter format resumes after this.
Covered: worked model answers to all nine open questions (Ch1-3 six-item check + Ch4 Q1-3), delivered in chat.
Correction made: my Ch4 Q3 wrongly called ex03's 39% "coin-flipping". ex03 uses t=4, so chance is 25%, not 50%.
  Simulated at q=251, Delta=62: sigma=2 ->100%, 20 ->88%, 40 ->57%, 62 ->38.7% (matches observed), 125 ->25.6%, 500 ->25.2%.
Verified numerically: canonical vs coefficient norm for a=1+X+X^2+X^3 at N=4 — ||a||_inf=1, ||sigma(a)||_inf=2.613,
  a*a coeff norm 4 (= N, hits expansion bound) vs canonical 6.828 = 2.613^2 (submultiplicative with constant 1).
Weak spots: still unmeasured — answers were supplied by me, not produced by Parth. Next session should spot-check
  retention with one or two quick questions before teaching, rather than assuming Ch1-4 is consolidated.
Revisit next time: start Ch5 (Ring-LWE) with a brief retention check on the psi-twist sign and on alpha=sigma/q.

## 2026-08-27 — Chapter 5: Ring-LWE and the Path to Practicality
Exercise assigned: tier0_math/ex04_rlwe.py (re-derive encrypt_rlwe/decrypt_rlwe; watch fresh noise 3 -> 18 after addition;
  also read Artifact 5.1's he_mul for the exact-integer tensor product before t/q rescale)
Verified numerically: f(5)=x^2+x mod 8 = 6; depth formula d ~ [log(q/2t)-log B]/log(tN) gives 3.5 / 12.0 / 25.3
  at log2 q = 60 / 200 / 438 (N=2^12/2^13/2^14, t=8, B=10) — consistent with "real deployments reach depth 20+".
Asked: two retention checks (A: psi^N = -1 as source of negacyclic sign; B: which of q=2^27 vs 2^54 at n=1024 is
  more secure and what the other buys) plus Ch5 Q1-3 (lost independence -> ideal-lattice assumption; why the t/q
  rescale leaves one delta and makes C ~ tN independent of q; why raising q is a poor route to depth 30).
Answers: pending.
Weak spots: still unmeasured — Ch1-4 was delivered as model answers, never tested against Parth's own reasoning.
  The retention checks A/B are the first real signal; prioritize them over the Ch5 questions if his time is short.
Revisit next time: A/B first, then Ch5 Q1-3. Next chapter: Ch6 (The Arc of Homomorphic Encryption), opening Part II.

## 2026-08-28 — Chapter 6: The Arc of Homomorphic Encryption
No ring-arithmetic exercise pairs with this chapter (historical/conceptual). Assigned a written comparison
  (Paillier vs Ch5 RLWE SHE noise walls, per book's Artifact 6.1) — doubles as a second attempt at Ch5 Q1.
Housekeeping: installed tenseal in this environment; verified tier1_ckks/ex06_first_encrypt.py runs 4/4 —
  ready for when the daily sessions reach real CKKS material (~Ch10).
Answers: pending. Open backlog: retention checks A (psi^N sign) / B (alpha=sigma/q), Ch5 Q1-3, Ch6 Q1-3.
Weak spots: unmeasured across seven sessions — the accumulating backlog is itself the primary signal now.
Revisit next time: full backlog above. If next session is also silent despite the 2026-08-26 "catch up now,
  continue daily" decision, raise the format question again explicitly rather than silently repeating the pattern.

## 2026-08-29 — Chapter 7: The Noise Barrier
Exercise: ran tier1_ckks/ex09_depth_limit.py live (5/5) — depth-1 CKKS context squares once, second squaring
  raises "ValueError: scale out of bounds" (the noise-budget-crosses-zero moment, concretely). Also pointed to
  the book's own Artifact 7.1 (instruments Ch5's toy RLWE scheme, logs noise budget bit-by-bit across levels).
Verified numerically: log2(tn) = log2(1024*4096) = 22 exactly, matching Result 7.1's per-level cost claim.
Format adjustment (own initiative, not confirmed by Parth): eight sessions with no answers. Reduced today to
  ONE focused checking question instead of the usual three, and stopped re-listing the full accumulated backlog
  verbatim each session (it was burying the current question). Backlog still exists but isn't restated in full.
Answers: pending.
Weak spots: unmeasured across eight sessions.
Revisit next time: the one Ch7 question takes priority over older backlog. Next chapter: Ch8 (BFV).

## 2026-08-30 — Chapter 8: BFV — Exact Arithmetic, Scale-Invariant
No dedicated exercise file pairs with Ch8/BFV in fhe-foundations (SEAL not installed in this environment).
Built and ran a from-scratch toy BFV (N=16, q=12289, t=8) verifying: fresh encrypt/decrypt round-trip on all
  8 messages; tensor->rescale-and-round->decrypt gives exactly 5*3=7 mod 8; noise budget 7.00 bits fresh ->
  1.88 bits after one multiplication (pre-relinearization) — confirms Result 8.1's shape at toy scale.
  Deliberately did NOT implement relinearization (Definition 8.5), which makes the point concrete: chaining
  a second multiplication is literally undefined without it (no degree-3 decrypt path).
Asked: one question (why ring dimension n is simultaneously the price of security and the driver of a larger
  per-multiplication noise cost O(tn) — same design choice or unrelated?).
Answers: pending.
Weak spots: unmeasured.
Revisit next time: today's question; Ch1-7 backlog held but not restated in full. Next: Ch9 (BGV), direct
  point-by-point comparison to today's BFV derivation (modulus switching vs scale-invariance).

## 2026-08-31 — Chapter 9: BGV — Exact Arithmetic, Modulus Switching
No dedicated exercise file for BGV either (OpenFHE not installed). Built a toy BGV implementation structurally
  parallel to Ch8's BFV toy (same N=16, t=8) for direct A/B comparison. Verified: fresh round-trip on all 8
  messages under m+te relation; homomorphic 5*3=7 mod 8 with NO rescale-and-round step (contrast BFV, which
  needs one); modulus switching q=2^60 -> q'=2^38 (22-bit drop) preserves message, noise budget 53.42 -> 34.00
  bits (consistent with Prop 9.1's "budget falls by ~log2(kappa) bits, permanently").
Taught: why BGV's pre-switch t^2*e*e' term survives (no rescale to kill it) making growth proportional to
  current noise E, vs BFV's constant-factor tn growth — the actual reason modulus switching is MANDATORY for
  BGV but optional for BFV, not just a different API for the same math.
Asked: one question — at what point (what condition on E relative to t/n/q) does BGV's proportional growth
  actually diverge from BFV's constant growth; toy's tiny error bound (+-1) made the two look similar (53.4->49.4,
  only 4 bits) since t^2*E*E' was negligible at that noise scale.
Answers: pending.
Weak spots: unmeasured.
Revisit next time: today's question + Ch8's question (why n is both security's price and noise-cost's driver) —
  these pair naturally. Next: Ch10 (CKKS) — most directly relevant to Parth's stated research focus
  (depth-optimal polynomial approximation of activations).

## 2026-09-01 — Chapter 10: CKKS — Approximate Arithmetic, the ML Workhorse
Most directly relevant chapter yet to Parth's stated research (depth-optimal polynomial approximation of
  activations). Verified numerically rather than just asserted:
  - canonical embedding slot pairing: zeta^15 = conj(zeta^1) exactly at N=8, confirming slot 0 pairs with N-1
  - book's own Artifact 10.1 (ax^2+bx+c, N=8192, chain [60,40,40,60], Delta=2^40) reproduced exactly:
    max abs error 1.93e-6, mean abs error 5.39e-7 (within book's stated 1e-3..1e-5 "expect" range, actually better)
  - deliberately exceeded a 2-level TenSEAL context's depth budget (3rd squaring) -> "ValueError: scale out of
    bounds", same error class as Ch7's ex09_depth_limit.py, now from CKKS's dual-purpose rescale specifically
Exercise: ran tier1_ckks/ex07_dot_product.py (4/4, error 1.64e-6) and ex08_polynomial.py (6/6) live.
  Assigned Parth a hands-on task: construct the depth-imbalanced-branch bug pattern himself (x*x*x at 2 levels
  vs a fresh constant at 0 levels, try adding directly) and observe whether TenSEAL errors, auto-aligns, or
  misbehaves silently.
Asked: one question — what decryption's final step does DIFFERENTLY to noise in CKKS vs BFV/BGV (not "how much"
  noise), and why that specific difference makes a wrong CKKS answer look plausible rather than obviously broken.
Answers: pending.
Weak spots: unmeasured across eleven sessions.
Revisit next time: today's question + Ch8/9's paired question on ring dimension n (still open). Next: Ch11
  (TFHE and Programmable Bootstrapping) — flag as a genuine architectural detour from the CKKS track.

## 2026-09-02 — Chapter 11: TFHE and Programmable Bootstrapping
Genuine architectural detour from the BFV/BGV/CKKS lineage, flagged as such. Installed concrete-ml v1.9.0 fresh
  in this environment (worked cleanly) and ran the book's own Artifact 11.1 for real, not just described:
  XGBoost (n_estimators=20, max_depth=3, n_bits=6) on sklearn breast-cancer data. compile() took 5.8s.
  clear-quantized acc 97.37%, simulate acc 97.37% (match), FHE-execute acc 100% on n=5 (~4s/sample),
  simulate vs FHE-execute predictions IDENTICAL on the tested slice — confirms book's claim that TFHE/PBS is
  exact w.r.t. the quantized model (not approximate like CKKS); all accuracy loss vs full-precision XGBoost
  comes from quantization, not FHE evaluation.
Taught: programmable bootstrapping evaluates arbitrary LUTs (not just polynomials) — the capability CKKS
  structurally lacks, which is *why* polynomial-approximation research (Parth's focus) is necessary for CKKS
  specifically; TFHE's compile-time bit-width failure vs CKKS's silent scale-mismatch failure, contrasted
  directly against last session's Ch10 content; the CKKS-vs-TFHE-vs-mixed workload decision procedure.
Asked: one question connecting TFHE's LUT capability to Parth's own research value proposition directly —
  is activation evaluation a "summing many products" or "many small decisions" problem in TFHE's terms, and
  what does his polynomial-approximation work let a CKKS pipeline avoid that isn't already solved by just
  switching to TFHE for that one piece.
Answers: pending.
Weak spots: unmeasured across twelve sessions.
Revisit next time: today's question + Ch8/9 (ring dimension n) + Ch10 (CKKS vs BFV/BGV noise-handling) — all
  still open. Next: Ch12 (Bootstrapping — turning leveled HE into fully HE), completes the CKKS/TFHE contrast.

## 2026-09-03 — Chapter 12: Bootstrapping — Turning Leveled HE into Fully HE
Attempted `pip install openfhe` (matches book's v1.5.1) to run Artifact 12.1 for real — package metadata
  installs but the compiled C++ extension (openfhe.openfhe) is non-functional in this environment. Flagged
  honestly rather than faking output. Substituted two direct verifications instead:
  - Artifact 12.1's own depth-budget arithmetic: levelsAvailableAfterBootstrap=10, approxBootstrapDepth=8,
    levelBudget=[4,4] -> total parameter depth 26, of which bootstrap OVERHEAD is 16 levels (62%), exceeding
    the 10-level (38%) useful-circuit budget. Bootstrap cost is not abstract — it structurally outweighs the
    circuit it's meant to serve at these example parameters.
  - Confirmed live on TenSEAL: no bootstrap-shaped method exists anywhere on context or ciphertext objects;
    a 3rd multiplication past a 2-level budget fails permanently ("scale out of bounds") — Section 12.7's
    "SEAL/TenSEAL has no escape hatch, for any scheme" claim, verified rather than just quoted.
Taught: Gentry's theorem precisely; bootstrappability vs circular security (Ch6 callback); CKKS's
  ModRaise/CoeffToSlot/EvalSine-EvalCos/SlotToCoeff pipeline and why modular reduction forces a sine/cosine
  polynomial approximation — explicitly named as structurally the SAME KIND of problem as Parth's own research
  (polynomial approximation of activations), just applied to sin/cos instead of ReLU/GELU/sigmoid; CKKS-vs-TFHE
  bootstrap cost table; bootstrap-vs-deepen decision checklist; library support matrix.
Asked: one question — does Parth's polynomial-approximation research (if it yields better degree/accuracy
  tradeoffs in general) transfer to improving CKKS's own EvalSine/EvalCos bootstrap step, or is the domain/
  accuracy-metric different enough to block reuse? Points him at a concrete, high-value connection between his
  research and the chapter just taught.
Answers: pending.
Weak spots: unmeasured across thirteen sessions.
Revisit next time: today's question + Ch8/9 (ring dimension n) + Ch10 (CKKS vs BFV/BGV noise handling) +
  Ch11 (TFHE-vs-CKKS value prop for his research) — all still open. Next: Ch13 (Packing, SIMD, Rotations,
  Relinearization, and Key Switching) — completes Part II.

## 2026-09-04 — Chapter 13: Packing, SIMD, Rotations, Relinearization, Key Switching
Part II complete. Verified live with TenSEAL (already installed):
  - .matmul() on a 16x16 random W: initially got max error 10.8 assuming W@x convention — WRONG. TenSEAL's
    matmul uses x^T@W (row-vector convention). Corrected: max abs error 1.42e-06, 43.3ms. Genuinely useful
    self-caught bug, presented to Parth as a debugging-habit lesson (verify library matmul convention on a
    tiny known case before trusting it on real weights).
  - .sum() (TenSEAL's hidden rotate-and-sum): decrypted -9.256611 vs true sum -9.256610; confirmed the
    defining broadcast property (every slot holds the total, not just slot 0).
Taught: SIMD packing as the primary throughput lever; row/column-major vs diagonal (Halevi-Shoup) packing for
  matvec, O(n) vs O(m log n) rotations; BSGS reducing to O(sqrt(n)); Galois automorphisms as rotation's
  mechanism and the runtime-not-compile-time Galois-key trap (OpenFHE requires naming offsets in advance,
  TenSEAL/SEAL default to power-of-two only); relinearization corrected as a COST choice not a correctness
  requirement (SEAL's own basics example decrypts un-relinearized size-3 ciphertexts); key switching as the
  single primitive unifying relinearization (s^2->s) and rotation's correction (s(X^k)->s); gadget-decomposition
  digit count coupling to the RNS chain; FHERMA/polycircuit flagged explicitly as directly relevant to Parth's
  stated FHERMA prep.
Exercise: ran both verifications live; assigned extension — repeat with a rectangular (non-square) W.
Asked: one question on whether "more depth" (bigger modulus chain) and "rotation/relin cost" are actually
  independent knobs, given Section 13.6.1's digit-count/RNS-chain coupling.
Answers: pending.
Weak spots: unmeasured across fourteen sessions. Full backlog (Ch8/9 ring dimension n; Ch10 CKKS vs BFV/BGV
  noise handling; Ch11 TFHE-vs-CKKS research value; Ch12 EvalSine/EvalCos transfer; Ch13 depth/rotation coupling)
  all still open — none blocking, all carried forward per standing instructions.
Revisit next time: Part II is done. Next: Ch14 (Parameter Selection and Security Standards), opening Part III —
  FHE Engineering, the most directly practical material yet for FHERMA prep.

## 2026-09-04 (2nd session same day, routine re-fired) — Chapter 14: Parameter Selection and Security Standards
Verified live rather than just cited: fed TenSEAL/SEAL the book's own depth-5 example chain (320 bits total:
  [60,40,40,40,40,40,60]) at N=8192 -> hard REJECTION ("ValueError: encryption parameters are not set correctly"),
  matching book's claim that N=2^13 maxes at 218 bits (insufficient for 320). Same chain at N=16384 -> builds
  fine, matching book's claim of 438-bit budget (sufficient). SEAL enforces the HomomorphicEncryption.org table
  internally, at least for sufficiently-bad cases — genuinely useful thing to know for real deployments.
Verified arithmetic: both worked examples exactly — depth-5 chain sums to 320 bits (5 usable levels), 3-layer
  NN artifact chain sums to 400 bits (7 usable levels); table's N-doubling -> log2(q)-budget-doubling pattern
  confirmed at ratio 2.00-2.02 across all five steps (2^10 through 2^15).
Taught: parameters as a JOINT security/functionality solve (not independent knobs); the tradeoff triangle;
  the special-prime-is-never-a-compute-level trap and the q0-is-the-END-not-the-start direction trap; full
  CKKS parameter derivation recipe; RNS/CRT as why the API is a prime-bit-size list (triple duty: log2(q),
  level count, scale trajectory); lattice-estimator for non-standard secret distributions (flagged as relevant
  to Ch12's sparse-secret CKKS bootstrapping).
Exercise: ran the security-boundary test live on the depth-5 example; assigned reproducing it on the book's
  3-layer NN example (N=16384 chain should build, same chain at N=8192 should reject).
Asked: one question connecting Parth's own research directly to today's material — does shaving one level off
  activation-polynomial degree (3->2) actually move a real deployment down a full N bracket, or usually just
  add slack within the same bracket; what property of total circuit depth determines which case applies.
Answers: pending.
Weak spots: unmeasured across fifteen sessions. Full Ch8-13 backlog still open, not restated verbatim.
Revisit next time: today's question. Next: Ch15 (The Library Landscape) — likely a lighter survey chapter;
  good natural point for a consolidated backlog check-in if silence continues.

## 2026-09-05 — Chapter 15: The Library Landscape
Survey chapter, light session as flagged last time. Verified live: TenSEAL's 5-line dot-product artifact
  (poly_modulus_degree=8192, chain [60,40,40,60], vectors [1,2,3,4].[5,6,7,8]) -> decrypted 70.00000891 vs
  exact 70. Matches book's claim exactly.
Taught: library map by scheme/bootstrap/niche; OpenFHE bootstraps CKKS+FHEW/TFHE only (NOT BGV/BFV, which
  stay leveled even there); scheme-switching as the practical escape hatch when polynomial approximation
  genuinely can't reach required accuracy for one function (switch that piece to TFHE); Enable(...) and
  accumulator-overflow gotchas; TenSEAL/SEAL/OpenFHE three-way verbosity comparison on the same dot product.
Did the consolidated check-in flagged in the 2026-09-04 log entry: compressed the growing backlog down to the
  THREE most research-relevant open questions instead of re-listing everything (Ch12 EvalSine/EvalCos transfer;
  Ch14 N-bracket sensitivity to shaving activation-polynomial degree; Ch8/9 ring dimension n's dual role as
  security's price and noise-cost's driver). Full question history remains in this log's earlier entries,
  not discarded, just not repeated verbatim each session.
Answers: pending. Sixteen sessions running with no responses.
Weak spots: unmeasured.
Revisit next time: the three consolidated questions above, whenever Parth engages. Next: Ch16 (CKKS Scale and
  Level Management in Practice) — the hands-on payoff of Ch14's parameter-selection theory.
