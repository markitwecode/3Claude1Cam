"""Chapter 1, scene 7: ten thousand random numbers (nextrandom, randlist, rs). Clips c1.test.1 – c1.test.5."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

PANEL = "#161A21"

NEXTRANDOM = """let nextrandom seed =
  let a = 16807.0 in
  let m = 2147483647.0 in
  let t = a *. seed in
  t -. m *. (floor (t /. m))"""

RANDLIST = """let rec randlist (seed, seeds) = function
  | 0 -> (seed, seeds)
  | n -> randlist (nextrandom seed, seed::seeds) (n-1)"""

# The toplevel's own line breaks for these two replies at a narrower margin
# (Format.set_margin 45 / 50, OCaml 5.4.1): same text, wrapped to fit the frame.
RANDLIST_REPLY = """val randlist :
  float * float list ->
  int -> float * float list = <fun>"""
EXAMPLE_REPLY = """- : float * float list =
(1622650073., [282475249.; 16807.; 1.])"""

# OCaml 5.4.1's reply to `let seed, rs = randlist (1.0, []) 10000;;`, verbatim.
SEED_LINE = "val seed : float = 1043618065."
RS_LINE = "val rs : float list ="
RS_LINES = """  [1484786315.; 925166085.; 1614852353.; 721631166.; 173942219.; 1229443779.;
   789328014.; 570809709.; 1760109362.; 270600523.; 2108528931.; 16480421.;
   519782231.; 162430624.; 372212905.; 1954184989.; 898872741.; 1651521688.;
   1114791388.; 1325968501.; 1469981427.; 465437343.; 1732504088.;
   280054095.; 1924919450.; 1244369648.; 1524535715.; 706293012.;
   1372325856.; 1302473561.; 941382430.; 2137445578.; 1937168414.;
   1852570660.; 495231255.; 1092873378.; 140232191.; 328129841.; 632752255.;
   227857208.; 1616471915.; 719842438.; 1402481130.; 745001020.; 791471334.;
   2131048000.; 312659966.; 1389551813.; 443838892.; 854190041.; 741774068.;
   267473377.; 1372555293.; 1539748349.; 697860888.; 1261546017.; 734770781.;
   1512111397.; 813238415.; 1034499961.; 602256496.; 462191385.; 250718457.;
   246489360.; 295426232.; 468306241.; 877829533.; 1130589227.; 1914364883.;
   1479854970.; 878528585.; 1268712064.; 115837978.; 1803525169.; 689954646.;
   1174020926.; 651968560.; 391152461.; 1776325865.; 2015344107.; 246977673.;
   1381242649.; 1115030853.; 190703911.; 316761032.; 464218769.; 1537522160.;
   1958981931.; 390463588.; 224009597.; 235243732.; 620352731.; 1374109567.;
   832140633.; 675075162.; 1296171190.; 2009054653.; 1534419747.; 145880482.;
   1649432515.; 403989126.; 1112417244.; 1290575192.; 896661113.; 218545469.;
   1002393512.; 2131316096.; 551979127.; 932010335.; 665881436.; 1975412808.;
   639877791.; 1781707137.; 894518191.; 568004958.; 1331430214.; 629489848.;
   183264178.; 162027282.; 464592882.; 93302056.; 1178713033.; 1401486247.;
   1846150129.; 1646978216.; 1104441491.; 111995009.; 66193165.; 2038880392.;
   79340676.; 871801051.; 967550305.; 2067810758.; 1600354198.; 1746626663.;
   1516388116.; 1308870791.; 173082747.; 189881227.; 478010722.; 739707315.;
   255334803.; 164203714.; 1893097038.; 1587694259.; 292950569.; 918323194.;
   41453146.; 1217297445.; 256768724.; 586494122.; 586258194.; 660494391.;
   507554325.; 699716071.; 672895139.; 76065072.; 1594869218.; 1439459639.;
   641123634.; 1650611940.; 177447368.; 301427463.; 525804524.; 553672425.;
   926899509.; 794676486.; 690277940.; 2115070333.; 1062048650.; 1653192448.;
   1808855340.; 126475289.; 1028198214.; 1739565096.; 1515748830.;
   427491435.; 319330584.; 666483848.; 854842154.; 1853528448.; 1975611245.;
   1905343266.; 1229802342.; 1416055428.; 2091603253.; 1068308139.;
   198239748.; 982076370.; 1094563396.; 44402415.; 889814989.; 290736902.;
   417580014.; 1935788352.; 595665917.; 367638848.; 894945148.; 1868608068.;
   317883051.; 941451621.; 1595942893.; 789094274.; 1150772108.; 422742112.;
   1444245279.; 1273601104.; 256005435.; 1742330161.; 1514599036.;
   956344512.; 2113041793.; 293237373.; 1386995194.; 1509339194.; 891946522.;
   1020832915.; 592544922.; 1746311153.; 1471539715.; 143832370.;
   2041568248.; 1039556199.; 1608726047.; 1205124472.; 2123533995.;
   1560620058.; 1837598795.; 1028172251.; 98318742.; 1405510706.;
   1047695837.; 59221314.; 1822176683.; 1096018886.; 1528104537.;
   1270922857.; 812074106.; 291115596.; 795788616.; 638657646.; 2034314619.;
   1527649272.; 156357479.; 1010056202.; 1139413443.; 1110927723.;
   1216083346.; 846825145.; 2100385733.; 315213605.; 1629637749.;
   1139833627.; 895118866.; 296359237.; 1361440746.; 1188627020.;
   1964199872.; 166733080.; 54185744.; 575493576.; 1810324496.; 1765549585.;
   53514233.; 747348448.; 61758907.; 1710119765.; 188311628.; 8827553.;
   67975851.; 1808633248.; 1290488843.; 1264775607.; 1711469075.;
   1537468597.; 706677101.; 518290019.; 190285086.; 157683412.; 985907152.;
   1571668636.; 632570698.; 791081325.; 1773794197.; 1787141077.;
   1727982894.; 794213057.; 633163306.; 682601940.; 1573439414.; 1041956036.;
   1169697582.; 758914445.; 2096291761.; 1502226099.; 1665995955.;
   948048264.; 1596326605.; 1816773893.; ...]"""

# Clip 4's printout window (row centres) and its fade zone.
Y_FIRST, Y_LAST, FADE, FADE_TOP = 1.5, -2.85, 0.4, 0.3


def race_header():
    """The scoreboard's comparisons header (ch1_s4), small; matched by hand if that file isn't ready."""
    ref = T("comparisons on 10,000 random items", size=34)
    try:
        here = str(Path(__file__).resolve().parent)
        if here not in sys.path:
            sys.path.insert(0, here)
        from ch1_s4_contest import make_scoreboard
        hdr = make_scoreboard().col_headers[0].copy()
        hdr.scale(min(ref.width / hdr.width, 0.9 / hdr.height))
        return hdr
    except Exception:
        return ref


def panel(code, pad_x=0.35, pad_y=0.28):
    """The code box: a dark rounded panel behind a Code (z −2, so token boxes show above it)."""
    box = RoundedRectangle(corner_radius=0.16, width=code.width + 2 * pad_x + 0.08,
                           height=code.height + 2 * pad_y)
    box.set_stroke(DIM, 2).set_fill(PANEL, 1).set_z_index(-2)
    box.move_to(code).shift(RIGHT * 0.04)
    return box


def prompt(src, size):
    """A toplevel input line with its DIM `#` prompt."""
    m = Code("# " + src, size=size)
    m.find("#").set_color(DIM)
    return m


def left_at(m, x):
    return m.shift(RIGHT * (x - m.get_left()[0]))


class TestData(NarratedScene):
    def construct(self):
        self.nextrandom_part()
        self.reply_part()
        self.randlist_part()
        self.call_part()
        self.poly_part()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # c1.test.1: the generator's code
    def nextrandom_part(self):
        with self.say("c1.test.1") as c:
            hdr = race_header().move_to(UP * 3.2)
            self.play(FadeIn(hdr, shift=0.3 * DOWN, run_time=0.8),
                      time_span(FlashAround(hdr, time_width=1.5), 0.4, 1.9))
            c.wait_until("no particular order")

            code = Code(NEXTRANDOM, size=38)
            code.move_to(LEFT * 0.45 + UP * 0.55)
            for v in ("a", "m", "t"):                      # only the function's name in YELLOW
                code.find(f"let {v}")[-1].set_color(FG)
            box = panel(code)
            self.code1, self.box1 = code, box
            self.play(FadeIn(box, shift=0.2 * UP), FadeIn(code, shift=0.2 * UP), run_time=1.2)

            c.wait_until("never")
            never = T("“never mind how this works”", size=32, color=DIM, slant=ITALIC)
            never.next_to(box, DOWN, buff=0.45)
            self.never = never
            self.play(FadeOut(hdr, shift=0.2 * UP), FadeIn(never, shift=0.2 * DOWN), run_time=1.0)

            c.wait_until("mult")
            L = [code.line(i) for i in range(5)]
            self.L1 = L
            b_a = token_box(code.find("16807.0", line=1), L[1])
            b_s = token_box(code.find("a *. seed", line=3), L[3])
            self.play(FadeIn(b_a, scale=1.15), run_time=1.0)
            self.play(FadeIn(b_s, scale=1.15), run_time=1.0)

            c.wait_until("mod")
            big = code.find("2147483647.0", line=2)
            b_m = token_box(big, L[2], color=GOLD)
            tag = MathTex(r"2^{31} - 1", font_size=60, color=GOLD)
            tag.next_to(box, RIGHT, buff=0.3).set_y(L[2].get_y())
            self.tag31, self.b_m = tag, b_m
            self.play(ReplacementTransform(b_a, b_m), FadeOut(b_s), run_time=1.2)
            self.play(FadeIn(tag, shift=0.3 * LEFT), run_time=1.0)

    # c1.test.2: floats, the remainder, the replies
    def reply_part(self):
        code, box, L = self.code1, self.box1, self.L1
        with self.say("c1.test.2") as c:
            ops = [code.find("*.", line=3), code.find("-.", line=4),
                   code.find("*.", line=4), code.find("/.", line=4)]
            uls = [underline(o, YELLOW, buff=0.1) for o in ops]
            self.play(LaggedStart(*[Create(u) for u in uls], lag_ratio=0.25),
                      FadeOut(self.b_m), FadeOut(self.never), run_time=1.4)

            c.wait_until("floor")
            brace = Brace(L[4], DOWN, buff=0.18, color=YELLOW)
            rem = T("the remainder", size=34, color=YELLOW).next_to(brace, DOWN, buff=0.15)
            self.play(GrowFromCenter(brace), FadeIn(rem, shift=0.25 * DOWN), run_time=1.2)

            c.wait_until("reply")
            d = 3.6 - box.get_top()[1]
            self.play(FadeOut(brace), FadeOut(rem), *[FadeOut(u) for u in uls],
                      *[m.animate.shift(UP * d) for m in (box, code, self.tag31)], run_time=1.2)
            x0 = code.get_left()[0]
            r1 = left_at(Code("val nextrandom : float -> float = <fun>", size=32), x0)
            r1.set_y(box.get_bottom()[1] - 0.5)
            self.play(FadeIn(r1, shift=0.2 * DOWN), run_time=1.0)

            c.wait_until("one")
            q2 = left_at(prompt("nextrandom 1.0;;", 32), x0).set_y(r1.get_y() - 0.68)
            self.play(FadeIn(q2, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("you get")
            pre = left_at(Code("- : float =", size=32), x0).set_y(q2.get_y() - 0.55)
            num = Code("16807.", size=32).next_to(pre, RIGHT, buff=0.3).align_to(pre, DOWN)
            self.play(FadeIn(pre),
                      ReplacementTransform(code.find("16807.0", line=1).copy(), num), run_time=1.5)

            c.wait_until("park")
            card_t = T("Park and Miller, 1988: the ‘minimal standard’ generator", size=30, color=DIM)
            card = RoundedRectangle(corner_radius=0.12, width=card_t.width + 0.6, height=card_t.height + 0.4)
            card.set_stroke(DIM, 1.5).set_fill(BG, 0)
            card_t.move_to(DOWN * 3.1)
            card.move_to(card_t)
            self.card = VGroup(card, card_t)
            self.replies1 = [r1, q2, pre, num]
            self.play(FadeIn(self.card, shift=0.2 * UP), run_time=1.0)

    # c1.test.3: randlist and its example
    def randlist_part(self):
        code1, box1 = self.code1, self.box1
        with self.say("c1.test.3") as c:
            code = Code(RANDLIST, size=28)
            box = panel(code, pad_x=0.3, pad_y=0.25)
            VGroup(box, code).move_to(ORIGIN).shift(UP * (0.35 - box.get_top()[1]))
            k = 0.75
            P = box1.get_center()
            T_ = UP * (3.48 - box1.height * k / 2)
            self.play(*[FadeOut(m) for m in self.replies1], FadeOut(self.tag31),
                      *[m.animate.scale(k, about_point=P).shift(T_ - P) for m in (box1, code1)],
                      time_span(FadeIn(box, shift=0.2 * UP), 0.6, 1.6),
                      time_span(FadeIn(code, shift=0.2 * UP), 0.6, 1.6), run_time=1.6)

            c.wait_until("pair")
            L = [code.line(i) for i in range(3)]
            hb = token_box(code.find("(seed, seeds)", line=0), L[0])
            self.play(FadeIn(hb, scale=1.15), run_time=1.0)

            c.wait_until("count")
            self.play(Transform(hb, token_box(code.find("(n-1)", line=2), L[2])), FadeOut(self.card),
                      run_time=1.5)

            c.wait_until("zero")
            zero = code.find("0", line=1)
            const = T("a constant pattern", size=30, color=YELLOW)
            const.next_to(L[1], RIGHT, buff=0.7)
            self.play(Transform(hb, token_box(zero, L[1])), run_time=1.5)
            self.play(FadeIn(const, shift=0.3 * LEFT), run_time=0.9)

            c.wait_until("trick")
            x0 = code.get_left()[0]
            trick = VGroup(T("Lecture 4: two results", size=28, color=DIM),
                           T("in one accumulator", size=28, color=DIM)).arrange(DOWN, buff=0.12,
                                                                                aligned_edge=LEFT)
            trick.next_to(box, DOWN, buff=0.45).align_to(box, RIGHT).shift(LEFT * 0.15)
            self.play(FadeIn(trick, shift=0.2 * DOWN), run_time=1.0)

            c.wait_until("accumulating argument")
            d = 3.48 - box.get_top()[1]
            rep = left_at(Code(RANDLIST_REPLY, size=28), x0)
            rep.next_to(box, DOWN, buff=0.4).shift(UP * d)
            left_at(rep, x0)
            self.play(FadeOut(box1), FadeOut(code1),
                      *[m.animate.shift(UP * d) for m in (box, code, hb, const, trick)],
                      time_span(FadeIn(rep, shift=0.2 * DOWN), 0.8, 1.6), run_time=1.6)

            c.wait_until("example")
            q = left_at(prompt("randlist (1.0, []) 3;;", 28), x0)
            q.set_y(rep.get_bottom()[1] - 0.6)
            self.play(FadeOut(hb), FadeOut(const), FadeIn(q, shift=0.2 * DOWN), run_time=1.2)

            c.wait_until("three steps")
            ex = left_at(Code(EXAMPLE_REPLY, size=28), x0)
            ex.next_to(q, DOWN, buff=0.22)
            left_at(ex, x0)
            seed_g = ex.find("1622650073.", line=1)
            nxt = T("next seed", size=30, color=GOLD).next_to(seed_g, DOWN, buff=0.3)
            self.play(FadeIn(ex, shift=0.2 * DOWN), time_span(FadeIn(nxt, shift=0.2 * DOWN), 0.8, 1.6),
                      run_time=1.6)

            c.wait_until("ending in")
            E1 = ex.line(1)
            n16 = ex.find("16807.", line=1)
            n1 = ex.find("1.]", line=1)[:2]
            bx = [token_box(n16, E1), token_box(n1, E1)]
            self.play(LaggedStart(*[FadeIn(b, scale=1.15) for b in bx], lag_ratio=0.6), run_time=1.4)

            c.wait_until("then one")
            lst_g = ex.find("[282475249.; 16807.; 1.]", line=1)
            y_a = nxt.get_y()
            arr = Arrow(RIGHT * lst_g.get_right()[0] + UP * y_a, RIGHT * lst_g.get_left()[0] + UP * y_a,
                        buff=0.1, stroke_width=4, color=TEAL, max_tip_length_to_length_ratio=0.08)
            newest = T("newest first", size=30, color=TEAL).next_to(arr, DOWN, buff=0.15)
            self.play(GrowArrow(arr), FadeIn(newest, shift=0.2 * DOWN), run_time=1.2)

    # c1.test.4: ten thousand of them
    def call_part(self):
        X0 = -6.55
        with self.say("c1.test.4") as c:
            call = left_at(prompt("let seed, rs = randlist (1.0, []) 10000;;", 32), X0).set_y(3.2)
            c.wait_until("ten thousand")
            sweep_clear(self, time_span(FadeIn(call, shift=0.2 * DOWN), 0.5, 1.2))

            sl = left_at(Code(SEED_LINE, size=28), X0).set_y(2.48)
            rl = left_at(Code(RS_LINE, size=28), X0).set_y(2.02)
            lst = Code(RS_LINES, size=20)
            n = len(RS_LINES.splitlines())
            rows = [lst.line(i) for i in range(n)]
            left_at(lst, X0 + 2 * 0.166)
            lst.shift(UP * (Y_FIRST - rows[0].get_y()))
            dist = Y_LAST - rows[-1].get_y()
            p0 = lst.get_center().copy()

            def window(g):
                for r in rows:
                    y = r.get_y()
                    op = min(1.0, max(0.0, (Y_FIRST + FADE_TOP - y) / FADE_TOP),
                             max(0.0, (y - (Y_LAST - FADE)) / FADE))
                    r.set_opacity(op * g)

            def scroll(m, a):
                s = smooth(min(1.0, max(0.0, (a - 0.2) / 0.8)))
                m.move_to(p0 + UP * dist * s)
                window(min(1.0, a / 0.12))

            T_run = max(2.2, c.until("let") - 0.1)
            self.play(time_span(FadeIn(sl), 0, 0.4), time_span(FadeIn(rl), 0, 0.4),
                      UpdateFromAlphaFunc(lst, scroll, rate_func=linear, run_time=T_run), run_time=T_run)

            c.wait_until("let")
            lb = token_box(call.find("seed, rs"), call.line(0))
            self.play(FadeIn(lb, scale=1.15), run_time=1.0)

            c.wait_until("seed")
            val = sl.find("1043618065.")
            self.play(FadeOut(lb), *recolor(val, YELLOW), FlashAround(val, run_time=2, time_width=1.5),
                      run_time=2)
            c.wait_until("check value")
            tick = check_mark().next_to(sl, RIGHT, buff=0.5)
            note = VGroup(T("Park and Miller’s", size=30, color=GREEN),
                          T("published check value", size=30, color=GREEN)).arrange(DOWN, buff=0.1,
                                                                                    aligned_edge=LEFT)
            note.next_to(tick, RIGHT, buff=0.3)
            self.play(Create(tick), FadeIn(note, shift=0.2 * LEFT), run_time=1.2)

            c.wait_until("rs")
            rb = token_box(rl.line(0), rl.line(0), height=rl.height + 0.16)
            self.play(FadeIn(rb, scale=1.1), run_time=1.0)

            c.wait_until("backwards")
            cap = T("… ends 16807., 1.", size=34, color=GOLD)
            cap.next_to(rows[-1], RIGHT, buff=0.45)
            set_backstroke(cap)
            self.cap = cap
            self.play(FadeIn(cap, shift=0.3 * LEFT), run_time=1.0)

    # c1.test.5: <= works on any type
    def poly_part(self):
        with self.say("c1.test.5") as c:
            le = Mono("<=", size=140)
            frame = RoundedRectangle(corner_radius=0.2, width=le.width + 1.1, height=le.height + 1.0)
            frame.set_stroke(BLUE, 5)
            grp = VGroup(frame, le).move_to(UP * 0.3)
            sweep_clear(self, time_span(Create(frame), 0.5, 1.5), time_span(FadeIn(le), 0.7, 1.5),
                        keep=[self.cap], run_time=1.5)

            c.wait_until("le")
            tys = [Mono("int", size=56, color=GREEN).next_to(grp, UP, buff=0.6),
                   Mono("float", size=56, color=GREEN).move_to(grp.get_center() + LEFT * 3.9 + DOWN * 1.5),
                   Mono("string", size=56, color=GREEN).move_to(grp.get_center() + RIGHT * 3.9 + DOWN * 1.5)]
            order = [tys[1], tys[0], tys[2]]                 # said: floats, integers, strings
            self.play(time_span(FadeOut(self.cap), 1.0, 2.0),
                      LaggedStart(*[FadeIn(t, shift=0.4 * (t.get_center() - grp.get_center()) / 3)
                                    for t in order], lag_ratio=0.35), run_time=2.0)
