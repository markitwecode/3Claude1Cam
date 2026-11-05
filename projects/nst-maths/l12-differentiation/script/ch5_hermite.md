# Chapter 5 · Hermite polynomials

NST IA Mathematics, Lecture 12 (Differentiation), part 5 of 7. Source: Berloff's notes, Chapter234_to_annotate.pdf pp. 62–63 (Example 42 and the box of the first few H_n; the lecturer's two corrections, frames 46:50 and 47:20); lecture 42:36–47:26; Examples Sheet I, I1 (p. 11).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch5_s1_hook)

> Title card: "Differentiation", "NST IA Mathematics · Lecture 12", "Part 5 · Hermite polynomials".
> On {last}, part four's Leibniz sum card returns in ch4 s4's exact styling, `(fg)^(n) = Σ_{m=0}^{n} (n choose m) f^(n−m) g^(m)` (f BLUE, g PURPLE, the binomial coefficient YELLOW), with ch4's small YELLOW Pascal's triangle beside it (owner ch4_s3_pattern; as ch4_s4_formula leaves it, rows 0 to 3: `1` / `1 1` / `1 2 1` / `1 3 3 1`). On {when}, both shrink into the top-right corner and stay parked there until scene 4 pulls them back.
> On {quantum}, a faint preview of scene 6's four stacked oscillator plots with the caption "quantum mechanics"; it fades on {define}.
> On {define}, a green-bordered card headed "Example 42: Hermite polynomials", as the notes draw it (p62). Inside it the definition assembles from the inside out: on {gauss}, `e^{−x²}` (PURPLE); on {diff}, `dⁿ/dxⁿ ( … )` wraps it; on {front}, `e^{x²}` (GOLD) slides in front; on {sign}, `(−1)^n`, then `H_n(x) ≡` on the left. The finished line is the notes' verbatim: `H_n(x) ≡ (−1)^n e^{x²} dⁿ/dxⁿ (e^{−x²})`.
> On {claim}, under it on the card, the notes' sentence: "Show that the recursion relation H_{n+1} = 2xH_n − 2nH_{n−1} holds."
> On {question}, a YELLOW arrow from the dⁿ/dxⁿ in the definition down to the recursion, with a YELLOW "?" on it. Scene 2 keeps the definition line (the card shrinks to the top edge).

[c5.hook.1] {title} Welcome back. This is part five, on Hermeet polynomials. {last} Last time, Leibniz's formula gave the Nth derivative of a product, with the numbers from Pascal's triangle as its coefficients. {pause}

[c5.hook.2] {when} So when do you actually need an Nth derivative? {quantum} In quantum mechanics, for instance. {define} Example forty-two in the notes builds a family of polynomials. {gauss} Start with E to the minus ex squared. {diff} Differentiate it N times. {front} Multiply by E to the ex squared, {sign} and by minus one to the power N. That's the Hermeet polynomial H N.

[c5.hook.3] {claim} The example asks you to show that H N plus one equals two ex times H N, minus two times N, times H N minus one. {question} So how does a definition full of derivatives become a rule that builds each polynomial from the two before it? {pause}

## Scene 2 · The definition at work (ch5_s2_define)

