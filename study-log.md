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

## 2026-09-14 — Chapter 22: Quantization-Aware Training for FHE
TFHE-side counterpart to Ch21's CKKS depth budgeting. Verified live:
  - Accumulator bit-width formula (Fact 22.2, ceil(log2(k))+8 for 4-bit weights/activations): crosses the
    16-bit ceiling exactly at fan-in k~800 (18 bits needed), matching the book's "a few hundred input
    features... routinely pushes past 16" claim precisely rather than just quoting it. k=256->16 bits (edge),
    k=800/1024->18 bits, k=4096->20 bits.
  - Built a from-scratch straight-through estimator (custom torch.autograd.Function: forward = real Delta*round(x/Delta),
    backward = identity grad) and ran real gradient descent through a genuinely-4-bit-rounding linear layer.
    First attempt (lr=0.5) diverged — reported honestly, not hidden — corrected to lr=0.05: loss fell
    4.67 -> 0.0084 monotonically over 6 steps, gradients nonzero throughout, despite REAL rounding applied
    every single forward pass. Also printed the raw staircase Q(w) values directly to show true dQ/dw is
    genuinely zero almost everywhere (w=-1.0->Q=-1.333, w=-0.75->Q=-0.667, flat in between).
Taught: TFHE forces quantization on EVERY graph value not just I/O; naive post-training quantization fails
  for the same compounding-error reason as Ch19's polynomial approximation; Concrete-ML+Brevitas division of
  labor (Brevitas does QAT/STE, Concrete-ML compiles); accumulator overflow as the dominant real compile
  failure (arithmetic, not implementation detail); CKKS-vs-TFHE pipeline comparison table; scheme choice as a
  TRAINING-time decision (retrofitting across schemes costs accuracy vs deciding early).
Exercise: both verifications run live; explicitly skipped the book's full CIFAR-10+Brevitas artifact (dataset
  download + real training time not suited to this daily-cadence environment) in favor of verifying the two
  conceptually load-bearing facts (accumulator arithmetic, STE mechanism) directly — flagged as a deliberate
  scope choice, not silently omitted.
Asked: one question connecting today's fan-in-driven accumulator cost to yesterday's Ch21 activation-depth-
  domination finding — does TFHE accumulator risk scale with network WIDTH the same way CKKS activation depth
  scales with network DEPTH (same structural root, different currency) or are they genuinely unrelated
  bottlenecks that happen to both hurt?
Answers: pending.
Weak spots: unmeasured across twenty-three sessions.
Revisit next time: today's question. Next: Ch23 (Federated Learning and Homomorphic Encryption) — shifts
  from single-model inference to multi-party settings.

## 2026-09-16 — Chapter 23: Federated Learning and Homomorphic Encryption
NOTE: routine fired 2026-09-15 and 09-16 while session was idle; resumed with ONE session rather than
  replaying both days — gap noted, not repeated.
Verified live: full 2-client FedAvg secure-aggregation pipeline in TenSEAL (N=8192, chain [60,40,60] — only
  1 inner level needed since aggregation never multiplies). Encrypted aggregate matched TRUE plaintext FedAvg
  weighted average to max abs error 2.1e-11 — confirms Observation 23.1 (aggregation is pure depth-0 addition)
  essentially exactly. Also ran the book's own suggested security exercise: server attempts to decrypt an
  individual client's update directly -> correctly refused ("ValueError: ...doesn't hold a secret_key") —
  concrete demonstration of what HE protects here (individual updates) vs what it does NOT (see below).
Taught: FL and HE solve adjacent-not-identical problems; secure aggregation needs only additive homomorphism
  (why Paillier suffices, CKKS chosen mainly for infrastructure reuse not necessity); the chapter's real
  payload — HE-protected aggregation defeats a curious SERVER seeing individual updates, but says NOTHING
  about gradient inversion (mitigated only by cohort size, not cryptography) or membership inference against
  the final aggregate MODEL (leak is in the output artifact itself, HE never touches this); DP-SGD as the
  necessary complement — HE protects the channel, DP protects the information content, not substitutes;
  encrypted model evaluation / PSI / threshold HE as the broader design space; OpenMined PySyft/Datasites/NAIRR.
Exercise: both artifacts run live; assigned scaling the simulation to 20 clients and reasoning about how
  gradient-inversion resistance changes with cohort size (cryptography stays identical, privacy property does not).
Asked: one question directly raised by my own 2-client demo — is there a minimum cohort size below which HE
  secure aggregation provides NO meaningful practical protection at all, even with perfect cryptography (what
  can a server infer from just the sum of 2 known-n updates)?
Answers: pending.
Weak spots: unmeasured across twenty-four sessions.
Revisit next time: today's question. Next: Ch24 (Encrypted Training: The Frontier) — training rather than
  inference under encryption, the hardest remaining problem in the book.

## 2026-09-17 — Chapter 24: Encrypted Training: The Frontier (Part IV complete)
Verified live, the capstone demo of this closing chapter:
  - Recomputed Sec 24.3's per-iteration depth arithmetic exactly: 1(Xw)+5(OpenFHE P-S degree-7 sigmoid table)
    +1(backward matmul)+1(update rescale, lr=0.1 is non-integer so NOT free)=8 levels/iter, x10=80 total. Match.
  - Built and ran a REAL scalar encrypted logistic regression training loop in TenSEAL (naive Horner, no P-S
    available in TenSEAL), deliberately budgeted for exactly 1 iteration's depth (11 levels via Horner:
    1+8+1+1). Iteration 0: SUCCESS, encrypted w=0.0600 exactly matching plaintext w=0.0600. Iteration 1: FAILED,
    "ValueError: scale out of bounds" — Observation 24.1 (depth accumulates monotonically, no bootstrap =
    training cannot continue) reproduced as an EXECUTED failure, not just described. First attempt hit an
    unrelated packing-shape bug (vector-size mismatch from per-row gradient accumulation); simplified to scalar
    (n=1 feature) logistic regression to isolate the actual point (depth exhaustion) from packing mechanics —
    noted honestly as a debugging step, not hidden.
Taught: training multiplies inference's FIXED depth by iteration count (the whole chapter in one sentence);
  backprop roughly doubles per-iteration depth without introducing new non-polynomial barriers (polynomials
  differentiate to polynomials); three honestly-costed approaches (full-bootstrap/theoretically complete but
  prohibitive; hybrid — the field's actual pragmatic answer, exactly Ch22's LoRA pattern; shallow-bounded — the
  one corner solidly practical today); Concrete-ML's ACTUAL scope is narrower than marketing — fit_encrypted
  works only for logistic-regression-shaped SGDClassifier, NOT neural nets/forests/arbitrary PyTorch, and the
  v1.8 hybrid LLM feature is NOT an exception (still frozen-base-encrypted-inference + plaintext adapter
  training); open problems named precisely (training-time BN needs encrypted rsqrt, no clean shortcut like
  inference folding; encrypted attention backward; full transformer training not close to feasible).
Exercise: full failure-mode demo run live; assigned widening to a 2-iteration budget (22 levels) and confirming
  the failure point moves to iteration 2 exactly as predicted.
Asked: one question probing whether Paterson-Stockmeyer (8 vs 11 levels/iter) changes WHICH training approach
  becomes viable for deeper networks, or only extends approach (c)'s iteration ceiling — i.e. does the T-multiplier
  in Observation 24.1 dominate regardless of per-activation cost.
Answers: pending.
Weak spots: unmeasured across twenty-five sessions.
Revisit next time: today's question. PART IV (Privacy-Preserving Machine Learning) IS COMPLETE. Next: Ch25
  (Multi-Party Homomorphic Encryption), opening Part V — Advanced Topics and the Frontier.

## 2026-09-18 — Chapter 25: Multi-Party Homomorphic Encryption (opens Part V)
OpenFHE's actual Multiparty* API not runnable in this environment (same C++ build limitation as prior
  sessions) — verified the two underlying mathematical claims directly instead of describing the skeleton
  uncritically:
  - Simulated full-threshold (N=5-of-5) additive secret sharing: shares sum to true secret exactly (82=82).
    A coalition of N-1=4 parties (missing one share) is consistent with ALL 97 possible secret values with
    EQUAL probability — genuine information-theoretic zero-knowledge, not just "hard to guess." Demonstrates
    Definition 25.1's security claim directly rather than asserting it.
  - Combinatorially verified Property 25.1's MKHE cost scaling: k+1 ciphertext components, addition cost k+1
    (linear), multiplication cost (k+1)^2 (quadratic, from full cross-terms before relinearization-across-keys).
    k=2->10: addition grew 3.67x, multiplication grew 13.44x — matches O(k) vs O(k^2) exactly. This is the
    concrete combinatorial reason MKHE tops out around a handful of parties while threshold FHE's evaluation
    cost stays entirely flat in N.
Taught: threshold FHE (one shared key, evaluation completely untouched, ALL Part II-IV optimizations carry
  over unchanged — only keygen/decryption differ) vs MKHE (independent keys, no advance agreement, cost grows
  with distinct keys touched); noise flooding/smudging (2^40-2^80x ciphertext noise) as a security-critical,
  easy-to-miss parameter in hand-rolled threshold decryption; proxy re-encryption as a DISTINCT narrower
  primitive (moves a ciphertext between single-owner keys, does NOT enable joint computation); trust-model
  decision rule — threshold for standing federations with known membership, MKHE for ad hoc/session-based
  collaboration; OpenFHE (mature threshold) vs Lattigo (deepest multiparty feature set, WASM-friendly,
  collective bootstrapping).
Exercise: both simulations run live with exact numerical confirmation; assigned extending to genuine Shamir
  t-of-N (not just full N-of-N) secret sharing via polynomial interpolation.
Asked: one question connecting today's "threshold evaluation cost flat in N" property back to Ch23's FedAvg
  depth-0 aggregation — does THRESHOLD DECRYPTION itself (not evaluation) scale with participant count, or
  is a threshold-FHE FedAvg genuinely free to scale to hundreds of hospitals the way MKHE could never be?
Answers: pending.
Weak spots: unmeasured across twenty-six sessions.
Revisit next time: today's question. Next: Ch26 (Scheme Switching and Hybrid Computation).

## 2026-09-19 — Chapter 26: Scheme Switching and Hybrid Computation
Closes the CKKS<->TFHE thread forward-referenced since Ch11. Quantified Rule of Thumb 26.1 with an explicit
  crossover cost model rather than leaving it qualitative, using order-of-magnitude figures already established
  in this course (Ch11's 1-10ms PBS latency range, Ch17's "10-100x a single multiply" rule applied to a
  degree-15 Chebyshev activation ~25ms packed): switching_cost(n) = n*(pbs_ms + extraction_overhead),
  ckks_cost(n) = flat ~25ms regardless of n (packed). Crossover at n ~= 7.1 active slots — switching cheaper
  below, CKKS-polynomial cheaper above (n=1:3.5 vs 25ms switching wins; n=8:28 vs 25ms CKKS-poly wins; n=32:
  112 vs 25ms CKKS-poly wins decisively). Explicitly flagged as illustrative order-of-magnitude reasoning, not
  a measured benchmark, matching the book's own hedging style for unverified latency claims.
