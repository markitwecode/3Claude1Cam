"""Tiny CE 0.22 scenes backing the "verified how" column of ../GL_TO_CE.md.

Each scene exercises one group of translations. Render them all (last frame only):

    .venv/bin/manim -ql -s --media_dir reference/3b1b/_scratch_media \
        reference/3b1b/tools/gl_to_ce_snippets.py -a

A scene that renders without error, and whose last frame looks right, is what
"rendered" means in the table. Scenes are named V01..V16 to match the table.
"""
from manim import *


class V01_FadeArgs(Scene):
    """GL FadeIn(m, shift=v) == CE FadeIn(m, shift=v); GL FadeIn(m, scale=2) == CE FadeIn(m, scale=0.5)."""
    def construct(self):
        a, b, c = Square(1), Circle(0.5), Triangle()
        VGroup(a, b, c).arrange(RIGHT, buff=1)
        self.play(FadeIn(a, shift=UP))          # rises into place (same in GL)
        self.play(FadeIn(b, scale=0.5))         # grows from half size (GL: scale=2)
        self.play(FadeIn(c, target_position=ORIGIN + 3 * DOWN, scale=0.1))  # GL FadeInFromPoint
        d = Dot().next_to(c, RIGHT)
        self.add(d)
        self.play(FadeOut(d, shift=RIGHT, scale=0.5))  # FadeOut semantics match GL
        self.add(Text("V01 fade args", font_size=24).to_corner(UL))


class V02_WriteCreate(Scene):
    """GL ShowCreation -> CE Create; Write on Text/MathTex; DrawBorderThenFill; Uncreate."""
    def construct(self):
        t = Text("Write on Text", font_size=40)
        m = MathTex(r"\sum_{k=1}^n k = \frac{n(n+1)}{2}")
        c = Circle(0.6, color=BLUE)
        s = Square(1, fill_opacity=0.6, color=GREEN)
        VGroup(t, m, VGroup(c, s).arrange(RIGHT)).arrange(DOWN, buff=0.6)
        self.play(Write(t))                       # CE: run_time 1 (<15 glyphs) else 2
        self.play(Write(m, run_time=1.5))
        self.play(Create(c), DrawBorderThenFill(s))
        tmp = Line(LEFT, RIGHT).next_to(c, DOWN)
        self.play(Create(tmp)); self.play(Uncreate(tmp))
        self.add(Text("V02 write/create", font_size=24).to_corner(UL))


class V03_TexKinds(Scene):
    """GL Tex == CE MathTex, GL TexText == CE Tex, GL Text == CE Text. t2c / isolate."""
    def construct(self):
        math = MathTex(r"e^{i\pi} + 1 = 0", tex_to_color_map={r"\pi": YELLOW, "e": BLUE})
        text_mode = Tex(r"The area is $\pi r^2$", tex_to_color_map={"area": GREEN})
        pango = Text("plain Text with t2c", t2c={"t2c": RED}, font_size=36)
        parts = MathTex("{{a}}^2 + {{b}}^2 = {{c}}^2")   # no spaces: "{{ b }}" would be the part " b "
        parts.set_color_by_tex("b", TEAL)        # exact match on a part's tex_string
        iso = MathTex(r"f(x) = x^2 + 2x + 1", substrings_to_isolate=["x"])
        first_x = iso.get_part_by_tex("x")       # FIRST occurrence only
        box = SurroundingRectangle(first_x, buff=0.05)
        VGroup(math, text_mode, pango, parts, iso).arrange(DOWN, buff=0.45)
        box.move_to(first_x)
        self.add(math, text_mode, pango, parts, iso, box)
        self.add(Text("V03 MathTex/Tex/Text", font_size=24).to_corner(UL))


