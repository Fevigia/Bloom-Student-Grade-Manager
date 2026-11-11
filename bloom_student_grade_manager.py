import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

# Cute Student Grade Management System
# Uses only Python's built-in libraries (Tkinter + CSV).

BG = "#FFF7FB"
CARD = "#FFFFFF"
PINK = "#F4A7C2"
DARK_PINK = "#C64F7B"
LAVENDER = "#EEE8FF"
TEXT = "#40364A"
MUTED = "#887B91"
GREEN = "#DDF6E8"


def letter_grade(average):
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


class GradeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloom ✿ Student Grade Manager")
        self.root.geometry("1000x760")
        self.root.minsize(850, 680)
        self.root.configure(bg=BG)
        self.records = []

        self.name_var = tk.StringVar()
        self.id_var = tk.StringVar()
        self.mark_vars = {
            "Mathematics": tk.StringVar(),
            "English": tk.StringVar(),
            "Programming": tk.StringVar(),
            "Database": tk.StringVar(),
        }

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground=TEXT,
            rowheight=30,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=LAVENDER,
            foreground=TEXT,
            font=("Segoe UI", 10, "bold"),
            padding=8,
            relief="flat",
        )
        style.map("Treeview", background=[("selected", "#F9D8E5")])
        style.configure("Vertical.TScrollbar", background=LAVENDER, troughcolor=BG)

    def label(self, parent, text, size=10, color=TEXT, bold=False):
        return tk.Label(
            parent,
            text=text,
            bg=parent.cget("bg"),
            fg=color,
            font=("Segoe UI", size, "bold" if bold else "normal"),
        )

    def rounded_button(self, parent, text, command, bg=PINK, fg=TEXT):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=DARK_PINK,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=9,
        )

    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=28, pady=(22, 12))
        tk.Label(
            header, text="✿", bg=BG, fg=DARK_PINK,
            font=("Segoe UI", 30, "bold")
        ).pack(side="left", padx=(0, 12))
        title_area = tk.Frame(header, bg=BG)
        title_area.pack(side="left")
        tk.Label(
            title_area, text="Bloom Student Grade Manager",
            bg=BG, fg=TEXT, font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")
        tk.Label(
            title_area, text="A simple little place to manage student marks ♡",
            bg=BG, fg=MUTED, font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(2, 0))

        # Main input card
        card = tk.Frame(self.root, bg=CARD, highlightbackground="#F1D8E5", highlightthickness=1)
        card.pack(fill="x", padx=28, pady=8)
        tk.Label(
            card, text="  ✧  Add a student", bg=CARD, fg=DARK_PINK,
            font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=18, pady=(16, 12))

        self.label(card, "Student name", color=MUTED, bold=True).grid(
            row=1, column=0, sticky="w", padx=20, pady=(0, 5)
        )
        self.label(card, "Student ID", color=MUTED, bold=True).grid(
            row=1, column=1, sticky="w", padx=12, pady=(0, 5)
        )

        self.name_entry = ttk.Entry(card, textvariable=self.name_var, font=("Segoe UI", 11))
        self.name_entry.grid(row=2, column=0, sticky="ew", padx=(20, 12), ipady=7)
        self.id_entry = ttk.Entry(card, textvariable=self.id_var, font=("Segoe UI", 11))
        self.id_entry.grid(row=2, column=1, sticky="ew", padx=12, ipady=7)

        card.grid_columnconfigure(0, weight=2)
        card.grid_columnconfigure(1, weight=1)
        card.grid_columnconfigure(2, weight=1)
        card.grid_columnconfigure(3, weight=1)

        self.label(card, "Marks (enter a number from 0 to 100)", color=MUTED, bold=True).grid(
            row=3, column=0, columnspan=4, sticky="w", padx=20, pady=(18, 8)
        )
        mark_colors = ["#FFF0F5", "#F3EEFF", "#EAF8F2", "#FFF6E8"]
        for i, (subject, var) in enumerate(self.mark_vars.items()):
            col = i
            mark_box = tk.Frame(card, bg=mark_colors[i], padx=10, pady=8)
            mark_box.grid(row=4, column=col, sticky="ew", padx=(20 if col == 0 else 7, 7 if col < 3 else 20), pady=(0, 16))
            tk.Label(
                mark_box, text=subject, bg=mark_colors[i], fg=TEXT,
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w")
            entry = ttk.Entry(mark_box, textvariable=var, font=("Segoe UI", 11), width=12)
            entry.pack(fill="x", pady=(5, 0), ipady=4)

        actions = tk.Frame(card, bg=CARD)
        actions.grid(row=5, column=0, columnspan=4, sticky="w", padx=20, pady=(0, 18))
        self.rounded_button(actions, "♡  Calculate & Add", self.add_student, bg=PINK).pack(side="left")
        self.rounded_button(actions, "Clear fields", self.clear_fields, bg=LAVENDER).pack(side="left", padx=9)

        # Result summary
        summary = tk.Frame(self.root, bg=BG)
        summary.pack(fill="x", padx=28, pady=(12, 4))
        self.result_title = tk.Label(
            summary, text="Your latest result will appear here ✨",
            bg=BG, fg=DARK_PINK, font=("Segoe UI", 12, "bold")
        )
        self.result_title.pack(anchor="w")
        self.result_detail = tk.Label(
            summary, text="Add a student's details and marks to get started.",
            bg=BG, fg=MUTED, font=("Segoe UI", 10)
        )
        self.result_detail.pack(anchor="w", pady=(3, 0))

        # Table section
        table_card = tk.Frame(self.root, bg=CARD, highlightbackground="#F1D8E5", highlightthickness=1)
        table_card.pack(fill="both", expand=True, padx=28, pady=(10, 8))
        table_top = tk.Frame(table_card, bg=CARD)
        table_top.pack(fill="x", padx=16, pady=(13, 8))
        tk.Label(
            table_top, text="♡  Student results", bg=CARD, fg=TEXT,
            font=("Segoe UI", 13, "bold")
        ).pack(side="left")
        self.count_label = tk.Label(
            table_top, text="0 students", bg=CARD, fg=MUTED,
            font=("Segoe UI", 9)
        )
        self.count_label.pack(side="right")

        columns = ("id", "name", "average", "grade", "status")
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=8)
        headings = {
            "id": "Student ID",
            "name": "Student name",
            "average": "Average / 100",
            "grade": "Letter grade",
            "status": "Result",
        }
        widths = {"id": 120, "name": 260, "average": 140, "grade": 120, "status": 140}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center" if col != "name" else "w")
        self.tree.tag_configure("even", background="#FFF9FC")
        self.tree.tag_configure("odd", background="#FFFFFF")
        self.tree.pack(fill="both", expand=True, padx=14, pady=(0, 12))

        bottom = tk.Frame(self.root, bg=BG)
        bottom.pack(fill="x", padx=28, pady=(0, 18))
        self.rounded_button(bottom, "Export to CSV", self.export_csv, bg=LAVENDER).pack(side="left")
        self.rounded_button(bottom, "Remove selected", self.remove_selected, bg="#FFE3E9").pack(side="left", padx=9)
        tk.Label(
            bottom, text="Made for learning • Python + Tkinter",
            bg=BG, fg=MUTED, font=("Segoe UI", 9)
        ).pack(side="right")

    def add_student(self):
        name = self.name_var.get().strip()
        student_id = self.id_var.get().strip()

        if not name:
            messagebox.showerror("Missing information", "Please enter the student's name.")
            self.name_entry.focus_set()
            return
        if not student_id:
            messagebox.showerror("Missing information", "Please enter the student ID.")
            self.id_entry.focus_set()
            return
        if any(r["id"].casefold() == student_id.casefold() for r in self.records):
            messagebox.showerror("Duplicate ID", "That student ID is already in the results table.")
            return

        marks = {}
        for subject, var in self.mark_vars.items():
            raw = var.get().strip()
            if not raw:
                messagebox.showerror("Missing mark", f"Please enter a mark for {subject}.")
                return
            try:
                mark = float(raw)
            except ValueError:
                messagebox.showerror("Invalid mark", f"The mark for {subject} must be a number.")
                return
            if not 0 <= mark <= 100:
                messagebox.showerror("Mark out of range", f"{subject} must be between 0 and 100.")
                return
            marks[subject] = mark

        average = sum(marks.values()) / len(marks)
        grade = letter_grade(average)
        status = "Pass ✓" if average >= 50 else "Needs support"

        record = {
            "id": student_id,
            "name": name,
            "marks": marks,
            "average": round(average, 2),
            "grade": grade,
            "status": status,
        }
        self.records.append(record)
        row_num = len(self.records)
        self.tree.insert(
            "", "end",
            values=(student_id, name, f"{average:.2f}", grade, status),
            tags=("even" if row_num % 2 == 0 else "odd",)
        )
        self.count_label.config(text=f"{len(self.records)} student{'s' if len(self.records) != 1 else ''}")
        self.result_title.config(text=f"✧  {name}'s average is {average:.2f}/100 — Grade {grade}")
        self.result_detail.config(
            text=f"Math: {marks['Mathematics']:g}   •   English: {marks['English']:g}   •   "
                 f"Programming: {marks['Programming']:g}   •   Database: {marks['Database']:g}   •   {status}"
        )
        self.clear_fields(keep_result=True)

    def clear_fields(self, keep_result=False):
        self.name_var.set("")
        self.id_var.set("")
        for var in self.mark_vars.values():
            var.set("")
        self.name_entry.focus_set()
        if not keep_result:
            self.result_title.config(text="Your latest result will appear here ✨")
            self.result_detail.config(text="Add a student's details and marks to get started.")

    def remove_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Nothing selected", "Select a student row first.")
            return
        selected_ids = {self.tree.item(item, "values")[0] for item in selected}
        self.records = [r for r in self.records if r["id"] not in selected_ids]
        for item in selected:
            self.tree.delete(item)
        # Rebuild rows so the alternating background remains tidy.
        rows = list(self.tree.get_children())
        for index, item in enumerate(rows):
            self.tree.item(item, tags=("even" if index % 2 else "odd",))
        self.count_label.config(text=f"{len(self.records)} student{'s' if len(self.records) != 1 else ''}")
        self.result_title.config(text="Selected student record(s) removed.")
        self.result_detail.config(text="Your remaining results are still in the table.")

    def export_csv(self):
        if not self.records:
            messagebox.showinfo("No records", "Add at least one student before exporting.")
            return
        path = filedialog.asksaveasfilename(
            title="Save student results",
            defaultextension=".csv",
            filetypes=[("CSV file", "*.csv")],
            initialfile="student_results.csv",
        )
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Student ID", "Student Name", "Mathematics", "English",
                    "Programming", "Database", "Average", "Letter Grade", "Result"
                ])
                for r in self.records:
                    writer.writerow([
                        r["id"], r["name"],
                        r["marks"]["Mathematics"], r["marks"]["English"],
                        r["marks"]["Programming"], r["marks"]["Database"],
                        r["average"], r["grade"], r["status"]
                    ])
            messagebox.showinfo("Export complete", f"Results saved successfully to:\n{path}")
        except OSError as exc:
            messagebox.showerror("Could not save file", f"An error occurred:\n{exc}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GradeApp(root)
    root.mainloop()
