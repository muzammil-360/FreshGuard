import tkinter as tk
from datetime import datetime, timedelta
import random

# ================= GLOBAL BASE DATE =================
BASE_VIEW_DATE = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

# ================= PRODUCT GENERATOR =================
def generate_products(category, count=90):
    start = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0) - timedelta(days=30)
    end = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0) + timedelta(days=15)

    config = {
        "Bread & Buns": (3, 40),
        "Cakes & Pastries": (2, 120),
        "Cookies & Rusks": (15, 90),
        "Savory Bakery": (2, 60)
    }

    shelf, base_price = config[category]
    products = []

    for i in range(count):
        mfg = start + timedelta(days=random.randint(0, (end - start).days - shelf))
        exp = mfg + timedelta(days=shelf)

        products.append({
            "name": f"{category} Item {i+1}",
            "category": category,
            "mfg": mfg,
            "exp": exp,
            "price": base_price + random.randint(10, 50)
        })
    return products

# ================= DETAIL PANEL =================
def open_detail(p, status, discount, final_price, view_date):
    win = tk.Toplevel()
    win.title(p["name"])
    win.geometry("450x450")
    win.configure(bg="#020617")

    tk.Label(win, text=p["name"],
             font=("Segoe UI", 16, "bold"),
             bg="#020617", fg="white").pack(pady=15)

    freshness = max(
        0,
        min(100, int((p["exp"] - view_date).days /
                     (p["exp"] - p["mfg"]).days * 100))
    )

    advice = "Sell today with discount" if status == "⚠ BEST BEFORE" else "Fresh & safe for sale"

    details = [
        f"Category        : {p['category']}",
        f"Manufactured    : {p['mfg'].date()}",
        f"Best Before     : {p['exp'].date()}",
        f"Freshness       : {freshness}%",
        f"Status          : {status}",
        f"Advice          : {advice}",
        f"Original Price  : ₹{p['price']}",
        f"Discount        : {discount}%",
        f"Final Price     : {final_price}"
    ]

    for d in details:
        tk.Label(win, text=d,
                 bg="#020617", fg="#e5e7eb",
                 font=("Segoe UI", 11),
                 anchor="w").pack(fill="x", padx=30, pady=4)

# ================= CATEGORY VIEW (CENTER ALIGNED FIX) =================
def open_category_view(category):
    root = tk.Toplevel()
    root.title(category)
    root.state("zoomed")
    root.configure(bg="#020617")

    products = generate_products(category)
    view_date = BASE_VIEW_DATE

    tk.Label(root, text=category,
             font=("Segoe UI", 22, "bold"),
             bg="#020617", fg="white").pack(pady=10)

    # ---------- DATE CONTROLS ----------
    def change_date(offset):
        nonlocal view_date
        view_date = BASE_VIEW_DATE + timedelta(days=offset)
        render()

    date_frame = tk.Frame(root, bg="#020617")
    date_frame.pack(pady=5)

    for label, d in [("Yesterday", -1), ("Today", 0), ("Tomorrow", 1)]:
        tk.Button(
            date_frame, text=label,
            bg="#1e293b", fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0, padx=15, pady=6,
            command=lambda x=d: change_date(x)
        ).pack(side="left", padx=10)

    def new_batch():
        nonlocal products
        products = generate_products(category)
        render()

    tk.Button(
        root, text="🆕 New Batch Arrived",
        bg="#22c55e", fg="white",
        font=("Segoe UI", 11, "bold"),
        bd=0, padx=20, pady=8,
        command=new_batch
    ).pack(pady=10)

    # ---------- CANVAS + SCROLL ----------
    container = tk.Frame(root, bg="#020617")
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg="#020617", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    holder = tk.Frame(canvas, bg="#020617")
    window_id = canvas.create_window((0, 0), window=holder, anchor="n")

    # ✅ CENTER ALIGN FIX (FROM FROZEN FOOD)
    def center_holder(event):
        canvas_width = event.width
        holder.update_idletasks()
        frame_width = holder.winfo_reqwidth()
        x = max((canvas_width - frame_width) // 2, 0)
        canvas.coords(window_id, x, 0)

    canvas.bind("<Configure>", center_holder)

    holder.bind("<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.bind_all("<MouseWheel>",
        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # ---------- RENDER PRODUCTS ----------
    def render():
        for w in holder.winfo_children():
            w.destroy()

        col = row = 0

        for p in products:
            days_left = (p["exp"] - view_date).days
            if days_left < 0:
                continue

            if days_left <= 1:
                status = "⚠ BEST BEFORE"
                discount = random.choice([20, 30, 40])
                final_price = f"₹{int(p['price'] * (100 - discount) / 100)}"
                color = "#facc15"
            else:
                status = "✅ FRESH"
                discount = 0
                final_price = f"₹{p['price']}"
                color = "#22c55e"

            card = tk.Frame(
                holder, bg="#020617",
                highlightthickness=2,
                highlightbackground=color,
                padx=12, pady=12
            )
            card.grid(row=row, column=col, padx=18, pady=18)

            tk.Label(card, text=p["name"],
                     bg="#020617", fg="white",
                     font=("Segoe UI", 10, "bold")).pack()

            tk.Label(card, text=status,
                     bg="#020617", fg=color,
                     font=("Segoe UI", 9)).pack()

            tk.Label(card, text=f"{p['price']} → {final_price}",
                     bg="#020617", fg="#e5e7eb",
                     font=("Segoe UI", 10)).pack(pady=5)

            tk.Button(
                card, text="View",
                bg="#020617", fg="white",
                bd=0,
                command=lambda x=p, s=status, d=discount, f=final_price:
                open_detail(x, s, d, f, view_date)
            ).pack()

            col += 1
            if col == 4:
                col = 0
                row += 1

    render()

# ================= MAIN BAKERY PAGE =================
def open_bakery_page():
    root = tk.Toplevel()
    root.title("Bakery Smart Display Counter")
    root.state("zoomed")
    root.update_idletasks()

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

    main = tk.Frame(root, bg="#020617")
    main.place(relx=0.5, rely=0.52, anchor="center")

    tk.Label(main, text="Bakery Smart Display Counter",
             font=("Segoe UI", 24, "bold"),
             bg="#020617", fg="white").pack(pady=40)

    frame = tk.Frame(main, bg="#020617")
    frame.pack()

    categories = [
        ("Bread & Buns", "#f59e0b"),
        ("Cakes & Pastries", "#ec4899"),
        ("Cookies & Rusks", "#22c55e"),
        ("Savory Bakery", "#38bdf8")
    ]

    row = col = 0
    for cat, color in categories:
        card = tk.Frame(
            frame, bg="#020617",
            highlightthickness=2,
            highlightbackground=color,
            padx=30, pady=30
        )
        card.grid(row=row, column=col, padx=40, pady=40)

        tk.Label(card, text=cat,
                 font=("Segoe UI", 13, "bold"),
                 bg="#020617", fg="white").pack(pady=10)

        tk.Button(
            card, text="Open Counter",
            bg="#020617", fg=color,
            bd=0,
            font=("Segoe UI", 11, "bold"),
            command=lambda c=cat: open_category_view(c)
        ).pack()

        col += 1
        if col == 2:
            col = 0
            row += 1