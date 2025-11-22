from manim import *

widget_thickness = 0.7

widget_length = 1.0

# percent
preview_size = 0

offset_size = 0.3

extra_trigger_area = 0.3


def calculate_widget_reveal_size(progress: float):
    progress = max(progress, preview_size)
    return (offset_size + widget_thickness) * progress


def calculate_surface_size(progress: float):
    reveal_size = calculate_widget_reveal_size(progress)
    return reveal_size + extra_trigger_area


def calculate_vars(progress: float):
    progress = max(progress, preview_size)

    # at left
    x = (offset_size + widget_thickness) * (progress - 1) + offset_size
    y = 0.0
    surface_width = calculate_surface_size(progress)
    surface_height = widget_length
    return x, y, surface_width, surface_height


texts: list


def get_vars(progress: float, update_arrow=False):
    global texts

    x, y, surface_width, surface_height = calculate_vars(progress)
    x = round(x, 2)
    y = round(y, 2)
    surface_width = round(surface_width, 2)
    surface_height = round(surface_height, 2)
    font_size = 18
    texts = [
        Text(font="TX-02", text=f"x = {x}", font_size=font_size),
        Text(font="TX-02", text=f"y = {y}", font_size=font_size),
        Text(
            font="TX-02", text=f"surface_width = {surface_width}", font_size=font_size
        ),
        Text(
            font="TX-02", text=f"surface_height = {surface_height}", font_size=font_size
        ),
    ]
    if update_arrow:
        up_arrow_x = Arrow(
            start=DOWN * 0.2,
            end=0,
            buff=0,
            color=WHITE,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )
        up_arrow_x.next_to(texts[0].get_right())
        up_arrow_width = up_arrow_x.copy()
        up_arrow_width.next_to(texts[2].get_right())

        texts.append(up_arrow_x)
        texts.append(up_arrow_width)

    variables = VGroup(*texts).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

    return variables


