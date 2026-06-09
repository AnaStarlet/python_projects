import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
from datetime import datetime
import dashscope
from dashscope import Generation


class FinancialAdvisorBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Советчик по финансам - Qwen AI Ассистент")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ffe4ec")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#ffe4ec')
        self.style.configure('TLabel', background='#ffe4ec', foreground='#b3406c', font=('Arial', 11, 'bold'))
        self.style.configure('TLabelframe', background='#ffe4ec', foreground='#b3406c', font=('Arial', 12, 'bold'))
        self.style.configure('TLabelframe.Label', background='#ffe4ec', foreground='#b3406c',
                             font=('Arial', 12, 'bold'))
        self.style.configure('TButton', font=('Arial', 10, 'bold'), background='#ff99bb', foreground='#b3406c')
        self.style.map('TButton', background=[('active', '#ffc0d0')])
        self.style.configure('TCombobox', fieldbackground='white', foreground='#b3406c')

        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        title_label = ttk.Label(self.main_frame, text="💖 Финансовый AI Советник  💖", font=('Arial', 20, 'bold'),
                                foreground='#ff6699')
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        self.create_input_frame()
        self.create_output_frame()

        dashscope.api_key = "sk-7069a2a215e042f79c5a3702b299dccd"
        dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

        self.output_text.insert(tk.END, "✅ AI модель готова к работе\n\n")

        self.advice_history = []

    def create_input_frame(self):
        input_frame = ttk.LabelFrame(self.main_frame, text="📊 Ваши финансовые показатели", padding="15")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10), pady=10)
        input_frame.grid_rowconfigure(0, weight=0)
        input_frame.grid_rowconfigure(8, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Возраст:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.age_entry = ttk.Entry(input_frame, width=25)
        self.age_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=10)

        ttk.Label(input_frame, text="Ежемесячный доход (руб.):").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.income_entry = ttk.Entry(input_frame, width=25)
        self.income_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=10)

        ttk.Label(input_frame, text="Ежемесячные расходы (руб.):").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.expenses_entry = ttk.Entry(input_frame, width=25)
        self.expenses_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=10)

        ttk.Label(input_frame, text="Накопления (руб.):").grid(row=3, column=0, sticky=tk.W, pady=8)
        self.savings_entry = ttk.Entry(input_frame, width=25)
        self.savings_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=8, padx=10)

        ttk.Label(input_frame, text="Кредитная нагрузка (руб.):").grid(row=4, column=0, sticky=tk.W, pady=8)
        self.debt_entry = ttk.Entry(input_frame, width=25)
        self.debt_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=8, padx=10)

        ttk.Label(input_frame, text="Финансовая цель:").grid(row=5, column=0, sticky=tk.W, pady=8)
        self.goal_combo = ttk.Combobox(input_frame,
                                       values=["Создать резервный фонд", "Накопить на недвижимость", "Инвестировать",
                                               "Погасить долги", "Накопить на пенсию", "Крупная покупка"], width=23)
        self.goal_combo.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=8, padx=10)
        self.goal_combo.set("Создать резервный фонд")

        ttk.Label(input_frame, text="Уровень риска:").grid(row=6, column=0, sticky=tk.W, pady=8)
        self.risk_combo = ttk.Combobox(input_frame, values=["Консервативный", "Умеренный", "Агрессивный"], width=23)
        self.risk_combo.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=8, padx=10)
        self.risk_combo.set("Умеренный")

        ttk.Label(input_frame, text="Семейное положение:").grid(row=7, column=0, sticky=tk.W, pady=8)
        self.family_combo = ttk.Combobox(input_frame, values=["Холост/Не замужем", "В браке", "С детьми", "Разведен/а"],
                                         width=23)
        self.family_combo.grid(row=7, column=1, sticky=(tk.W, tk.E), pady=8, padx=10)
        self.family_combo.set("Холост/Не замужем")

        analyze_btn = ttk.Button(input_frame, text="✨ Получить AI рекомендации (Qwen) ✨",
                                 command=self.get_recommendations)
        analyze_btn.grid(row=8, column=0, columnspan=2, pady=20)

    def create_output_frame(self):
        output_frame = ttk.LabelFrame(self.main_frame, text="💡 Qwen AI Анализ и рекомендации", padding="15")
        output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0), pady=10)
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_rowconfigure(1, weight=0)
        output_frame.grid_columnconfigure(0, weight=1)

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=('Arial', 10), bg='white',
                                                     fg='#b3406c')
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        btn_frame = ttk.Frame(output_frame)
        btn_frame.grid(row=1, column=0, pady=5)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)

        save_btn = ttk.Button(btn_frame, text="💾 Сохранить рекомендации", command=self.save_advice)
        save_btn.grid(row=0, column=0, padx=5, sticky=tk.W)

        clear_btn = ttk.Button(btn_frame, text="🗑 Очистить", command=self.clear_output)
        clear_btn.grid(row=0, column=1, padx=5)

        history_btn = ttk.Button(btn_frame, text="📜 История советов", command=self.show_history)
        history_btn.grid(row=0, column=2, padx=5, sticky=tk.E)

    def get_recommendations(self):
        try:
            age = int(self.age_entry.get()) if self.age_entry.get() else 0
            income = float(self.income_entry.get()) if self.income_entry.get() else 0
            expenses = float(self.expenses_entry.get()) if self.expenses_entry.get() else 0
            savings = float(self.savings_entry.get()) if self.savings_entry.get() else 0
            debt = float(self.debt_entry.get()) if self.debt_entry.get() else 0
            goal = self.goal_combo.get()
            risk = self.risk_combo.get()
            family = self.family_combo.get()

            if age <= 0 or income <= 0:
                messagebox.showwarning("Внимание", "Пожалуйста, заполните обязательные поля (возраст и доход)")
                return

            user_data = {
                "age": age,
                "income": income,
                "expenses": expenses,
                "savings": savings,
                "debt": debt,
                "goal": goal,
                "risk": risk,
                "family": family
            }

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "🤖 Qwen AI анализирует ваши данные...\n\n")
            self.root.update()

            advice = self.get_qwen_advice(user_data)

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, advice)

            self.advice_history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data": user_data,
                "advice": advice
            })

        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения")

    def get_qwen_advice(self, data):
        monthly_surplus = data['income'] - data['expenses']

        prompt = f"""Ты профессиональный финансовый советник. Проанализируй данные клиента и предоставь четкие, строгие рекомендации.

Данные клиента:
Возраст: {data['age']} лет
Ежемесячный доход: {data['income']:,.0f} рублей
Ежемесячные расходы: {data['expenses']:,.0f} рублей
Накопления: {data['savings']:,.0f} рублей
Кредитная нагрузка: {data['debt']:,.0f} рублей
Финансовая цель: {data['goal']}
Уровень риска: {data['risk']}
Семейное положение: {data['family']}
Свободный денежный поток: {monthly_surplus:,.0f} рублей в месяц

Напиши ответ в следующем формате:

ФИНАНСОВЫЙ АНАЛИЗ
(опиши текущую ситуацию)

РЕКОМЕНДАЦИИ
(дай конкретные советы по улучшению)

СТРАТЕГИЯ ДОСТИЖЕНИЯ ЦЕЛИ: {data['goal']}
(опиши пошаговый план)

ДЕЙСТВИЯ НА БЛИЖАЙШИЕ 30 ДНЕЙ
(перечисли конкретные шаги)

Отвечай строго, четко, без звездочек, без маркдауна, используй только обычный текст с дефисами для списков."""

        try:
            response = Generation.call(
                model='qwen-turbo',
                prompt=prompt,
                max_tokens=1500,
                temperature=0.7,
                top_p=0.8
            )

            if response.status_code == 200:
                return response.output.text
            else:
                return self.fallback_advice(data)

        except Exception as e:
            return self.fallback_advice(data)

    def fallback_advice(self, data):
        monthly_surplus = data['income'] - data['expenses']
        savings_ratio = (data['savings'] / (data['income'] * 12)) * 100 if data['income'] > 0 else 0
        debt_to_income = (data['debt'] / (data['income'] * 12)) * 100 if data['income'] > 0 else 0

        recommendations = []

        recommendations.append("ФИНАНСОВЫЙ АНАЛИЗ (резервный режим)")
        recommendations.append("")
        recommendations.append(f"Текущая ситуация:")
        recommendations.append(f"- Ежемесячный свободный поток: {monthly_surplus:,.0f} рублей")
        recommendations.append(f"- Коэффициент накоплений: {savings_ratio:.1f}% от годового дохода")
        recommendations.append(f"- Долговая нагрузка: {debt_to_income:.1f}% от годового дохода")

        if monthly_surplus <= 0:
            recommendations.append("")
            recommendations.append("КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ:")
            recommendations.append("Ваши расходы превышают доходы. Немедленно пересмотрите бюджет.")

        recommendations.append("")
        recommendations.append("РЕКОМЕНДАЦИИ:")

        if data['debt'] > 0 and debt_to_income > 30:
            recommendations.append("1. Приоритет номер один: погашение долгов")
            recommendations.append("   - Используйте метод снежного кома для погашения кредитов")
            recommendations.append("   - Рассмотрите рефинансирование")

        if data['savings'] < data['expenses'] * 3:
            recommendations.append("2. Создание резервного фонда")
            recommendations.append(f"   - Цель: накопить {data['expenses'] * 6:,.0f} рублей")
            recommendations.append("   - Откладывайте 10-20% от дохода автоматически")

        if monthly_surplus > 0:
            recommendations.append("3. Инвестиционная стратегия:")
            if data['risk'] == "Консервативный":
                recommendations.append("   - Рекомендуется: ОФЗ, корпоративные облигации")
                recommendations.append("   - Соотношение: 80% облигации, 20% акции")
            elif data['risk'] == "Умеренный":
                recommendations.append("   - Рекомендуется: сбалансированный портфель ETF")
                recommendations.append("   - Соотношение: 60% акции, 40% облигации")
            else:
                recommendations.append("   - Рекомендуется: агрессивный рост через акции")
                recommendations.append("   - Соотношение: 80% акции, 20% альтернативные инвестиции")

        recommendations.append("")
        recommendations.append(f"СТРАТЕГИЯ ДОСТИЖЕНИЯ ЦЕЛИ: {data['goal']}")

        if data['goal'] == "Создать резервный фонд":
            target = data['expenses'] * 6
            months_needed = target / monthly_surplus if monthly_surplus > 0 else 999
            recommendations.append(f"- Необходимо накопить: {target:,.0f} рублей")
            recommendations.append(f"- При текущем темпе: {months_needed:.1f} месяцев")

        recommendations.append("")
        recommendations.append("ДЕЙСТВИЯ НА БЛИЖАЙШИЕ 30 ДНЕЙ:")
        recommendations.append("1. Проанализировать все расходы за последние 3 месяца")
        recommendations.append("2. Настроить автоматическое отчисление 10% от дохода")
        recommendations.append("3. Составить план погашения долгов")
        recommendations.append("4. Открыть накопительный счет для финансовой цели")

        recommendations.append("")
        recommendations.append("=" * 60)
        recommendations.append("Примечание: рекомендации носят информационный характер.")

        return "\n".join(recommendations)

    def save_advice(self):
        if self.output_text.get(1.0, tk.END).strip():
            filename = f"financial_advice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.output_text.get(1.0, tk.END))
            messagebox.showinfo("Успех", f"Рекомендации сохранены в файл: {filename}")
        else:
            messagebox.showwarning("Внимание", "Нет рекомендаций для сохранения")

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("История финансовых советов")
        history_window.geometry("800x500")
        history_window.configure(bg="#ffe4ec")

        history_window.grid_rowconfigure(0, weight=1)
        history_window.grid_columnconfigure(0, weight=1)

        text_area = scrolledtext.ScrolledText(history_window, wrap=tk.WORD, font=('Arial', 9), bg='white', fg='#b3406c')
        text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

        if not self.advice_history:
            text_area.insert(tk.END, "История пуста")
        else:
            for i, entry in enumerate(self.advice_history, 1):
                text_area.insert(tk.END, f"\n{'=' * 60}\n")
                text_area.insert(tk.END, f"Совет #{i} - {entry['timestamp']}\n")
                text_area.insert(tk.END, f"{'=' * 60}\n")
                text_area.insert(tk.END, entry['advice'])
                text_area.insert(tk.END, "\n\n")


def main():
    root = tk.Tk()
    app = FinancialAdvisorBot(root)
    root.mainloop()


if __name__ == "__main__":
    main()