Taught: why CKKS and TFHE are complementary (bounded-by-degree approximation error vs exact-regardless-of-
  sharpness PBS, directly connecting to Ch18/19's ReLU-vs-sigmoid ~950x leverage gap finding); the five-step
  OpenFHE pipeline (slot extraction -> EvalCKKStoFHEW -> FHEW EvalFunc/PBS -> EvalFHEWtoCKKS -> repacking);
  v1.4+ ConvertRLWEToCKKS/ConvertCKKSToRLWE for functional bootstrapping and EvalFastRotation; the sequential
  slot-extraction bottleneck as THE open problem (no packed/SIMD way to hand n values to FHEW's bootstrap at
  once, unlike CKKS's one-op-per-n-slots) — batched vs selective switching as the two unresolved research
  directions, neither closing the gap yet.
Exercise: crossover model run live; assigned re-running under different PBS-latency (GPU ~1ms) and polynomial-
  degree assumptions with a stated prediction (faster PBS pushes crossover UP, cheaper CKKS poly pushes it
  DOWN — the two levers pull the threshold in opposite directions).
Asked: one question connecting directly to Parth's own research — does better polynomial approximation (his
  work) push the switching/CKKS-poly crossover DOWN, shrinking switching's addressable territory, and was
  switching ever actually competing with his approach for smooth functions, or is its real competition confined
  to genuine kinks/discontinuities his techniques structurally can't help regardless?
Answers: pending.
Weak spots: unmeasured across twenty-seven sessions.
Revisit next time: today's question. Next: Ch27 (FHE for Computer Vision, NLP, and Large Language Models) —
  domain applications, Part V continues.

## 2026-09-20 — Chapter 27: FHE for CV, NLP, and LLMs
ENVIRONMENT NOTE: fresh container this session (repo and Python packages both gone). Re-cloned repo via
  add_repo/register_repo_root flow, reinstalled tenseal (now 0.3.18, was 0.3.16) and concrete-ml, verified
  both import correctly before proceeding. Same recovery procedure as the original session setup.
Verified live:
  - CryptoNets throughput/latency: 250s / 4096-image batch = 61.04 ms/image amortized, exact match to book's
    "~60ms" claim. Confirmed the throughput-vs-latency gap is structural to SIMD packing, not a 2016 artifact.
  - Built Artifact 27.A's exact softmax strategy (polynomial exp + Newton-Raphson reciprocal, NO division
    primitive anywhere). FIRST ATTEMPT FAILED HONESTLY: fit exp(z) on R=10 with degree-10 Chebyshev -> max
    error 0.15, NEGATIVE probabilities in output. Diagnosed: exp(10)/exp(-10) ~= 485 million dynamic range,
    untrackable by any bounded-degree polynomial over that wide a domain — a sharper instance of Ch18
    Observation 18.2 (calibrate the fitting range) than seen before, since exp's exponential growth makes
    bad-range mistakes catastrophic rather than gradual. FIXED: recalibrated to R=4 (realistic post-sqrt(d_k)-
    scaling attention-logit magnitude), same degree -> max error 1.1e-05, all-positive, sums to 0.99998.
  - Newton-Raphson reciprocal (x_{n+1}=x_n*(2-d*x_n)) verified converging QUADRATICALLY in isolation:
    iters 0-5 error 6.85e-02 -> 3.42e-02 -> 8.56e-03 -> 5.35e-04 -> 2.09e-06 -> 3.19e-11.
Taught: the CryptoNets throughput/latency gap as permanent to SIMD-packed FHE; the three transformer-specific
  obstacles (softmax's exp+division, layer norm's 1/sqrt, depth x sequentiality in autoregressive generation
  compounding per-token); the honest capability-vs-roadmap gap (small models published/shipped today, hybrid
  architectures production-shipped today, full frontier LLM encrypted end-to-end still roadmap); explicit
  warning about Zama's "500-1000 TPS" being confidential BLOCKCHAIN transactions, not LLM tokens/sec — three
  different metrics routinely conflated; walked through Artifact 27.A's full encrypted-transformer-classifier
  design (CKKS primary + scheme-switched layer-norm rsqrt only, per Ch26's cost model).
Exercise: both softmax pieces run live, INCLUDING the honest failure-then-diagnosis-then-fix rather than a
  clean first try; assigned implementing the analogous Newton-Raphson inverse-square-root for layer norm
  (x_{n+1}=x_n*(1.5-0.5*d*x_n^2)) and verifying similarly fast convergence.
Asked: one question connecting my own R-calibration mistake directly to Parth's research — does calibration
  discipline differ meaningfully between bounded functions (sigmoid/tanh) and unbounded fast-growing ones
  (exp), or is "measure empirical range" always sufficient regardless; what reasoning tool from Ch18-19 alone
  would have caught the R=10 mistake before running any code.
Answers: pending.
Weak spots: unmeasured across twenty-eight sessions.
Revisit next time: today's question. Next: Ch28 (Hardware Acceleration, Standardization, and Open Problems) —
  closing chapter of the main text before the appendices.

## 2026-09-21 — Chapter 28: Hardware Acceleration, Standardization, and Open Problems
Carried over from Ch27's assigned exercise (Newton-Raphson inverse-sqrt for layer norm), run before
  starting today's chapter:
  - First attempt used seed x0=1/d over a wide test range d in [0.1,50] -> FAILED to converge quadratically
    (error crept down only linearly, 0.217->0.024 over 5 iters). Diagnosed: the rsqrt Newton basin of
    convergence requires x0*sqrt(d) in (0, sqrt(3)); x0=1/d violates this for d<0.33.
  - Second attempt "fixed" with a single global constant seed over the SAME wide range -> catastrophic
    divergence (error exploded past 1e116 by iter 5) — the rsqrt basin is far narrower than the reciprocal
    iteration's, so one seed cannot cover a 500x dynamic range the way it could for exp/reciprocal.
  - Correct fix: recognized layer-norm variance is not naturally as wide-ranging as an arbitrary softmax
    logit range — restricted to a realistic post-normalization band d in [0.5,2.0], single constant seed
    (geometric mean) -> clean quadratic convergence, error 0.49 -> 1.0e-10 over 5 iterations.
  - This is a stronger, self-discovered instance of the same calibration lesson from Ch27: rsqrt's
    convergence basin is narrower than reciprocal's, so "measure the empirical range" is necessary but for
    rsqrt specifically the range ALSO has to be narrow enough for one global seed to work, which reciprocal
    Newton-Raphson tolerates much better.
Chapter 28 is a landscape/survey chapter, structurally different from the rest of the book — most claims
  (company figures, dollar amounts, conference dates) are explicitly tagged Verify/Likely by the book itself,
  meaning they are snapshot business facts as of mid-2026, not derivable/checkable by computation the way
  Parts I-IV's math is. No python3 verification was possible or appropriate here; taught the chapter's
  actual content and structure instead of running code.
Taught: DARPA DPRIVE's explicit "within 10x of unencrypted" target and three performers' reported kernel
  speedups (Intel HERACLES 1,074x-5,547x, Duality TREBUCHET, SRI CraterLake-lineage) — three-to-four-orders-
  of-magnitude speedups now demonstrated in silicon/near-silicon, but on FHE-internal kernels (NTT, modmul,
  key-switching), not necessarily end-to-end application latency; three hardware tiers (photonic/Optalysys,
  ASIC/Niobium+Cornami, GPU+vector/HEXL+FIDESlib); compiler efforts (Google HEIR, Zama Concrete v2.10)
  attacking engineering cost rather than raw speed; standardization via HomomorphicEncryption.org's Security
  Standard v1.1 underpinning every library's parameter tables referenced since Ch6/Ch17; the critical epistemic
  tool of the chapter — three maturity tiers (production deployment, enterprise pilot, funding/roadmap
  announcement) and why conflating them is the single most common calibration error in FHE industry commentary;
  the six open problems (bootstrapping cost, encrypted training, batch scheme switching, FHE-friendly
  architectures, FHE+MPC+ZKP composition, compiler auto-optimization) and Artifact 28.A's feasibility ranking
  of the top three on a 2-3yr horizon.
Exercise: mapped Parth's own research (depth-optimal polynomial approximation of activations) onto Artifact
  28.A's open-problems table myself as a worked example, since no code applies here: it sits primarily under
  "FHE-friendly architectures" (designing around what FHE evaluates cheaply, rather than approximating
  ReLU/softmax after the fact) with a secondary connection to bootstrapping cost reduction (fewer/lower-degree
  polynomial terms -> shallower circuits -> less bootstrapping pressure, tying back to Ch17's Paterson-
  Stockmeyer depth argument and Ch19's approximation theory).
Asked: (1) of the six open problems, which would a genuinely depth-optimal activation-approximation result
  move the needle on most directly, and does it change the Artifact 28.A feasibility rating for any of the
  three ranked problems; (2) the chapter's three-tier maturity framework (production/pilot/roadmap) — is there
  an analogous three-tier distinction worth applying to research claims themselves (a proven bound, a
  numerically-verified-but-unproven claim, a conjectured-but-untested claim), and where would Parth currently
  place his own depth-optimality result on that scale; (3) is there a natural FHERMA challenge that maps onto
  Artifact 28.A's #1-ranked problem (batch scheme switching) as a testable near-term project.
Answers: pending.
Weak spots: unmeasured across twenty-nine sessions.
Revisit next time: today's three questions. Next: Appendix A (Notation and Prerequisites) — main text (Ch1-28)
  now complete; entering the appendices, first session to judge how much teaching-style treatment they warrant.

## 2026-09-22 — Appendix A: Notation and Mathematical Prerequisites
First appendix session. Judgment call: Appendix A is a genuine reference (symbol table + probability/linear-
  algebra/complexity-theory background used throughout Parts I-V), not new content, so treated it as a lighter
  consolidation-and-verify session rather than a full chapter lecture — read the actual appendix text as
  required, but taught by connecting each piece to where it was already used across Ch1-28 rather than
  introducing it as new material.
Verified live (three checks, one per subsection):
  - A.2 discrete Gaussian tail bound P(|X|>t*sigma) ~ e^{-t^2/2}: computed true Gaussian tail vs the bound for
    t=1..6. Bound holds as a valid upper bound throughout (ratio true/bound shrinks from 0.52 at t=1 to 0.13 at
    t=6) -- confirms the "concentrates sharply, noise stays below threshold except with negligible probability"
    claim underlying every noise-budget argument since Ch7.
  - A.3 centered representative convention: naive x%q on a small negative value (x=-3, q=97) gives 94 (looks
    LARGE, would falsely trip a noise-growth bound); centered representative in [-q/2,q/2) correctly recovers
    -3. Concrete demonstration of why the book's convention choice isn't cosmetic -- an implementation using
    naive Python-style mod throughout would misjudge noise growth.
  - A.4 negligible vs non-negligible crossover: at the book's standard lambda=128, 1/lambda^100 (1.9e-211) is
    actually SMALLER than negl(128)=2^-128 (2.9e-39) -- i.e. negl has NOT yet overtaken a degree-100
    polynomial bound at the standard security parameter. Found the actual crossover (where 2^-lambda first
    drops below 1/lambda^100 for all larger lambda) at lambda=997, far past 128. Correct and useful
    illustration that "negligible" is an asymptotic, eventually-true statement (Definition A.2's "there exists
    lambda_0"), not an assertion that automatically holds at any specific practical lambda for arbitrary
    polynomial degree.
Taught: the symbol table as a cross-reference to notation used since Ch1 (N, q, t, R_q, chi, Delta, L/ell,
  lambda); A.2's Gaussian-tail-to-noise-budget connection (Ch7); A.3's CRT double-duty (plaintext batching,
  Ch2/Ch10; RNS ciphertext modulus, Ch4) as "the single most load-bearing piece of algebra in the book" per
  the text itself, and the centered-representative convention as the reason "small stays small" through every
  noise-growth argument; A.4's PPT/negligible/advantage formal vocabulary underlying every IND-CPA reduction
  since Part I, with the concrete crossover computation above as a corrective to reading "negligible" as a
  loose qualifier.
Exercise: none newly assigned -- A.3's CRT/RNS mechanics were already exercised directly in earlier sessions
  (Ch1, Ch4); this session's three verification scripts stand in as the appendix's own "exercise."
Asked: (1) does the negl(128) vs 1/lambda^100 crossover result change how Parth would read a security proof
  that reduces to "advantage is negligible" without stating an explicit lambda_0 -- should a careful reader
  always ask what lambda_0 a given reduction actually needs; (2) the centered-representative bug pattern (naive
  mod silently inflating a small negative noise term) -- has Parth's own FHERMA/CKKS code been audited for this
  specific class of representation bug, given TenSEAL/OpenFHE both handle it internally but any of his own
  from-scratch toy implementations across earlier sessions would not have; (3) still-open from Ch28: which of
  the six open problems his depth-optimal-approximation work moves most directly, carried forward unanswered.
Answers: pending.
Weak spots: unmeasured across thirty sessions.
Revisit next time: today's three questions, plus Ch28's three carried-forward questions (still unanswered).
  Next: Appendix B (Installation and Environment Setup) -- likely an even lighter session than today's, since
  it's setup instructions rather than conceptual content; will assess and probably fold B+C+D (Installation,
  Code Index, Further Reading) into a single short closing session rather than three more daily slots, given
  none of them carry new teachable ideas the way A did.

## 2026-09-23 — Appendices B, C, D: Installation, Code Index, Sources — MAIN TEXT + APPENDICES COMPLETE
Folded B+C+D into one closing session as flagged last time -- none carry new conceptual content (setup
  instructions, artifact index, bibliography), so treated as a single wrap-up rather than three more daily
  slots.
Verified live against this environment's actually-installed (newer-than-pinned) versions, directly testing
  the book's own closing claim ("API surfaces move faster than any book, verify against current docs"):
  - B.3 TenSEAL: book pins v0.3.16, this environment has v0.3.18. Ran the book's exact hello-world (CKKS
    context, v+v, decrypt) verbatim -> [2.0000000028, 4.0000000054, 5.9999999990], correct despite the two
    minor-version gap. Matches Appendix C.3's specific claim that TenSEAL's Python bindings are more stable
    across versions than OpenFHE's C++ surface.
  - B.4 Concrete ML: book pins v1.8, this environment has v1.9.0. Confirmed the exact documented footgun:
    model.compile(X) returns a bare concrete.fhe.Circuit with NO .predict() method
    ("'Circuit' object has no attribute 'predict'", reproduced verbatim) -- the caller must call
    model.predict(X, fhe='execute') on the ORIGINAL model object, not the compile() return value. Confirmed
    correct and still true two minor versions past the pin.
Taught: B's version-pinning discipline and the specific per-library friction points (OpenFHE has NO official
  Docker image despite guides implying otherwise -- direct instance of the book's own "verify company/tooling
  claims" ethic turned inward on itself; SEAL's HEXL linking gotcha; Lattigo's v4->v5->v6 import-path churn);
  C's artifact index by Part and the three build conventions (SKELETON C++ = illustrative not drop-in, Python
  artifacts = directly runnable, design-document artifacts = intentionally not code, e.g. 27.A); D's source
  list, with two standouts flagged as directly useful beyond citation-list value: (1) Ko's arXiv beginner
  textbook unifies LWE/RLWE/GLWE/GLev/GGSW under one $(A_0,...,A_{k-1},B)$ form with $B=\sum A_iS_i+\Delta M+E$,
  which reframes this book's Part II "four separate schemes" presentation as one construction at different
  parameter choices; (2) Ko's explicit note that BOTH encryption sign conventions ($B=+\sum A_iS_i+...$ vs
  $B=-\sum A_iS_i+...$) are in live use across the literature, proven equivalent -- flagged as directly
  relevant to Parth given the real convention-mismatch bug hit firsthand in the Ch13 session (TenSEAL's x^T@W
  vs assumed W@x), same failure mode one level up the stack (sign convention vs multiplication-order
  convention) -- worth checking explicitly the next time a formula from a paper doesn't match this book's or a
  library's output.
