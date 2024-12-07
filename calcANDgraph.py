import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Главное меню")
        self.geometry("400x300")
        self.init_ui()

    def init_ui(self):
        # Первая кнопка - Калькулятор
        calc_button = ttk.Button(self, text="Калькулятор", command=self.open_calculator)
        calc_button.pack(pady=20)

        # Вторая кнопка - Нарисовать график
        graph_button = ttk.Button(self, text="Нарисовать график", command=self.open_graph_menu)
        graph_button.pack(pady=20)

    def open_calculator(self):
        Calculator(self)

    def open_graph_menu(self):
        GraphMenu(self)


class Calculator(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Калькулятор")
        self.geometry("300x400")
        self.result = tk.StringVar(value="0")
        self.init_ui()

    def init_ui(self):
        # Поле для отображения результата
        result_label = ttk.Entry(self, textvariable=self.result, font=("Arial", 18), justify="right")
        result_label.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Кнопки
        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "C", "0", "=", "+"
        ]
        for i, btn in enumerate(buttons):
            action = lambda x=btn: self.on_button_click(x)
            ttk.Button(self, text=btn, command=action).grid(row=1 + i // 4, column=i % 4, sticky="nsew")

        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == "C":
            self.result.set("0")
        elif char == "=":
            try:
                self.result.set(eval(self.result.get()))
            except Exception:
                self.result.set("Ошибка")
        else:
            if self.result.get() == "0":
                self.result.set(char)
            else:
                self.result.set(self.result.get() + char)


class GraphMenu(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Меню выбора функции")
        self.geometry("300x200")
        self.init_ui()

    def init_ui(self):
        self.functions = {
            "x^2": lambda x, k: k * x ** 2,
            "x^3": lambda x, k: k * x ** 3,
            "sin(x)": lambda x, k: k * math.sin(x),
            "cos(x)": lambda x, k: k * math.cos(x),
            "kx": lambda x, k: k * x
        }
        self.function_var = tk.StringVar(value="x^2")

        ttk.Label(self, text="Выберите функцию:").pack(pady=10)
        ttk.Combobox(self, values=list(self.functions.keys()), textvariable=self.function_var).pack()

        ttk.Button(self, text="Далее", command=self.open_graph_window).pack(pady=20)

    def open_graph_window(self):
        selected_func = self.functions[self.function_var.get()]
        GraphWindow(self, selected_func)


class GraphWindow(tk.Toplevel):
    def __init__(self, parent, func):
        super().__init__(parent)
        self.title("Построение графика")
        self.geometry("600x400")
        self.func = func
        self.k = tk.DoubleVar(value=1)
        self.init_ui()

    def init_ui(self):
        ttk.Label(self, text="Коэффициент k:").pack()
        ttk.Scale(self, from_=-10, to=10, variable=self.k, orient="horizontal", command=self.update_graph).pack(fill="x")

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.update_graph()

    def update_graph(self, event=None):
        x = [i / 10 for i in range(-100, 101)]
        y = [self.func(i, self.k.get()) for i in x]


        self.ax.clear()
        self.ax.plot(x, y, label=f"y = {self.func}")
        self.ax.legend()
        self.ax.grid()
        self.canvas.draw()


if __name__ == "__main__":
    app = App()
    app.mainloop()