class V04_TransformMatching(Scene):
    """CE TransformMatchingTex matches whole parts by tex_string; TransformMatchingShapes by glyph shape."""
    def construct(self):
        a = MathTex("{{ a }}^2", "+", "{{ b }}^2", "=", "{{ c }}^2").shift(UP)
        b = MathTex("{{ c }}^2", "=", "{{ a }}^2", "+", "{{ b }}^2").shift(UP)
        self.add(a)
        self.play(TransformMatchingTex(a, b, path_arc=PI / 2))
        t1 = Text("silent", font_size=48).shift(DOWN)
        t2 = Text("listen", font_size=48).shift(DOWN)
        self.add(t1)
        self.play(TransformMatchingShapes(t1, t2, path_arc=PI / 2))
        k1 = MathTex("{{ x }} + {{ y }}").shift(2.5 * DOWN)
        k2 = MathTex("{{ x }} - {{ z }}").shift(2.5 * DOWN)
        self.add(k1)
        self.play(TransformMatchingTex(k1, k2, key_map={" y ": " z "}))  # keys include the spaces
        self.add(Text("V04 matching transforms", font_size=24).to_corner(UL))


class V05_Transforms(Scene):
    """TransformFromCopy, ReplacementTransform, FadeTransform(Pieces), MoveToTarget, Restore."""
    def construct(self):
        a = Square(0.8, color=BLUE).shift(4 * LEFT + UP)
        b = Circle(0.4, color=RED).shift(1.5 * LEFT + UP)
        self.add(a)
        self.play(TransformFromCopy(a, b, path_arc=-PI / 2))   # a stays, copy morphs into b
        c = Triangle(color=GREEN).scale(0.5).shift(1 * RIGHT + UP)
        self.play(ReplacementTransform(b, c))                   # b leaves scene, c remains
        w1 = MathTex("x^2").shift(4 * RIGHT + UP)
        w2 = Text("squared", font_size=30).shift(4 * RIGHT + UP)
        self.add(w1)
        self.play(FadeTransform(w1, w2))
        g1 = VGroup(*[Dot() for _ in range(3)]).arrange(RIGHT).shift(DOWN + 3 * LEFT)
        g2 = VGroup(*[Square(0.3) for _ in range(3)]).arrange(DOWN).shift(DOWN + 1 * LEFT)
        self.add(g1)
        self.play(FadeTransformPieces(g1, g2))
        s = Star(color=YELLOW).scale(0.4).shift(DOWN + 2 * RIGHT)
        self.add(s)
        s.save_state()
        s.generate_target()
        s.target.shift(RIGHT * 2).set_color(PINK)
        self.play(MoveToTarget(s))
        self.play(Restore(s))
        self.add(Text("V05 transforms", font_size=24).to_corner(UL))


class V06_Lagged(Scene):
    """lag_ratio on LaggedStart / LaggedStartMap / AnimationGroup / the animation / play()."""
    def construct(self):
        rows = [VGroup(*[Square(0.4) for _ in range(8)]).arrange(RIGHT, buff=0.15) for _ in range(5)]
        VGroup(*rows).arrange(DOWN, buff=0.3)
        self.play(LaggedStart(*[FadeIn(m, shift=0.3 * UP) for m in rows[0]], lag_ratio=0.2))
        self.play(LaggedStartMap(FadeIn, rows[1], shift=0.3 * UP, lag_ratio=0.2))
        self.play(AnimationGroup(*[GrowFromCenter(m) for m in rows[2]], lag_ratio=0.1))
        self.play(FadeIn(rows[3], lag_ratio=0.3))           # lag across submobjects
        self.play(Create(rows[4]), lag_ratio=0.1)           # play() kwarg is set on each anim
        self.add(Text("V06 lag_ratio", font_size=24).to_corner(UL))