Exercise: the two live version-drift verifications above stood in as this closing session's exercise, directly
  exercising Appendix D.3's own instruction ("How to use these: for what to actually type, the library
  documentation, always").
Asked: (1) given Ko's GLWE unification, does reframing Part II's four schemes as one construction change how
  Parth would explain his own depth-optimal-approximation result's scheme-independence (or lack thereof) --
  does the polynomial-approximation result depend on CKKS specifically or transfer to the GLWE frame generally;
  (2) the sign-convention warning -- worth an explicit audit pass over any of Parth's own from-scratch formulas
  against whichever convention his primary reference paper uses, given the Ch13 near-miss was a structurally
  identical class of bug; (3) STRUCTURAL, not carried from a specific chapter: the entire main text (Ch1-28)
  and all four appendices are now complete after 32 sessions -- proposing the daily slot pivot from "next
  chapter" to either (a) FHERMA challenge practice applying the material directly, (b) a spaced-repetition pass
  revisiting the weakest/most error-prone sessions (Ch13's convention bug, Ch18-19's calibration-range
  mistakes, Ch24's depth-exhaustion demo), or (c) close focus on the depth-optimal-approximation research
  question itself using the book's Part III/IV toolkit -- Parth's call, and absent an answer, next session
  will default to (a) FHERMA practice as the most concrete, since it's this book's own D.3 recommendation for
  "research directions... open engineering problems with measurable scoring."
Answers: pending.
Weak spots: unmeasured across thirty-one sessions (zero of ~35+ questions answered across the full curriculum
  to date).
Revisit next time: the structural pivot question above takes priority; also still carrying Ch28's open-problem
  question and Appendix A's crossover/audit questions if useful. CURRICULUM STATUS: main text and appendices
  complete. Next session defaults to FHERMA challenge practice (tier4_fherma exercises in fhe-foundations/)
  absent a redirect from Parth.

## 2026-09-24 — FHERMA Practice: ex18 Activation Optimization + fherma_config Depth Budgeting
Default path taken absent a redirect from Parth (proposed last session): pivoted the daily slot from "next
  chapter" (book is complete) to FHERMA challenge practice, starting with tier4_fherma/ex18 and
  fherma_config.py -- the exact workflow this book's own D.3 flags for "research directions... open
  engineering problems with measurable scoring," and squarely inside Parth's depth-optimal-approximation focus.
Ran live and verified:
  - ex18_activation_challenge.py: 7/7 checks pass. Sigmoid[-8,8]@0.05 -> degree 7 (error 0.0296); ReLU[-5,5]@0.3
    -> degree 6 (error 0.2166); GELU[-5,5]@0.1 -> degree 6 (error 0.0901). Noted the search log's error is NOT
    monotonically decreasing in degree (deg 3->0.116, deg 4->0.133 WORSE, deg 5->0.062, deg 6->0.069 WORSE
    again, then monotone from 7 on) -- a real Chebyshev-interpolation-vs-parity artifact, not a bug; worth
    remembering that a "first degree that passes" search can be mildly lucky/unlucky depending on exactly
    where the threshold falls relative to a local bump.
  - fherma_config.py: 16/16 checks pass. Confirmed OpenFHE's real EvalChebyshevFunction depth table
    (CHEBYSHEV_DEPTH) against the naive ceil(log2(d+1)) formula: degree 7 costs 5 levels (formula says 3,
    understating by 2); degree 15 costs 6 (formula says 4). Table is a step function: (5,4),(13,5),(27,6)...
    meaning e.g. EVERY degree from 6 through 13 costs exactly the same 5 multiplicative levels.
  - MAIN FINDING (built and verified myself, not in the original exercise): ex18's stated objective is
    "minimize degree subject to accuracy," but the real FHE cost is DEPTH, and degree->depth is a many-to-one
    step function -- so minimizing degree is not the same objective as minimizing depth, and stopping at the
    first passing degree leaves accuracy on the table for free. Concretely: sigmoid's degree-7 pick costs
    depth 5 and gets error 0.0296, but degree 13 costs the IDENTICAL depth 5 and gets error 0.00296 -- a ~10x
    accuracy improvement at ZERO additional multiplicative depth, simply by searching to the top of the depth
    plateau rather than stopping at the first passing degree. Verified the same free win for ReLU and GELU
    (both jump degree 6 -> degree 12 within the same depth-5 plateau). Wrote and ran a corrected
    optimize_activation_depth_correct() implementing "minimize depth, then maximize accuracy within that
    depth's plateau" as the two-phase search, confirmed against all three activations.
Taught: FHERMA's challenge structure and scoring axes (accuracy vs performance/depth); the ex18 capstone
  workflow (Chebyshev at increasing degree, stop at threshold); why depth, not degree, is the real FHE cost
  (ties directly to Ch17's Paterson-Stockmeyer material); the plateau-exploitation insight above as a concrete,
  actionable refinement to how Parth's own depth-optimal-approximation work should frame its objective
  function -- "minimize degree" and "minimize depth" are NOT interchangeable once OpenFHE's real (non-injective,
  step-function) degree->depth cost is used instead of the textbook ceil(log2(d+1)) formula.
Exercise: built and verified the corrected two-phase optimizer myself (see MAIN FINDING above) since Parth
  hasn't been answering; this is the natural next exercise for tier4_fherma if he wants to extend ex18 for
  real, alongside fherma_config's plaintext-multiply and ring-selection gotchas (a plaintext multiply costs a
  level; forgetting the HYBRID key-switching auxiliary modulus P predicts one ring dimension too small).
Asked: (1) does Parth's own depth-optimal-approximation research already optimize against a real per-library
  depth table (OpenFHE's step function, or SEAL/TenSEAL's equivalent) or against the smooth
  ceil(log2(degree+1)) idealization -- if the latter, the plateau-exploitation finding above may be directly
  applicable free accuracy in his own results; (2) is the non-monotonic Chebyshev error-vs-degree pattern
  (worse at some even degrees than the preceding odd one) something his approximation-theory background
  expects generically, or specific to interpolation-vs-least-squares/parity effects for this class of function;
  (3) still open from Ch28/Appendix A: which open problem his work moves most directly, and the GLWE-framing
  question from the closing session.
Answers: pending.
Weak spots: unmeasured across thirty-two sessions (zero of ~38+ questions answered to date).
Revisit next time: today's plateau-exploitation question is the highest-value one to get an answer on, given
  direct relevance to Parth's actual research. Next: continue FHERMA practice track -- likely ex14 (Chebyshev/
  Remez, explicitly the prerequisite tier4 flags for activation challenges) if not already solid, or move to
  submission/ (the real OpenFHE C++ contract) to see the CLI/config.json workflow end to end.

## 2026-09-25 — FHERMA Practice: ex14 Chebyshev Fundamentals + a from-scratch Remez implementation
Continued the FHERMA track per last session's plan. Ran ex14_poly_activation.py first (5/5 pass, sigmoid/ReLU
  degree-vs-error table reproduces exactly the same numbers as ex18's search log, confirming the two exercises
  use the same interpolation-based Chebyshev method under the hood).
Gap noticed: tier4's own README explicitly recommends Remez ("gives the true minimax polynomial, which is
  optimal... start with Chebyshev, try Remez if you need to shave off one more degree") but NO exercise or
  file anywhere in the repo actually implements Remez (grep -ril "remez" across the whole repo: zero hits).
  Given this is squarely Parth's stated research area (depth-optimal polynomial approximation), treated this
  as today's real content: built a minimal Remez exchange algorithm from scratch rather than teaching from an
  exercise that doesn't exist.
Built and verified: a Remez exchange implementation (degree+2 reference points, alternation equations solved
  exactly, extrema re-located on a fine grid each iteration, 20 iterations) for sigmoid on [-8,8], compared
  against a LEAST-SQUARES Chebyshev-series truncation baseline (numpy chebfit, not the same construction as
  ex14/ex18's interpolation-at-n-nodes method -- flagged explicitly as a different baseline, not a re-measurement
  of yesterday's exact numbers, to avoid conflating two different approximation methods both loosely called
  "Chebyshev").
  - degree 7: Chebyshev-truncation err 0.031906, Remez err 0.029024 -> Remez wins by 1.10x
  - degree 13: Chebyshev-truncation err 0.004068, Remez err 0.001892 -> Remez wins by 2.15x
  Both results consistent with the standard approximation-theory fact that Chebyshev-series truncation is
  within a factor of roughly (2/pi)ln(degree) of the true minimax error, so Remez's advantage should widen
  (slowly) with degree -- which is exactly the direction observed (1.10x at deg 7, 2.15x at deg 13).
Taught: the interpolation-vs-least-squares-vs-minimax distinction inside "Chebyshev approximation" as a
  category (ex14/ex18 interpolate at exactly n=degree+1 Chebyshev nodes, which is fast and simple but not
  provably minimax; a least-squares truncated series is a different construction again; Remez alone targets
  the max-error objective directly via the equioscillation theorem: the true minimax degree-d polynomial's
  error alternates sign exactly d+2 times at equal magnitude, which is what the exchange algorithm's
  alternation-equation system directly encodes); connected this to yesterday's plateau-exploitation finding --
  Remez is a second, independent, compounding lever on top of "search to the top of the depth plateau," since
  both attack the same "get more accuracy for the same depth" objective from different angles (which degree to
  use vs which polynomial of that degree to use).
Exercise: the Remez implementation itself stands in as today's exercise (built and run live, not left
  unverified); the natural extension if Parth picks this up is combining both levers -- Remez fit AT the top
  of a depth plateau (e.g. degree 13 for the depth-5 budget) rather than at the first-passing degree -- which
  was not run today for time but is a direct, mechanical combination of the last two sessions' findings.
Asked: (1) does Parth's own approximation work use Chebyshev interpolation, least-squares truncation, or
  Remez/minimax currently -- given the two independent free-accuracy levers found this week (plateau
  exploitation + minimax fitting), which is more likely to already be captured in his existing pipeline vs
  genuinely new; (2) the equioscillation theorem (minimax error alternates sign exactly d+2 times at equal
  magnitude) is a NECESSARY AND SUFFICIENT condition for optimality -- does this give a cheap way to check
  whether an already-computed polynomial (from any method) is minimax-optimal, without re-running Remez, just
  by counting sign alternations of its error curve; (3) still carrying forward the plateau-exploitation
  question from yesterday and the GLWE/open-problems questions from the closing sessions, all still
  unanswered.
