import tkinter as tk
from datetime import datetime

# =====================================================
# FINAL STAGE CONFIG (LOCKED)
# =====================================================

CATEGORIES = [
    "Fresh Produce",
    "Dairy",
    "Meat / Seafood",
    "Bakery",
    "Pantry Staples",
    "Frozen Food",
    "Beverages",
    "Household / Personal Care",
]

BASE_STOCK_VALUE = {
    "Fresh Produce": 45000,
    "Dairy": 38000,
    "Meat / Seafood": 52000,
    "Bakery": 30000,
    "Pantry Staples": 60000,
    "Frozen Food": 48000,
    "Beverages": 42000,
    "Household / Personal Care": 55000,
}

RISK_PROFILE = {
    "Fresh Produce": {"risk": 0.35, "discount": 0.20},
    "Dairy": {"risk": 0.25, "discount": 0.15},
    "Meat / Seafood": {"risk": 0.40, "discount": 0.25},
    "Bakery": {"risk": 0.30, "discount": 0.20},
    "Pantry Staples": {"risk": 0.05, "discount": 0.02},
    "Frozen Food": {"risk": 0.08, "discount": 0.05},
    "Beverages": {"risk": 0.04, "discount": 0.02},
    "Household / Personal Care": {"risk": 0.01, "discount": 0.00},
}

# =====================================================
# SUMMARY DASHBOARD (FINAL)
# =====================================================

