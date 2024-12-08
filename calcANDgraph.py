import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging


class App(tk.Tk):
    def __init__(self):
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w", encoding = "UTF-8")
        super().__init__()
        self.title("Главное меню")
        logging.info('Было запущено приложение')
        self.geometry("400x300")

        # Добавляем обработчик закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.init_ui()

    def init_ui(self):
        # Первая кнопка - Калькулятор
        calc_button = tk.Button(self, text="Калькулятор", command=self.open_calculator, height=5, width=30, font=("Arial", 10), background='#91959e', activebackground="#82898f")
        calc_button.pack(pady=20)

        # Вторая кнопка - Нарисовать график     
        graph_button = tk.Button(self, text="Нарисовать график", command=self.open_graph_menu, height=5, width=30, font=("Arial", 10), background='#91959e', activebackground="#82898f")
        graph_button.pack(pady=20)


    def on_close(self):
        logging.info('Закрыто главное окно')
        self.destroy()  # Закрывает окно

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


         # Добавляем обработчик закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        

        self.init_ui()
        logging.info('Был открыт калькулятор')
        
    
    def on_close(self):
        logging.info('Закрыт калькулятор')
        self.destroy()

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
                logging.info(f'Example: {self.result.get()}')
                self.result.set(eval(self.result.get()))
                logging.info(f'Result: {self.result.get()}')
            except ZeroDivisionError:
                self.result.set("Ошибка")
                logging.error(f'Ошибка деления на ноль')
            except Exception:
                self.result.set("Ошибка")
                logging.error(f'{self.result.get()}')
                
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

         # Добавляем обработчик закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.init_ui()
        logging.info('Было открыто Меню выбора функции')


    def on_close(self):
        logging.info('Закрыто Меню выбора функции')
        self.destroy()

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
        selected_func_name = self.function_var.get()  # Получаем название функции
        GraphWindow(self, selected_func, selected_func_name)


class GraphWindow(tk.Toplevel):
    def __init__(self, parent, func, func_name):
        super().__init__(parent)
        self.title("Построение графика")
        logging.info('Было открыто построение графика')
        self.geometry("600x400")
        self.func = func
        self.func_name = func_name  # Сохраняем название функции
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
        self.ax.plot(x, y, label=f"{self.func_name}, k={self.k.get():.2f}")  # Используем название функции
        self.ax.legend()
        self.ax.grid()
        self.canvas.draw()
        logging.info(f'Был нарисован график - {self.func_name} с коэффицентом - {self.k.get()}')


if __name__ == "__main__":
    app = App()
    app.mainloop()