> The definition line from scene 1 sits along the top (same object; e^{x²} GOLD, e^{−x²} PURPLE throughout the chapter).
> On {gauss}, small axes at left: the PURPLE bell curve y = e^{−x²}, labelled "Gaussian". On {inverse}, the GOLD e^{x²} pulses, and `e^{x²} · e^{−x²} = 1` appears under the axes, each factor in its colour.
> Centre-right, a table with three rows (n = 0, 1, 2) and three columns headed `dⁿ/dxⁿ e^{−x²}`, `× (−1)^n e^{x²}`, `H_n`. Row n = 0, on {zero}: `e^{−x²}`; on {one0}, the GOLD and PURPLE factors meet and vanish together → `H_0 = 1`.
> Row n = 1, on {first}: `−2x e^{−x²}` (small tag "chain rule, part 2"). On {hone}, `× (−1) e^{x²}`: GOLD and PURPLE cancel, the two minus signs flash YELLOW and cancel → `H_1 = 2x`.
> Row n = 2, on {second}: a side line, the product rule on `−2x · e^{−x²}`; on {four}, `−2 e^{−x²} + (−2x)(−2x) e^{−x²}` → `(4x² − 2) e^{−x²}`; on {htwo}, the Gaussian cancels → `H_2 = 4x² − 2`.
> On {pattern}, the PURPLE e^{−x²} in every row of the middle column glows at once and the GOLD e^{x²} sweeps them off. On {lead}, the leading terms `1`, `−2x`, `4x²` light up in turn with "× (−2x)" arrows between them; on {flip}, `(−2)^n xⁿ` → `× (−1)^n` → `2ⁿ xⁿ` (YELLOW), caption "degree n".
> On {check}, the recursion with n = 1 put in: `H_2 = 2x·H_1 − 2·1·H_0 = 2x·2x − 2 = 4x² − 2`; on {tick}, a GREEN tick against row 2's H_2.
> On {ladder}, the three H_n slide right into a narrow card at the right edge, the H_n ladder: rungs from the bottom up, `H_0 = 1`, `H_1 = 2x`, `H_2 = 4x² − 2`, labels YELLOW, two empty rungs above them. The ladder stays on screen through scene 6. Every derivative and H_0 to H_2 checked with sympy 1.14.0.

[c5.def.1] {gauss} Look first at the function inside, E to the minus ex squared. Its graph is a bell-shaped curve, called a Gaussian. {inverse} The factor in front, E to the ex squared, is one over the Gaussian. So whenever a derivative is a polynomial times the Gaussian, the factor in front strips the Gaussian off.

[c5.def.2] {zero} Take N equal to zero first. With no derivatives, {one0} the two exponentials cancel, and H zero is one. {first} For N equal to one, the chain rule gives minus two ex, times the Gaussian. {hone} Multiply by E to the ex squared, and by minus one. The Gaussian goes, the minus signs cancel, and H one is two ex.

[c5.def.3] {second} For N equal to two, differentiate minus two ex, times the Gaussian, with the product rule. {four} You get minus two, times the Gaussian, plus four ex squared, times the Gaussian. {htwo} Strip off the Gaussian, and H two is four ex squared, minus two. {pause}

[c5.def.4] {pattern} So every derivative is a polynomial, times the Gaussian. {lead} Each one multiplies the highest power by minus two ex, {flip} and the minus one to the power N cancels all those minus signs. So H N is a polynomial of degree N, with leading coefficient two to the power N.

[c5.def.5] {check} Now test the claim with N equal to one. It says H two is two ex times H one, minus two times H zero. That's four ex squared, minus two. {tick} It matches. {pause} {ladder} These are the bottom rungs of a ladder, and the recursion is how we'll climb it.

## Scene 3 · Peel off one derivative (ch5_s3_peel)

