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

## 2026-09-06 — Chapter 16: CKKS Scale and Level Management in Practice
Verified live, two clean results:
  - Bug 3 (undersized Delta): Delta=2^20 -> max abs error 0.747 on ax^2+bx+c; Delta=2^40 (book default) ->
    1.93e-06. Ratio: 386,747x worse with undersized Delta, ZERO exceptions in either case — confirms the
    book's warning that precision-loss bugs are genuinely silent (decrypts cleanly, just wrong).
  - Bug 2 (level mismatch): tested (x*x*x) + d where d is a fresh 0-level ciphertext vs main path at 2 levels.
    TenSEAL AUTO-ALIGNS the levels silently, giving exact result (3.875 vs expected 3.875, no error/exception).
    This RESOLVES the exercise assigned back in the 2026-09-01 (Ch10) session, where I speculated without
    testing whether TenSEAL errors/auto-aligns/misbehaves — now tested: it auto-aligns. TenSEAL structurally
    eliminates Bug 2 the same way it eliminates Bug 1 (rescale-hiding), which SEAL's explicit API does NOT do
    (would need manual mod_switch_to_inplace).
Taught: the three governing rules; Bug1/2/3 symptom-to-cause mapping; level diagrams as pre-implementation
  verification (the diagram IS the Ch14 depth derivation, read backwards); OpenFHE's FIXEDMANUAL -> FLEXIBLEAUTO
  scaling-technique ladder ("learn on manual, deploy on flexible-auto").
Exercise: both bugs demonstrated with real measured numbers; suggested OpenFHE deliberate-bug reproduction
  (values off by a factor of Delta, ~10^12) as a follow-up once OpenFHE is buildable in this environment.
Asked: one question — where must TenSEAL's auto-alignment logic live relative to SEAL's explicit (non-aligning)
  API, and what would that imply about mixing raw SEAL calls with TenSEAL objects.
Answers: pending.
Weak spots: unmeasured across seventeen sessions.
Revisit next time: today's question + the three consolidated questions from 2026-09-05 (Ch12 EvalSine transfer,
  Ch14 N-bracket sensitivity, Ch8/9 ring dimension n). Next: Ch17 (Performance Profiling and Optimization) —
  closes out Part III's practical-engineering run before Part IV (ML applications) begins.

## 2026-09-07 — Chapter 17: Performance Profiling and Optimization
Part III complete. Most directly research-relevant chapter yet. Verified live: implemented Paterson-Stockmeyer
  polynomial evaluation with explicit multiplicative-depth tracking (a Val wrapper incrementing .lvl on every
  mult, mirroring Ch16's rescale-per-multiply rule), tested at degree 15 against numpy.polyval ground truth:
  naive Horner = 15 sequential levels, Paterson-Stockmeyer = 6 levels, BOTH exactly match true value (0.400815).
  Confirms O(d)->O(log d) depth reduction by actual execution. Noted honestly: my 6 levels doesn't hit the
  book's tighter ~4-5 estimate for this case, likely non-minimal baby-step power scheduling in my construction —
  flagged as an open implementation detail rather than claimed as optimal.
Taught: cost hierarchy (multiply > rotation > encrypt/decrypt > keygen, bootstrap dwarfing all per-call);
  Paterson-Stockmeyer's REFRAME — the real value isn't "faster fixed approximation" but "changes what degree
  is affordable at all" at fixed depth budget, directly reframing how to think about the practical value of
  Parth's own polynomial-approximation research; BSGS and tree-reduction as callbacks to Ch13's already-verified
  TenSEAL behavior; rotation-key over-provisioning (gigabytes from "generate every offset just in case") as the
  dominant memory trap; Intel HEXL (free 2-5x AVX-512 accel, build flag only) and FHERMA as concrete levers.
Exercise: full working Paterson-Stockmeyer implementation with depth tracking in scratchpad; suggested tuning
  block size toward book's tighter estimate, or pushing to d=31/63 to watch the gap widen.
Asked: one question designed to make Parth revise his OWN prior Ch14 answer with new information — given that
  PS makes high-degree affordable at near-constant depth, does that make N-bracket crossings from his research's
  improvements MORE likely (achievable degree so much higher that small gains compound) or LESS likely (PS
  already absorbs most of the degree increase into log-depth, little room left to reduce further)?
Answers: pending.
Weak spots: unmeasured across eighteen sessions.
Revisit next time: today's question. Part III (FHE Engineering) is DONE. Next: Ch18 (The Non-Polynomial
  Barrier), opening Part IV — Privacy-Preserving Machine Learning, where Parth's actual research area begins.