class V07_Indications(Scene):
    """CE's own highlight family: Circumscribe, ShowPassingFlash, Indicate, Flash, Wiggle."""
    def construct(self):
        words = VGroup(*[Text(w, font_size=40) for w in ["circumscribe", "passing flash", "indicate", "flash", "wiggle"]])
        words.arrange(DOWN, buff=0.5)
        self.add(words)
        self.play(Circumscribe(words[0], time_width=0.5))
        self.play(ShowPassingFlash(SurroundingRectangle(words[1], color=YELLOW), time_width=0.5))
        self.play(Indicate(words[2]))
        self.play(Flash(words[3].get_right() + 0.3 * RIGHT, flash_radius=0.3))
        self.play(Wiggle(words[4]))
        self.add(Text("V07 indications", font_size=24).to_corner(UL))


class V08_Backstroke(Scene):
    """GL set_backstroke(BLACK, 5) -> CE set_stroke(BLACK, 5, background=True)."""
    def construct(self):
        plane = NumberPlane(background_line_style={"stroke_color": BLUE, "stroke_width": 4})
        self.add(plane)
        plain = MathTex(r"f(x) = x^2", font_size=72).shift(2 * UP)
        backed = MathTex(r"f(x) = x^2", font_size=72)
        backed.set_stroke(BLACK, 8, background=True)
        txt = Text("label with backstroke", font_size=40).shift(2 * DOWN)
        txt.set_stroke(BLACK, 6, background=True)
        self.add(plain, backed, txt)
        self.add(Text("V08 backstroke (top: none)", font_size=24).to_corner(UL).set_stroke(BLACK, 4, background=True))


class V09_Braces(Scene):
    """Brace, brace.get_tex / get_text (no style kwargs!), put_at_tip, BraceLabel(font_size=)."""
    def construct(self):
        bar = Rectangle(width=5, height=0.5, color=BLUE).shift(UP)
        b1 = Brace(bar, DOWN, buff=0.1)
        lab1 = b1.get_tex("n")                    # MathTex, kwargs go to put_at_tip
        b2 = Brace(bar, UP)
        lab2 = MathTex(r"\frac{n}{2}", font_size=30)
        b2.put_at_tip(lab2, buff=0.1)             # styled label: build it, then put_at_tip
        b3 = Brace(bar, RIGHT)
        lab3 = b3.get_text("height")              # CE get_text returns Tex (text mode)
        sq = Square(1).shift(2 * DOWN)
        bl = BraceLabel(sq, "s", brace_direction=LEFT, font_size=36)  # label style kwargs OK here
        self.add(bar, b1, lab1, b2, lab2, b3, lab3, sq, bl)
        self.play(GrowFromCenter(Brace(bar, DOWN, buff=0.8)))
        self.add(Text("V09 braces", font_size=24).to_corner(UL))


class V10_Numbers(Scene):
    """DecimalNumber / Integer, ChangeDecimalToValue, CountInFrom idiom, make_number_changeable idiom."""
    def construct(self):
        d = DecimalNumber(0, num_decimal_places=2, include_sign=True, font_size=60).shift(2 * UP)
        self.add(d)
        self.play(ChangeDecimalToValue(d, -3.14159, run_time=1))
        n = Integer(250, font_size=60)
        self.add(n)
        self.play(ChangeDecimalToValue(n, 1000), run_time=1)      # GL CountInFrom(n, 0): set_value(0) first
        # GL: tex.make_number_changeable("0.00") -- CE: build the label and the number separately
        tracker = ValueTracker(0.5)
        lhs = MathTex("p =", font_size=60)
        val = DecimalNumber(tracker.get_value(), font_size=60)
        row = VGroup(lhs, val).arrange(RIGHT).shift(2 * DOWN)
        val.add_updater(lambda m: m.set_value(tracker.get_value()).next_to(lhs, RIGHT))
        pct = DecimalNumber(37.5, unit=r"\%", num_decimal_places=1).next_to(row, RIGHT, buff=1)
        self.add(row, pct)
        self.play(tracker.animate.set_value(0.87))
        self.add(Text("V10 numbers", font_size=24).to_corner(UL))


