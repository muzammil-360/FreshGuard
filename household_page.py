import tkinter as tk
from datetime import datetime, timedelta
import random

BASE_DATE = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

HOUSEHOLD_DATA = {
    "🧼 Cleaning & Hygiene": {
        "All-Purpose Cleaners": ["Amway LOC Cleaner", "Colin Surface Cleaner"],
        "Floor Cleaners": ["Lizol Floor Cleaner", "Harpic Floor Cleaner"],
        "Toilet Cleaners": ["Harpic Toilet Cleaner", "Domex Toilet Expert"],
        "Dishwashing": ["Vim Liquid Gel", "Pril Dishwash"],
        "Glass Cleaners": ["Colin Glass Cleaner"]
    },
    "👤 Personal Care": {
        "Soaps & Body Wash": ["Dettol Soap", "Dove Body Wash"],
        "Hair Care": ["Khadi Shampoo", "Clinic Plus Shampoo"],
        "Oral Care": ["Colgate Toothpaste", "Sensodyne"],
        "Skin Care": ["Nivea Cream", "Simple Face Wash"],
        "Deodorants": ["Nivea Deo", "Fogg Spray"]
    },
    "👶 Sensitive Care": {
        "Baby Care": ["Himalaya Baby Lotion", "Johnson Baby Shampoo"],
        "Feminine Hygiene": ["Whisper Pads", "Namyaa Intimate Wash"],
        "Men’s Grooming": ["Old Spice Aftershave", "Beard Oil"]
    },
    "🏡 Home & Wellness": {
        "Air Care": ["Godrej Air Freshener", "Stanfresh Spray"],
        "Pest Control": ["Hit Spray", "Naphthalene Balls"],
        "Fabric Care": ["Comfort Conditioner", "Ujala Whitener"],
        "Kitchen Hygiene": ["Vim Degreaser", "Baby Bottle Cleanser"],
        "Wellness": ["Essential Oils", "Bath Salts"]
    }
}

# ---------- PRODUCT GENERATOR ----------
def generate_products(category, names, count=40):
    products = []
    for i in range(count):
        name = random.choice(names)
        mfg = BASE_DATE - timedelta(days=random.randint(30, 300))
        exp = mfg + timedelta(days=random.randint(180, 540))
        products.append({
            "name": f"{name} #{i+1}",
            "category": category,
            "mfg": mfg,
            "exp": exp,
            "price": random.randint(80, 450),
            "chemical": random.choice(["Low", "Medium", "High"]),
            "skin_safe": random.choice(["Yes", "No"]),
            "child_safe": random.choice(["Yes", "No"])
        })
    return products

# ================= MAIN PAGE =================
def open_household_page():
    root = tk.Toplevel()
    root.title("Household & Personal Care")
    root.state("zoomed")
    root.configure(bg="#020617")

    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()

    canvas.create_rectangle(0, 0, w, h, fill="#020617", outline="")
    canvas.create_rectangle(0, h * 0.58, w, h, fill="#0f172a", outline="")

    container = tk.Frame(root, bg="#020617")
    container.place(relx=0.5, rely=0.52, anchor="center")

    tk.Label(
        container,
        text="Household & Personal Care Ecosystem",
        font=("Segoe UI", 26, "bold"),
        bg="#020617",
        fg="white"
    ).pack(pady=(0, 25))

    grid = tk.Frame(container, bg="#020617")
    grid.pack()

    row = col = 0
    for zone, categories in HOUSEHOLD_DATA.items():
        box_height = 280 if row == 0 else 240

        card = tk.Frame(
            grid,
            bg="#020617",
            highlightthickness=3,
            highlightbackground="#38bdf8",
            width=480,
            height=box_height,
            padx=18,
            pady=14
        )
        card.grid(row=row, column=col, padx=30, pady=22)
        card.pack_propagate(False)

        tk.Label(
            card,
            text=zone,
            font=("Segoe UI", 17, "bold"),
            bg="#020617",
            fg="#38bdf8"
        ).pack(anchor="w", pady=(0, 10))

        for cat in categories:
            tk.Button(
                card,
                text=cat,
                font=("Segoe UI", 11),
                bg="#020617",
                fg="white",
                bd=0,
                anchor="w",
                command=lambda c=cat, n=categories[cat]: open_category_page(c, n)
            ).pack(fill="x", pady=3)

        col += 1
        if col == 2:
            col = 0
            row += 1