## 2026-09-08 — Chapter 18: The Non-Polynomial Barrier (opens Part IV)
THE chapter Parth's research question comes from. Ran the book's own Artifact 18.A live, exactly as specified
  (N=16384, chain [60]+[35]*8+[60], Delta=2^35, x in linspace(-6,6,16)):
  - Step 1: confirmed hasattr(enc_x, 'relu') == False — structural absence, not a missing convenience method.
  - Step 2: degree-4 least-squares ReLU fit, max abs error in-range [-6,6] = 0.1806 (book: ~1.8e-1, exact match)
  - Step 3: degree-8 fit, max abs error = 0.0880 (book: ~9e-2, exact match). Ratio 2.05x — book's "factor of two,
    not an order of magnitude" confirmed precisely.
  - Out-of-range: degree-8 poly at x=9 (true ReLU=9) -> -64.56 (wrong SIGN and magnitude). At x=-9 (true=0) ->
    -73.56. Observation 18.2 (approximation quality is a statement about an interval, not a function) made
    fully concrete with real numbers, not just cited.
Taught: the structural (CKKS) vs economic (BFV/BGV finite-domain) distinction in why non-polynomial functions
  are unreachable; "matmul isn't the hard part, activations are" as the central misconception to kill; x^2 as
  the one activation CKKS was "made for"; the three crossing strategies (polynomial approx / TFHE-PBS / scheme
  switching) and their one-line tradeoffs — "there is no strategy that avoids paying somewhere"; ReLU's corner
  as the reason doubling degree only bought 2x accuracy, not an order of magnitude.
Exercise: full artifact run live; assigned extending to sigmoid (smooth, no corner) as contrast, with a stated
  prediction (smooth functions should show much better degree-4->degree-8 improvement ratio than ReLU's 2x) for
  Parth to verify himself.
Asked: one question reframing Parth's own research strategy directly — given degree-8's only-2x in-range gain
  despite Paterson-Stockmeyer making its depth cost nearly free (Ch17), is pushing degree higher actually the
  right lever for corner-shaped (ReLU-like) activations, or does the diminishing-returns pattern argue for a
  different approach (smoothing the target, piecewise calibration, accepting Strategy 2/3 for corners)?
Answers: pending.
Weak spots: unmeasured across nineteen sessions.
Revisit next time: today's question. Next: Ch19 (Polynomial Activation Approximation) — almost literally
  Parth's thesis topic; expect this to be the highest-value session yet.

## 2026-09-09 — Chapter 19: Polynomial Activation Approximation (Parth's core thesis topic)
Ran the book's own Artifact 19.A live in full (Chebyshev fits, ReLU/sigmoid/GELU, degrees 4/8/15/27, in-range
  AND out-of-range error on [-8,8]):
  ReLU:    degree4 err=4.61e-01 -> degree27 err=8.48e-02  (5.4x improvement)
  GELU:    degree4 err=3.64e-01 -> degree27 err=2.64e-03  (137.8x improvement)
  sigmoid: degree4 err=1.14e-01 -> degree27 err=2.22e-05  (5118.1x improvement)
  ~950x leverage gap between kinked (ReLU) and smooth-analytic (sigmoid) functions at IDENTICAL degree
  investment. This is a precise, quantitative answer to the question asked in the 2026-09-08 (Ch18) session
  about whether pushing degree is worth it for corner-shaped activations: for ReLU specifically, clearly not —
  research effort has dramatically higher leverage on smooth activations (GELU/sigmoid/tanh/Swish) than on ReLU.
  Also: out-of-range blowup is catastrophic even for BOUNDED sigmoid (3.97 abs error one unit outside [-8,8],
  vs a function whose whole range is [0,1]) — boundedness of phi does not protect against polynomial blowup,
  only staying inside the fit range does.
  Also verified: OpenFHE's real depth table exceeds naive ceil(log2(d+1)) by a CONSTANT 2 levels at every
  published degree bracket (3-5 through 248-495) — not a rough margin, a fixed systematic offset from internal
  scaling overhead. Degree-15 sigmoid costs 6 levels not 4.
Taught: monomial ill-conditioning (condition number ~O((1+sqrt2)^2d)) and why no real pipeline fits monomials
  past toy degree; Chebyshev basis as same-cost/better-conditioned fix; Remez/equioscillation for true L-infinity
  minimax vs L2 least-squares; composite strategies (GELU->sigmoid closed form, composition p_k-o-...-o-p_1 at
  SAME depth as direct high-degree eval but better numerics/convergence shape, x^2 as zero-cost option for
  co-designed architectures); budget depth from OpenFHE's library table, never the formula.