class V11_Updaters(Scene):
    """ValueTracker + always_redraw / add_updater(call_updater=True) / mob.always / f_always."""
    def construct(self):
        t = ValueTracker(-3)
        dot = Dot(color=YELLOW).add_updater(lambda m: m.move_to(t.get_value() * RIGHT), call_updater=True)
        label = Text("dot", font_size=30)
        label.always.next_to(dot, UP)                     # GL: label.always.next_to(dot, UP)
        line = always_redraw(lambda: Line(ORIGIN + 2 * DOWN, dot.get_center(), color=BLUE))
        num = DecimalNumber(0)
        f_always(num.set_value, t.get_value)              # GL: num.f_always.set_value(t.get_value)
        num.always.to_corner(UR)
        sq = Square(0.5).shift(2 * UP)
        trail = TracedPath(dot.get_center, dissipating_time=0.5, stroke_color=YELLOW)  # GL TracingTail(dot, time_traced=0.5)
        self.add(trail, dot, label, line, num, sq)
        self.play(t.animate.set_value(3), run_time=1.5)
        self.play(UpdateFromAlphaFunc(sq, lambda m, a: m.set_fill(RED, opacity=a)))
        self.play(t.animate.increment_value(-2))
        dot.clear_updaters()
        self.add(Text("V11 updaters", font_size=24).to_corner(UL))


class V12_MovingCamera(MovingCameraScene):
    """GL self.frame -> CE self.camera.frame (MovingCameraScene); save_state/Restore; auto_zoom."""
    def construct(self):
        grid = VGroup(*[Square(0.8).set_stroke(GREY_B, 2) for _ in range(40)]).arrange_in_grid(5, 8, buff=0.1)
        target = grid[13].copy().set_fill(YELLOW, 0.8)
        self.add(grid, target)
        frame = self.camera.frame
        frame.save_state()
        self.play(frame.animate.set(height=3).move_to(target))   # GL: frame.animate.set_height(3).move_to(t)
        self.play(frame.animate.shift(RIGHT * 2))
        self.play(Restore(frame))
        self.play(self.camera.auto_zoom(grid[:8], margin=0.3))
        self.add(Text("V12 moving camera", font_size=12).next_to(grid[0], UP, aligned_edge=LEFT))


class V13_ThreeD(ThreeDScene):
    """GL frame.reorient(theta, phi) -> CE set_camera_orientation(theta=theta-90deg, phi=phi)."""
    def construct(self):
        axes = ThreeDAxes(x_range=(-3, 3), y_range=(-3, 3), z_range=(-2, 2), x_length=6, y_length=6, z_length=4)
        surf = Surface(lambda u, v: axes.c2p(u, v, 0.4 * np.sin(u) * np.cos(v)),
                       u_range=(-3, 3), v_range=(-3, 3), resolution=(16, 16), fill_opacity=0.7)
        xlab = MathTex("x").move_to(axes.c2p(3.4, 0, 0))
        self.set_camera_orientation(theta=-120 * DEGREES, phi=70 * DEGREES)   # GL reorient(-30, 70)
        title = Text("V13 3D: GL reorient(-30,70)", font_size=24).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)                               # GL: title.fix_in_frame()
        self.add(axes, surf, xlab)
        self.move_camera(theta=-150 * DEGREES, zoom=1.2, run_time=1)          # GL frame.animate.reorient(-60).set_height(8/1.2)
        self.begin_ambient_camera_rotation(rate=0.2)                          # GL frame.add_ambient_rotation(0.2)
        self.wait(0.5)
        self.stop_ambient_camera_rotation()


