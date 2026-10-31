import tkinter as tk
from datetime import datetime, timedelta
import random

BASE_DATE = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

# ==================================================
# DATA CONFIG
# ==================================================
CATEGORY_DATA = {
    "Red Meat": [
        ("Beef Steak", "Contains Beef", 3, 700),
        ("Pork Ribs", "Contains Pork", 3, 680),
        ("Lamb Meat", "Halal Friendly", 3, 650),
        ("Goat Meat", "Halal Friendly", 3, 620),
    ],
    "Poultry": [
        ("Chicken Breast", "Halal Friendly", 2, 220),
        ("Turkey Meat", "Halal Friendly", 2, 350),
        ("Duck Meat", "Halal Friendly", 2, 300),
    ],
    "Game Meat": [
        ("Venison", "Wild Meat", 2, 780),
        ("Rabbit Meat", "Wild Meat", 1, 520),
    ],
    "Processed Meat": [
        ("Bacon", "Contains Pork", 7, 400),
        ("Sausage", "Contains Pork", 7, 380),
    ],
    "Finfish": [
        ("Salmon", "Fatty Fish", 1, 550),
        ("Tuna", "Lean Fish", 1, 500),
        ("Cod", "Lean Fish", 1, 460),
    ],
    "Shellfish": [
        ("Prawns", "Allergy Alert", 1, 520),
        ("Crab", "Allergy Alert", 1, 600),
    ],
    "Mollusks": [
        ("Squid", "Seafood", 1, 480),
        ("Oysters", "Seafood", 1, 620),
    ],
    "Exotic Seafood": [
        ("Octopus", "Seafood", 1, 700),
        ("Sea Urchin", "Seafood", 1, 820),
    ],
}

# ==================================================
# PRODUCT GENERATOR
# ==================================================
def generate_products(category, count=40):
    products = []
    base = CATEGORY_DATA[category]

    for i in range(count):
        name, tag, shelf, price = random.choice(base)
        mfg = BASE_DATE - timedelta(days=random.randint(0, shelf))
        exp = mfg + timedelta(days=shelf)

        products.append({
            "name": f"{name} #{i+1}",
            "category": category,
            "religion": tag,
            "mfg": mfg,
            "exp": exp,
            "price": price
        })
    return products

# ==================================================
# PRODUCT DETAIL PAGE
# ==================================================
def open_product_detail(p, status, discount, final_price, days_left):
    win = tk.Toplevel()
    win.title(p["name"])
    win.geometry("520x500")
    win.configure(bg="#020617")

    tk.Label(win, text=p["name"],
             font=("Segoe UI", 16, "bold"),
             bg="#020617", fg="white").pack(pady=15)

    action = (
        "❌ Discard Immediately" if days_left <= 0 else
        "⚠ Sell Today with Discount" if days_left == 1 else
        "✅ Safe for Sale"
    )

    details = [
        f"Category        : {p['category']}",
        f"Religious Tag   : {p['religion']}",
        f"Manufactured   : {p['mfg'].date()}",
        f"Expiry Date    : {p['exp'].date()}",
        f"Days Remaining : {days_left}",
        f"Status         : {status}",
        f"Original Price : ₹{p['price']}",
        f"Discount       : {discount}%",
        f"Final Price    : {final_price}",
        "",
        "Storage Advice : Keep refrigerated (0–4°C)",
        f"Action         : {action}"
    ]

    for d in details:
        tk.Label(win, text=d,
                 font=("Segoe UI", 11),
                 bg="#020617", fg="#e5e7eb",
                 anchor="w").pack(fill="x", padx=35, pady=4)

