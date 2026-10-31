import tkinter as tk
import dairy_page
import fresh_produce_page
import bakery_page
import meat_seafood_page
import frozen_foods_page
import pantry_staples_page
import beverages_page
import household_page

# ✅ SUMMARY IMPORT
from company_summary import open_company_summary


def open_dashboard(username):
    root = tk.Toplevel()
    root.title("Dashboard - Food Expiry Management System")
    root.state("zoomed")
    root.update_idletasks()

    # ---------- BACKGROUND ----------
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    canvas.create_rectangle(
        0, 0,
        root.winfo_screenwidth(),
        root.winfo_screenheight(),
        fill="#020617",
        outline=""
    )

    canvas.create_rectangle(
        0,
        root.winfo_screenheight() // 2,
        root.winfo_screenwidth(),
        root.winfo_screenheight(),
        fill="#0f172a",
        outline=""
    )

    # ---------- MAIN CONTENT FRAME (CENTER LOCK) ----------
    main_frame = tk.Frame(root, bg="#020617", padx=30, pady=25)
    main_frame.place(relx=0.5, rely=0.52, anchor="center")

    # ---------- HEADER ----------
    tk.Label(
        main_frame,
        text=f"Welcome, {username}",
        font=("Segoe UI", 20, "bold"),
        bg="#020617",
        fg="white"
    ).pack(pady=(0, 5))

    tk.Label(
        main_frame,
        text="Select a product category",
        font=("Segoe UI", 11),
        bg="#020617",
        fg="#94a3b8"
    ).pack(pady=(0, 15))

    # ✅ OPTIONAL SUMMARY BUTTON (SAFE & CENTERED)
    tk.Button(
        main_frame,
        text="📊 Company Summary",
        font=("Segoe UI", 11, "bold"),
        bg="#020617",
        fg="#38bdf8",
        bd=0,
        activebackground="#020617",
        activeforeground="#38bdf8",
        command=open_company_summary
    ).pack(pady=(0, 25))

    # ---------- CARD CONTAINER ----------
    card_frame = tk.Frame(main_frame, bg="#020617")
    card_frame.pack()

    categories = [
        ("Fresh Produce", "#22c55e"),
        ("Dairy", "#38bdf8"),
        ("Meat / Seafood", "#ef4444"),
        ("Bakery", "#f59e0b"),
        ("Pantry Staples", "#a855f7"),
        ("Frozen Foods", "#06b6d4"),
        ("Beverages", "#0ea5e9"),
        ("Household / Personal Care", "#10b981")
    ]

    def open_category(name):

        if name == "Dairy":
            dairy_page.open_dairy_page()

        elif name == "Fresh Produce":
            fresh_produce_page.open_fresh_produce_page()

        elif name == "Bakery":
            bakery_page.open_bakery_page()

        elif name == "Meat / Seafood":
            meat_seafood_page.open_meat_seafood_page()

        elif name == "Frozen Foods":
            frozen_foods_page.open_frozen_foods_page()

        elif name == "Pantry Staples":
            pantry_staples_page.open_pantry_staples_page()

        elif name == "Beverages":
            beverages_page.open_beverages_page()

        elif name == "Household / Personal Care":
            household_page.open_household_page()

        else:
            win = tk.Toplevel(root)
            win.title(name)
            win.geometry("500x300")
            win.configure(bg="#020617")

            tk.Label(
                win,
                text=name,
                font=("Segoe UI", 16, "bold"),
                bg="#020617",
                fg="white"
            ).pack(pady=20)

            tk.Label(
                win,
                text="Category page coming soon",
                font=("Segoe UI", 11),
                bg="#020617",
                fg="#94a3b8"
            ).pack()

    # ---------- BUTTONS AS INDIVIDUAL RECTANGLE CARDS ----------
    row = col = 0
    for cat, border_color in categories:

        card = tk.Frame(
            card_frame,
            bg="#020617",
            highlightthickness=2,
            highlightbackground=border_color,
            padx=6,
            pady=6
        )
        card.grid(row=row, column=col, padx=18, pady=18)

        btn = tk.Button(
            card,
            text=cat,
            font=("Segoe UI", 11, "bold"),
            width=24,
            height=3,
            bg="#020617",
            fg="white",
            activebackground="#020617",
            activeforeground="white",
            bd=0,
            relief="flat",
            command=lambda c=cat: open_category(c)
        )
        btn.pack()

        col += 1
        if col == 2:
            col = 0
            row += 1