class V14_Axes(Scene):
    """Axes(x_length, y_length) + plot + get_graph_label + add_coordinates; NumberLine.add_numbers."""
    def construct(self):
        axes = Axes(x_range=(-3, 3, 1), y_range=(-1, 9, 2), x_length=6, y_length=4, tips=False).shift(UP * 0.6)
        axes.add_coordinates()                                   # GL add_coordinate_labels()
        g = axes.plot(lambda x: x ** 2, x_range=(-3, 3), color=BLUE)   # GL axes.get_graph(f)
        lab = axes.get_graph_label(g, "x^2", x_val=2.5, direction=RIGHT)
        dot = Dot(axes.i2gp(2, g), color=YELLOW)
        area = axes.get_area(g, x_range=(0, 2), opacity=0.4)
        nl = NumberLine(x_range=(0, 10, 1), length=8).to_edge(DOWN)   # GL NumberLine(width=8)
        nl.add_numbers(font_size=24)
        tick = Dot(nl.n2p(7), color=RED)
        self.add(axes, g, lab, dot, area, nl, tick)
        self.add(Text("V14 axes", font_size=24).to_corner(UL))


class V15_Geometry(Scene):
    """Arrow/Vector/DashedLine/Arc/Rectangle/SurroundingRectangle/BackgroundRectangle/Underline/Cross."""
    def construct(self):
        arr = Arrow(LEFT * 2, RIGHT * 2, buff=0, stroke_width=6, color=BLUE)   # GL thickness -> stroke_width
        vec = Vector(UP * 1.5, color=GREEN)
        dash = DashedLine(LEFT, RIGHT, dash_length=0.1)
        arc = Arc(radius=0.8, start_angle=0, angle=PI, color=YELLOW)          # keywords! positional order differs
        rect = Rectangle(width=2.5, height=1, color=PURPLE)                    # keywords! GL (width, height) positional
        word = Text("underline me", font_size=32)
        under = Underline(word, buff=0.1, color=YELLOW)
        boxed = Text("boxed", font_size=32)
        box = SurroundingRectangle(boxed, buff=0.15, corner_radius=0.1)
        on_plane = Text("bg rect", font_size=32)
        bg = BackgroundRectangle(on_plane, buff=0.1, fill_opacity=0.8)
        crossed = Text("wrong", font_size=32)
        cross = Cross(crossed, stroke_width=4)
        grid = VGroup(arr, vec, dash, arc, rect, VGroup(word, under), VGroup(boxed, box),
                      VGroup(bg, on_plane), VGroup(crossed, cross))
        grid.arrange_in_grid(3, 3, buff=0.6)
        self.add(NumberPlane().set_opacity(0.3))
        self.play(GrowArrow(arr), GrowFromCenter(rect), Create(arc))
        self.play(Rotate(rect, PI / 4, about_point=rect.get_left()))
        self.add(vec, dash, word, under, boxed, box, bg, on_plane, crossed, cross)
        self.add(Text("V15 geometry", font_size=24).to_corner(UL))


class V16_Layout(Scene):
    """arrange / arrange_in_grid(rows, cols, buff=(h, v)) / next_to aligned_edge / sizing idioms."""
    def construct(self):
        cell = Square(0.5, fill_opacity=0.5, color=TEAL)
        grid = VGroup(*(cell.copy() for _ in range(12)))          # GL cell.get_grid(3, 4) / replicate
        grid.arrange_in_grid(3, 4, buff=(0.1, 0.3))               # (horizontal, vertical) buff
        grid.to_edge(LEFT)
        wide = Text("a long caption that is too wide for the slot", font_size=40)
        if wide.width > 5:                                        # GL set_max_width(5)
            wide.scale_to_fit_width(5)
        wide.next_to(grid, RIGHT, buff=0.5, aligned_edge=UP)
        tall = Rectangle(width=1, height=1, color=RED).next_to(wide, DOWN, aligned_edge=LEFT)
        tall.stretch_to_fit_height(2, about_edge=UP)              # GL set_height(2, stretch=True, about_edge=UP)
        sized = Circle(color=YELLOW).scale_to_fit_height(1.5).next_to(tall, RIGHT)  # GL set_height(1.5)
        self.add(grid, wide, tall, sized)
        self.add(Text("V16 layout", font_size=24).to_corner(UL))