> The definition line stays at the top, the ladder card at the right edge. Hero, centre: the notes' chain (p62), verbatim, one line per beat, each line under the last.
> On {goal}, a YELLOW `H_{n+1}` label appears centre, with an empty rung above H_2 on the ladder lighting faintly.
> On {write}: `H_{n+1} = (−1)^{n+1} e^{x²} d^{n+1}/dx^{n+1} (e^{−x²})`, copied out of the definition line (TransformFromCopy), every n turning into n + 1 with a YELLOW flash.
> On {split}: `= (−1)^{n+1} e^{x²} dⁿ/dxⁿ (d/dx e^{−x²})`: the d^{n+1}/dx^{n+1} splits into dⁿ/dxⁿ outside and d/dx inside; small tag "(112), part 4".
> On {chain}: `= (−1)^{n+1} e^{x²} dⁿ/dxⁿ (−2x e^{−x²})`; the inner d/dx e^{−x²} turns into −2x e^{−x²}, while scene 2's row n = 1 flashes on the ladder side. On {inside}, the bracket `(−2x e^{−x²})` is outlined.
> On {out}, the −2 lifts out of the bracket to the front; tag "constants come out: part 1". On {signs}, `(−1)^{n+1} · (−2)` sits alone; on {merge}, it becomes `2 · (−1) · (−1)^{n+1}` → `2 (−1)^{n+2}` → `2 (−1)^n`, the signs YELLOW.
> On {front}, the new line: `= 2(−1)^n e^{x²} dⁿ/dxⁿ (x e^{−x²})` (GOLD e^{x²}, PURPLE e^{−x²}), checked with sympy 1.14.0 against H_1 to H_5 from the definition.
> On {board}, a small inset beside it, in handwriting style: the lecturer's board at 45:01, `= −2(−1)^n e^{x²} dⁿ/dxⁿ (x e^{−x²})`, its leading − struck through in RED; an arrow points to the notes' next-page line `H_{n+1} = 2(−1)^n e^{x²}( … )` (p63). (Sympy: the board's −2(−1)^n gives −H_{n+1}. The planner re-checked the 45:01 frame in the continuity review: the board reads "= −2(−1)ⁿ e^{x²} dⁿ/dxⁿ(xe^{−x²})", and she says "minus 2, minus 1 to the power n" twice at 44:37, so the slip is real.)
> On {left}, `x e^{−x²}` is circled, as the lecturer circled it (frame 46:50), with x BLUE and e^{−x²} PURPLE and her labels "f" and "g" written above them. On {product}, a small × between x and e^{−x²} flashes. On {leibniz}, the parked Leibniz sum card in the corner pulses.

[c5.peel.1] {goal} Now the proof. We want H N plus one, so start from the definition with N plus one in place of N. {write} That's minus one to the power N plus one, times E to the ex squared, times the Gaussian differentiated N plus one times. {split} Split those derivatives into one first, then N more. That changes nothing.

[c5.peel.2] {chain} The first derivative we already know, from the chain rule: minus two ex, times the Gaussian. {inside} So now the Nth derivative acts on minus two ex, times the Gaussian. {out} The minus two is a constant, so it comes out in front, {signs} next to minus one to the power N plus one.

[c5.peel.3] {merge} Write minus two as two, times minus one. The minus ones make minus one to the power N plus two, which is minus one to the power N. {front} So the factor in front is two, times minus one to the power N. {board} If you copied minus two here from the board, that's a slip: the printed line on the next page has plus two. {left} What's left is the Nth derivative of ex, times the Gaussian. {product} That's a product, differentiated N times, {leibniz} which is exactly the job of Leibniz's formula. {pause}

## Scene 4 · Leibniz with a factor that runs out (ch5_s4_leibniz)

> Scene 3's last line `= 2(−1)^n e^{x²} dⁿ/dxⁿ (x e^{−x²})` shrinks to a strip under the definition at the top; the ladder card stays at the right edge.
> On {card}, part four's Leibniz sum card flies from the corner to the centre (same object, ch4 s4 styling). On {fg}, the notes' line "Defining f = x and g = e^{−x²}": x (BLUE) drops into the f slots, e^{−x²} (PURPLE) into the g slots, and the card reads `dⁿ/dxⁿ x e^{−x²} = Σ_{m=0}^{n} (n choose m) f^(n−m) g^(m)`.
> On {terms}, the sum unrolls into a row of its n + 1 terms: `(n choose 0) f^(n) g^(0) + (n choose 1) f^(n−1) g^(1) + … + (n choose n−1) f^(1) g^(n−1) + (n choose n) f^(0) g^(n)`, binomial coefficients YELLOW. On {ask}, a YELLOW "?" over the row.
> On {runs}, a small BLUE derivative chain for f under the row: `x → 1 → 0 → 0 → …`, with the lecturer's margin note `f^(m) = 0, m > 1` (frame 46:50; the notes say "f^(k) = 0 for k > 1"). On {dead}, every term up to and including the one with f^(2) is struck through in RED and dims, "= 0" under them; on {two}, the last two terms stay bright.
> On {row}, part four's Pascal's triangle (owner ch4_s3_pattern, rows 0 to 3 as in scene 1, YELLOW) appears small at left and grows one new row in the same style, row 4 `1 4 6 4 1` (ch4 never built it); row four lights, all but its last two entries dim, and `4 1` are labelled `(4 choose 3) = 4`, `(4 choose 4) = 1` ("row n = 4").
> On {coef}, the first survivor resolves: `(n choose n−1)` → `n`, `f^(1)` → `1`, leaving `n g^(n−1)`. On {second}, the second: `(n choose n)` → `1`, `f^(0)` → `x`, leaving `x g^(n)`. On {typo}, a small inset of the notes' printed `(n choose 0) f^(0) g^(n)`, its 0 overwritten by a handwritten n and "= 1" written above, as on the lecturer's page (frame 47:20).
> On {result}, the notes' line (p63) verbatim: `= n d^{n−1}/dx^{n−1} e^{−x²} + x dⁿ/dxⁿ e^{−x²}` (x BLUE, e^{−x²} PURPLE), checked with sympy 1.14.0 for n = 1 to 6.
> On {compare}, a thumbnail of part four's worked example (ch4 s5, (x² e^{−x})^(n)) with its three surviving terms, beside this row with two; caption "x²: three terms · x: two terms".

[c5.leib.1] {card} Here's Leibniz's formula from part four. {fg} Let ex be the first function, F, in blue, and the Gaussian the second, G, in purple. {terms} The sum has N plus one terms. The term labelled M differentiates the Gaussian M times, and ex the other N minus M times. {ask} How many of those terms survive? {pause}

[c5.leib.2] {runs} Ex runs out fast. Its first derivative is one, and every derivative after that is zero. {dead} So every term that differentiates ex twice or more is zero. {two} Only the last two terms survive: the one where ex is differentiated once, and the one where it's left alone. {row} In the row of Pascal's triangle, only the last two numbers are used, N and one.

[c5.leib.3] {coef} In the first survivor, ex is differentiated once, to give one, and the Gaussian N minus one times. Its coefficient is N choose N minus one, which is N. {second} In the second, ex stays as it is, and the Gaussian gets all N derivatives. Its coefficient is N choose N, which is one. {typo} The notes print N choose zero here. The lecturer corrected it to N choose N, though both equal one.

[c5.leib.4] {result} So the Nth derivative of ex times the Gaussian has two terms: N times the Gaussian differentiated N minus one times, plus ex times the Nth derivative of the Gaussian. {compare} In part four's example, ex squared survived two derivatives, and three terms were left. Ex survives one, so two are left here.

## Scene 5 · Assemble the recursion (ch5_s5_assemble)

> On {back}, scene 3's strip and scene 4's two-term result slide toward the centre. On {insert}, scene 3's strip `2(−1)^n e^{x²} dⁿ/dxⁿ (x e^{−x²})` returns to the centre and its `dⁿ/dxⁿ (x e^{−x²})` is replaced by scene 4's two-term result (TransformFromCopy), giving the notes' "and so" line (p63) verbatim: `H_{n+1} = 2(−1)^n e^{x²} (x dⁿ/dxⁿ e^{−x²} + n d^{n−1}/dx^{n−1} e^{−x²})` (x BLUE, e^{x²} GOLD, e^{−x²} PURPLE).
> On {firstterm}, the first term lights and its x moves out to sit beside the 2: `2x · (−1)^n e^{x²} dⁿ/dxⁿ e^{−x²}` (x stays BLUE). On {match}, the definition line at the top slides down beside it and the matching factors flash in pairs; on {hn}, they collapse into `H_n`: the first term is `2xH_n`.
> On {secondterm}, the second term lights: `2n · (−1)^n e^{x²} d^{n−1}/dx^{n−1} e^{−x²}`. Under it, the definition with n − 1 in place of n: `H_{n−1} = (−1)^{n−1} e^{x²} d^{n−1}/dx^{n−1} (e^{−x²})`.
> On {mismatch}, the two sign powers `(−1)^n` and `(−1)^{n−1}` flash YELLOW. On {move}, `(−1)^n = −(−1)^{n−1}` appears and the extra − (YELLOW) slides out to the front. On {minus}, the second term becomes `−2nH_{n−1}`, its − still YELLOW. On {whence}, that YELLOW − flies into place in `= 2xH_n − 2nH_{n−1}`.
> On {result}, the notes' last line `= 2xH_n − 2nH_{n−1}` completes, then `H_{n+1} = 2xH_n − 2nH_{n−1}` alone, in a YELLOW box with a small caption "n ≥ 1". On {holds}, the claim on scene 1's Example 42 card (shown small) gets a GREEN tick.
> Every line checked with sympy 1.14.0: the recursion against H_0 to H_5 from the definition, n = 1 to 4, and the sign step (−1)^{n+1}·(−2) = 2(−1)^n, 2n(−1)^n = −2n(−1)^{n−1}.

[c5.build.1] {back} Now put the pieces together. {insert} In H N plus one, replace that Nth derivative with the two surviving terms, the ex term first. In front, two, times minus one to the power N, times E to the ex squared, stays as it was.

[c5.build.2] {firstterm} Take the first term, and bring its ex out front, next to the two. {match} What's left is minus one to the power N, times E to the ex squared, times the Nth derivative of the Gaussian. {hn} That's the definition of H N, exactly. So the first term is two ex times H N.

[c5.build.3] {secondterm} The second term has the Gaussian differentiated N minus one times, so it should give H N minus one. {mismatch} But H N minus one carries minus one to the power N minus one, and here we have minus one to the power N. {move} They differ by one factor of minus one. Take it out front, {minus} and the term becomes minus two times N, times H N minus one. {pause}

[c5.build.4] {whence} That's where the minus sign in the recursion comes from. {result} So H N plus one equals two ex times H N, minus two times N, times H N minus one. {holds} It holds for every N from one up, as the example claimed. {pause=1.5}

## Scene 6 · Climb the ladder (ch5_s6_ladder)

> The boxed recursion from scene 5 sits top-centre; on {climb}, the ladder card moves to centre-left and grows: rungs H_0, H_1, H_2 filled, H_3 and H_4 empty.
> On {three}, n = 2 put into the box: `H_3 = 2x·H_2 − 4·H_1`. On {expand}, `2x(4x² − 2) = 8x³ − 4x` and `4·2x = 8x`, each factor copied from its rung (TransformFromCopy). On {hthree}, `H_3 = 8x³ − 12x` fills the next rung.
> On {typo}, an inset of the notes' box (p63), verbatim: "The first few Hermite polynomials are H_0 = 1, H_1 = 2x, H_2 = 4x² − 2, H_3 = 8x³ − 12, H_4 = 16x⁴ − 48x² + 12, …", with "8x³ − 12" outlined RED and the lecturer's handwritten x added after the 12 (frame 47:20).
> On {parity}, the rungs get tags: H_0 and H_2 "even powers only", H_1 "odd powers only". On {odd}, `2x·H_2` and `H_1` both light with "odd" tags, and H_3's rung gets "odd powers only"; the RED "− 12" in the inset gets a RED cross.
> On {four}, n = 3: `H_4 = 2x·H_3 − 6·H_2`, with `2x(8x³ − 12x) = 16x⁴ − 24x²` and `6(4x² − 2) = 24x² − 12`. On {hfour}, `H_4 = 16x⁴ − 48x² + 12` fills the top rung; on {notypo}, the notes' H_4 in the inset gets a GREEN tick, caption, the lecturer's words: "This is not the typo". (Sympy 1.14.0: H_0 to H_4 all match the definition; the misprinted 8x³ − 12 would give a wrong H_4 with a −24x term.)
> On {why}, the ladder slides left. On {osc}, four stacked plots appear on the right, `H_n(x) e^{−x²/2}` for n = 0, 1, 2, 3 (BLUE curves, unnormalised, each scaled to the same height, x from about −4 to 4), each labelled with its n; caption `H_n(x) e^{−x²/2}` with e^{−x²/2} PURPLE. On {zeros}, each curve's zero crossings get YELLOW dots: none; one at 0; two at ±1/√2; three at 0 and ±√(3/2) (sympy).
> On {packet}, a caption under the plots, the lecturer's words: "localized packets of the wave function".

[c5.ladder.1] {climb} Now climb the ladder. Pause the video, and try H three yourself first. {pause=1.5} {three} Put N equal to two. H three is two ex times H two, minus four times H one. {expand} Two ex times H two is eight ex cubed, minus four ex. Four times H one is eight ex. {hthree} Take that away, and H three is eight ex cubed, minus twelve ex.

[c5.ladder.2] {typo} The notes print H three as eight ex cubed, minus twelve, without the ex. The lecturer corrected it. {parity} You can catch that by eye. H zero and H two have only even powers, and H one only odd ones. {odd} Two ex times H two, and H one, both have only odd powers, so H three must too. A lone twelve can't belong.

[c5.ladder.3] {four} One more step up the ladder. H four is two ex times H three, minus six times H two. {hfour} That gives sixteen ex to the fourth, minus forty-eight ex squared, plus twelve. {notypo} That matches the notes, and the lecturer checked it: this one is not a typo.

[c5.ladder.4] {why} So why do physicists care? {osc} Multiply H N by E to the power minus ex squared over two, and you get the wave functions of the quantum harmonic oscillator, the quantum version of a mass on a spring. {zeros} The first is a single bump, and each one after it crosses zero once more. {packet} In the lecturer's words, they're localised packets of the wave function.

## Scene 7 · Recap (ch5_s7_recap)

> On {recap}, four small panels (2 × 2) appear, each a miniature of the visual that taught it, same objects and colours, with its sentence's short line under it; each lights on its mark while the others dim.
> On {r1}, from scene 2: row n = 2 of the table, `(4x² − 2) e^{−x²}` times GOLD `e^{x²}`, the PURPLE Gaussian cancelling → `H_2 = 4x² − 2`. Line: "polynomial × Gaussian, Gaussian removed".
> On {r2}, from scene 3: `d^{n+1}/dx^{n+1}` splitting into `dⁿ/dxⁿ (d/dx …)`, ending at `2(−1)^n e^{x²} dⁿ/dxⁿ (x e^{−x²})`. Line: "peel off one derivative".
> On {r3}, from scene 4: the row of terms with all but the last two struck through in RED, and Pascal's row `1 4 6 4 1` with `4 1` lit (YELLOW). Line: "x runs out: two terms".
> On {r4}, from scenes 5 and 6: the YELLOW-boxed `H_{n+1} = 2xH_n − 2nH_{n−1}` above the full ladder card, H_0 to H_4. Line: "the recursion builds the ladder".
> On {sheet}, the panels clear for the I1 card (this scene owns it), in the series' question-card style that ch3 s7's H4 card set: a rounded rectangle with a DIM border, the label "I1" in YELLOW at the top left, the sheet's text in white under it, course colours only inside the maths, about two thirds of the frame wide. The text verbatim from Examples Sheet I (p. 11) but with "Leibniz" spelled as the series does: "I1. Use Leibniz's formula to establish that Z_n ≡ dⁿ/dxⁿ e^{−x²/2} is a solution of the differential equation d²Z_n/dx² + x dZ_n/dx + (n + 1)Z_n = 0." (e^{−x²/2} PURPLE). Part seven reuses this card (ch7 s5). Hint lines under it: on {gdef}, `g = e^{−x²/2}`; on {gprime}, `g′ = −x g` (checked with sympy 1.14.0); on {hint}, `differentiate n + 1 times: Leibniz on x g`, with a small "two terms" tag pointing back at the r3 miniature.
> On {next}, the card clears; the notes' stationary-point figure fades in, as part six's hook draws it (owner ch6_s1_hook: the BLUE curve with y′ = (x + 2)(x + ½)(x − 3/2)², x from about −2.6 to 2.5, no labels yet), and on {shape} small YELLOW dots land on its maximum and minimum.
> End card: hold for about eight seconds after the last word; the music carries it.

[c5.recap.1] {recap} Time for a recap. {r1} Every derivative of the Gaussian is a polynomial times the Gaussian, and the factor in front removes the Gaussian. {r2} To get the recursion, peel off one derivative, and you're left with ex times the Gaussian. {r3} Ex runs out after one derivative, so Leibniz's sum keeps just two terms. {r4} Those two terms give the recursion, and the recursion builds the whole ladder. {pause}

[c5.recap.2] {sheet} Sheet question eye one uses the same trick. {gdef} Write G for E to the power minus ex squared over two. {gprime} Its derivative is minus ex, times G. {hint} Differentiate that equation N plus one times, using Leibniz on the right, and again only two terms survive. {pause}

[c5.recap.3] {next} Next time, we go back to graphs, {shape} and see what the derivatives tell you about the shape of a curve. {pause}