# ==================================================
# SAFETY INSPECTION PAGE (UNCHANGED)
# ==================================================
def open_category_products(category):
    root = tk.Toplevel()
    root.title(category)
    root.state("zoomed")
    root.configure(bg="#020617")

    products = generate_products(category)
    shown = []

    tk.Label(root, text=f"{category} – Safety Inspection",
             font=("Segoe UI", 22, "bold"),
             bg="#020617", fg="#ef4444").pack(pady=15)

    if category in ["Red Meat", "Processed Meat"]:
        tk.Label(
            root,
            text="⚠ This category may contain Beef / Pork. Select as per preference.",
            font=("Segoe UI", 11),
            bg="#020617", fg="#facc15"
        ).pack()

    tk.Label(root, text="Check status for date (YYYY-MM-DD)",
             font=("Segoe UI", 11),
             bg="#020617", fg="#94a3b8").pack(pady=5)

    date_entry = tk.Entry(root, font=("Segoe UI", 11))
    date_entry.pack()

    listbox = tk.Listbox(root, width=160, height=22,
                         font=("Segoe UI", 10))
    listbox.pack(pady=15)

    def check_status():
        listbox.delete(0, tk.END)
        shown.clear()

        try:
            view_date = datetime.strptime(date_entry.get(), "%Y-%m-%d")
        except:
            return

        for p in products:
            days_left = (p["exp"] - view_date).days

            if days_left < 0:
                continue

            if days_left == 1:
                status = "⚠ CONSUME TODAY"
                discount = 50
                final_price = f"₹{int(p['price'] * 0.5)}"
            else:
                status = "✅ SAFE"
                discount = 0
                final_price = f"₹{p['price']}"

            shown.append({
                **p,
                "status": status,
                "discount": discount,
                "final_price": final_price,
                "days_left": days_left
            })

        for p in shown:
            listbox.insert(
                tk.END,
                f"{p['name']} | {p['religion']} | {p['status']} | {p['final_price']}"
            )

    def open_selected(event):
        if not listbox.curselection():
            return
        p = shown[listbox.curselection()[0]]
        open_product_detail(
            p,
            p["status"],
            p["discount"],
            p["final_price"],
            p["days_left"]
        )

    listbox.bind("<Double-Button-1>", open_selected)

    tk.Button(
        root,
        text="Check Safety Status",
        bg="#ef4444",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        bd=0,
        padx=20,
        pady=8,
        command=check_status
    ).pack(pady=5)

# ==================================================
# MAIN MEAT & SEAFOOD CATEGORY PAGE (BG CHANGED ONLY)
# ==================================================

def open_meat_seafood_page():
    root = tk.Toplevel()
    root.title("Meat & Seafood")
    root.state("zoomed")
    root.update_idletasks()

    # ===== BACKGROUND (SAME AS FRESH PRODUCE) =====
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

    # ===== CENTERED CONTENT =====
    main = tk.Frame(root, bg="#020617")
    main.place(relx=0.5, rely=0.52, anchor="center")

    tk.Label(
        main,
        text="Meat & Seafood – Safety Categories",
        font=("Segoe UI", 24, "bold"),
        bg="#020617",
        fg="white"
    ).pack(pady=30)

    frame = tk.Frame(main, bg="#020617")
    frame.pack()

    categories = list(CATEGORY_DATA.keys())

    row = col = 0
    for cat in categories:
        # ===== ORIGINAL CARD STYLE (UNCHANGED) =====
        card = tk.Frame(
            frame,
            bg="#020617",
            highlightthickness=2,
            highlightbackground="#ef4444",
            width=260,
            height=140
        )
        card.grid(row=row, column=col, padx=25, pady=25)
        card.grid_propagate(False)

        tk.Label(
            card,
            text=cat,
            font=("Segoe UI", 13, "bold"),
            bg="#020617",
            fg="white"
        ).pack(pady=(25, 10))

        tk.Label(
            card,
            text="Safety Inspection",
            font=("Segoe UI", 10),
            bg="#020617",
            fg="#94a3b8"
        ).pack()

        tk.Button(
            card,
            text="Inspect",
            bg="#020617",
            fg="#ef4444",
            font=("Segoe UI", 11, "bold"),
            bd=0,
            command=lambda c=cat: open_category_products(c)
        ).pack(pady=10)

        col += 1
        if col == 4:
            col = 0
            row += 1