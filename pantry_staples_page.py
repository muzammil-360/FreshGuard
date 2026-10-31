import tkinter as tk
from tkinter import ttk, simpledialog
from datetime import datetime, timedelta
import random

# ================= BASE DATE =================
BASE_DATE = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

# ================= PANTRY CONFIG =================
PANTRY_CATEGORIES = {
    "Rice": (365, (70, 8, 1)),
    "Pulses": (300, (22, 2, 60)),
    "Flour": (180, (12, 2, 76)),
    "Cooking Oil": (180, (0, 100, 0)),
    "Spices": (540, (18, 5, 50)),
    "Sugar & Salt": (720, (0, 0, 100)),
    "Dry Fruits": (240, (15, 45, 40))
}

PRICES = {
    "Rice": (60, 120),
    "Pulses": (80, 160),
    "Flour": (40, 90),
    "Cooking Oil": (140, 260),
    "Spices": (50, 300),
    "Sugar & Salt": (30, 70),
    "Dry Fruits": (200, 600)
}

# ================= PRODUCT GENERATOR =================
def generate_pantry_products(count=220):
    products = []
    for i in range(count):
        category = random.choice(list(PANTRY_CATEGORIES.keys()))
        shelf_life, nutrition = PANTRY_CATEGORIES[category]

        mfg_offset = random.randint(0, shelf_life + 30)
        mfg = BASE_DATE - timedelta(days=mfg_offset)
        exp = mfg + timedelta(days=shelf_life)

        price = random.randint(*PRICES[category])
        protein, fat, carbs = nutrition
        calories = protein*4 + carbs*4 + fat*9

        products.append({
            "name": f"{category} Item {i+1}",
            "category": category,
            "mfg": mfg,
            "exp": exp,
            "price": price,
            "protein": protein,
            "fat": fat,
            "carbs": carbs,
            "calories": calories
        })
    return products

# ================= STATUS LOGIC =================
def get_status(expiry_date, view_date):
    days_left = (expiry_date - view_date).days
    if days_left < 0:
        return "EXPIRED", "red"
    elif days_left <= 30:
        return "NEAR EXPIRY", "orange"
    else:
        return "SAFE", "green"

# ================= DETAIL WINDOW =================
def open_detail_window(product, status):
    win = tk.Toplevel()
    win.title(product["name"])
    win.geometry("560x560")
    win.configure(bg="#020617")

    tk.Label(win, text=product["name"],
             font=("Segoe UI", 16, "bold"),
             bg="#020617", fg="white").pack(pady=12)

    days_left = (product["exp"] - BASE_DATE).days

    details = [
        f"Category           : {product['category']}",
        f"Manufactured Date  : {product['mfg'].date()}",
        f"Expiry Date        : {product['exp'].date()}",
        f"Days Remaining     : {days_left}",
        f"Price              : ₹{product['price']}",
        f"Status             : {status}",
        "",
        "Nutrition (per 100g)",
        f"Protein            : {product['protein']} g",
        f"Fat                : {product['fat']} g",
        f"Carbohydrates      : {product['carbs']} g",
        f"Calories           : {product['calories']} kcal",
        "",
        "Storage Advice     : Store in cool, dry place"
    ]

    for d in details:
        tk.Label(win, text=d,
                 font=("Segoe UI", 11),
                 bg="#020617", fg="#e5e7eb",
                 anchor="w").pack(fill="x", padx=30, pady=4)

# ================= MAIN PANTRY PAGE =================
def open_pantry_staples_page():
    root = tk.Toplevel()
    root.title("Pantry Staples – Smart Inventory")
    root.state("zoomed")

    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    canvas.create_rectangle(
        0, 0,
        root.winfo_screenwidth(),
        root.winfo_screenheight(),
        fill="#020617", outline=""
    )
    canvas.create_rectangle(
        0,
        root.winfo_screenheight() * 0.55,
        root.winfo_screenwidth(),
        root.winfo_screenheight(),
        fill="#0f172a", outline=""
    )

    main = tk.Frame(root, bg="#020617")
    main.place(relx=0.5, rely=0.48, anchor="center")

    tk.Label(main, text="Pantry Staples – Shelf Life Monitor",
             font=("Segoe UI", 24, "bold"),
             bg="#020617", fg="white").pack(pady=(0, 6))

    # ---------- DATE ----------
    date_var = tk.StringVar(value=BASE_DATE.strftime("%Y-%m-%d"))
    tk.Entry(main, textvariable=date_var, width=15).pack(pady=4)

    products = generate_pantry_products()

    # ---------- SEARCH BUTTON (DAIRY-STYLE) ----------
    def search_product():
        query = simpledialog.askstring("Search Product", "Enter product name:")
        if not query:
            return
        tree.delete(*tree.get_children())
        view_date = datetime.strptime(date_var.get(), "%Y-%m-%d")

        for p in products:
            if query.lower() in p["name"].lower():
                status, color = get_status(p["exp"], view_date)
                shelf = (p["exp"] - p["mfg"]).days
                tree.insert("", "end", values=(
                    p["name"], p["category"],
                    p["mfg"].date(), p["exp"].date(),
                    f"{shelf} days", status
                ), tags=(color,))

    tk.Button(
        main,
        text="Search Product",
        bg="#38bdf8",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        bd=0,
        padx=18,
        pady=6,
        command=search_product
    ).pack(pady=6)

    # ---------- TABLE ----------
    frame = tk.Frame(main)
    frame.pack(pady=12)

    cols = ("Product", "Category", "MFG", "EXP", "Shelf Life", "Status")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=16)

    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=140, anchor="center")

    tree.pack(side="left")
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    def load_table():
        tree.delete(*tree.get_children())
        view_date = datetime.strptime(date_var.get(), "%Y-%m-%d")
        for p in products:
            status, color = get_status(p["exp"], view_date)
            shelf = (p["exp"] - p["mfg"]).days
            tree.insert("", "end", values=(
                p["name"], p["category"],
                p["mfg"].date(), p["exp"].date(),
                f"{shelf} days", status
            ), tags=(color,))

        tree.tag_configure("green", background="#dcfce7")
        tree.tag_configure("orange", background="#fef9c3")
        tree.tag_configure("red", background="#fee2e2")

    load_table()

    def on_double_click(event):
        sel = tree.focus()
        if not sel:
            return
        name = tree.item(sel)["values"][0]
        for p in products:
            if p["name"] == name:
                status, _ = get_status(
                    p["exp"],
                    datetime.strptime(date_var.get(), "%Y-%m-%d")
                )
                open_detail_window(p, status)
                break

    tree.bind("<Double-Button-1>", on_double_click)

    tk.Button(
        main,
        text="Apply Date",
        bg="#22c55e",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        bd=0,
        padx=20,
        pady=8,
        command=load_table
    ).pack(pady=8)