"""Chapter 1, scene 2: the crew (master shot) and the conveyor of files. Clips c1.crew.1 – c1.crew.4.

Master shot (shared with ch1_s5_director, s8, ch2; numbers match s5's master_shot):
  you      T 36 YELLOW at (0, 3.4)
  producer 3.2 x 0.8 at (0, 2.45), T 32 label
  row y=1.0, boxes 2.8 x 0.7, labels 28: series-planner x=-5.1; script-writer xN x=-1.7 (+2 copies
  behind at +0.1/+0.2 up-right, all BLUE); `vk voice` x=1.7 (DIM outline, Mono DIM label);
  chapter-director xN x=5.1 (front lit, 2 DIM copies behind at +0.08/+0.16 up-right)
  8 builders 0.75 x 0.45 at y=-0.5, centred x=3.0, gap 0.15; DIM T 28 "scene-builder × 6–8" at (3.0, -1.05)
  connectors DIM width 2: you->producer, producer bottom -> each front box top, director bottom -> each builder top.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# ---------------------------------------------------------------- shared look (as ch1_s5_director)
def agent(w, h, label=None, size=30, mono=False, outline=BLUE, fill_op=0.15, label_color=FG):
    back = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(width=0).set_fill(BG, 1)
    rect = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(outline, 3).set_fill(BLUE, fill_op)
    g = VGroup(back, rect)
    if label:
        t = (Mono if mono else T)(label, size=size, color=label_color)
        if t.width > w - 0.2:
            t.scale_to_fit_width(w - 0.2)
        g.add(t)
    return g


def builder_box(w, h):
    return RoundedRectangle(corner_radius=min(0.15, h / 3), width=w, height=h).set_stroke(BLUE, 3).set_fill(BLUE, 0.15)


def page(w, h, color=TEAL, fill_op=0.1, stroke=3):
    f = min(w, h) * 0.28
    body = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - f, 0],
                   [w / 2 - f, h / 2, 0], [-w / 2, h / 2, 0])
    body.set_stroke(color, stroke).set_fill(color, fill_op)
    corner = VMobject().set_points_as_corners([[w / 2 - f, h / 2, 0], [w / 2 - f, h / 2 - f, 0],
                                               [w / 2, h / 2 - f, 0]])
    corner.set_stroke(color, max(1.5, stroke - 1))
    return VGroup(body, corner)


def row_xs(cx, n, w, gap):
    pitch = w + gap
    return [cx + (i - (n - 1) / 2) * pitch for i in range(n)]


def conn(a, b, width=2):
    return Line(a.get_bottom(), b.get_top()).set_stroke(DIM, width).set_z_index(-1)


def badge(text, color, size=28):
    t = T(text, size=size, color=color)
    r = RoundedRectangle(corner_radius=0.1, width=t.width + 0.26, height=0.44).set_stroke(color, 2).set_fill(BG, 1)
    t.move_to(r)
    return VGroup(r, t).set_z_index(3)


def page_pair(w=0.6, h=0.75, two=True):
    if not two:
        return VGroup(page(w, h))
    back = page(w, h).shift(0.12 * UP + 0.12 * RIGHT)
    front = page(w, h)
    front.add_to_back(page(w, h)[0].set_stroke(width=0).set_fill(BG, 1))
    return VGroup(back, front)


def file_row(label, size=28, w=0.36, h=0.46, color=TEAL, label_color=FG):
    p = page(w, h, color=color)
    t = Mono(label, size=size, color=label_color).next_to(p, RIGHT, buff=0.2)
    return VGroup(p, t)


# ---- opacity helpers: scale every part's fill/stroke opacity relative to its full-strength value
def record(mob):
    for m in mob.get_family():
        if isinstance(m, VMobject):
            m._base = (m.get_fill_opacity(), m.get_stroke_opacity())


def set_k(mob, k):
    for m in mob.get_family():
        b = getattr(m, "_base", None)
        if b is not None:
            m.set_fill(opacity=b[0] * k, family=False)
            m.set_stroke(opacity=b[1] * k, family=False)
    return mob


ROW = 26.5   # one size for all four row labels (chapter-director is 2.54 wide in the 2.8 box)


class Crew(NarratedScene):
    def construct(self):
        # ------------------------------------------------ master shot pieces
        you = T("you", size=36, color=YELLOW).move_to([0, 3.4, 0])
        producer = agent(3.2, 0.8, "producer", 32).move_to([0, 2.45, 0])
        planner = agent(2.8, 0.7, "series-planner", ROW).move_to([-5.1, 1.0, 0])
        writers = VGroup(*[agent(2.8, 0.7, "script-writer" if k == 0 else None, ROW)
                           .move_to([-1.7 + 0.1 * k, 1.0 + 0.1 * k, 0]) for k in (2, 1, 0)])
        voice = agent(2.8, 0.7, "vk voice", ROW, mono=True, outline=DIM, label_color=DIM).move_to([1.7, 1.0, 0])
        dir_back = VGroup(*[agent(2.8, 0.7, None, 28, outline=DIM, fill_op=0.06)
                            .move_to([5.1 + 0.08 * k, 1.0 + 0.08 * k, 0]) for k in (2, 1)])
        dir_front = agent(2.8, 0.7, "chapter-director", ROW).move_to([5.1, 1.0, 0])
        builders = [builder_box(0.75, 0.45).move_to([x, -0.5, 0]) for x in row_xs(3.0, 8, 0.75, 0.15)]
        brow = VGroup(*builders)
        blabel = T("scene-builder × 6–8", size=28, color=DIM).move_to([3.0, -1.05, 0])
        top_conns = VGroup(Line(you.get_bottom() + 0.05 * DOWN, producer.get_top()).set_stroke(DIM, 2).set_z_index(-1),
                           *[conn(producer, b) for b in (planner, writers[-1], voice, dir_front)])
        bconn = VGroup(*[conn(dir_front, b) for b in builders])
        wfront = writers[-1]
        # "×N" count tags: T 26.5 DIM, right edge 0.1 inside the front box's right edge, centre y = 0.42
        w_n = T("×N", size=ROW, color=DIM)
        w_n.move_to([wfront.get_right()[0] - 0.1, 0.42, 0], aligned_edge=RIGHT)
        d_n = T("×N", size=ROW, color=DIM)
        d_n.move_to([dir_front.get_right()[0] - 0.1, 0.42, 0], aligned_edge=RIGHT)

        tree = VGroup(top_conns, bconn, you, producer, planner, writers, voice, dir_back, dir_front, brow, blabel, w_n, d_n)

        def enter(box, line):
            return [Create(line), FadeIn(box[0]), FadeIn(box[1]), FadeIn(box[2], shift=0.3 * DOWN)]

        # ================================================= c1.crew.1
        with self.say("c1.crew.1") as c:
            self.play(FadeIn(you, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("producer")
            self.play(*enter(producer, top_conns[0]), run_time=1.2)
            notes = VGroup(*[T(s, size=28, color=DIM) for s in ("plans", "runs the stages", "keeps the state files")])
            for n, y in zip(notes, (3.0, 2.62, 2.24)):
                n.move_to([2.0, y, 0], aligned_edge=LEFT)
            for n, cue, nxt in zip(notes, ("It plans", "runs each stage", "keeps the state"),
                                   ("runs each stage", "keeps the state", "planner")):
                c.wait_until(cue)
                self.play(FadeIn(n, shift=0.2 * LEFT), run_time=0.8)
            c.wait_until("planner")
            self.play(*enter(planner, top_conns[1]), run_time=1.2)
            c.wait_until("writers")
            # the three writers enter stacked on one spot, then fan out (parallel)
            finals = [w.get_center() for w in writers]
            for w in writers[:2]:
                w.move_to(wfront)
            self.play(FadeIn(writers[0]), FadeIn(writers[1]), FadeIn(wfront[0]), FadeIn(wfront[1]),
                      FadeIn(wfront[2], shift=0.3 * DOWN), Create(top_conns[2]), run_time=1.2)
            c.wait_until("one per chapter")
            self.play(FadeIn(w_n, shift=0.2 * DOWN), run_time=0.8)
            c.wait_until("all working at once")
            self.play(writers[0].animate.move_to(finals[0]), writers[1].animate.move_to(finals[1]),
                      run_time=min(1.0, c.until(floor=0.4)))

        # ================================================= c1.crew.2
        with self.say("c1.crew.2") as c:
            self.play(*enter(voice, top_conns[3]), run_time=1.2)
            no_tok = T("no tokens", size=28, color=GREEN).move_to([1.7, 0.36, 0])
            c.wait_until("uses no tokens")
            self.play(FadeIn(no_tok, shift=0.2 * DOWN), run_time=0.8)
            c.wait_until("directors")
            dfinals = [d.get_center() for d in dir_back]
            for d in dir_back:
                d.move_to(dir_front)
            self.play(FadeIn(dir_back[0]), FadeIn(dir_back[1]), FadeIn(dir_front[0]), FadeIn(dir_front[1]),
                      FadeIn(dir_front[2], shift=0.3 * DOWN), Create(top_conns[4]), run_time=1.2)
            c.wait_until("one per chapter")
            self.play(dir_back[0].animate.move_to(dfinals[0]), dir_back[1].animate.move_to(dfinals[1]),
                      FadeIn(d_n, shift=0.2 * DOWN), run_time=0.9)
            c.wait_until("one at a time")
            self.play(FlashAround(dir_front, color=BLUE, run_time=1.5, time_width=1.5))
            c.wait_until("builders")
            self.play(*[Create(l) for l in bconn],
                      LaggedStart(*[FadeIn(b, shift=0.15 * DOWN) for b in builders], lag_ratio=0.15),
                      run_time=1.8)
            c.wait_until("all in parallel")
            self.play(FadeIn(blabel, shift=0.2 * DOWN), run_time=0.9)

        # ================================================= c1.crew.3
        with self.say("c1.crew.3") as c:
            record(tree)
            settle(self, tree)
            tree.save_state()
            tree.generate_target()
            tree.target.scale(0.5).move_to([-3.0, 2.3, 0])
            set_k(tree.target, 0.4)
            self.play(MoveToTarget(tree), FadeOut(notes), FadeOut(no_tok), run_time=min(1.8, c.until("plan")))

            # conveyor of files, one stage per producer, left to right
            xs = row_xs(0, 6, 0.6, 1.64)          # pitch 2.24
            y = -1.4
            specs = [(("request +", "material"), True, you, DOWN),
                     (("PLAN.md", "project.json"), True, planner, UP),
                     (("script/", "chN_….md"), False, wfront, DOWN),
                     (("audio/*.wav", "manifest.json"), True, voice, UP),
                     (("scenes/", "chN_sK_….py"), False, brow, DOWN),
                     (("out/", "chN_….mp4"), False, dir_front, UP)]
            stages, pages_, arrows = [], [], []
            for (lines, two, src, side), x in zip(specs, xs):
                pg = page_pair(two=two).move_to([x, y, 0])
                lab = VGroup(*[Mono(s, size=28) for s in lines]).arrange(DOWN, buff=0.14)
                lab.next_to(pg, side, buff=0.18)
                if lab.get_left()[0] < -6.6:
                    lab.shift((-6.6 - lab.get_left()[0]) * RIGHT)
                st = VGroup(pg, lab).set_z_index(2)
                stages.append((st, src))
                pages_.append(pg)
            for a, b in zip(pages_[:-1], pages_[1:]):
                arrows.append(Arrow([a.get_right()[0], y, 0], [b.get_left()[0], y, 0], buff=0.12,
                                    stroke_width=3, tip_length=0.18, color=DIM))

            cues = ["plan", "become the plan file", "script", "audio", "scenes", "video"]
            nexts = ["become the plan file", "script", "audio", "scenes", "video", "files"]
            for i, (cue, nxt) in enumerate(zip(cues, nexts)):
                c.wait_until(cue)
                st, src = stages[i]
                anims = [TransformFromCopy(src, st)]
                if i > 0:
                    anims.append(GrowArrow(arrows[i - 1]))
                self.play(*anims, run_time=min(1.5, 0.75 * c.until(nxt)))

            c.wait_until("files")
            self.play(LaggedStart(*[FlashAround(p, color=TEAL, time_width=1.5) for p in pages_], lag_ratio=0.3),
                      run_time=min(3.0, 0.8 * c.until("brief")))

            c.wait_until("brief")
            note = T("paths + decisions", size=28, color=TEAL).set_z_index(3)
            note.next_to(producer, LEFT, buff=0.3)
            self.play(FadeIn(note, shift=0.2 * LEFT), run_time=0.8)
            self.play(note.animate.scale(0.4).move_to(planner).set_opacity(0), run_time=1.4)
            self.remove(note)

            c.wait_until("It reads only")
            reads = VGroup(*[file_row(s) for s in ("reports", "vk status", "STATUS.md", "PLAN.md")])
            for r, yy in zip(reads, (3.45, 2.85, 2.25, 1.65)):
                r.move_to([1.32, yy, 0], aligned_edge=LEFT)
            self.play(LaggedStart(*[FadeIn(r, shift=0.3 * RIGHT) for r in reads], lag_ratio=0.4),
                      FlashAround(producer, color=TEAL, run_time=1.5), run_time=2.2)

            drift = file_row("scenes/*.py").set_z_index(3)
            drift.move_to([1.32, 0.9, 0], aligned_edge=LEFT)
            self.play(FadeIn(drift, target_position=pages_[4].get_center()), run_time=1.2)
            c.wait_until("never the code")
            xmark = cross_mark(RED).scale(1.3).move_to(drift[0]).set_z_index(4)
            self.play(drift.animate.set_color(RED), Create(xmark), run_time=min(0.8, c.until(floor=0.4)))

        # ================================================= c1.crew.4
        with self.say("c1.crew.4") as c:
            sweep_clear(self, Restore(tree), keep=[tree])

            tick_page = page(0.34, 0.42).move_to([-1.5, 3.4, 0])
            tick_lab = Mono("PLAN.md", size=28).next_to(tick_page, LEFT, buff=0.18)
            tick = check_mark(YELLOW).scale(0.8).move_to([-0.8, 3.4, 0])
            tick_txt = T("the one checkpoint", size=30, color=YELLOW).move_to([-2.0, 2.75, 0], aligned_edge=RIGHT)
            c.wait_until("approve the plan")
            self.play(FadeIn(tick_page), FadeIn(tick_lab), Create(tick), run_time=1.0)
            self.play(FadeIn(tick_txt, shift=0.2 * DOWN), run_time=0.8)

            c.wait_until("state")
            states = VGroup(file_row("STATUS.md", w=0.4, h=0.5), file_row("projects/INDEX.md", w=0.4, h=0.5))
            for s, yy in zip(states, (-2.35, -3.15)):
                s.move_to([2.0, yy, 0], aligned_edge=LEFT)
            self.play(LaggedStart(*[FadeIn(s, shift=0.3 * DOWN) for s in states], lag_ratio=0.4), run_time=1.4)

            c.wait_until("resume")
            tree.generate_target()
            set_k(tree.target, 0.25)
            self.play(MoveToTarget(tree), run_time=1.2)
            prompt = Mono("continue <project>", size=32, color=YELLOW).move_to([-4.0, -2.3, 0])
            c.wait_until("you say continue")
            self.play(FadeIn(prompt, shift=0.2 * RIGHT), FadeOut(tick_page, tick_lab, tick, tick_txt), run_time=0.9)
            vks = agent(2.8, 0.7, "vk status", 28, mono=True, outline=DIM, label_color=DIM).move_to([-4.0, -3.15, 0])
            c.wait_until("vee-kay status reads")
            self.play(FadeIn(vks), run_time=0.8)
            paths = [Line(s[0].get_left(), vks.get_right() + 0.15 * (UP if i == 0 else DOWN))
                     for i, s in enumerate(states)]
            self.play(*[VShowPassingFlash(p.set_stroke(TEAL, 5), time_width=0.6) for p in paths],
                      *flash(states, color=TEAL), run_time=1.2)
            c.wait_until("find where it stopped")
            tree.generate_target()
            set_k(tree.target, 1.0)
            self.play(MoveToTarget(tree), run_time=min(1.2, c.until("agents")))

            c.wait_until("agents")
            # clear the whole resume/state row first, so nothing new lands on old text
            self.play(FadeOut(prompt, vks, states), run_time=0.7)
            # one agent file + Opus badge per agent type, each built in place at its own box
            def tag():
                return VGroup(page(0.26, 0.32).set_z_index(3), badge("Opus", BLUE)).arrange(RIGHT, buff=0.15)
            tags = VGroup(tag().next_to(producer, RIGHT, buff=0.3),
                          tag().move_to([-4.85, 0.3, 0]),
                          tag().move_to([-2.0, 0.3, 0]),
                          tag().move_to([dir_front.get_x() + 0.2, 1.88, 0]),
                          tag().move_to([1.3, -1.65, 0]))
            legend = VGroup(page(0.4, 0.5), Mono(".claude/agents/", size=30, color=TEAL), badge("Opus", BLUE))
            legend.arrange(RIGHT, buff=0.3).move_to([-1.5, -2.6, 0])
            self.play(LaggedStart(*[GrowFromCenter(t) for t in tags], lag_ratio=0.2), run_time=1.4)
            c.wait_until("agents folder")
            self.play(FadeIn(legend), run_time=0.9)

            c.wait_until("kit")
            cl_page = page(0.4, 0.5, color=DIM).move_to([-5.1, -0.55, 0])
            cl_lab = Mono("CLAUDE.md", size=28, color=DIM).next_to(cl_page, DOWN, buff=0.15)
            self.play(FadeIn(cl_page), FadeIn(cl_lab), run_time=0.8)
            cl_x = cross_mark(RED).scale(1.3).move_to(cl_page).set_z_index(4)
            self.play(Create(cl_x), run_time=0.7)
            kit = badge("kit", GOLD).next_to(cl_page, RIGHT, buff=0.35)
            c.wait_until("carries its whole kit")
            self.play(FadeIn(kit, shift=0.2 * UP), run_time=0.7)
            self.play(kit.animate.move_to([-6.05, 0.3, 0]), run_time=1.2)

            c.wait_until("depth")
            bx = 6.9
            levels = (producer.get_y(), dir_front.get_y(), builders[-1].get_y())
            bracket = VGroup(Line([bx, levels[0], 0], [bx, levels[2], 0]),
                             *[Line([bx - 0.15, yy, 0], [bx, yy, 0]) for yy in levels]).set_stroke(YELLOW, 4)
            depth_txt = T("two deep (limit: three)", size=30, color=YELLOW)
            depth_txt.move_to([6.5, -1.75, 0], aligned_edge=RIGHT)
            path = [top_conns[4], bconn[-1]]
            self.play(Create(bracket), *[l.animate.set_stroke(YELLOW, 3) for l in path], run_time=1.5)
            self.play(FadeIn(depth_txt, shift=0.2 * DOWN), run_time=0.9)

        # back to the master shot alone, hold, fade
        self.wait(1.5)
        self.play(FadeOut(tags, legend, cl_page, cl_lab, cl_x, kit, bracket, depth_txt),
                  *[l.animate.set_stroke(DIM, 2) for l in path], run_time=1.0)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