Answers: pending.
Weak spots: unmeasured across thirty-three sessions (zero of ~41+ questions answered to date).
Revisit next time: today's equioscillation-counting question is cheap to verify and worth prioritizing if
  Parth engages. Next: combine the two found levers (Remez at the top of the depth plateau) as a concrete
  worked example, or move to submission/ (the real OpenFHE C++ contract) if the algorithmic side feels
  sufficiently covered.

## 2026-09-26 — FHERMA Practice: combining both levers (Remez fit at the top of the depth plateau)
Combined the two independent free-accuracy levers found this week: (Tue) search to the top of the
  OpenFHE depth plateau rather than stopping at the first passing degree, and (Fri) use Remez minimax instead
  of Chebyshev truncation/interpolation for a given degree. Ran both together, comparing against ex18's naive
  baseline (first-passing-degree Chebyshev interpolation) at the SAME multiplicative depth (5 levels) for all
  three activations:
  - Sigmoid[-8,8]: ex18 naive (degree 7, Chebyshev interp) = 0.029640; Remez at plateau-top (degree 13) =
    0.001892 -> 15.7x more accurate, zero extra depth.
  - GELU[-5,5]: ex18 naive (degree 6, Chebyshev interp) = 0.090143; Remez at plateau-top (degree 13) =
    0.003672 -> 24.5x more accurate, zero extra depth.
  - ReLU[-5,5]: did NOT reproduce the clean pattern -- Remez at degree 13 gave 0.057898, notably worse than
    the plateau-exploited CHEBYSHEV interpolation result from Tuesday (degree 12, error 0.008027), and
    non-monotonic within Remez itself (degree 12 Remez error 0.411106, degree 13 Remez error 0.057898 --
    a huge jump). Diagnosed: NOT a broken exchange loop -- verified the final reference-point errors DO
    alternate sign correctly (a genuine equioscillating set), so the algorithm converged to *a* local
    equioscillating solution, just an unstable/poor one for this case. Read this as ReLU's kink at x=0 making
    the exchange algorithm's convergence landscape much rougher than for the two smooth functions (sigmoid,
    GELU), where Remez converged cleanly and fast. Did not fully resolve within today's session -- flagged
    explicitly as unresolved rather than glossed over.
Taught: this is the same structural fact as the ~950x kinked-vs-smooth leverage gap surfaced many sessions
  ago (Ch18-19 calibration work) showing up in a completely different guise -- there, it was about how many
  polynomial terms a kink costs relative to a smooth function for the SAME error target; here, it is that even
  the OPTIMIZATION PROCEDURE (Remez exchange) for finding the minimax polynomial behaves qualitatively
  differently -- clean, fast, monotonic convergence for smooth targets vs rough, non-monotonic, possibly
  poorly-converged behavior for a kinked target -- suggesting kinked activations may be doubly disadvantaged
  in a real optimization pipeline (harder to approximate well AND harder to reliably fit optimally).
Exercise: today's combined-lever comparison IS the exercise, run and reported honestly including the ReLU
  anomaly; the natural follow-up (not done today) is either a more careful/correct Remez implementation
  (proper alternation-preserving reference update, not just "top-m |error| points sorted by x") to check
  whether the ReLU anomaly is a real optimization-landscape difficulty or an artifact of my simplified
  exchange loop, or switching to a smoothed/clipped ReLU variant (as real CKKS-friendly architectures often
  do) to sidestep the kink entirely.
Asked: (1) is Parth's own activation-approximation work targeting smooth functions (GELU/sigmoid/swish-style,
  where today's combined levers gave clean 15-25x free-accuracy wins) or kinked ones (ReLU-style, where the
  same procedure broke down) -- this matters a lot for which of this week's findings actually transfers to his
  pipeline; (2) given the ReLU anomaly might be a bug in my simplified reference-point selection rather than a
  fundamental optimization-landscape fact, does Parth have a reference (his own code, a paper, or a library
  like Remez/minimax packages) to cross-check whether Remez genuinely struggles with ReLU-class kinks or my
  implementation is just weak; (3) still carrying the equioscillation-counting diagnostic question and the
  plateau/GLWE/open-problems questions from earlier sessions, all still unanswered.
Answers: pending.
Weak spots: unmeasured across thirty-four sessions (zero of ~44+ questions answered to date). Also a genuine
  open technical loose end from today (ReLU Remez anomaly) rather than just an unanswered question -- worth
  resolving before trusting the Remez lever for kinked activations specifically.
Revisit next time: resolve the ReLU Remez anomaly (better exchange implementation or a clipped/smoothed ReLU
  variant) before extending the combined-lever approach further; otherwise move to submission/ (the real
  OpenFHE C++ contract) since the algorithmic FHERMA-practice track has now covered its core techniques
  (plateau exploitation, Remez, and their combination/limits).

## 2026-09-27 — FHERMA Practice: attempting to fix the ReLU Remez anomaly, finding a second bug instead
Followed up on Friday's flagged loose end: implemented a v2 Remez with a proper alternation-enforcing
  reference-point update (single left-to-right pass merging same-sign consecutive extrema into the
  larger-magnitude one, THEN downselecting to exactly m=degree+2 points), rather than yesterday's crude
  "top-m |error| points sorted by x" heuristic that could silently select a non-alternating set.
Result: did NOT resolve the ReLU anomaly. relu degree 13 max error stayed at 0.058008 (vs yesterday's
  0.057898 -- essentially unchanged); degree 12 broke even earlier (iteration 0 found only 13 alternating
  extrema when 14 are needed, so no exchange happened at all, coeffs are just the very first linear solve --
  0.191995). This is informative: it suggests ReLU's Remez difficulty is NOT primarily an artifact of the
  naive reference-selection heuristic -- something more structural about the kink is making convergence
  genuinely hard, consistent with Friday's hypothesis, though still not conclusively proven (a correctly
  implemented Remez might still behave better than either of my two attempts).
SECOND, unrelated bug found via the sigmoid sanity check (run specifically to confirm v2 didn't regress the
  cases that worked cleanly Friday): sigmoid degree 13 error REGRESSED from Friday's clean 0.001892 to
  0.012702 under v2. Root cause identified: the "downselect to exactly m points by repeatedly removing the
  globally smallest-magnitude point" step is WRONG -- removing an INTERIOR point from a strictly alternating
  sequence merges its two same-sign neighbors (which sit two positions apart, same parity, same sign) into new
  adjacency, silently breaking the alternation the first step had just enforced. Removing only endpoints is
  safe; removing interior points is not, and my greedy "always remove the globally smallest" rule has no way
  to know which case it's in. This is a genuine implementation-correctness lesson, not a research result: the
  classical Remez exchange algorithm's exact reference-point-update rule is more subtle than the equioscillation
  theorem's statement suggests, and both of my two homebrew attempts this week have real, distinct bugs in that
  update step specifically -- the theorem is a clean necessary-and-sufficient CONDITION for optimality, but
  turning it into a convergent, correct ITERATIVE ALGORITHM is a separate and harder engineering problem.
Taught: the gap between "I can state the optimality condition" (equioscillation) and "I can reliably compute
  the optimum" (a correct exchange algorithm) -- directly relevant given Friday's proposed diagnostic
  ("count sign alternations to check optimality") is still valid and cheap, but this week showed twice over
  that COMPUTING a correctly-alternating minimax fit is the harder direction. Recommended, rather than continue
  patching a homebrew implementation for research-grade numbers, using a validated library (e.g. Sollya's
  native Remez implementation, or a maintained Python minimax/Remez package) for anything beyond this week's
  teaching purposes -- exactly Appendix D.3's closing advice ("for what to actually type, the library
  documentation, always") applied to algorithms as much as APIs.
Exercise: today's v2 implementation attempt and its diagnosis (both the non-fix for ReLU and the new sigmoid
  regression) stood in as the exercise; no further homebrew Remez debugging planned -- next practical step
  if Parth wants a working Remez for his own research is identifying and testing an established library rather
  than continuing to patch this week's toy versions.
Asked: (1) does Parth already have access to a validated Remez/minimax implementation (Sollya is the standard
  in the floating-point/polynomial-approximation literature) for his own depth-optimal work, or has this week's
  toy-implementation experience changed how he'd budget time between "derive the approach" and "find/verify an
  existing correct implementation"; (2) unresolved from Friday, still relevant: is ReLU-class kinked-activation
  approximation actually in scope for his research, or is the target smooth (in which case this week's
  Remez difficulties are a genuinely interesting side-quest but not blocking); (3) all earlier carried-forward
  questions (equioscillation-counting diagnostic, plateau exploitation, GLWE framing, open problems) remain
  unanswered and are carried forward again without repeating the full list here.
Answers: pending.
Weak spots: unmeasured across thirty-five sessions (zero of ~47+ questions answered to date). Two genuine
  unresolved technical loose ends now (ReLU Remez convergence; correct alternation-preserving downselection),
  both flagged rather than papered over, and both pointing toward the same resolution (use a validated library).
Revisit next time: FHERMA algorithmic practice track has now run its course for this round (plateau
  exploitation, Remez, their combination, and the limits of a homebrew Remez implementation all covered
  honestly, including where it broke). Next: move to submission/ (the real OpenFHE C++ contract: CLI flags,
  solver class, config.json workflow) to close the loop from algorithm to actual FHERMA submission shape.

## 2026-09-28 — FHERMA Practice: the real submission/ contract, closing this week's arc
Moved from algorithmic practice (plateau exploitation, Remez) into submission/ -- the actual OpenFHE C++
  FHERMA contract. Read main.cpp, yourSolution.h/.cpp, config.json, and the submission README rather than
  teaching from memory of what a FHERMA submission "probably" looks like.
Contract as actually specified: evaluator invokes the binary with six paths to OpenFHE BINARY-serialized
  objects (--cc, --key_pub, --key_mult, --key_rot, --input, --output). NO secret key anywhere in the process --
  the whole submission threat model is that eval() cannot decrypt, branch on plaintext, or otherwise depend on
  seeing cleartext at any point; if an approach needs that, "it needs redesigning, not debugging" (README's own
  words, correctly blunt). yourSolution.cpp's worked example applies EvalChebyshevFunction(sigmoid, degree=7,
  [-8,8]) as the shape "most activation challenges take."
Direct, submission-shape application of this week's finding: the skeleton's own worked example uses degree=7
  -- literally the naive first-passing-degree pick this week's Tuesday session showed leaves accuracy on the
  table. Verified via fherma_config.py: degree 7 and degree 13 cost the IDENTICAL mult_depth=5 and the
  IDENTICAL ring_dimension=16384 (config.json's already-declared values, unchanged either way) -- so swapping
  the skeleton's degree constant from 7 to 13 is a literal one-line code change, zero re-declaration of
  config.json needed, for the same ~10x accuracy improvement found Tuesday. This is as close to "submission-
  ready" as this week's finding gets without an actual FHERMA challenge to submit against.
Found a precise, worth-noting disagreement with the repo's own pre-submission checklist: its last item reads
  "degree is the *lowest* that meets the accuracy bar, not the first that worked" -- i.e. it explicitly
  endorses degree-minimization via systematic search as the target metric. This week's plateau finding shows
  that's not quite right once OpenFHE's real (step-function, non-injective) depth table is used: the correct
  guidance is "lowest DEPTH that meets the bar, then highest degree free within that depth," since degree and
  depth are not interchangeable. Framed as a specific, actionable correction to a specific, existing document
  rather than a vague critique.
Taught: the six-argument CLI contract and the no-secret-key threat model; why config.json is "where most
  submissions fail" (mult_depth from the real table not the formula; every rotation offset must be declared or
  EvalRotate throws at runtime; ring dimension must account for HYBRID key-switching's auxiliary modulus P);
  the SKELETON-labeling convention from Appendix C applied concretely here (this C++ is illustrative, cross-
  check EvalChebyshevFunction's exact signature against the pinned OpenFHE version's own examples/ tree before
  trusting it verbatim); could not compile or run this harness live, since OpenFHE remains non-functional in
  this environment (a standing, previously-flagged constraint) -- said so plainly rather than claiming a build
  that didn't happen.
Exercise: the fherma_config.py verification above (degree 7 vs 13, identical depth/ring) stood in as today's
  exercise, directly applied to the actual submission skeleton's own example rather than an abstract case.
Asked: (1) does Parth have OpenFHE building successfully wherever he actually develops (unlike this sandboxed
  environment), and if so would he be willing to compile this submission skeleton with the degree-13 patch and
  confirm the predicted accuracy improvement holds under real CKKS noise/rescaling, not just the noiseless
  Python approximation used all week; (2) the checklist-correction above -- worth a one-line edit to the
  repo's own submission/README.md checklist item, or does the "lowest degree" phrasing already implicitly
  assume plateau-awareness that just wasn't spelled out; (3) all earlier carried-forward questions (Remez
  library validation, kinked-vs-smooth research scope, equioscillation diagnostic, GLWE framing, open
  problems) remain unanswered and are carried forward without repeating the full list.