# ================= CATEGORY PAGE (CENTER + SCROLL + DATE APPLY) =================
def open_category_page(category, product_names):
    win = tk.Toplevel()
    win.title(category)
    win.state("zoomed")
    win.configure(bg="#020617")

    # ---------- BACKGROUND ----------
    canvas_bg = tk.Canvas(win, highlightthickness=0)
    canvas_bg.pack(fill="both", expand=True)

    w = win.winfo_screenwidth()
    h = win.winfo_screenheight()
    canvas_bg.create_rectangle(0, 0, w, h, fill="#020617", outline="")
    canvas_bg.create_rectangle(0, h * 0.6, w, h, fill="#0f172a", outline="")

    # ---------- CENTER CONTAINER ----------
    container = tk.Frame(win, bg="#020617")
    container.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        container,
        text=category,
        font=("Segoe UI", 24, "bold"),
        bg="#020617",
        fg="white"
    ).pack(pady=(10, 5))

    tk.Label(
        container,
        text="Select a product to view detailed safety & usage analysis",
        font=("Segoe UI", 11),
        bg="#020617",
        fg="#94a3b8"
    ).pack(pady=(0, 15))

    # ---------- DATE FILTER ----------
    date_frame = tk.Frame(container, bg="#020617")
    date_frame.pack(pady=8)

    tk.Label(
        date_frame,
        text="View Date:",
        bg="#020617",
        fg="white",
        font=("Segoe UI", 10)
    ).pack(side="left", padx=6)

    date_var = tk.StringVar(value=BASE_DATE.strftime("%Y-%m-%d"))
    date_entry = tk.Entry(
        date_frame,
        textvariable=date_var,
        width=12,
        justify="center"
    )
    date_entry.pack(side="left", padx=6)

    # ---------- SCROLLABLE AREA ----------
    canvas = tk.Canvas(container, bg="#020617", highlightthickness=0, width=900, height=520)
    canvas.pack()

    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas, bg="#020617")
    window = canvas.create_window((0, 0), window=frame, anchor="n")

    def resize(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(window, width=900)

    frame.bind("<Configure>", resize)
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    products = generate_products(category, product_names)

    grid = tk.Frame(frame, bg="#020617")
    grid.pack(pady=20)

    # ---------- RENDER FUNCTION ----------
    def render_products():
        for w in grid.winfo_children():
            w.destroy()

        try:
            view_date = datetime.strptime(date_var.get(), "%Y-%m-%d")
        except:
            return

        row = col = 0
        for p in products:
            days_left = (p["exp"] - view_date).days

            if days_left > 90:
                status = "SAFE"
                color = "#22c55e"
            elif days_left > 30:
                status = "CAUTION"
                color = "#facc15"
            else:
                status = "NEAR EXPIRY"
                color = "#fb923c"

            card = tk.Frame(
                grid,
                bg="#020617",
                highlightthickness=2,
                highlightbackground=color,
                width=380,
                height=150,
                padx=14,
                pady=10
            )
            card.grid(row=row, column=col, padx=30, pady=22)
            card.pack_propagate(False)

            tk.Label(
                card,
                text=p["name"],
                font=("Segoe UI", 11, "bold"),
                bg="#020617",
                fg="white",
                wraplength=340,
                justify="left"
            ).pack(anchor="w")

            tk.Label(
                card,
                text=f"Status: {status}",
                font=("Segoe UI", 10),
                bg="#020617",
                fg=color
            ).pack(anchor="w", pady=(4, 2))

            tk.Label(
                card,
                text=f"Price: ₹{p['price']}",
                font=("Segoe UI", 10),
                bg="#020617",
                fg="#e5e7eb"
            ).pack(anchor="w")

            tk.Button(
                card,
                text="View Full Analysis",
                bg="#020617",
                fg=color,
                bd=0,
                font=("Segoe UI", 10, "bold"),
                command=lambda x=p: open_product_kundali(x)
            ).pack(anchor="e", pady=(6, 0))

            col += 1
            if col == 2:
                col = 0
                row += 1

    # ---------- APPLY DATE BUTTON ----------
    tk.Button(
        date_frame,
        text="Apply Date",
        bg="#22c55e",
        fg="white",
        bd=0,
        font=("Segoe UI", 10, "bold"),
        padx=14,
        command=render_products
    ).pack(side="left", padx=8)

    # ---------- INITIAL LOAD ----------
    render_products()


# ================= PRODUCT DETAIL PAGE =================
def open_product_kundali(p):
    win = tk.Toplevel()
    win.title(p["name"])
    win.state("zoomed")
    win.configure(bg="#020617")

    canvas = tk.Canvas(win, bg="#020617", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    frame = tk.Frame(canvas, bg="#020617")
    canvas.create_window((0, 0), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    win.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    tk.Label(
        frame,
        text=p["name"],
        font=("Segoe UI", 26, "bold"),
        bg="#020617",
        fg="white"
    ).pack(pady=30)

    info = [
        f"Category           : {p['category']}",
        f"Manufactured Date  : {p['mfg'].date()}",
        f"Expiry Date        : {p['exp'].date()}",
        f"Chemical Strength  : {p['chemical']}",
        f"Skin Safe          : {p['skin_safe']}",
        f"Child Safe         : {p['child_safe']}",
        f"Original Price     : ₹{p['price']}",
        f"Suggested Discount : {'30%' if p['chemical']=='High' else '10%'}",
        "",
        "SYSTEM ANALYSIS:",
        "• Chemical effectiveness reduces over time",
        "• High chemical products require extra caution",
        "• Replace before expiry for hygiene & safety"
    ]

    for line in info:
        tk.Label(
            frame,
            text=line,
            font=("Segoe UI", 13),
            bg="#020617",
            fg="#e5e7eb",
            anchor="w"
        ).pack(fill="x", padx=260, pady=6)