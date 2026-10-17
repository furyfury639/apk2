from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.config import Config

# ضبط أبعاد النافذة (تحاكي شاشة هاتف)
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

Window.clearcolor = (0.1, 0.1, 0.15, 1)


class Calculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        # شاشة العرض
        self.display = Label(
            text='0',
            font_size=48,
            halign='right',
            valign='middle',
            size_hint=(1, 0.25),
            color=(1, 1, 1, 1)
        )
        self.display.bind(size=self.display.setter('text_size'))
        self.add_widget(self.display)

        self.current = ''
        self.operation = None
        self.previous = None

        # شبكة الأزرار
        buttons = [
            ['C', '⌫', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]

        grid = GridLayout(cols=4, spacing=8, size_hint=(1, 0.75))

        for row in buttons:
            for label in row:
                btn = Button(
                    text=label,
                    font_size=28,
                    background_normal='',
                    background_color=self.get_color(label),
                    color=(1, 1, 1, 1)
                )
                btn.bind(on_press=self.on_button_press)
                grid.add_widget(btn)

        self.add_widget(grid)

    def get_color(self, label):
        """تلوين الأزرار حسب نوعها"""
        if label in ['÷', '×', '-', '+', '=']:
            return (1.0, 0.5, 0.0, 1)   # برتقالي للعمليات
        elif label in ['C', '⌫', '%', '±']:
            return (0.4, 0.4, 0.45, 1)  # رمادي للأزرار الخاصة
        return (0.2, 0.2, 0.25, 1)      # رمادي غامق للأرقام

    def on_button_press(self, instance):
        text = instance.text

        if text == 'C':
            self.current = ''
            self.previous = None
            self.operation = None
            self.display.text = '0'

        elif text == '⌫':
            self.current = self.current[:-1]
            self.display.text = self.current if self.current else '0'

        elif text == '±':
            if self.current:
                self.current = str(-float(self.current))
                self.display.text = self.current

        elif text in ['+', '-', '×', '÷', '%']:
            if self.current:
                self.previous = float(self.current)
                self.operation = text
                self.current = ''
                self.display.text = f'{self.previous} {text}'

        elif text == '=':
            self.calculate()

        else:  # أرقام ونقطة
            if text == '.' and '.' in self.current:
                return
            self.current += text
            self.display.text = self.current

    def calculate(self):
        if self.previous is None or not self.current:
            return
        try:
            b = float(self.current)
            a = self.previous
            op = self.operation

            if op == '+':
                result = a + b
            elif op == '-':
                result = a - b
            elif op == '×':
                result = a * b
            elif op == '÷':
                if b == 0:
                    self.display.text = 'خطأ'
                    self.current = ''
                    return
                result = a / b
            elif op == '%':
                result = a * b / 100

            # تنسيق النتيجة
            if result == int(result):
                result = int(result)
            self.display.text = str(result)
            self.current = str(result)
            self.previous = None
            self.operation = None

        except Exception:
            self.display.text = 'خطأ'
            self.current = ''


class CalculatorApp(App):
    def build(self):
        self.title = 'آلة حاسبة'
        return Calculator()


if __name__ == '__main__':
    CalculatorApp().run()
    
