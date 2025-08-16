# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.lang import Builder
from random import choice

KV = """
<PadButton@Button>:
    size_hint: None, None
    width: dp(64)
    height: dp(64)
    font_size: '18sp'
    background_normal: ''
    background_color: 0.15,0.16,0.2,1
    color: 1,1,1,1
    canvas.before:
        Color:
            rgba: 0.2,0.22,0.28,1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [16,]

<GameRoot>:
    orientation: 'vertical'
    padding: dp(12)
    spacing: dp(12)

    BoxLayout:
        size_hint_y: None
        height: dp(44)
        Label:
            id: score_lbl
            text: root.score_text
            font_size: '18sp'
            bold: True
            color: 1,1,1,1
        Label:
            id: status_lbl
            text: root.status_text
            font_size: '18sp'
            halign: 'right'
            color: 1,1,1,1

    Board:
        id: board
        size_hint_y: 1

    BoxLayout:
        size_hint_y: None
        height: dp(84)
        spacing: dp(8)
        Widget:
        BoxLayout:
            orientation: 'vertical'
            size_hint_x: None
            width: dp(210)
            spacing: dp(8)

            Widget:
                size_hint_y: None
                height: dp(8)

            BoxLayout:
                size_hint_y: None
                height: dp(64)
                spacing: dp(8)
                Widget:
                PadButton:
                    text: "⬆"
                    on_release: root.set_dir(0,1)
                Widget:

            BoxLayout:
                size_hint_y: None
                height: dp(64)
                spacing: dp(8)
                PadButton:
                    text: "⬅"
                    on_release: root.set_dir(-1,0)
                PadButton:
                    text: "⟳"
                    on_release: root.restart()
                PadButton:
                    text: "➡"
                    on_release: root.set_dir(1,0)

            BoxLayout:
                size_hint_y: None
                height: dp(64)
                spacing: dp(8)
                Widget:
                PadButton:
                    text: "⬇"
                    on_release: root.set_dir(0,-1)
                Widget:
        Widget:
"""

Builder.load_string(KV)

CELL = 24
GRID_W = 16
GRID_H = 24
START_LEN = 4
TICK_BASE = 0.12

class Board(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.bind(size=self._redraw_bg, pos=self._redraw_bg)

    def _redraw_bg(self, *_):
        with self.canvas.before:
            self.canvas.before.clear()
            Color(0.07,0.08,0.1,1)
            Rectangle(pos=self.pos, size=self.size)

class GameRoot(BoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.board = None
        Clock.schedule_once(self._post_init)

    def _post_init(self, *_):
        self.board = self.ids.board
        self.score = 0
        self.game_over = False
        self.dir = (1,0)
        midx, midy = GRID_W//2, GRID_H//2
        self.snake = [(midx - i, midy) for i in range(START_LEN)]
        self.food = self._new_food()
        self.speed = TICK_BASE
        self._touch_start = None
        self._draw()
        self.event = Clock.schedule_interval(self._update, self.speed)

    @property
    def score_text(self):
        return f"امتیاز: {self.score}"

    @property
    def status_text(self):
        return "تمام!" if self.game_over else "در حال بازی"

    def _new_food(self):
        free = [(x,y) for x in range(GRID_W) for y in range(GRID_H) if (x,y) not in self.snake]
        return choice(free) if free else (0,0)

    def _update(self, dt):
        if self.game_over:
            return
        dx, dy = self.dir
        headx, heady = self.snake[0]
        nx, ny = headx + dx, heady + dy

        if nx < 0 or nx >= GRID_W or ny < 0 or ny >= GRID_H or (nx,ny) in self.snake:
            self.game_over = True
            self.ids.score_lbl.text = self.score_text
            self.ids.status_lbl.text = self.status_text
            return

        self.snake.insert(0, (nx, ny))
        if (nx, ny) == self.food:
            self.score += 1
            self.food = self._new_food()
            self.speed = max(0.05, self.speed - 0.004)
            self.event.cancel()
            self.event = Clock.schedule_interval(self._update, self.speed)
        else:
            self.snake.pop()

        self._draw()

    def _draw(self):
        if not self.board:
            return
        bx, by = self.board.pos
        with self.board.canvas:
            self.board.canvas.clear()
            Color(0.09,0.1,0.12,1)
            Rectangle(pos=self.board.pos, size=self.board.size)
            fx, fy = self.food
            Color(0.95,0.37,0.37,1)
            Rectangle(pos=(bx + fx*CELL, by + fy*CELL), size=(CELL, CELL))
            for i, (x,y) in enumerate(self.snake):
                Color(0.35+0.2*(i==0), 0.85, 0.55, 1)
                Rectangle(pos=(bx + x*CELL, by + y*CELL), size=(CELL, CELL))

        self.ids.score_lbl.text = self.score_text
        self.ids.status_lbl.text = self.status_text

    def set_dir(self, dx, dy):
        if self.game_over:
            return
        cdx, cdy = self.dir
        if (dx,dy) == (-cdx,-cdy):
            return
        self.dir = (dx,dy)

    def on_touch_down(self, touch):
        self._touch_start = touch.pos
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self._touch_start:
            sx, sy = self._touch_start
            ex, ey = touch.pos
            dx = ex - sx
            dy = ey - sy
            if abs(dx) > 20 or abs(dy) > 20:
                if abs(dx) > abs(dy):
                    self.set_dir(1,0) if dx>0 else self.set_dir(-1,0)
                else:
                    self.set_dir(0,1) if dy>0 else self.set_dir(0,-1)
        self._touch_start = None
        return super().on_touch_up(touch)

    def restart(self):
        if self.event:
            self.event.cancel()
        self.__init__()
        Clock.schedule_once(self._post_init, 0)

class SnakeApp(App):
    title = "Snake - Kivy"
    def build(self):
        Window.clearcolor = (0.07,0.08,0.1,1)
        Window.size = (GRID_W*CELL + 24, GRID_H*CELL + 160)
        return GameRoot()

if __name__ == "__main__":
    SnakeApp().run()
