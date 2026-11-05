"""Chapter 1, scene 7: graph databases, and setting up Traverse. Clips c1.trav.1 – c1.trav.3."""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


def card(text, w=3.0, h=1.15, size=38, color=BLUE):
    lab = T(text, size)
    w = max(w, lab.width + 0.7)
    box = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(color, 3).set_fill(BG, 1)
    lab.move_to(box)
    return VGroup(box, lab)


def badge(text, color):
    lab = T(text, 32, color)
    pill = RoundedRectangle(corner_radius=0.3, width=lab.width + 0.55, height=0.62)
    pill.set_stroke(color, 2.5).set_fill(color, 0.15).move_to(lab)
    return VGroup(pill, lab)


def cylinder_icon(color=FG):
    w, h = 0.46, 0.5
    top = Ellipse(width=w, height=0.16).set_stroke(color, 3).shift(UP * h / 2)
    left = Line(UP * h / 2 + LEFT * w / 2, DOWN * h / 2 + LEFT * w / 2).set_stroke(color, 3)
    right = Line(UP * h / 2 + RIGHT * w / 2, DOWN * h / 2 + RIGHT * w / 2).set_stroke(color, 3)
    bot = Arc(radius=w / 2, start_angle=PI, angle=PI).stretch(0.08 / (w / 2), 1)
    bot.set_stroke(color, 3).shift(DOWN * h / 2)
    return VGroup(top, left, right, bot)


def folder_icon(color=FG):
    p = Polygon([-0.28, 0.2, 0], [-0.08, 0.2, 0], [0.0, 0.12, 0], [0.28, 0.12, 0],
                [0.28, -0.2, 0], [-0.28, -0.2, 0])
    return p.set_stroke(color, 3).set_fill(BG, 0)


def file_icon(color=GOLD):
    body = Polygon([-0.35, 0.45, 0], [0.15, 0.45, 0], [0.35, 0.25, 0], [0.35, -0.45, 0],
                   [-0.35, -0.45, 0]).set_stroke(color, 3).set_fill(color, 0.12)
    fold = VMobject().set_points_as_corners([[0.15, 0.45, 0], [0.15, 0.25, 0], [0.35, 0.25, 0]])
    fold.set_stroke(color, 2.5)
    lab = Mono("movies.tvdb", 28).next_to(body, DOWN, buff=0.18)
    return VGroup(body, fold, lab)


