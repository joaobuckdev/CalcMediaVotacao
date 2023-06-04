import tkinter as tk
from tkinter import ttk
import pyperclip
from decimal import Decimal, ROUND_HALF_UP

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Média de Avaliação")
        self.root.geometry("400x550")

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#2c3e50")
        self.style.configure("TLabel", background="#2c3e50", foreground="#f1f1f1", font=("Arial", 12))
        self.style.configure(
            "TButton",
            background="#f1f1f1",
            foreground="#000000",
            font=("Arial", 12, "bold"),
            width=10,
            pady=5,
            borderwidth=0,
            relief=tk.RAISED,
        )
        self.style.map("TButton", background=[("active", "#e0e0e0")])

        self.labels = []
        self.entries = []

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        frame.config(style="TFrame")

        for i in range(1, 6):
            label = ttk.Label(frame, text=f"Avaliações de {i} estrelas:")
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            entry = ttk.Entry(frame, width=10, validate="key")
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")

            # Adiciona validação para permitir somente números, delete e backspace
            entry['validatecommand'] = (entry.register(self.validate_entry), '%P')

            self.labels.append(label)
            self.entries.append(entry)

        calculate_button = ttk.Button(
            frame, text="Calcular Média", command=self.calculate_average
        )
        calculate_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="we")

        reset_button = ttk.Button(
            frame, text="Resetar", command=self.reset_calculator
        )
        reset_button.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        copy_result_button = ttk.Button(
            frame, text="Copiar Resultado", command=self.copy_result
        )
        copy_result_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        copy_calculation_button = ttk.Button(
            frame, text="Copiar Cálculo", command=self.copy_calculation
        )
        copy_calculation_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.result_label = ttk.Label(
            frame, text="", font=("Arial", 14, "bold"), foreground="#f1f1f1", wraplength=350
        )
        self.result_label.grid(row=10, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.calculation_label = ttk.Label(
            frame, text="", foreground="#f1f1f1", wraplength=350
        )
        self.calculation_label.grid(row=11, column=0, columnspan=2, padx=10, pady=10, sticky="we")

        credits_label = ttk.Label(
            frame, text="Developed by João Guilherme\nVer. 1.0.1", foreground="#f1f1f1"
        )
        credits_label.grid(row=12, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    def calculate_average(self):
        ratings = []
        weights = [1, 2, 3, 4, 5]  # Pesos corretos

        for entry in self.entries:
            rating = entry.get()
            if rating.isdigit():
                ratings.append(int(rating))
            else:
                ratings.append(0)

        total_ratings = sum(ratings)
        if total_ratings > 0:
            sum_products = sum([(rating * weight) for rating, weight in zip(ratings, weights)])
            average = Decimal(sum_products) / Decimal(total_ratings)
            average = average.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
            calculation = " + ".join([f"({rating}*{weight})" for rating, weight in zip(ratings, weights)])

            if average % 1 == 0:
                average = int(average)

            self.result_label.config(text=f"Média: {average} estrelas.")
            self.calculation_label.config(text=f"Cálculo: ({calculation}) / {total_ratings}")
        else:
            self.result_label.config(text="Nenhuma avaliação válida inserida.")
            self.calculation_label.config(text="")

    def reset_calculator(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

        self.result_label.config(text="")
        self.calculation_label.config(text="")

    def validate_entry(self, value):
        # Verifica se o valor digitado é um número válido ou uma tecla de controle
        valid_keys = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '', '\b', '\x7f'}
        return all(char in valid_keys for char in value)

    def copy_result(self):
        result = self.result_label.cget("text")
        pyperclip.copy(result)

    def copy_calculation(self):
        calculation = self.calculation_label.cget("text")
        pyperclip.copy(calculation)


root = tk.Tk()

calculator = Calculator(root)

root.mainloop()