Exercise: full artifact run live, all three functions x four degrees x in/out-of-range; assigned a tanh
  prediction-then-verify extension (predict whether its improvement ratio lands nearer sigmoid's ~5000x or
  GELU's ~140x based on curvature/asymmetry, then check).
Asked: one question pushing further on today's finding — since composition p_k-o-...-o-p_1 costs the SAME
  depth as direct evaluation but has different convergence SHAPE, and ReLU's kink is a step-adjacent target,
  could composition's shape (not its depth) close some of the 950x leverage gap against smooth functions, or
  is the kink fundamentally the same obstacle either way?
Answers: pending.
Weak spots: unmeasured across twenty sessions, though today's content is about as close to direct engagement
  with Parth's actual research as this coaching format can get without his input.
Revisit next time: today's question. Next: Ch20 (Encrypted Inference: Linear Models and Decision Trees) —
  first full-pipeline chapter of Part IV.

## 2026-09-12 — Chapter 20: Encrypted Inference: Linear Models and Decision Trees
NOTE: routine fired 2026-09-10, 09-11, and 09-12 while session was idle; resumed with ONE session covering
  the next chapter rather than replaying three separate days — gap noted here, not repeated three times.
First full end-to-end chapter. Verified live, both artifacts:
  - Full TenSEAL encrypted logistic regression pipeline (N=32768, chain [60]+[40]*10+[60], degree-7 Chebyshev
    sigmoid fit, naive Horner): prediction 0.83077 vs true sigmoid(1.7)=0.84553, abs error 1.48e-02 — exact
    match to book's stated numbers.
  - Trust boundary test: ctx.copy() -> make_context_public() -> decrypt attempt correctly raises
    "ValueError: the current context of the tensor doesn't hold a secret_key" — confirms real enforcement,
    not just a code-layout convention.
  - XGBoost n_bits sweep on real sklearn breast_cancer data (Concrete-ML): n_bits=2->0.937, 4->0.972, 6->0.951,
    8->0.979. NON-MONOTONIC (dips at n_bits=6) — diverges from book's idealized "climbs then plateaus" shape.
    Reported honestly as a genuine empirical finding, not smoothed over. LogisticRegression baseline: 0.951
    (ties exactly with XGB n_bits=6, coincidentally).
Taught: plaintext-multiply-still-costs-a-level trap (skips relin, not rescale); the same degree-7 fit needs
  10 levels via naive Horner vs 3 via OpenFHE's Paterson-Stockmeyer EvalChebyshevFunction — "when CKKS feels
  inexplicably slow, check the polynomial evaluation strategy first"; decision trees/XGBoost belong to TFHE
  because comparison is exactly the LUT primitive PBS evaluates natively; accuracy-privacy-performance triangle,
  no free corner.
Exercise: both artifacts run live with real numbers; assigned completing the book's left-as-exercise
  accuracy-delta loop (threshold decrypted logreg predictions on breast_cancer, compare to plaintext accuracy),
  with a stated prediction (does the ~1.5e-2 error flip any near-0.5 classifications) to verify.
Asked: one question about the non-monotonic XGBoost sweep specifically — real phenomenon for tree quantization
  vs my experiment being flawed, and what's structurally different between quantizing a threshold comparison
  vs a polynomial coefficient.
Answers: pending.
Weak spots: unmeasured across twenty-one sessions.
Revisit next time: today's question. Next: Ch21 (Encrypted Neural Network Inference) — full architectures,
  combining Ch13 packing + Ch17 optimization + Ch19 activation approximation.

## 2026-09-13 — Chapter 21: Encrypted Neural Network Inference
Where Ch13 packing + Ch17 Paterson-Stockmeyer + Ch19 calibrated fitting converge into full architectures.
Verified live:
  - Recomputed Table 21.5's worked depth budget independently against OpenFHE's real degree table (Ch19,
    Fact 19.3), not taken on faith: degree15->6/activation->22 total; degree13->5/activation->19 total;
    degree5->4/activation->16 total. Exact match to book on all three.
  - PROVED (not just cited) BatchNorm folding as an exact algebraic identity: unfolded (linear then separate
    BN) vs folded (single affine W'=gamma*W/sqrt(sigma2+eps), b'=gamma*(b-mu)/sqrt(sigma2+eps)+beta) — max
    abs diff 1.665e-16 (floating point noise only).
  - PROVED argmax(softmax(z)) == argmax(z) across 5 random trials, always exact — confirms the softmax-removal
    shortcut is mathematically exact, not a heuristic that usually works.
Taught: three architecture-adaptation steps (activation replacement per-layer not globally, BatchNorm folding
  as mandatory not optional since CKKS can't do the raw division anyway, softmax->argmax shortcut); CryptoNets'
  x^2/avg-pool conservative 2016 baseline and the field's subsequent relaxation (P-S + bootstrapping + Chebyshev
  calibration arriving together); im2col reducing convolution to the same diagonal-matmul machinery; the KEY
  ratio — at degree 15, activations consume 18 of 22 total levels (~82%), linear layers only 4 — meaning every
  degree reduction in Parth's own fitting research multiplies its savings by activation COUNT in a real network;
  CryptoLab/Niobium hardware partnership as a signal the field expects hardware, not just algorithms, for
  transformer-scale encrypted inference.
Exercise: both algebraic proofs run live; assigned extending the depth table to a 7-activation (5-conv+2-FC)
  network at degree 15 vs 5, with a stated prediction that activation dominance INCREASES with network depth
  (linear layers stay flat at 1 level each, activation cost scales with count).
Asked: one question connecting the 82% activation-dominance ratio to whether CKKS bootstrapping (resetting
  depth mid-network) changes the RELATIVE value of Parth's polynomial-approximation research, or just changes
  how often the activation-depth cost is paid rather than how much per occurrence.
Answers: pending.
Weak spots: unmeasured across twenty-two sessions.
Revisit next time: today's question. Next: Ch22 (Quantization-Aware Training for FHE) — the TFHE-side
  counterpart to this chapter's CKKS-side depth budgeting.