class Traverse(NarratedScene):
    def construct(self):
        self.clip_dbs()
        self.clip_setup()
        self.clip_shell()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c1.trav.1
    def clip_dbs(self):
        title = T("Graph databases", 52).move_to(UP * 2.7)
        neo, mem, nep = card("Neo4j"), card("Memgraph"), card("Amazon Neptune")
        dots = T("…", 48)
        VGroup(neo, mem, nep, dots).arrange(RIGHT, buff=0.35).move_to(UP * 0.8)
        duck = card("DuckDB").move_to(LEFT * 2.2 + DOWN * 1.4)
        json = badge("JSON", TEAL).next_to(duck, RIGHT, buff=0.45)
        graphs = badge("graphs", YELLOW).next_to(json, RIGHT, buff=0.3)

        trav = card("Traverse", w=4.6, h=1.4, size=52, color=YELLOW).move_to(RIGHT * 2.9 + UP * 0.7)
        neo_dst = neo.copy().move_to(LEFT * 3.9 + UP * 0.7)
        cy_t = T("Cypher", 44, YELLOW).next_to(trav, DOWN, buff=0.45)
        cy_n = T("Cypher", 44, YELLOW).move_to([neo_dst.get_x(), cy_t.get_y(), 0])
        browser = VGroup(T("runs in your web browser:", 38, GREEN),
                         T("nothing to install", 38, GREEN)).arrange(DOWN, buff=0.22)
        browser.next_to(cy_t, DOWN, buff=0.6)
        java = T("Java + a server", 38, DIM).move_to([neo_dst.get_x(), browser[0].get_y(), 0])

        with self.say("c1.trav.1", gap=1.0) as c:
            self.play(*appear(title), run_time=min(1.0, c.until("Neo four J")))  # early: title of the shot
            c.wait_until("Neo four J")
            self.play(*appear(neo), run_time=0.9)
            c.wait_until("Memgraph")
            self.play(*appear(mem), run_time=0.9)
            c.wait_until("Amazon Neptune")
            self.play(*appear(nep, dots, lag=0.4), run_time=1.2)
            c.wait_until("duck")
            self.play(*appear(duck, json, lag=0.4), run_time=min(1.2, c.until("graph features")))  # early: JSON badge recalls Lecture 4
            c.wait_until("graph features")
            self.play(*appear(graphs), run_time=1.0)
            self.play(FlashAround(graphs, color=YELLOW, run_time=1.2, time_width=1.5))
            c.wait_until("store JSON")
            self.play(FlashAround(json, color=TEAL, run_time=min(1.4, c.until("traverse")), time_width=1.5))

            c.wait_until("traverse")
            self.play(*during(disappear(title, mem, nep, dots, duck, json, graphs), 0, 0.45),
                      *during([neo.animate.move_to(neo_dst)], 0.4, 0.85),
                      *during(appear(trav), 0.55, 1.0),
                      run_time=min(2.0, c.until("Cypher")))
            c.wait_until("Cypher")
            self.play(*appear(cy_t), run_time=1.0)
            c.wait_until("Neo four J", nth=1)
            self.play(*fly(cy_t, cy_n), run_time=min(1.5, c.until("browser")))
            c.wait_until("browser")
            self.play(*appear(browser[0]), run_time=1.0)
            c.wait_until("No Java")
            self.play(*appear(java), run_time=0.9)
            c.wait_until("nothing to install")
            self.play(*appear(browser[1]), run_time=0.9)
        self.dbs_group = [neo, trav, cy_t, cy_n, browser, java]

    # ------------------------------------------------------------------ c1.trav.2
    def clip_setup(self):
        # browser window
        win = RoundedRectangle(corner_radius=0.2, width=10.2, height=6.8).set_stroke(DIM, 3)
        win.set_fill(BG, 1).move_to(RIGHT * 1.5 + DOWN * 0.15)
        bar_y = win.get_top()[1] - 0.6
        bar_line = Line([win.get_left()[0], bar_y - 0.6, 0], [win.get_right()[0], bar_y - 0.6, 0])
        bar_line.set_stroke(DIM, 2)
        lights = VGroup(*[Dot(radius=0.09, color=col) for col in (RED, GOLD, GREEN)]).arrange(RIGHT, buff=0.16)
        lights.move_to([win.get_left()[0] + 0.6, bar_y, 0])
        addr = RoundedRectangle(corner_radius=0.2, width=7.8, height=0.6).set_stroke(DIM, 2)
        addr.move_to([win.get_x() + 0.6, bar_y, 0])
        side_x = win.get_left()[0] + 4.0
        side_line = Line([side_x, bar_y - 0.6, 0], [side_x, win.get_bottom()[1], 0]).set_stroke(DIM, 2)
        cyl = cylinder_icon().move_to([win.get_left()[0] + 0.7, bar_y - 1.25, 0])
        fold = folder_icon().move_to([win.get_left()[0] + 1.6, bar_y - 1.25, 0])
        window = VGroup(win, bar_line, lights, addr, side_line, cyl, fold)

        url = Mono("https://traverse.truespar.com/", 28).move_to(addr)
        side_cx = (win.get_left()[0] + side_x) / 2
        main_cx = (side_x + win.get_right()[0]) / 2
        db_name = T("movies", 34, weight=BOLD).move_to([side_cx, 0.4, 0])
        db_nodes = T("Nodes: Movie, Person", 28).next_to(db_name, DOWN, buff=0.25)
        demo_note = T("demo: smaller, other properties", 28, DIM).move_to([main_cx, 0.4, 0])

        course = VGroup(T("course", 28, DIM), T("materials page", 28, DIM)).arrange(DOWN, buff=0.12)
        course.move_to([-5.35, 2.3, 0])
        file = file_icon().move_to([-5.35, 0.1, 0])

        ring = Circle(radius=0.45).set_stroke(YELLOW, 4).move_to(cyl)
        ring2 = Circle(radius=0.45).set_stroke(YELLOW, 4).move_to(fold)
        del_lab = T("Delete", 30)
        del_btn = VGroup(RoundedRectangle(corner_radius=0.12, width=del_lab.width + 0.6, height=0.62)
                         .set_stroke(RED, 0).set_fill(RED, 0.85).move_to(del_lab), del_lab)
        del_btn.move_to([side_cx, -1.1, 0])

        d_title = T("Delete database", 32, weight=BOLD)
        d_hint = T("Type delete to confirm", 28)
        d_field_txt = Mono("delete", 28)
        d_field = VGroup(Rectangle(width=4.0, height=0.6).set_stroke(DIM, 2), d_field_txt)
        d_field_txt.move_to(d_field[0]).align_to(d_field[0], LEFT).shift(RIGHT * 0.2)
        d_body = VGroup(d_title, d_hint, d_field).arrange(DOWN, buff=0.3)
        d_box = RoundedRectangle(corner_radius=0.15, width=4.9, height=d_body.height + 0.6)
        d_box.set_stroke(RED, 2.5).set_fill(BG, 1).move_to(d_body)
        dialog = VGroup(d_box, d_title, d_hint, d_field).move_to([main_cx, -1.6, 0])

        up_lab = T("Upload .tvdb or .tvmodel", 30)
        up_btn = VGroup(RoundedRectangle(corner_radius=0.12, width=up_lab.width + 0.6, height=0.66)
                        .set_stroke(BLUE, 2.5).set_fill(BLUE, 0.2).move_to(up_lab), up_lab)
        up_btn.move_to([main_cx, 1.25, 0])
        file_dst = file.copy().move_to([main_cx, -0.6, 0])

        with self.say("c1.trav.2", gap=0.8) as c:
            sweep_clear(self, FadeIn(window), run_time=min(1.6, c.until("download")))
            c.wait_until("download")
            self.play(*appear(*course, lag=0.3), run_time=0.9)  # early: the file's source, said as "course page"
            self.play(FadeIn(file, shift=1.0 * DOWN), run_time=min(1.2, c.until("open")))
            c.wait_until("open")
            self.play(*appear(url), run_time=1.0)
            c.wait_until("demo")
            self.play(*appear(db_name, db_nodes, lag=0.5), run_time=1.3)
            c.wait_until("smaller")
            self.play(*appear(demo_note), run_time=1.0)
            c.wait_until("delete")
            self.play(GrowFromCenter(ring), run_time=0.8)
            c.wait_until("then Delete")
            self.play(*appear(del_btn), run_time=0.8)
            c.wait_until("type the word")
            self.play(*appear(dialog), run_time=1.0)
            c.wait_until("upload")
            self.play(*disappear(del_btn, db_name, db_nodes, demo_note),
                      ReplacementTransform(ring, ring2), run_time=1.0)
            c.wait_until("then Upload")
            self.play(*during(disappear(dialog), 0, 0.45), *during(appear(up_btn), 0.5, 1.0), run_time=1.2)
            c.wait_until("pick the file")
            self.play(*fly(file, file_dst), run_time=min(1.5, c.until()))
        self.ring2 = ring2

    # ------------------------------------------------------------------ c1.trav.3
    def clip_shell(self):
        url = Mono("https://github.com/ept/cypher-shell", 28, color=BLUE).move_to(UP * 2.75)
        l1 = Mono("$ node cypher-shell.mjs movies.tvdb", 28, t2c={"$": DIM})
        l2 = Mono("Traverse 0.8.0: movies.tvdb has", 28)
        l3 = Mono("26114 nodes and 49811 relationships.", 28)
        l4 = Mono("Enter :help for help. Changes are lost on exit", 28)
        l5 = Mono("unless you use :save.", 28)
        l6 = Mono("cypher>", 28, color=YELLOW)
        lines = VGroup(l1, l2, l3, l4, l5, l6).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        for m in (l4, l5, l6):
            m.shift(DOWN * 0.55)
        term = RoundedRectangle(corner_radius=0.18, width=12.4, height=lines.height + 0.8)
        term.set_stroke(DIM, 2.5).set_fill(BG, 1)
        lines.move_to(term).align_to(term, LEFT).shift(RIGHT * 0.5)
        VGroup(term, lines).move_to(DOWN * 0.35)

        nodes = select(l3, "26114 nodes")[0]
        rels = select(l3, "49811 relationships")[0]
        split = T("= 2,935 + 23,179", 28, GOLD)
        split.move_to([nodes.get_x(), (l3.get_bottom()[1] + l4.get_top()[1]) / 2, 0])
        tag = T("tables, no picture", 30, DIM).next_to(term, DOWN, buff=0.25).align_to(term, RIGHT)

        with self.say("c1.trav.3") as c:
            c.wait_until("small program")
            sweep_clear(self, FadeIn(term), *appear(l1), run_time=min(1.4, c.until("cypher shell")))
            c.wait_until("cypher shell")
            self.play(*appear(url), run_time=1.0)
            c.wait_until("same engine")
            self.play(*appear(l2, l3, l4, l5, l6, lag=0.25), run_time=min(1.8, c.until("banner")))
            c.wait_until("banner")
            self.play(*recolor(nodes, GOLD), *appear(split), run_time=1.0)
            self.play(*recolor(rels, GOLD), run_time=0.8)
            c.wait_until("text tables")
            self.play(*appear(tag), run_time=1.0)
        self.wait(1.2)