Answers: pending.
Weak spots: unmeasured across thirty-six sessions (zero of ~50+ questions answered to date).
Revisit next time: this closes the FHERMA-practice arc that started Wednesday (plateau exploitation -> Remez ->
  Remez debugging -> real submission contract, ending on a concrete, verified, submission-shape recommendation).
  Open for redirect: continue deeper into FHERMA (a specific real challenge from fherma.io, if Parth names one),
  return to spaced-repetition review of earlier weak spots (the Ch13 convention bug, Ch18-19 calibration
  mistakes, Ch24 depth-exhaustion demo), or Parth's own research question directly. Absent a redirect, default
  next session: a spaced-repetition review pass, since the algorithmic FHERMA track has reached a natural
  stopping point and revisiting weak spots is the one branch not yet tried this cycle.

## 2026-09-29 — Spaced-Repetition Review: Ch13 convention bug, Ch24 depth-exhaustion, Ch18-19 calibration
Default path taken per last session's proposal absent a redirect from Parth: first review-cycle pass over
  earlier weak spots rather than continuing straight FHERMA practice, to check these findings still hold and
  are genuinely retained rather than one-off session artifacts.
Re-verified live, independently reconstructed (not copy-pasted from old scratchpad, since scratchpads don't
  persist across sessions -- this forced a genuine from-scratch re-derivation, arguably a better test of
  retention than replaying old code would have been):
  - Ch13 convention bug: re-ran TenSEAL's enc_x.matmul(W) for a 3x2 asymmetric W, confirmed AGAIN it computes
    x^T @ W (row-vector convention), matching x@W exactly ([22, 28] both ways) -- re-derived the original
    finding without needing to recall the exact numbers, only the shape of the fact ("TenSEAL is row-vector,
    not W@x"), which is the right level for retention (concept over exact digits).
  - Ch24 depth-exhaustion demo: had to rebuild the parameter budget from scratch and hit a real, useful
    speed bump doing so -- first attempt at N=8192 with 11 scale primes overflowed the 218-bit security cap
    immediately (ValueError before any computation ran); realized the fix required recalling Ch14's ring-
    dimension/security-cap relationship (RING_CAPS-style table, reused all week in fherma_config.py), not just
    Ch24 content -- a good sign the material connects across chapters rather than sitting in isolated silos.
    Fixed with N=16384 (cap 438 bits) and 11 scale primes of 28 bits (60+60+11*28=428, fits). Reproduced the
    exact original result: iteration 0 succeeds (w updates to 0.5887), iteration 1 fails with "end of modulus
    switching chain reached" -- Observation 24.1 (naive-Horner training exhausts its depth budget almost
    immediately) held up under independent re-derivation.
  - Ch18-19 calibration-range lesson: NOT re-run today (time budget), but noted this one has already had
    organic, unplanned spaced repetition multiple times since the original session -- most directly in the
    Ch27 softmax R=10-vs-R=4 exp-fitting failure, and again implicitly in this week's Remez/plateau work
    (both explicitly framed as instances of the same "calibrate the domain, don't assume it" principle). Given
    it has already resurfaced organically at least twice without prompting, judged lower-priority for today's
    dedicated review slot than the two that hadn't been touched since their original session.