def open_company_summary():
    root = tk.Toplevel()
    root.title("Company Summary – Inventory Intelligence System")
    root.state("zoomed")
    root.configure(bg="#020617")

    # ---------- SCROLL SYSTEM ----------
    canvas = tk.Canvas(root, bg="#020617", highlightthickness=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    holder = tk.Frame(canvas, bg="#020617")
    window = canvas.create_window((0, 0), window=holder, anchor="n")

    WIDTH = 1200

    def center_content(event):
        x = max((event.width - WIDTH) // 2, 0)
        canvas.coords(window, x, 0)
        canvas.itemconfig(window, width=WIDTH)

    canvas.bind("<Configure>", center_content)
    holder.bind("<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind_all("<MouseWheel>",
        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # ---------- HEADER ----------
    tk.Label(
        holder,
        text="Company Summary – Executive Dashboard",
        font=("Segoe UI", 26, "bold"),
        bg="#020617",
        fg="white"
    ).pack(pady=(30, 6))

    tk.Label(
        holder,
        text="Date-based inventory risk, loss and recovery analysis",
        font=("Segoe UI", 11),
        bg="#020617",
        fg="#94a3b8"
    ).pack(pady=(0, 25))

    # ---------- DATE BAR ----------
    date_bar = tk.Frame(holder, bg="#020617")
    date_bar.pack(pady=10)

    tk.Label(date_bar, text="Analysis Date:",
             bg="#020617", fg="#e5e7eb",
             font=("Segoe UI", 11)).pack(side="left", padx=6)

    date_entry = tk.Entry(date_bar, font=("Segoe UI", 11),
                          width=14, justify="center")
    date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
    date_entry.pack(side="left", padx=8)

    content = tk.Frame(holder, bg="#020617")
    content.pack(pady=10)

    # =================================================
    # CORE RENDER (FINAL LOGIC)
    # =================================================
    def render():
        for w in content.winfo_children():
            w.destroy()

        try:
            view_date = datetime.strptime(date_entry.get(), "%Y-%m-%d")
        except:
            tk.Label(content, text="Invalid date format (YYYY-MM-DD)",
                     bg="#020617", fg="#ef4444",
                     font=("Segoe UI", 12, "bold")).pack(pady=20)
            return

        days_offset = max((view_date - datetime.today()).days, 0)

        risk_map = {}
        loss_map = {}

        total_stock = total_discount = total_waste = total_recoverable = 0

        for cat in CATEGORIES:
            base = BASE_STOCK_VALUE[cat]
            profile = RISK_PROFILE[cat]

            risk_factor = min(1, profile["risk"] + days_offset * 0.01)
            risk_amt = int(base * risk_factor)

            discount_loss = int(risk_amt * profile["discount"])
            waste_loss = int(risk_amt * (0.10 if risk_factor > 0.3 else 0.03))
            recoverable = base - discount_loss - waste_loss

            risk_map[cat] = risk_amt
            loss_map[cat] = discount_loss + waste_loss

            total_stock += base
            total_discount += discount_loss
            total_waste += waste_loss
            total_recoverable += recoverable

        # ---------- KPI CARDS ----------
        kpi_frame = tk.Frame(content, bg="#020617")
        kpi_frame.pack(pady=15)

        def kpi(title, value, color):
            f = tk.Frame(kpi_frame, bg="#020617",
                         highlightthickness=2,
                         highlightbackground=color,
                         width=260, height=120)
            f.pack(side="left", padx=18)
            f.pack_propagate(False)
            tk.Label(f, text=title, bg="#020617",
                     fg="#94a3b8", font=("Segoe UI", 11)).pack(pady=(22, 4))
            tk.Label(f, text=value, bg="#020617",
                     fg="white", font=("Segoe UI", 18, "bold")).pack()

        kpi("Total Stock Value", f"₹{total_stock}", "#38bdf8")
        kpi("Discount + Waste Loss", f"₹{total_discount + total_waste}", "#facc15")
        kpi("Waste Loss", f"₹{total_waste}", "#ef4444")
        kpi("Recoverable Value", f"₹{total_recoverable}", "#22c55e")

        # ---------- OVERALL GRAPH ----------
        tk.Label(content, text="Overall Financial Impact",
                 font=("Segoe UI", 20, "bold"),
                 bg="#020617", fg="white").pack(pady=(40, 15))

        g1 = tk.Canvas(content, width=900, height=260,
                       bg="#020617", highlightthickness=0)
        g1.pack()

        bars = [
            ("Recoverable", total_recoverable, "#22c55e"),
            ("Discount Loss", total_discount, "#facc15"),
            ("Waste Loss", total_waste, "#ef4444"),
        ]

        max_val = max(v for _, v, _ in bars)
        scale = 200 / max_val if max_val else 1

        x = 150
        for label, val, color in bars:
            h = val * scale
            g1.create_rectangle(x, 240-h, x+120, 240, fill=color, outline="")
            g1.create_text(x+60, 250, text=label, fill="#e5e7eb")
            g1.create_text(x+60, 230-h, text=f"₹{val}",
                           fill="white", font=("Segoe UI", 10, "bold"))
            x += 200

        # ---------- CATEGORY RISK GRAPH ----------
        tk.Label(content, text="Category-wise Risk Exposure",
                 font=("Segoe UI", 20, "bold"),
                 bg="#020617", fg="white").pack(pady=(40, 15))

        g2 = tk.Canvas(content, width=1000, height=360,
                       bg="#020617", highlightthickness=0)
        g2.pack()

        max_risk = max(risk_map.values())
        scale = 240 / max_risk if max_risk else 1

        x = 60
        for cat in CATEGORIES:
            risk = risk_map[cat]
            h = risk * scale

            ratio = risk / BASE_STOCK_VALUE[cat]
            color = "#22c55e" if ratio <= 0.15 else "#facc15" if ratio <= 0.35 else "#ef4444"

            g2.create_rectangle(x, 300-h, x+90, 300, fill=color, outline="")
            g2.create_text(x+45, 310, text=cat.split()[0],
                           fill="#e5e7eb", font=("Segoe UI", 9))
            g2.create_text(x+45, 290-h, text=f"₹{risk}",
                           fill="white", font=("Segoe UI", 9, "bold"))
            x += 115

        # ---------- GROUPED GRAPH ----------
        tk.Label(content, text="Category-wise Risk vs Actual Loss",
                 font=("Segoe UI", 20, "bold"),
                 bg="#020617", fg="white").pack(pady=(40, 15))

        g3 = tk.Canvas(content, width=1000, height=380,
                       bg="#020617", highlightthickness=0)
        g3.pack()

        max_val = max(max(risk_map.values()), max(loss_map.values()))
        scale = 260 / max_val if max_val else 1

        x = 50
        for cat in CATEGORIES:
            hr = risk_map[cat] * scale
            hl = loss_map[cat] * scale

            g3.create_rectangle(x, 330-hr, x+35, 330, fill="#ef4444", outline="")
            g3.create_rectangle(x+40, 330-hl, x+75, 330, fill="#facc15", outline="")
            g3.create_text(x+37, 345, text=cat.split()[0],
                           fill="#e5e7eb", font=("Segoe UI", 9))
            x += 115

        # ---------- FINAL ADVICE ----------
        tk.Label(content, text="Executive Decision Insight",
                 font=("Segoe UI", 20, "bold"),
                 bg="#020617", fg="white").pack(pady=(40, 15))

        insights = [
            "• Bakery and Meat / Seafood require immediate action due to high risk.",
            "• Early discounting can significantly reduce potential waste.",
            "• Pantry, Frozen and Household categories remain stable.",
            "• Date-based analysis enables proactive inventory decisions.",
        ]

        for line in insights:
            tk.Label(content, text=line,
                     bg="#020617", fg="#94a3b8",
                     font=("Segoe UI", 11),
                     anchor="w").pack(fill="x", padx=120, pady=4)

    tk.Button(
        date_bar,
        text="Apply Date",
        bg="#22c55e",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        bd=0,
        padx=20,
        pady=7,
        command=render
    ).pack(side="left", padx=10)

    render()