class WaylandComponentAnimation(MovingCameraScene):
    def construct(self):
        global texts

        # 1. 绘制屏幕框
        screen = Rectangle(
            width=6,
            height=4,
            fill_color=GRAY,
            fill_opacity=0.2,
            stroke_color=GRAY,
            stroke_opacity=0.5,
            stroke_width=3,
        )
        screen_label = Text("Screen", font_size=24).next_to(screen, UP)

        self.play(Create(screen), Write(screen_label))

        # 2. 绘制组件（天蓝色，右侧圆角）
        component = RoundedRectangle(
            width=widget_thickness,
            height=widget_length,
            corner_radius=[0, 0, 0.1, 0.1],
            fill_color=BLUE,
            fill_opacity=0.8,
            stroke_color=BLUE,
            stroke_width=2,
        )
        # 只让右侧圆角，左侧保持直角（通过调整）
        pos = (LEFT * widget_thickness * 0.5) + RIGHT * calculate_widget_reveal_size(
            0.0
        )
        component.move_to(screen.get_left() + pos + UP * 0)

        self.play(FadeIn(component))

        # 3. 放大镜头聚焦到组件

        # 缩放和移动摄像机
        self.play(
            self.camera.frame.animate.scale(0.6).move_to(
                screen.get_left() + RIGHT * 1.0
            )
        )

        font_size = 14
        base_info_text = VGroup(
            Text(
                font="TX-02",
                text=f"widget_thickness: {widget_thickness}",
                font_size=font_size,
            ),
            Text(
                font="TX-02",
                text=f"widget_length: {widget_length}",
                font_size=font_size,
            ),
            Text(
                font="TX-02", text=f"preview_size: {preview_size}", font_size=font_size
            ),
            Text(font="TX-02", text=f"offset_size: {offset_size}", font_size=font_size),
            Text(
                font="TX-02",
                text=f"extra_trigger_area: {extra_trigger_area}",
                font_size=font_size,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        base_info_text.move_to(LEFT * 5 + DOWN * 1)

        # 创建变量显示
        variables = get_vars(0.0)
        variables.move_to(RIGHT * 0.3)

        self.play(FadeIn(base_info_text), FadeIn(variables))
        self.wait(1.0)

        # 4. 添加 x 和 y 的箭头指示
        # x 箭头（水平）
        x_arrow = Arrow(
            start=component.get_corner(UL) + LEFT * 0.5,
            end=component.get_corner(UL),
            buff=0,
            color=WHITE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )
        x_label = Text("x", font_size=24).next_to(x_arrow, LEFT, buff=0.1)

        # y 箭头（垂直）
        y_arrow = Arrow(
            start=component.get_corner(UL) + UP * 0.5,
            end=component.get_corner(UL),
            buff=0,
            color=WHITE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )
        y_label = Text("y", font_size=24).next_to(y_arrow, UP, buff=0.1)

        self.play(
            GrowArrow(x_arrow), Write(x_label), GrowArrow(y_arrow), Write(y_label)
        )
        self.wait(0.5)

        # 5. 添加各个区域框
        # a. Offset 区域（蓝色半透明，在组件左侧）
        offset = Rectangle(
            width=offset_size,
            height=widget_length,
            fill_color=BLUE,
            fill_opacity=0.3,
            stroke_color=BLUE,
            stroke_width=2,
        )
        offset.next_to(component, LEFT, buff=0)
        offset_label = Text("Offset", font_size=18, color=BLUE).next_to(
            offset, DOWN, buff=0.2
        )

        # b. Padding 区域（橙色半透明，在组件右侧）
        padding = Rectangle(
            width=extra_trigger_area,
            height=widget_length,
            fill_color=GREEN,
            fill_opacity=0.3,
            stroke_color=GREEN,
            stroke_width=2,
        )
        padding.next_to(component, RIGHT, buff=0)
        padding_label = Text("Padding", font_size=18, color=GREEN).next_to(
            padding, DOWN, buff=0.2
        )

        self.play(
            FadeIn(offset), Write(offset_label), FadeIn(padding), Write(padding_label)
        )
        self.wait(0.5)

        # c. Total Content 区域（黄色半透明，覆盖所有）
        total_content = Rectangle(
            width=offset_size + widget_thickness + extra_trigger_area,
            height=widget_length,
            fill_color=YELLOW,
            fill_opacity=0.2,
            stroke_color=YELLOW,
            stroke_width=3,
        )
        total_content.move_to(offset.get_left() + RIGHT * (total_content.width / 2))
        total_content_label = Text("Total Content", font_size=20, color=YELLOW).next_to(
            total_content, UP, buff=0.2
        )

        self.play(FadeIn(total_content), Write(total_content_label))
        self.wait(0.5)

        # d. Surface 区域（红色半透明，在屏幕框内侧）
        surface = Rectangle(
            width=calculate_surface_size(0),
            height=1,
            fill_color=RED,
            fill_opacity=0.3,
            stroke_color=RED,
            stroke_width=2,
        )
        surface.align_to(screen, LEFT)
        surface_label = Text("Surface", font_size=20, color=RED).next_to(
            surface, UP * 2.5, buff=0.2
        )

        self.play(FadeIn(surface), Write(surface_label))
        self.wait(1)

        # 6. 动画移动部分
        # 创建 ValueTracker 来追踪移动进度
        tracker = ValueTracker(0)

        # 计算移动距离
        move_distance = (offset_size + widget_thickness) * (1 - preview_size)
        # start_x = total_content.get_left()[0]
        # end_x = screen.get_right()[0] - total_content.width / 2
        # move_distance = end_x - start_x

        # 创建更新函数
        def update_surface(mob):
            progress = tracker.get_value()

            new_surface = Rectangle(
                width=calculate_surface_size(progress),
                height=1,
                fill_color=RED,
                fill_opacity=0.3,
                stroke_color=RED,
                stroke_width=2,
            )
            new_surface.align_to(screen, LEFT)
            mob.become(new_surface)

        # 更新变量值
        def update_variables(mob):
            progress = tracker.get_value()
            new_vars = get_vars(progress)
            new_vars.move_to(mob.get_center())
            mob.become(new_vars)

            up_arrow_x.next_to(texts[0].get_right())
            up_arrow_width.next_to(texts[2].get_right())

        surface.add_updater(update_surface)
        variables.add_updater(update_variables)

        up_arrow_x = Arrow(
            start=DOWN * 0.2,
            end=DOWN * 0,
            buff=0,
            color=WHITE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25,
        )
        up_arrow_width = up_arrow_x.copy()
        up_arrow_x.next_to(texts[0].get_right())
        up_arrow_width.next_to(texts[2].get_right())

        self.play(
            GrowArrow(up_arrow_x),
            GrowArrow(up_arrow_width),
        )

        # 执行移动动画
        self.play(
            tracker.animate.set_value(1),
            total_content.animate.shift(RIGHT * move_distance),
            component.animate.shift(RIGHT * move_distance),
            offset.animate.shift(RIGHT * move_distance),
            padding.animate.shift(RIGHT * move_distance),
            total_content_label.animate.shift(RIGHT * move_distance),
            offset_label.animate.shift(RIGHT * move_distance),
            padding_label.animate.shift(RIGHT * move_distance),
            x_arrow.animate.shift(RIGHT * move_distance),
            x_label.animate.shift(RIGHT * move_distance),
            y_arrow.animate.shift(RIGHT * move_distance),
            y_label.animate.shift(RIGHT * move_distance),
            surface_label.animate.shift(RIGHT * (total_content.width / 2 - 0.05)),
            run_time=4,
            rate_func=smooth,
        )

        surface.remove_updater(update_surface)
        variables.remove_updater(update_variables)

        self.wait(2)