Taught: the value of reconstructing a past finding from the underlying concept rather than replaying saved
  code -- both re-derivations required real (if small) new problem-solving (choosing a correct W shape to
  distinguish the two conventions; rebuilding a valid parameter budget from Ch14's security-cap relationship),
  which is a more honest test of whether prior sessions actually built durable understanding versus session-
  local pattern matching.
Exercise: both re-derivations above stood in as today's exercise.
Asked: (1) does reconstructing Ch24's parameter budget requiring a recalled security-cap relationship from
  Ch14 (rather than Ch24 itself) match how Parth would expect FHE knowledge to organize in his own head --
  cross-chapter dependency rather than per-chapter silos -- or does his own mental model of the material look
  different; (2) is there a specific earlier session's finding Parth would flag as HIGH priority for a review
  pass, as opposed to my own guess (Ch13, Ch18-19, Ch24) from three-plus weeks ago; (3) all earlier carried-
  forward questions (FHERMA/Remez library validation, kinked-vs-smooth research scope, equioscillation
  diagnostic, GLWE framing, open problems, submission checklist correction) remain unanswered and are carried
  forward without repeating the full list.
Answers: pending.
Weak spots: unmeasured across thirty-seven sessions (zero of ~53+ questions answered to date). Positive
  signal, though: today's independent re-derivations both succeeded, which is closer to direct evidence of
  retention than anything a verbal check-in could provide -- worth noting explicitly since Parth has never
  confirmed retention any other way.
Revisit next time: open for redirect (continue spaced-repetition review of other sessions, return to FHERMA
  with a specific real challenge, or focus directly on Parth's research question). Absent a redirect, default
  next session: pick 1-2 more candidate weak spots from mid-conversation (the Ch4 "39% ~ chance" self-correction,
  the Ch10/Ch16 TenSEAL level-mismatch speculation-then-correction, or the Ch22 STE divergence-then-fix) for the
  same live re-derivation treatment.

## 2026-09-30 — Spaced-Repetition Review Round 2: TenSEAL level auto-alignment confirmed; STE divergence NOT reproduced
Continued the review-pass default from last session, picking two more candidates: the Ch10/16 TenSEAL
  level-mismatch auto-alignment finding, and the Ch22 STE divergence-then-fix.
  - TenSEAL level-mismatch: re-verified cleanly. Built a fresh mismatch (a*a consumes a rescale/level, b left
    untouched) and added the two directly -- succeeded without error, result [11.0, 24.0, 39.0] exactly
    matching plain addition, confirming again TenSEAL auto-mod-switches to align levels on add rather than
    throwing. Second clean re-derivation of this one (first was the original Ch16 session; this is now
    re-confirmed independently a second time).
  - Ch22 STE divergence-then-fix: did NOT reproduce. Built a fresh, deliberately simple scalar test (single
    weight w, 4-bit STE quantizer, MSE toward a fixed target) at both lr=0.5 and lr=0.05. Result was the
    OPPOSITE of the original finding: lr=0.5 converged FASTER (loss 0.253 -> 0.0009 by step 1) than lr=0.05
    (0.253 -> only 0.092 after 6 steps), with no divergence at either rate. The original session's numbers
    (loss exploding to 43636 at lr=0.5, then clean convergence 4.67->0.0084 at lr=0.05) describe a much larger-
    scale blowup than anything a single-scalar toy can produce -- almost certainly the original exercise used a
    real weight tensor/multi-parameter layer, where STE's identity-gradient approximation can compound
    divergently ACROSS parameters/layers in a way a single scalar has no mechanism to reproduce (there is
    nothing here for error to compound through). Reported this plainly rather than forcing a false
    confirmation or quietly dropping the mismatch.
Taught (about the review process itself, not new FHE content): this is exactly the kind of honest gap spaced
  repetition is supposed to surface -- I could recall the QUALITATIVE lesson (STE + high learning rate can
  diverge because the identity-gradient approximation doesn't track the quantizer's true, mostly-flat loss
  landscape) but could not reconstruct the specific setup that produced it, and my simplified stand-in didn't
  reproduce the phenomenon. This is a genuine limitation of memory-based review versus having the original
  artifact: a qualitative fact ("STE can diverge at high lr") survived; the quantitative instance (the specific
  setup that demonstrated it) did not, and manufacturing a fake replay would have been worse than admitting
  that directly.
Exercise: both re-verification attempts above stood in as the exercise, including the inconclusive one,
  reported as inconclusive rather than papered over.
Asked: (1) does Parth still have the original Ch22 STE exercise setup (or can reconstruct it) to check whether
  it really was a multi-parameter/tensor case, confirming or correcting today's hypothesis about why the
  scalar reconstruction didn't reproduce the divergence; (2) more generally -- given two spaced-repetition
  sessions now (Ch13/Ch24 fully reproduced; Ch10-16 reproduced twice; Ch22 NOT reproduced) -- does this pattern
  (concrete numerical/library facts hold up under reconstruction, but a specific dynamical/training-instability
  result does not) match what Parth would expect for which KINDS of FHE facts are safe to recall from memory
  in his own work versus which need re-verification every time; (3) all earlier carried-forward questions
  remain unanswered and are carried forward without repeating the full list.
Answers: pending.
Weak spots: unmeasured across thirty-eight sessions (zero of ~56+ questions answered to date). Notably: this
  is the first review-pass item that did NOT survive reconstruction, a useful data point in itself about which
  categories of past findings are robust.
Revisit next time: open for redirect. Absent one, default next session: continue the review cycle with the
  Ch4 probability self-correction (39% vs the correct 25% chance baseline for a t=4 exercise) as a quick,
  low-cost arithmetic re-check, then consider whether the review cycle has covered enough ground to return to
  either FHERMA practice or Parth's research question directly.

## 2026-10-01 — Ch4 review (confirmed) + fresh Ch19 re-read: this week's FHERMA work was already in the book
Quick Ch4 review first: re-ran ex03_lwe.py's large-noise decryption test fresh. Confirmed t=4 (plaintext
  modulus) exactly as before, large-noise accuracy exactly 39.00% again (deterministic script, same seed
  behavior). The original correction holds: chance baseline for t=4 is 25%, not the 50% I wrongly asserted in
  the Ch4 catch-up session months ago; 39% sits meaningfully above the 25% chance floor, meaning large-noise
  decryption in this toy LWE instance retains weak residual signal rather than being pure noise -- a precise
  point worth keeping, not just "it's broken."
Then, rather than a third weak-spot replay, did something more valuable: re-read Ch19 (Polynomial Activation
  Approximation) FRESH from fhe-book.html for the first time since it was originally taught, specifically to
  check it against everything built ad hoc this week (plateau exploitation, Remez, the submission skeleton).
  Result: most of this week's "findings" were already explicit in Ch19's own content, which I apparently didn't
  connect back to at the time:
  - Ch19 Table 19.5 (Paterson-Stockmeyer depth budget) is EXACTLY fherma_config.py's CHEBYSHEV_DEPTH table --
    verified programmatically, both give [(5,4),(13,5),(27,6),(59,7),(119,8),(247,9),(495,10)], a literal match.
    This means the depth plateau structure (degrees 6-13 all costing 5 levels) that took a dedicated session
    this week to notice was sitting directly in Ch19's own table the whole time -- the book just didn't spell
    out the optimization IMPLICATION (search to the top of a plateau) the way this week's live exploration did.
    Worth being honest about: this week added the optimization INSIGHT on top of a fact the book already stated,
    it didn't discover a new fact.
  - Ch19 Section 19.3 states Theorem 19.2 (Chebyshev equioscillation, d+2 alternating extrema) in exactly the
    form used to diagnose both Remez bugs this week -- confirms the diagnostic tool used was the textbook-
    correct one, independently re-derived under pressure rather than looked up, which is a good retention sign.
  - Ch19 Section 19.3 explicitly recommends this week's exact workflow for chasing extra accuracy: "if you are
    chasing the last bit of tail robustness, run Remez explicitly in cleartext and hand OpenFHE the resulting
    coefficients via EvalChebyshevSeries" -- i.e. the book already anticipates that EvalChebyshevFunction (used
    in yesterday's submission skeleton) may only be near-minimax, not true minimax, and tells you to precompute
    real Remez coefficients yourself if you want the extra accuracy. This week's homebrew Remez attempt was
    the right instinct, just under-executed (both exchange-loop bugs found Friday/Saturday).
  - Ch19 Section 19.4's GELU closed-form reduction (GELU(x) ~ x*sigmoid(1.702x), reusing a single sigmoid
    polynomial rather than fitting GELU's Gaussian-CDF shape from scratch) is NOT a strict improvement on this
    week's from-scratch erf-based GELU fit, contrary to my first assumption when I found this passage --
    verified live: the Swish-based approximation itself has a 0.0203 floor error on [-5,5] BEFORE even applying
    sigmoid's own polynomial-fitting error on top, which is worse than this week's achieved degree-13
    Remez/Chebyshev erf-fit error of 0.00367. So the closed-form reduction trades accuracy for engineering
    simplicity (one polynomial to build and verify instead of two) -- a real tradeoff, not a free lunch, and
    whether it's worth taking depends on whether 0.02 clears the challenge's accuracy bar. Caught my own
    overclaim here mid-session (first framed this as "this week duplicated work," corrected to "this week's
    extra work bought real accuracy the shortcut doesn't give") rather than letting the overstated version
    stand.
Taught: the value of occasionally re-reading SOURCE material fresh rather than only reviewing one's own derived
  exercises -- today's Ch19 re-read surfaced that an entire week of "discoveries" was mostly reconnecting
  already-taught facts to their optimization implications, which is a different (still valuable, but more
  modest) kind of progress than net-new discovery, and worth being honest about rather than overselling the
  week's novelty.
Exercise: the depth-table reconciliation and the GELU tradeoff verification above stood in as today's exercise.
Asked: (1) given today's finding that the plateau-exploitation insight was implicit in Ch19's own table, does
  Parth's own research track findings against the literature carefully enough to know when a result is genuinely
  novel versus a known fact rediscovered under a new framing -- is there a standard practice (lit review pass,
  explicit "what's new here" section) worth adopting given how easily this happened even with the SOURCE
  material already read once; (2) the GELU tradeoff (0.02 floor from the closed-form reduction vs 0.0037 from
  a from-scratch fit) -- does Parth's own FHERMA/research work have a stated accuracy bar that would make this
  decision concrete (i.e. is 0.02 good enough for his use case, making the engineering savings worth it) rather
  than an abstract comparison; (3) all earlier carried-forward questions remain unanswered and are carried
  forward without repeating the full list.
Answers: pending.
Weak spots: unmeasured across thirty-nine sessions (zero of ~59+ questions answered to date).
Revisit next time: open for redirect. The spaced-repetition review cycle plus today's fresh-source-reread both
  suggest a useful pattern worth continuing periodically (review old exercises AND periodically re-read
  original chapters fresh, not just once). Absent a redirect, default next session: return to generative work
  -- apply today's GELU/Remez-coefficient findings to update the combined-levers results from earlier this
  week (swap in real Remez coefficients for sigmoid/GELU via EvalChebyshevSeries-style precomputation, and
  re-run the depth-plateau comparison with the corrected, book-recommended workflow instead of this week's
  under-executed homebrew Remez).

## 2026-10-02 — Resolving the ReLU Remez anomaly: a correct implementation, and a real (not buggy) answer
Followed up on last session's plan: fixed the actual bug behind Saturday's v2 regression, then used the
  corrected implementation to settle the week-long open question about whether ReLU's Remez difficulty was
  a bug or real.
Root cause of Saturday's v2 regression, finally isolated: downselecting from >m alternating extrema to
  exactly m=degree+2 points by repeatedly removing the globally-smallest-magnitude point can remove an
  INTERIOR point, which always merges its two same-sign neighbors (two positions apart in an alternating
  sequence, hence same sign) into new adjacency -- silently breaking alternation. The fix (v3): downselect by
  trimming only from the two ENDS of the alternating list, always removing whichever boundary point has
  smaller magnitude. This preserves contiguity, which trivially preserves alternation (a sub-window of an
  alternating sequence is still alternating; an arbitrary subset is not).
Verified v3 against every case touched this week:
  - Sigmoid degree 13: 0.001892 -- EXACTLY matches Friday's original (buggy-implementation) result. The v1
    bug apparently never triggered for this specific case's extrema pattern, so the fix changes nothing here --
    good, since it means Friday's headline 15.7x combined-lever number for sigmoid stands as originally
    reported, now on a verified-correct implementation rather than a lucky one.
  - GELU degree 13: 0.003672 -- also matches Friday exactly, same story.
  - ReLU degree 13: 0.058008 -- UNCHANGED from both buggy versions. This is the conclusive answer to the
    open question: ran it at 30, 60, and 100 iterations, result is bit-identical every time (0.058008) --
    the algorithm has fully converged to a genuine fixed point of the exchange map, not something still
    moving that more iterations would improve. With a PROVABLY alternation-correct implementation now in hand,
    this rules out "implementation bug" as the explanation. The remaining explanation is the one hypothesized
    Saturday: Remez (a local, Newton-like iterative method) can converge to a valid equioscillating LOCAL
    fixed point that is not the global minimax, and ReLU's kink makes the standard Chebyshev-node initial
    reference-point guess land in a bad basin of attraction for this function specifically -- something the
    two smooth functions (sigmoid, GELU) don't suffer from. A fix would need kink-aware initialization
    (e.g. forcing x=0 into the initial reference set) or a continuation/homotopy approach, not just more
    iterations or a bug-free exchange step.
Net result: this week's combined-lever numbers for smooth activations are now validated on a correct Remez
  implementation (sigmoid 15.7x, GELU 24.5x free accuracy at the same depth, both unchanged from the original
  reports); the ReLU anomaly is conclusively real, not a bug, and specifically a local-convergence failure
  mode tied to the kink -- a genuinely interesting finding in its own right, since it suggests Remez-based
  approaches may need special handling for kinked activations in practice, beyond simply "run the algorithm."
Taught: the distinction between a converged-but-wrong result (a genuine local optimum of an iterative method)
  and a buggy result (the algorithm hasn't correctly implemented its own update rule) -- these look identical
  from the final number alone ("my optimizer says X") but require completely different fixes, and this week's
  three-session arc (v1 bug -> v2 different bug -> v3 correct, isolating ReLU as real) is a worked example of
  how to actually distinguish them: fix implementation issues one at a time, re-verify against KNOWN-GOOD
  cases after each fix, and only trust a "this is a real phenomenon" conclusion once the implementation passes
  its own sanity checks.
Exercise: today's v3 implementation and the full sigmoid/GELU/ReLU re-verification (including the
  30-vs-60-vs-100-iteration stability check on ReLU) stood in as the exercise.
Asked: (1) given ReLU's Remez difficulty is now confirmed real rather than a bug, is kink-aware Remez
  initialization (seeding x=0 into the reference set, or a degree-by-degree continuation from a low-degree
  solution) something Parth's own research already handles, or a genuinely open question worth exploring given
  his approximation focus; (2) does a local-vs-global optimum distinction for Remez specifically appear in the
  approximation theory literature Parth would have encountered, or is this week's finding likely rediscovering
  a known caveat (in the spirit of yesterday's Ch19 reconciliation) -- worth checking before treating it as
  novel; (3) all earlier carried-forward questions remain unanswered and are carried forward without repeating
  the full list.
Answers: pending.
Weak spots: unmeasured across forty sessions (zero of ~62+ questions answered to date). Positive note: this
  closes out the week-long Remez/ReLU thread with a definitive, well-isolated answer rather than leaving it
  as an open loose end indefinitely.
Revisit next time: open for redirect. The FHERMA/Remez thread has reached a genuinely conclusive stopping
  point (not just a time-boxed pause). Absent a redirect, default next session: return to the main curriculum's
  spirit by picking a specific open research question to dig into directly -- e.g. survey (via Scholar_Feed, if
  still connected) recent literature on Remez-type algorithms for non-smooth/kinked target functions, to check
  today's finding against the actual research literature per Question 2 above, rather than continuing to
  rediscover results in isolation.

## 2026-10-03 — Literature check on the ReLU Remez finding (via ppml-research-assistant + Scholar Feed)
Followed through on Thursday's plan: checked the week's conclusive finding (Remez converges to a correctly-
  equioscillating but non-global-optimal fixed point for ReLU, not for smooth sigmoid/GELU) against the actual
  literature, using the newly-available ppml-research-assistant skill's Mode 1 (literature review) workflow
  over Scholar Feed, rather than asserting from memory whether this is known or novel.
Searched and read (abstract+introduction) three papers directly on point:
  - Filip, Nakatsukasa, Trefethen, Beckermann, "Rational minimax approximation via adaptive barycentric
    representations" (arXiv 1705.10132, SIAM J Sci Comput 2017) [Verified]. Central, highly relevant finding,
    but it CUTS AGAINST my hypothesis as originally framed: this paper is about RATIONAL Remez struggling near
    true singularities (discontinuities, poles, unbounded growth) -- their own text states "finding the best
    POLYNOMIAL approximation...can usually be done robustly by a standard implementation of the linear Remez
    algorithm," explicitly contrasting this with the rational case, which is the one that needs their new
    adaptive-barycentric/AAA-Lawson machinery. ReLU is continuous (just non-differentiable at one point, not
    discontinuous), so this paper's "difficult functions" (true discontinuities, poles, log singularities) are
    a harder class than ReLU's kink -- meaning the literature's prevailing view is that POLYNOMIAL Remez on a
    merely-kinked-but-continuous function like ReLU should generally be fine, which if anything predicts my
    result should NOT have happened as a generic phenomenon.
  - Garimella, Jha, Reagen, "Sisyphus: A Cautionary Tale of Using Low-Degree Polynomial Activations in
    Privacy-Preserving Deep Learning" (arXiv 2107.12342, 2021) [Verified]. Documents a related but DISTINCT
    failure mode -- the "escaping activation problem," where forward activations drift outside a polynomial's
    well-fit region during TRAINING, causing blowup. This is a training-dynamics problem (closer to Ch27's
    calibration-range lesson) not a one-shot Remez-convergence problem, so it doesn't directly confirm my
    specific finding either, though it's the same broad neighborhood (ReLU-polynomial replacement is full of
    known gotchas, just different ones than mine).
  - "Decision-Aware Quadratic ReLU Replacement for HE-Friendly Inference" (arXiv 2605.22237, 2026) [Verified].
    Confirms Remez-based ReLU replacement ("Remez-7") is cited as an established, standard baseline technique
    in the current HE-friendly-inference literature (they benchmark their own method as 3.7-4.1x faster than
    it) -- so the general approach of this week's exploration is mainstream, not naive. No mention of
    convergence-to-local-optimum as a caveat of that baseline.
Honest conclusion: the specific claim ("polynomial Remez can converge to a non-global local equioscillating
  fixed point for ReLU specifically, due to kink-related bad initialization") is NOT confirmed as a known,
  named result in what I could locate -- the closest adjacent literature (Filip et al.) is about a different,
  harder problem (rational approximation near true singularities) and if anything suggests continuous-but-
  kinked functions like ReLU should usually be fine for polynomial Remez, which is the opposite of what I
  observed. This week's finding stands as a genuinely narrower, implementation/initialization-specific result
  I have NOT found written up elsewhere, not a known textbook caveat -- a materially different conclusion than
  the Ch19 reconciliation two sessions ago (where the plateau-exploitation insight WAS already in the book).
  Correctly separating "rediscovered a known fact" from "found something not obviously in the literature I
  checked" is itself the point of doing this check rather than guessing either way.
Also worth separating (a clarification, not a new citation): Ch19's Theorem 19.2 states the equioscillation
  characterization requires only continuity of the target function -- so there's no THEORETICAL reason
  ReLU's kink should break the existence/characterization of a minimax polynomial. What's at issue is the
  NUMERICAL behavior of the iterative exchange algorithm specifically, a separate, computational-practice-level
  question from the underlying approximation-theory theorem, and the literature check above speaks to that
  practical question, not the theorem.
Taught: how to use the new ppml-research-assistant skill's literature-review mode properly -- search multiple
  angles, fetch actual abstracts/introductions rather than trusting search snippets, tag every claim with a
  verification status, and be willing to report "not confirmed, and the nearest literature actually points
  the other way" rather than forcing a tidy "yes, known" or "no, novel" conclusion.
Exercise: the literature search and honest reconciliation above stood in as today's exercise.
Asked: (1) given the literature doesn't confirm my hypothesis as framed, would it be worth Parth (or me, with
  more budget) actually investigating WHY the specific ReLU case got stuck -- e.g. checking whether a
  different initial reference-point placement (seeding x=0 explicitly) resolves it, which would distinguish
  "genuinely hard for any initialization" from "just this particular initialization was unlucky" -- the
  literature check didn't resolve this, it just confirmed the literature doesn't already answer it; (2) does
  Parth have Scholar Feed (or equivalent) access set up for his own ongoing lit-tracking, given how directly
  useful today's three-paper check was for calibrating confidence in a week-old finding; (3) all earlier
  carried-forward questions remain unanswered and are carried forward without repeating the full list.
Answers: pending.
Weak spots: unmeasured across forty-one sessions (zero of ~65+ questions answered to date).
Revisit next time: open for redirect. A natural next step if continuing this exact thread: actually test the
  x=0-seeded-initialization hypothesis from Question 1 live, since the literature check raised it but didn't
  answer it. Otherwise, open to returning to a different part of the curriculum, Parth's research directly, or
  another spaced-repetition round.

## 2026-10-04 — Correction: the "ReLU Remez anomaly" was partly a bad reference number, not a real effect
Set out to test yesterday's open question (does seeding x=0 into the initial reference set resolve ReLU's
  Remez difficulty) and ended up finding something more important: the anomaly itself was significantly
  overstated due to a mis-attributed number from over a week ago.
Initialization-robustness test: ran v3 Remez for ReLU degree 13 on [-5,5] from EIGHT different starting
  points -- the standard Chebyshev-node init, Chebyshev-node-with-x=0-forced-in, five randomly perturbed
  Chebyshev inits, and an equispaced init. SEVEN of eight converged to the exact same value, 0.058008, bit-
  for-bit. This is strong evidence 0.058008 is not a bad local optimum from an unlucky initialization -- it
  looks like the actual global minimax error for a degree-13 polynomial fitting ReLU on [-5,5], robustly
  reached from almost any reasonable starting point. (One perturbed trial landed worse, at 0.142663 --
  consistent with occasional non-convergence within 30 iterations from a sufficiently bad start, not with a
  competing, equally-good local optimum.)
This directly contradicted the comparison that had been driving the whole week's "ReLU anomaly" narrative:
  last Saturday's log claimed Remez's ~0.058 was "notably worse than the plateau-exploited CHEBYSHEV
  INTERPOLATION result from Tuesday (degree 12, error 0.008027)". Traced that 0.008027 figure back to its
  actual source today: it is SIGMOID's degree-12 Chebyshev-interpolation error on [-8,8] from Tuesday's
  session, not ReLU's -- I mis-attributed a number from one activation function's results table to a
  different activation function while writing that session's summary. Verified the ACTUAL ReLU Chebyshev-
  interpolation errors directly: degree 6 -> 0.2166, degree 12 -> 0.1153, degree 13 -> 0.1785 (non-monotonic,
  consistent with earlier observations, but nowhere near 0.008). Against the CORRECT baseline, Remez's 0.058
  is roughly 2x BETTER than degree-12 interpolation and 3x better than degree-13 interpolation -- exactly
  what minimax optimality guarantees (Remez's result must be <= any fixed-degree interpolation's error), not
  a violation of it.
Net correction to the week's record: there was no real "ReLU breaks Remez" phenomenon. There WERE two genuine
  implementation bugs (the v1 interior-point-removal bug and v2's edge case), correctly found and fixed along
  the way, and fixing them was worthwhile regardless -- but the specific conclusion drawn from the still-
  nonzero v3 error (0.058 "anomalously high") rested on comparing it to the wrong number. Once compared
  correctly, v3's Remez behaves exactly as approximation theory predicts, which also makes yesterday's
  literature check land differently in retrospect: Filip et al.'s observation that polynomial Remez is
  "usually robust" wasn't in tension with my finding after all -- it was correctly predicting today's result,
  and I just hadn't caught my own error yet when I read it.
Taught (about process, again): a week-long thread chasing a "finding" is itself a cautionary tale about re-
  verifying OLD numbers pulled into a NEW comparison, not just re-deriving new ones -- the actual bugs (v1,
  v2) were caught by careful re-verification; the bad REFERENCE number survived four separate sessions
  (Tue write-up error -> Wed, Fri, Sat, Sun all built on it) because none of those sessions re-checked the
  Tuesday number itself, only the new Remez numbers being compared against it. The fix going forward: when a
  "surprising" result rests on comparing today's number to a past session's number, re-derive the OLD number
  too, don't just trust the log.
Exercise: today's eight-initialization robustness test, plus the direct recomputation of ReLU's actual
  Chebyshev-interpolation errors at degrees 6/12/13, stood in as the exercise and is what surfaced the
  correction.
Asked: (1) this is a good concrete case study of exactly Question 2 from two sessions ago (proven/verified/
  conjectured scale for research claims) -- a "verified-by-reproduction" finding (ReLU anomaly, reproduced
  identically across three sessions) still turned out to rest on an unverified INPUT; does Parth's own
  practice re-check cited baseline numbers from his own past notes/code before building new comparisons on
  top of them, or is this a gap worth deliberately guarding against; (2) given the real, corrected picture is
  now "Remez robustly and correctly outperforms Chebyshev interpolation for ReLU, consistent with theory, no
  special kink-handling needed at degree 13 on this domain" -- does this change which of this week's
  downstream claims (the FHERMA submission-skeleton recommendation, the Ch19 reconciliation) need revisiting,
  or were those independent of the ReLU-specific error; (3) all earlier carried-forward questions remain
  unanswered and are carried forward without repeating the full list.
Answers: pending.
Weak spots: unmeasured across forty-two sessions (zero of ~68+ questions answered to date). This session is
  itself the clearest evidence yet of why that matters: an error persisted uncorrected for five days purely
  because nothing challenged it.
Revisit next time: open for redirect. Given today's correction, worth briefly re-auditing whether the FHERMA
  submission-skeleton recommendation (Wednesday) or the Ch19 reconciliation (Thursday) relied on the bad ReLU
  number anywhere -- a quick check, not a full redo, since both were primarily about sigmoid/GELU plateau
  exploitation, which never depended on the ReLU comparison.

## 2026-10-05 — Research-gap-finder pass on Parth's actual thesis question (ppml-research-assistant, Mode 2)
Curriculum (book), FHERMA arc, and review cycle have all reached natural closure points over the past two
  weeks, so pivoted today's session to point the research tooling directly at Parth's stated PhD focus --
  depth-optimal polynomial approximation of activations -- rather than another derived exercise, using the
  ppml-research-assistant skill's Mode 2 (research gap finder) over Scholar Feed.
Searched four angles: (1) multiplicative-depth-aware polynomial activation approximation generally, (2)
  minimax/Remez + CKKS depth budget, (3) Paterson-Stockmeyer depth-table granularity/step-function degree
  selection specifically, (4) joint degree/depth/accuracy optimization for HE activations. Read full
  abstract+introduction+method+results for the single closest-matching paper found.
MOST DIRECTLY RELEVANT: Woo, Ryu, Kim, "Degree-Constrained Interval Optimization for Minimax Polynomial
  Approximation in Homomorphic Encryption" (arXiv 2607.08042, 2026) [Verified]. Confirms minimax/Remez IS the
  standard tool for HE activation approximation (matching this week's own rediscovery), and explicitly names
  the degree-vs-depth tension in its introduction ("a higher degree generally leads to a larger homomorphic
  evaluation cost... governed by... multiplicative depth... reducing the minimax error solely by raising the
  polynomial degree is often impractical"). BUT their actual method FIXES degree at a single value (degree 15,
  stated explicitly: "for each candidate radius rho, we compute the degree-15 minimax polynomial") and
  optimizes the approximation INTERVAL (a distribution-aware radius, connecting directly to this book's
  Ch18/19/27 R-calibration material) against that fixed degree -- a different, complementary axis from degree
  selection against a real per-library depth-cost table. No engagement found with the non-injective
  (step-function) structure of an actual Paterson-Stockmeyer depth table.
Also found and partially relevant but not on-point: Sisyphus (2107.12342, escaping-activation problem, a
  training-time issue not a degree/depth optimization one) [Verified]; several ReLU-polynomial-replacement
  papers (quadratic replacement, layerwise approximation, decision-aware replacement) that treat degree as a
  design choice tuned empirically against accuracy, without reasoning explicitly about depth-table granularity
  [Verified, surveyed abstracts only].
Searched specifically for "Paterson-Stockmeyer depth granularity / step-function degree selection" and "joint
  degree-depth-accuracy optimization" as direct, skeptical checks before concluding anything was missing
  (per the skill's explicit instruction) -- neither search surfaced a paper engaging with this specific
  framing; results were dominated by unrelated secure-computation/matrix-multiplication papers.
HONEST CONCLUSION (gap assessment, not a final verdict -- stated with appropriate hedging per the verification
  rules): across what was searched and read this session, no paper was found that explicitly treats a real
  library's non-injective degree-to-multiplicative-depth cost table as an exploitable structure -- i.e.
  "minimize degree" and "minimize depth" are treated as interchangeable (or depth is abstracted to the
  idealized ceil(log2(d+1)) formula) in the papers surveyed, rather than distinguished via an actual
  implementation's step-function table the way this week's direct experimentation did. This is consistent
  with, not proof against, it being a genuine (if narrow) methodological contribution: combining (a) minimax
  fitting (standard, per Woo et al.) with (b) explicit degree selection at the TOP of a real depth-table
  plateau (apparently unaddressed) as a joint, two-part optimization specifically for HE deployment, layered
  on top of interval optimization (Woo et al.'s axis) rather than replacing it. A more thorough check (full
  related-work sections of the 15-20 nearest papers, not just abstracts) would be needed before treating this
  as confirmed novel -- today's search was a Mode-2 scoping pass, not an exhaustive related-work section.
Taught: the difference between "optimize the interval for a fixed degree" (Woo et al.'s axis, well-established
  and directly continuous with this book's Ch18/19/27 calibration material) and "optimize the degree itself
  against a real depth-cost table's granularity" (this week's own finding, not found addressed elsewhere) --
  these are orthogonal levers on the same underlying problem, and a real contribution would likely need to
  combine both rather than present the depth-plateau insight alone as sufficient.
Exercise: the search-and-read process above, including the two skeptical "is this already solved" searches,
  stood in as today's exercise.
Asked: (1) does this gap assessment match what Parth already knows of the field -- is Woo et al. (very recent,
  2026) already on his radar, and does his own related-work search turn up anything closer to the plateau-
  exploitation idea that Scholar Feed's semantic search missed; (2) if this gap holds up under a fuller check,
  the natural next step is a small controlled experiment -- combining Woo et al.'s interval optimization with
  plateau-aware degree selection on a real OpenFHE depth table and measuring whether the combination beats
  either lever alone -- is this worth scoping as an actual short paper/workshop contribution rather than a
  curiosity; (3) all earlier carried-forward questions remain unanswered and are carried forward without
  repeating the full list.
Answers: pending.
Weak spots: unmeasured across forty-three sessions (zero of ~71+ questions answered to date).
Revisit next time: open for redirect -- this is the first session in the whole 43-session run aimed squarely
  at producing something potentially useful for Parth's actual thesis rather than teaching/reviewing the book,
  so a response here (even a one-line "yes, already known" or "worth pursuing") would be unusually high-value
  if it ever comes. Absent one, next session could deepen this specific gap check (full related-work sections,
  not just abstracts) or return to the daily-habit format on a different thread.

## 2026-10-06 — Deepening the gap check: related-work section, citations, and foundational lineage
Continued yesterday's scoping pass with the deeper check it called for: read Woo et al.'s (2607.08042) full
  related-work and conclusion sections, checked its citation count (new paper, zero citations yet, as
  expected), and pulled its foundational lineage (the niche-specific prior art the paper's neighborhood
  actually builds on, not just generic HE landmarks).
STRONGEST new evidence, directly from the paper's own conclusion [Verified]: Woo et al. explicitly name their
  own open future work as "[i]ntegration of the proposed framework into end-to-end HE-based neural network
  inference, including... actual HE evaluation costs under SPECIFIC CRYPTOGRAPHIC LIBRARY IMPLEMENTATIONS...
  is an important direction for future investigation that builds upon the analytical foundation established
  here." This is the paper closest to this week's finding explicitly stating that connecting their
  (interval-optimization) framework to real per-library depth costs has NOT been done yet, by their own
  account -- meaningfully stronger evidence for the gap than yesterday's inference from silence.
Closest adjacent prior art found via foundational-lineage search: Ao & Boddeti, "AutoFHE: Automated Adaption
  of CNNs for Efficient Evaluation over FHE" (arXiv 2310.08012, 2023, 53 citations, highest-lift niche root for
  this specific sub-field) [Verified]. AutoFHE jointly optimizes LAYERWISE mixed-degree polynomials against
  BOOTSTRAPPING-OPERATION COUNT via a multi-objective evolutionary search (NSGA-II-style Pareto fronts,
  crossover/mutation over per-layer polynomial degree) across an entire CNN -- genuinely related (degree
  selection jointly with a real HE cost proxy) but at a different granularity (whole-network bootstrap
  scheduling, not a single activation's exact multiplicative-depth table) and with a different fitting method
  (their own co-evolved "EvoReLU" composite polynomials, not explicit Remez minimax). Degree mutations in their
  evolutionary search could implicitly land on plateau-respecting degrees through the fitness landscape, but
  the paper does not discuss or exploit the step-function structure explicitly, and does not combine it with
  true minimax fitting the way this week's exploration did.
Refined gap statement after the deeper check: the specific combination -- (a) reading a real library's
  degree-to-multiplicative-depth table as a step function with exploitable plateaus, for (b) a SINGLE
  activation function, fit via (c) true Remez minimax at the top of the relevant plateau -- still does not
  appear addressed by the two closest papers found (Woo et al.: interval optimization at one fixed degree, no
  depth-table engagement, explicitly flagged as future work in their own conclusion; AutoFHE: joint degree/
  bootstrap-count search at network granularity, different fitting method, no explicit plateau discussion).
  This is now a better-supported gap claim than yesterday's (inference from absence); it is supported by a
  direct quote from the nearest paper's own stated limitations.
Taught: the difference between "didn't find it" (yesterday, weaker) and "the closest paper says they haven't
  done it yet" (today, stronger) as evidence for a research gap -- the skill's own Mode 2 instructions flag
  exactly this distinction (rule 6: "flag if a gap might actually be solved work you haven't found yet --
  search before claiming absence"), and today's deeper pass is what that instruction is for.
Exercise: today's related-work/citations/lineage search stood in as the exercise.
Asked: (1) given AutoFHE is the closest adjacent prior art and uses evolutionary search rather than Remez,
  is there a principled reason to prefer exact minimax fitting at a depth-table-aware degree over an
  evolutionary/co-evolved approach for a SINGLE activation (interpretability and reproducibility of the
  exact minimax solution, vs. AutoFHE's advantage of jointly handling many layers at once) -- this seems like
  the right framing question if Parth wants to scope a contribution relative to both nearest papers rather
  than just one; (2) is AutoFHE itself already known to Parth, given it is the single most load-bearing
  adjacent paper in this specific niche (highest lift score of anything found across two sessions of
  searching); (3) all earlier carried-forward questions remain unanswered and are carried forward without
  repeating the full list.
Answers: pending.
Weak spots: unmeasured across forty-four sessions (zero of ~74+ questions answered to date).
Revisit next time: open for redirect. The gap-finder thread now has two sessions of increasingly well-
  supported evidence behind it (Woo et al.'s explicit future-work admission is the strongest single piece);
  a natural next step if continuing would be scoping the actual small experiment proposed yesterday (combine
  Woo et al.'s interval optimization with plateau-aware degree selection on a real OpenFHE table, measure the
  combination against each lever alone) rather than further literature searching, since the literature check
  itself has reached diminishing returns without Parth's input on which direction he'd actually want to take it.

## 2026-10-07 — The actual experiment: combining plateau-aware degree selection with Woo et al.'s interval optimization
Moved from literature search to the small constructive experiment proposed two sessions ago, since the lit
  check had reached diminishing returns without Parth's input. Built, for sigmoid under a standard-normal
  pre-activation distribution (matching Woo et al.'s experimental setup) at a FIXED depth budget (5
  multiplicative levels, plateau degrees 6-13 per OpenFHE's real table): a distribution-weighted MSE objective
  combining within-interval minimax-fit error and outside-interval extrapolation error, both density-weighted
  -- a simplified stand-in for Woo et al.'s DEF/DEP framework (their actual clipping-polynomial construction
  was not reproduced; noted explicitly as a simplification, not a replication).
First attempt had a real design flaw, caught and fixed before trusting the result: the initial "interval-
  optimization-only" condition held degree FIXED AT 13, which is itself the top of the depth-5 plateau -- not
  a fair isolation of the interval-optimization lever alone, since it was unintentionally already plateau-aware.
  Corrected by re-running with degree fixed at 7 (matching the naive baseline) for the interval-optimization-
  only condition, to properly isolate what each lever contributes.
Four conditions at the IDENTICAL multiplicative depth (5 levels, zero cost difference between any of them):
  - naive (degree 7, fixed interval [-8,8], matching this week's earlier naive baseline): MSE = 1.78e-4
  - interval optimization ALONE (Woo et al.'s lever: degree fixed at 7, radius optimized, R*=4.0): MSE =
    9.08e-7 -- a ~196x improvement over naive, confirming Woo et al.'s actual contribution is real and
    substantial on its own.
  - plateau-aware degree selection ALONE (this week's lever: degree optimized within the plateau, interval
    fixed at [-8,8]): MSE = 1.79e-6 -- a ~100x improvement over naive on its own.
  - COMBINED (both optimized jointly: degree*=13, R*=5.0): MSE = 5.55e-9 -- a further ~164x improvement
    beyond interval-optimization alone, and ~32,000x total improvement over the naive baseline, all at
    ZERO additional multiplicative depth versus every other condition.
This is a clean, honest confirmation of the gap-finder hypothesis from the last two sessions: plateau-aware
  degree selection is a genuinely ADDITIONAL, non-redundant lever on top of Woo et al.'s interval optimization
  (the closest published technique), not something their method already captures implicitly. The two levers
  compound rather than overlap, because they attack different parts of the same objective -- interval
  optimization trades within-interval accuracy against out-of-interval blowup for a FIXED degree; plateau
  selection extracts free accuracy from degrees that cost identical depth, independent of interval choice.
Taught: the value of building the smallest experiment that actually tests a hypothesis, including deliberately
  checking the experiment's OWN validity (the degree=13-vs-degree=7 fixed-degree flaw) before trusting its
  output -- the same self-correction discipline from Monday's ReLU-anomaly session, applied prospectively this
  time (caught during construction) rather than retrospectively (caught after a week of believing a wrong
  number).
Exercise: today's four-condition experiment, including the self-caught design flaw and its fix, stood in as
  the exercise.
Asked: (1) this result (now a genuine constructive finding, not just a literature gap) seems like the clearest
  candidate yet across 45 sessions for something directly usable in Parth's actual thesis work -- does this
  specific experimental design (distribution-weighted MSE, fixed depth budget, joint degree+interval search)
  match how he'd want to frame it, or would a real thesis-grade version need a different objective/setup;
  (2) the simplification versus Woo et al.'s actual DEP-based out-of-interval handling (raw extrapolation vs.
  their clipping-polynomial construction) -- is this gap large enough to matter for a real comparison, or
  reasonable for a first-pass sanity check; (3) all earlier carried-forward questions remain unanswered and
  are carried forward without repeating the full list.
Answers: pending.
Weak spots: unmeasured across forty-five sessions (zero of ~77+ questions answered to date).
Revisit next time: open for redirect -- this is now a complete, self-contained, three-session arc (gap search
  -> deepened gap search -> constructive experiment confirming the gap) with a genuinely compelling headline
  number (32,000x MSE improvement, zero extra depth) ready to show Parth if he engages. Absent a redirect,
  natural next steps: extend the experiment to GELU/tanh (matching Woo et al.'s other tested functions) for
  robustness, or implement Woo et al.'s actual DEP clipping construction properly rather than the simplified
  stand-in used today.

## 2026-10-08 — RESTART: curriculum pacing reset to Chapter 1 (Session 1 of a new cycle)
Genuine live instruction from Parth (first direct message since the engagement began): "Reset it and let's
  start from scratch." Clarified scope before acting, given the ambiguity and irreversibility risk -- asked
  whether this meant restarting curriculum pacing only, wiping study-log.md, or a full branch/log reset.
  Parth chose: restart curriculum pacing only. This log, the git branch, and all 45 prior sessions' history
  (full book coverage, the FHERMA/Remez week, the research-gap-finder arc) are explicitly KEPT, not wiped.
  This entry marks the start of a new teaching cycle beginning again at Chapter 1, per that instruction.
Re-read Chapter 1 (Modular Arithmetic and Algebraic Structures) fresh from fhe-book.html, as required --
  did not teach from memory of the first cycle's Ch1 session.
Verified live, fresh (not reused from the original Ch1 session, which is many weeks and a full cycle old):
  - Ran tier0_math/ex01_modular_arith.py: 16/16 checks pass (mod arithmetic, CRT reconstruction, NTT/INTT
    round-trip, NTT-convolution-theorem equivalence over 20 random pairs, and the negacyclic-vs-cyclic
    root-order rejection check).
  - Transcribed and ran Chapter 1's own Artifact 1.1 verbatim: RNS reconstruct (12345*6789+12345 mod
    17*19*23) = 1143, matching direct computation exactly; primitive 8th root of unity mod 17 found as 9,
    confirmed omega^8 = 1 mod 17; NTT-based cyclic convolution matched schoolbook O(N^2) convolution exactly
    on a random length-8 instance.
  - Verified Theorem 1.4's Gaussian tail bound (P(|X|>t*sigma) <= 2e^(-t^2/2)) numerically for t=1..4 --
    holds as a valid (non-tight) upper bound throughout, consistent with the book's own framing of it as a
    provable correctness/security budget rather than an exact tail probability.
Taught (fresh, this cycle): Z_q's group/ring/field structure and why q is chosen prime (Theorem 1.1: units
  exist iff gcd(a,q)=1, hence Z_q is a field iff q is prime); the Chinese Remainder Theorem as a ring
  isomorphism Z_q ~= Z_q1 x ... x Z_qk, and RNS as its direct engineering payoff (big-integer arithmetic on a
  500-bit modulus becomes independent machine-word arithmetic on ~9 limbs, parallelizable and SIMD-friendly --
  except division/comparison, which don't factor componentwise, forcing the RNS-BFV/RNS-CKKS redesigns covered
  later); discrete Gaussian noise and why its exponential tail (not a bounded-uniform alternative) is load-
  bearing for BOTH the correctness budget (Chapter 4, 5, 7) and the LWE hardness reduction itself (Chapter 4);
  the NTT as a finite-field FFT, requiring an N-th root of unity in F_q (hence N | q-1, the "NTT-friendly
  modulus" condition used throughout the book), collapsing polynomial multiplication from O(N^2) to O(N log N)
  -- concretely a ~2000x operation-count gap at N=2^15, the single largest algorithmic factor making FHE usable
  at all; the negacyclic-vs-cyclic pitfall (X^N+1 vs X^N-1) as a classic silent-sign-bug source, flagged for
  when Chapter 2 formalizes the ring R_q.
Exercise: ex01_modular_arith.py (run and verified above) plus Chapter 1's own Artifact 1.1 (reproduced from the
  book's text and run independently, both agreeing).
Asked (first questions of the new cycle, replacing rather than adding to the unanswered backlog from cycle 1
  -- noting the full prior backlog, ~77+ questions across 45 sessions, remains in this log's history above but
  is not being re-asked here since the format is restarting): (1) why must N specifically be a power of two for
  the clean log_2(N)-stage NTT recursion Chapter 1 describes -- what would break (not just "be less elegant")
  if N were, say, 12; (2) the chapter notes RNS breaks down for division/comparison -- can you name a concrete
  FHE operation (from what you already know, or a guess) that needs one of those, to connect this forward to
  why rescaling/mod-switching get their own chapters later; (3) Theorem 1.4's tail bound is stated with a
  slack (non-tight) constant -- does a looser-than-necessary provable bound ever cost you something concrete
  in parameter selection, or is slack always just "free" conservatism with no downside?
Answers: pending (session just started).
Weak spots: n/a yet this cycle -- tracking restarts here.
Revisit next time: Chapter 2 (Polynomial Rings and Cyclotomic Fields), continuing the new cycle. The full
  45-session history above remains the project's memory of what's already been explored in depth (FHERMA/
  Remez, the research-gap-finder thread); this restart is specifically about teaching pace/sequence, not
  erasing that context.
