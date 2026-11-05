# Chapter 4 · Leibniz's formula

NST IA Mathematics, Lecture 12 (Differentiation), part 4 of 7. Source: notes `Chapter234_to_annotate.pdf` pp. 59–62 (§4.8 (112) and its Note, the x³ chain; §4.9 Leibniz's formula: p. 60's blank and the top of p. 61 were filled on the board, frames 36:25 and 38:55; the proof by induction (114) and Pascal's rule, with her heading "Proof by induction: ① For n = 1" and margin note "m = n", frame 41:00); lecture recording 31:39–32:44 and 33:50–42:36 ((113), 32:44–33:50, is in part six). Every formula and number checked with sympy 1.14 (Python 3.11).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch4_s1_hook)

> On {title}: the title card, "Differentiation", "NST IA Mathematics · Lecture 12", "Part 4 · Leibniz's formula".
> On {last}: last time, small and side by side: part three's circle (owner ch3_s3_circle: centre (1, 0), radius 3, BLUE, the dashed line at x = 2.8 with GREEN tangent lines at (2.8, ±2.4)) and part three's swapped-axes thumbnail of Figure 29 (owner ch3_s6_reciprocal: y = x³ at (1, 1), slope 3, reflected in the dashed y = x into the cube root, slope ⅓). Both fade on {once}.
> On {once}: part two's product rule, centred: `(fg)' = f'g + fg'`, f BLUE and g PURPLE (the role colours for the whole chapter). On {ten}: below it, `\frac{d^{10}}{dx^{10}}\left(x^2 e^{-x}\right) = \;?`, x² BLUE, e^{−x} PURPLE, the "?" YELLOW.
> On {double}: a branching tree grows down from `fg`: two branches (`f'g`, `fg'`), then four, then eight, the labels shrinking to dots as it widens; a branch where the new prime lands on f is BLUE, one where it lands on g is PURPLE. A GOLD counter beside it ticks "2, 4, 8, …" and lands on "1024" on {thousand} (2^10 = 1024; checked with sympy 1.14). This doubling tree comes back in s3.
> On {ask}: the tree dims; the question in YELLOW: "a formula for the nth derivative of a product?" On {hands}: a small row of stick-figure hands, some raised and some down, and her line in quotes: "at least I'll tell you something new today".

[c4.hook.1] {title} This is part four of Differentiation. {last} Last time, you differentiated equations as they stand, like the equation of a circle, and met the reciprocal rule for inverse functions. {pause}

[c4.hook.2] {once} This time, take a product and differentiate it again and again. Once is easy. That's the product rule, from part two. {ten} But what about ten times? Take the tenth derivative of ex squared, times E to the minus ex. {pause}

[c4.hook.3] {double} Apply the product rule blindly, and every term splits into two each time. Two terms, then four, then eight. {thousand} After ten rounds, over a thousand. {pause}

[c4.hook.4] {ask} So here's the question. Is there a formula for the Nth derivative of a product? {pause} {hands} When the lecturer asked, some of the room had seen one. As she put it, at least she could tell the others something new today.

## Scene 2 · Again and again (ch4_s2_higher)

> On {nth}: top centre, (112) `\frac{d^n y}{dx^n}` with a DIM "(112)" and the label "the nth derivative". On {recursive}: beside it, `\frac{d^n y}{dx^n} \equiv \frac{d}{dx}\left(\frac{d^{n-1} y}{dx^{n-1}}\right)`. On {linear}: a small tag under it, "linear: sums split, constants come out".
> On {chain}: the top shrinks to a strip. Below it, the x³ derivative-chain card that part one started (ch1 s3: `x^3 \to 3x^2`, top-left), in its styling, now built out link by link: `x^3` (BLUE) → `3x^2` on {chain}, → `6x` on {second}, → `6` on {third}, → `0` on {fourth}, the derivatives GREEN; on {rest} a DIM tail "0, 0, 0, …". The card returns in this recap and in part six, beside x⁴'s.
> On {note}: the notes' grey Note box, verbatim: "Note: In general" over `\frac{d^n y}{dx^n} \equiv \left(\frac{d}{dx}\right)^n y \neq \left(\frac{dy}{dx}\right)^n`. On {apply}: the `\left(\frac{d}{dx}\right)^n` glows GREEN; on {power}: the `\left(\frac{dy}{dx}\right)^n` glows RED.
> On {six}: `6x` lifts off the chain card, GREEN, labelled "second derivative". On {square}: a copy of `3x^2` becomes `(3x^2)^2 = 9x^4` in RED, with a RED `\neq` between the two. (Checked with sympy 1.14: 6x and 9x⁴.)
> On {brackets}: everything dims except a small notation card: `f^{(n)} = \frac{d^n f}{dx^n}` (f BLUE, the bracketed n YELLOW). On {powernote}: beside it, DIM, `f^n` with the tag "a power". On {zero}: `f^{(0)} = f`. This card stays small in a corner through s6 and s7.

[c4.higher.1] {nth} First, the notation. Differentiate a function, then differentiate the result, and keep going. Do it N times, and you get the Nth derivative, written dee to the N of why, by dee ex to the N. {recursive} Each one is the derivative of the one before, a comment the lecturer called trivial. {linear} Like the first derivative, it's linear. Sums split up, and constants come out.

[c4.higher.2] {chain} Here's an example from part one, ex cubed. Its first derivative is three ex squared. {second} Differentiate again, and you get six ex. {third} Once more gives six. {fourth} The fourth derivative is the derivative of a constant, so it's zero, {rest} and so is every derivative after that.

[c4.higher.3] {note} The notes add a warning. In this notation, the power N sits on the operator. {apply} It means, apply dee by dee ex N times. {power} That's different from raising the first derivative to the power N. {six} For ex cubed, the second derivative is six ex. {square} The square of the first derivative is nine ex to the fourth. {pause}

[c4.higher.4] {brackets} There's also a shorter way to write it. The Nth derivative of a function F is F, with N in brackets up top. {powernote} Without the brackets, it would be a power. {zero} And F with zero in brackets is F differentiated zero times, which is F itself.

## Scene 3 · The pattern (ch4_s3_pattern)

> On {board}: her board (frame 36:25), rebuilt: at the top, "If `y(x) = f(x)\,g(x)` find `\frac{d^n y}{dx^n}`" (f BLUE, g PURPLE). A column of lines below it on the left; coefficients YELLOW throughout.
> On {first}: `y' = f'g + fg'`; on {ones}: a small YELLOW 1 over each term, copied to the right as the first row "1 1".
> On {second}: the hook's doubling tree returns for one level, under the y′ line: `f'g` branches into `f''g` and `f'g'` on {split}; `fg'` branches into `f'g'` and `fg''` on {split2} (BLUE branch where the prime lands on f, PURPLE where it lands on g). On {merge}: the two `f'g'` slide together into `2f'g'`. On {twos}: the line `y'' = f''g + 2f'g' + fg''` settles, and the row "1 2 1" is copied to the right.
> On {third}: `y''' = f'''g + 3f''g' + 3f'g'' + fg'''`, row "1 3 3 1". The three rows on the right now form a small triangle; on {what}: a YELLOW "?" over it.
> On {pascal}: a YELLOW frame round the triangle with her label "Pascal's triangle" (her board drew the frame in red; YELLOW here by the series palette). On {binom}: beside it, `(a+b)^1 = a + b`, `(a+b)^2 = a^2 + 2ab + b^2`, `(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3`, coefficients YELLOW.
> On {why}: the board lines dim. Two small splittings side by side: left, `f'g` → `f''g` and `f'g'` (BLUE arrow for the prime onto f, PURPLE arrow onto g); on {binom2}: right, `ab` times `(a + b)` → `a^2b` and `ab^2`. On {count}: the two trees flash together, the same shape.
> On {total}: GOLD sums beside the triangle's rows: `1 + 1 = 2`, `1 + 2 + 1 = 4`, `1 + 3 + 3 + 1 = 8`. On {ten}: row ten below, `1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1`, summing to the hook's GOLD "1024". (All checked with sympy 1.14.)

[c4.pattern.1] {board} So let's find the pattern, the way the lecturer did on the board. Call the product why, equal to F times G. {first} The first derivative is the product rule. F prime times G, plus F times G prime. {ones} Record the coefficients, one and one.

[c4.pattern.2] {second} Now differentiate again. Each piece is itself a product, so each one gets the product rule. {split} F prime times G gives F double prime times G, plus F prime times G prime. {split2} F times G prime gives F prime times G prime, plus F times G double prime. {merge} The two middle pieces are the same, so they combine. {twos} The coefficients are one, two, one.

[c4.pattern.3] {third} Once more, and the third derivative has coefficients one, three, three, one. {what} What's this? {pause} {pascal} A student called it out. It's Pascal's triangle. {binom} These are the binomial coefficients, the numbers you get when you expand the bracket, A, plus B, to the power N.

[c4.pattern.4] {why} Why Pascal's triangle? {pause} Each time you differentiate, every term splits into two, as the new prime lands either on F or on G. {binom2} Multiplying by the bracket, A, plus B, does the same. Each term splits into one with an extra A, and one with an extra B. {count} The bookkeeping is identical, so the same numbers come out. {total} So each row adds up to the count before combining, two, four, eight. {ten} For row ten, it's one thousand and twenty-four, the count from the start.

## Scene 4 · The formula (ch4_s4_formula)

> On {coef}: centre, `\binom{n}{m} = \frac{n!}{m!\,(n-m)!}` (YELLOW), labelled "n choose m". On {place}: s3's triangle, small (owner ch4_s3_pattern: rows "1 1", "1 2 1", "1 3 3 1", as on her board), gains a single "1" on top as row 0 (the row of (a + b)⁰), so that it reads rows 0 to 3; then the rows are numbered from 0 down the left and the places from 0 along each row; the entry in row 3, place 1 lights. From here on the series' triangle is these four rows (ch4 s7, the recap, ch5 s1); ch5 s4 adds row 4 and ch7 s5 shows row 5 alone. On {fact}: the factorials in the formula light one by one. On {example}: `\binom{3}{1} = \frac{3!}{1!\,2!} = \frac{6}{2} = 3` (numbers GOLD), and the lit entry reads 3.
> On {other}: `C_n^m` beside the bracket form, with "=" between them. On {poll}: a small DIM line under it, "Russia · Ukraine · Kazakhstan · China · France".
> On {formula}: her board (frame 38:55) as the hero, centred and large, under a small title "Leibniz's formula": `\frac{d^n (fg)}{dx^n} = \sum_{m=0}^{n} \binom{n}{m}\, f^{(n-m)}(x)\, g^{(m)}(x)`, f BLUE, g PURPLE, the binomial YELLOW. On {term}, its left side re-forms as `(fg)^{(n)}` (s2's bracket notation) and the (x)'s drop: `(fg)^{(n)} = \sum_{m=0}^{n} \binom{n}{m} f^{(n-m)} g^{(m)}`. That is the Leibniz sum card: s5–s7, the recap, ch5 (hook, s4) and ch7 s5 reuse it, so build it as one object.
> On {term}: the summand underlined piece by piece: the binomial, then `f^{(n-m)}`, then `g^{(m)}`. On {land}: braces under the two derivatives, "n − m on f" (BLUE) and "m on g" (PURPLE).
> On {choose}: a row of n small slots (n = 3 drawn), each holding one prime; m of them turn PURPLE (sent to g) and the rest BLUE (sent to f). With m = 1, the three ways flash in turn, and the count lands on the "3" in row 3 of the triangle.
> On {check}: n = 2 written out under the card: `\binom{2}{0} f''g + \binom{2}{1} f'g' + \binom{2}{2} fg''` → `f''g + 2f'g' + fg''`. On {match}: s3's y″ line slides in above it, the two match term by term, GREEN tick. (The formula checked against direct differentiation with sympy 1.14 for n = 1 to 6.)

[c4.formula.1] {coef} Each number in Pascal's triangle has a name. {place} Count the rows, and the places along each row, from zero. The number in row N, place M, is called N choose M. {fact} It's N factorial, divided by M factorial, and divided again by the factorial of N minus M. {example} Here's an example. Three choose one is six, over one times two, which is three.

[c4.formula.2] {other} There's another notation, a capital C with N and M attached. {poll} In the lecturer's poll, hands went up from students who learned it in Russia, Ukraine, Kazakhstan and China. France uses it too.

[c4.formula.3] {formula} Put it all together, and you get Leibniz's formula. The Nth derivative of the product is a sum over M, from zero to N. {term} Each term is N choose M, times F differentiated N minus M times, times G differentiated M times. {land} In words, M of the derivatives land on G, and the rest land on F. {choose} And N choose M counts the ways to pick which M of the N derivatives go to G. That's where the binomial coefficients come from.

[c4.formula.4] {check} Check it with N equal to two. M equals zero gives F double prime times G. M equals one gives two, times F prime times G prime. M equals two gives F times G double prime. {match} That's the second derivative from the board. {pause}

## Scene 5 · When most terms vanish (ch4_s5_example)

> On {back}: the hook's question returns at the top: `\frac{d^{10}}{dx^{10}}\left(x^2 e^{-x}\right) = \;?`, with the labels `f = x^2` (BLUE) and `g = e^{-x}` (PURPLE) under the two factors.
> On {runs}: f's chain on the left: `x^2 \to 2x \to 2 \to 0 \to 0`, the zeros DIM. On {alt}: g's chain on the right: `e^{-x} \to -e^{-x} \to e^{-x} \to -e^{-x}`, each minus sign flashing YELLOW as it appears.
> On {sum}: s4's Leibniz sum card, its terms written out in a row for general n: `\binom{n}{0} f^{(n)} g + \dots + \binom{n}{n-2} f'' g^{(n-2)} + \binom{n}{n-1} f' g^{(n-1)} + \binom{n}{n} f\, g^{(n)}`. On {zero}: every term whose f has three or more derivatives turns DIM and is struck through, leaving the last three. On {row}: row n of Pascal's triangle, drawn with dots in the middle, only its last three entries lit YELLOW: `\binom{n}{n-2} = \frac{n(n-1)}{2}`, `\binom{n}{n-1} = n`, `\binom{n}{n} = 1` (ch5 s4 lights the last two of a row the same way).
> On {general}: `\frac{d^n}{dx^n}\left(x^2 e^{-x}\right) = (-1)^n e^{-x}\left(x^2 - 2nx + n(n-1)\right)`, e^{−x} PURPLE, the polynomial BLUE.
> On {n1}: n = 1 gives `e^{-x}\left(2x - x^2\right)`, and beside it part two's product rule, `2x\,e^{-x} - x^2 e^{-x}`, GREEN tick.
> On {n10}: row ten, `1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1`, its last three entries lit, feeding `45 \cdot 2`, `10 \cdot 2x \cdot (-1)` and `1 \cdot x^2`. On {answer}: `\frac{d^{10}}{dx^{10}}\left(x^2 e^{-x}\right) = e^{-x}\left(x^2 - 20x + 90\right)`, boxed YELLOW; the hook's GOLD "1024" counter appears small in a corner. On {later}: a DIM tag "Part 5". (The general form for n = 1 to 15, and the n = 10 value, checked with sympy 1.14.)

[c4.example.1] {back} Now back to the tenth derivative from the start. The first factor, F, is ex squared. The second, G, is E to the minus ex. {runs} F runs out fast. Its derivatives are two ex, then two, then zero. {alt} G never runs out. Each derivative just flips its sign.

[c4.example.2] {sum} In Leibniz's formula, F gets N minus M of the derivatives. {zero} Once F gets three or more, that term is zero. So only the last three terms of the sum survive. {row} And only the last three numbers in the row matter. They are N times N minus one, over two, then N, then one.

[c4.example.3] {general} Put in the derivatives and collect. You get minus one to the power N, times E to the minus ex, times a short polynomial. It's ex squared, minus two N ex, plus N times N minus one. {n1} For N equal to one, that's two ex minus ex squared, times E to the minus ex, which is the product rule again.

[c4.example.4] {n10} For N equal to ten, the last three numbers in the row are forty-five, ten and one. {answer} So the tenth derivative is E to the minus ex, times ex squared, minus twenty ex, plus ninety. {pause} A short answer, against over a thousand terms the blind way. {later} Part five uses the same idea, on a harder product.

## Scene 6 · Proof by induction: two sums (ch4_s6_proof1)

> On {proof}: her heading (frame 41:00), "Proof by induction:", with two numbered steps, "① n = 1" and "② true for n ⇒ true for n + 1"; on {step}: ② lights YELLOW. s2's notation card stays small in a corner.
> On {base}: under ①, the sum card at n = 1: `\binom{1}{0} f'g + \binom{1}{1} fg' = f'g + fg'`, GREEN tick, labelled "product rule". On {domino}: a row of dominoes labelled 1, 2, 3, 4, …; the first tips over and knocks down the next, and so on.
> On {assume}: the dominoes shrink to a corner. s4's Leibniz sum card, framed YELLOW, with the tag "assume, for this n".
> On {diff}: `(fg)^{(n+1)} = \frac{d}{dx}\sum_{m=0}^{n}\binom{n}{m} f^{(n-m)} g^{(m)}`. On {inside}: the d/dx slides inside the sum, past the YELLOW coefficient. On {rule}: `= \sum_{m=0}^{n}\binom{n}{m}\left[f^{(n-m+1)} g^{(m)} + f^{(n-m)} g^{(m+1)}\right]`, a DIM "(114)" beside it; the extra derivative glows BLUE on f in the first product and PURPLE on g in the second. On {two}: the bracket splits into two sums, stacked: the first sum on top, the second below.
> On {rows}: under the sums, their terms as two rows of boxes, coefficients YELLOW above each box. First row: `f^{(n+1)}g`, `f^{(n)}g'`, `f^{(n-1)}g''`, …, `f'g^{(n)}`. Second row: `f^{(n)}g'`, `f^{(n-1)}g''`, …, `f'g^{(n)}`, `fg^{(n+1)}`. On {outofstep}: a YELLOW flash on `f^{(n)}g'`, first in the first row's second box, then in the second row's first box.
> On {last}: the second row's last box detaches to the right, with her margin note "m = n": `\binom{n}{n} f^{(0)} g^{(n+1)} = f\,g^{(n+1)}`. On {rest}: the second sum's top limit becomes n − 1 (YELLOW), as in the notes: `\sum_{m=0}^{n-1}\binom{n}{m} f^{(n-m)} g^{(m+1)} + f^{(0)} g^{(n+1)}`.
> On {shift}: the notes' relabelled line: `\sum_{m=1}^{n}\binom{n}{m-1} f^{(n-m+1)} g^{(m)} + f^{(0)} g^{(n+1)}`, the changed parts (the limits 1 and n, the m − 1, the n − m + 1, the m) YELLOW (the notes colour them red). On {slide}: the second row of boxes slides one place to the right, so each box sits under the box with the same product in the first row; the first row's first box `f^{(n+1)}g` sticks out on the left, the detached `fg^{(n+1)}` on the right. On {match}: each column's two products flash GREEN together; their YELLOW coefficients stay different. (Every line checked with sympy 1.14 at n = 4.)

[c4.induction.1] {proof} The notes prove the formula by induction, in two steps. {base} Step one, check it for N equal to one. That's done already. There, the sum is F prime times G, plus F times G prime, the product rule. {step} Step two, show that if it holds for some N, it also holds for N plus one. {domino} Then one gives two, two gives three, and so on, for every N.

[c4.induction.2] {assume} So assume the formula for the Nth derivative. {diff} To get the next one, differentiate once more. {inside} The coefficients are constants, so the derivative goes straight inside the sum, onto each product. {rule} Each product gets the product rule, one more derivative on F, plus one more derivative on G. {two} So the sum splits into two sums.

[c4.induction.3] {rows} Write out their terms. In the first sum, F has the extra derivative, and in the second, G does. {outofstep} The plan is to collect matching products, as on the board, but the two sums are out of step. {last} So first, take the last term of the second sum, where M equals N, out on its own. Its coefficient, N choose N, is one, so it's just F, times G differentiated N plus one times. {rest} The rest of that sum stops at N minus one.

[c4.induction.4] {shift} Now relabel. Replace M by M minus one everywhere. The new M runs from one to N. The coefficient becomes N choose, M minus one. And the product becomes F differentiated N minus M plus one times, times G differentiated M times. {slide} Only the label has changed, but now each term sits under its partner in the first sum. {match} Same derivatives on F, same derivatives on G. Only the coefficients differ. {pause}

## Scene 7 · Proof by induction: Pascal's rule (ch4_s7_proof2)

> Same layout as the end of s6: the sums above, the two rows of boxes below, the second row shifted.
> On {first}: the first row's sticking-out box detaches to the left: `\binom{n}{0} f^{(n+1)} g^{(0)} = f^{(n+1)} g`, as the notes' "Separate out m = 0". On {both}: both sums now show `\sum_{m=1}^{n}`, the limits YELLOW. On {add}: the columns merge into one sum, with the two end terms waiting either side: `(fg)^{(n+1)} = f^{(n+1)}g^{(0)} + \sum_{m=1}^{n}\left[\binom{n}{m} + \binom{n}{m-1}\right] f^{(n-m+1)} g^{(m)} + f^{(0)}g^{(n+1)}`, the square bracket YELLOW.
> On {pascal}: beside it, s3's Pascal's triangle (YELLOW); in two neighbouring rows, pairs of adjacent entries send V-shaped arrows into the entry below them (1 + 2 → 3, then 2 + 1 → 3). On {rule}: `\binom{n}{m} + \binom{n}{m-1} = \binom{n+1}{m}`, boxed YELLOW, with a DIM tag "Pascal's rule · notes §8.4.2".
> On {reason}: s4's row of prime slots, now n + 1 of them (four drawn, m = 2); the last slot flashes PURPLE with "to g: pick m − 1 from the rest", then BLUE with "to f: pick m from the rest" (counts 3 and 3, total 6 = `\binom{4}{2}`, GOLD).
> On {replace}: the YELLOW square bracket collapses into `\binom{n+1}{m}`. On {ends}: the two waiting end terms get the coefficients `\binom{n+1}{0} = 1` and `\binom{n+1}{n+1} = 1`, then slide into the sum, whose limits change to m = 0 and n + 1 (YELLOW). On {done}: `(fg)^{(n+1)} = \sum_{m=0}^{n+1}\binom{n+1}{m} f^{(n-m+1)} g^{(m)}`, boxed, beside s4's card: the two match with n + 1 in place of n, GREEN tick. On {every}: s6's dominoes, small, all fall.
> On {concrete}: the proof in miniature: the row `1  2  1` written twice, the second copy shifted one place to the right, under s3's products (first copy over `f'''g`, `f''g'`, `f'g''`; second over `f''g'`, `f'g''`, `fg'''`). On {addrows}: the columns add to `1  3  3  1`, and s3's y‴ line appears under it. On {copies}: three small labels: "the two sums" on the copies, "the relabelling" on the shift, "the end terms" on the two outer 1s. This picture of two rows linking up is the recap's. (Every line checked with sympy 1.14 at n = 4; Pascal's rule symbolically and for n up to 14.)

[c4.pascal.1] {first} Now do the same at the other end. Take the first term of the first sum, where M equals zero, out on its own. Its coefficient, N choose zero, is one, so it's F differentiated N plus one times, times G. {both} Now both sums run over the same M, from one to N, with the same products. {add} So add them. Each product gets the coefficient N choose M, plus N choose, M minus one. {pause}

[c4.pascal.2] {pascal} That sum of two coefficients is how Pascal's triangle is built. Each number in the triangle is the sum of the two above it. {rule} In symbols, N choose M, plus N choose, M minus one, equals N plus one, choose M. This is Pascal's rule, and the notes prove it in section eight point four point two.

[c4.pascal.3] {reason} Here's a quick way to see it. Send M of N plus one derivatives to G. Either the last one goes to G, and you pick M minus one from the rest, or it goes to F, and you pick all M from the rest. {pause}

[c4.pascal.4] {replace} So each bracket becomes N plus one, choose M. {ends} Now fold the two outer terms back in. N plus one choose zero is one, and so is N plus one choose N plus one. So the outer terms fit in as the first and last terms, and the sum now runs from zero to N plus one. {done} That's Leibniz's formula, with N plus one in place of N. {pause} {every} With step one, that proves it for every N. {pause}

[c4.pascal.5] {concrete} Step back. The whole proof is Pascal's triangle being built. Take the row one, two, one, and write it twice, the second copy shifted one place along. {addrows} Add down the columns, and you get one, three, three, one. That's the step from the second derivative to the third. {copies} The two copies are the two sums, the shift is the relabelling, and the ones at the ends are the outer terms.

## Scene 8 · Recap (ch4_s8_recap)

> On {recap}: a small "Recap" heading. Four panels in a 2×2 grid, each a small version of the visual that taught its idea (same objects, colours and styling), with its short line under it:
> On {r1}: s2's x³ chain card (BLUE x³; GREEN 3x², 6x, 6, 0) with s2's RED `(3x^2)^2 = 9x^4` and `\neq` beside the GREEN 6x. Line: "nth derivative: differentiate n times, not a power".
> On {r2}: s3's three board lines with the YELLOW-framed Pascal's triangle beside them; on {r2b}: s4's Leibniz sum card fades in under them. Line: "Leibniz: coefficients from Pascal's triangle".
> On {r3}: s5's row with its last three entries lit, and the boxed `e^{-x}\left(x^2 - 20x + 90\right)`. Line: "a polynomial factor cuts the sum short".
> On {r4}: s7's two shifted copies of `1  2  1` adding to `1  3  3  1`, with the small fallen dominoes. Line: "proof: induction and Pascal's rule".
> On {next}: the panels slide up and dim. `H_n(x) = (-1)^n e^{x^2}\frac{d^n}{dx^n}\left(e^{-x^2}\right)`, with e^{x²} GOLD and e^{−x²} PURPLE (part five's colours). On {recursion}: `H_{n+1} = 2xH_n - 2nH_{n-1}` under it, with a YELLOW "?". The line "Part 5 · Hermite polynomials".
> Then the end card, held about eight seconds after the last word (music carries it).

[c4.recap.1] {recap} Time for a recap. {r1} The Nth derivative means differentiate N times, which is different from raising the first derivative to the power N. {r2} Leibniz's formula gives the Nth derivative of a product. {r2b} Its coefficients are N choose M, the numbers in Pascal's triangle. {r3} When one factor is a polynomial, its derivatives run out, and only a few terms survive. {r4} And the proof is induction, with Pascal's rule doing the adding. {pause}

[c4.recap.2] {next} Next time, Leibniz at work. The Hermeet polynomials of quantum mechanics are defined with an Nth derivative, {recursion} and Leibniz's formula turns that definition into a rule that builds each one from the two before it. {pause}
