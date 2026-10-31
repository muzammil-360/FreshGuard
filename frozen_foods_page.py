import tkinter as tk
from datetime import datetime, timedelta
import random

# ================= SYSTEM DATE =================
SYSTEM_DATE = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

# ================= ITEMS =================
ITEMS = [
    ("Frozen Peas", "Vegetable", 120, 180),
    ("Frozen Corn", "Vegetable", 120, 160),
    ("Frozen Berries", "Fruit", 90, 400),
    ("Frozen Fries", "Snack", 90, 220),
    ("Frozen Pizza", "Ready Meal", 60, 380),
    ("Frozen Nuggets", "Meat", 60, 350),
    ("Frozen Fish Fillet", "Seafood", 45, 420),
    ("Ice Cream Tub", "Dessert", 30, 300),
]

DECAY = {
    "Vegetable": 0.15,
    "Fruit": 0.20,
    "Snack": 0.25,
    "Ready Meal": 0.30,
    "Meat": 0.40,
    "Seafood": 0.45,
    "Dessert": 0.50
}

# ================= STOCK =================
def generate_stock(count=160):
    stock = []
    for i in range(count):
        name, ftype, shelf, price = random.choice(ITEMS)
        frozen_days = random.randint(0, shelf + 5)
        frozen_date = SYSTEM_DATE - timedelta(days=frozen_days)
        expiry = frozen_date + timedelta(days=shelf)

        stock.append({
            "name": f"{name} #{i+1}",
            "type": ftype,
            "frozen_date": frozen_date,
            "expiry": expiry,
            "price": price
        })
    return stock

# ================= QUALITY LOGIC =================
def calculate_quality(item, view_date):
    if view_date > item["expiry"]:
        return 0

    days_to_expiry = (item["expiry"] - view_date).days
    if days_to_expiry <= 1:
        return 30

    if view_date < item["frozen_date"]:
        return 100

    days_passed = (view_date - item["frozen_date"]).days
    q = 100 - int(days_passed * DECAY[item["type"]])
    return max(0, min(100, q))

# ================= DETAIL =================
def open_detail(item, quality, discount, final_price):
    win = tk.Toplevel()
    win.title(item["name"])
    win.geometry("520x520")
    win.configure(bg="#020617")

    tk.Label(win, text=item["name"],
             font=("Segoe UI", 16, "bold"),
             bg="#020617", fg="white").pack(pady=15)

    for line in [
        f"Food Type        : {item['type']}",
        f"Frozen Date      : {item['frozen_date'].date()}",
        f"Expiry Date      : {item['expiry'].date()}",
        f"Quality          : {quality}%",
        f"Original Price  : ₹{item['price']}",
        f"Discount        : {discount}%",
        f"Final Price     : {final_price}",
    ]:
        tk.Label(win, text=line,
                 font=("Segoe UI", 11),
                 bg="#020617", fg="#e5e7eb",
                 anchor="w").pack(fill="x", padx=40, pady=4)

# ================= GRID VIEW =================
def open_quality_view(title, filter_fn):
    root = tk.Toplevel()
    root.title(title)
    root.state("zoomed")
    root.configure(bg="#020617")

    stock = generate_stock()

    tk.Label(root, text=title,
             font=("Segoe UI", 22, "bold"),
             bg="#020617", fg="#38bdf8").pack(pady=10)

    date_var = tk.StringVar(value=SYSTEM_DATE.strftime("%Y-%m-%d"))
    tk.Entry(root, textvariable=date_var,
             font=("Segoe UI", 11),
             justify="center").pack(pady=6)

    container = tk.Frame(root, bg="#020617")
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg="#020617", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    holder = tk.Frame(canvas, bg="#020617")
    window = canvas.create_window((0, 0), window=holder, anchor="n")

    canvas.bind("<Configure>",
        lambda e: canvas.itemconfig(window, width=e.width))
    holder.bind("<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind_all("<MouseWheel>",
        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def render():
        for w in holder.winfo_children():
            w.destroy()

        view_date = datetime.strptime(date_var.get(), "%Y-%m-%d")
        row = col = 0

        for item in stock:
            q = calculate_quality(item, view_date)
            if not filter_fn(q):
                continue

            if q >= 80:
                discount, color = 0, "#22c55e"
            elif q >= 50:
                discount, color = 30, "#facc15"
            elif q > 0:
                discount, color = 60, "#ef4444"
            else:
                discount, color = 0, "#991b1b"

            final_price = "Not for sale" if q == 0 else \
                f"₹{int(item['price'] * (100-discount)/100)}"

            card = tk.Frame(holder, bg="#020617",
                            highlightthickness=2,
                            highlightbackground=color,
                            width=280, height=200)
            card.grid(row=row, column=col, padx=25, pady=25)
            card.grid_propagate(False)

            tk.Label(card, text=item["name"],
                     bg="#020617", fg="white",
                     font=("Segoe UI", 10, "bold"),
                     wraplength=240).pack(pady=6)

            tk.Label(card, text=f"Quality: {q}%",
                     bg="#020617", fg=color).pack()

            tk.Label(card, text=f"{item['price']} → {final_price}",
                     bg="#020617", fg="#e5e7eb").pack(pady=4)

            tk.Button(card, text="View Details",
                      bg="#020617", fg=color,
                      bd=0,
                      font=("Segoe UI", 10, "bold"),
                      command=lambda x=item, qq=q,
                      d=discount, f=final_price:
                      open_detail(x, qq, d, f)).pack()

            col += 1
            if col == 4:
                col = 0
                row += 1

    tk.Button(root, text="Apply Date",
              bg="#38bdf8", fg="white",
              font=("Segoe UI", 10, "bold"),
              bd=0, padx=15, pady=6,
              command=render).pack(pady=6)

    render()

# ================= MAIN FROZEN PAGE =================
def open_frozen_foods_page():
    root = tk.Toplevel()
    root.title("Frozen Foods – Quality Monitor")
    root.state("zoomed")

    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # TOP DARK BG
    canvas.create_rectangle(
        0, 0,
        root.winfo_screenwidth(),
        root.winfo_screenheight(),
        fill="#020617",
        outline=""
    )

    # BOTTOM RECTANGLE (DASHBOARD STYLE)
    canvas.create_rectangle(
        0,
        root.winfo_screenheight() * 0.55,
        root.winfo_screenwidth(),
        root.winfo_screenheight(),
        fill="#0f172a",
        outline=""
    )

    main = tk.Frame(root, bg="#020617")
    main.place(relx=0.5, rely=0.48, anchor="center")

    tk.Label(main, text="Frozen Foods – Quality Monitor ❄️",
             font=("Segoe UI", 26, "bold"),
             bg="#020617", fg="white").pack(pady=15)

    tk.Label(main, text="Quality-based cold storage control panel",
             font=("Segoe UI", 12),
             bg="#020617", fg="#94a3b8").pack(pady=(0, 25))

    panel = tk.Frame(main, bg="#020617")
    panel.pack()

    buttons = [
        ("🟢 High Quality", "#22c55e",
         lambda: open_quality_view("High Quality Frozen Stock", lambda q: q >= 80)),
        ("🟡 Medium Quality", "#facc15",
         lambda: open_quality_view("Medium Quality Frozen Stock", lambda q: 50 <= q < 80)),
        ("🔴 Low Quality", "#ef4444",
         lambda: open_quality_view("Low Quality Frozen Stock", lambda q: 0 < q < 50)),
        ("❌ Unsafe / Expired", "#991b1b",
         lambda: open_quality_view("Unsafe / Expired Frozen Stock", lambda q: q == 0)),
        ("📅 View by Date", "#38bdf8",
         lambda: open_quality_view("Stock by Selected Date", lambda q: True)),
        ("📊 All Frozen Stock", "#0ea5e9",
         lambda: open_quality_view("Complete Frozen Stock", lambda q: True)),
    ]

    row = col = 0
    for text, color, cmd in buttons:
        card = tk.Frame(panel, bg="#020617",
                        highlightthickness=2,
                        highlightbackground=color,
                        width=320, height=150)
        card.grid(row=row, column=col, padx=35, pady=30)
        card.grid_propagate(False)

        tk.Label(card, text=text,
                 bg="#020617", fg="white",
                 font=("Segoe UI", 12, "bold")).pack(expand=True)

        tk.Button(card, text="Open",
                  bg="#020617", fg=color,
                  bd=0,
                  font=("Segoe UI", 11, "bold"),
                  command=cmd).pack(pady=10)

        col += 1
        if col == 3:
            col = 0
            row += 1

            import tkinter as tk
from datetime import datetime, timedelta
import random

# ================= SYSTEM DATE =================
SYSTEM_DATE = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

# ================= ITEMS =================
ITEMS = [
    ("Frozen Peas", "Vegetable", 120, 180),
    ("Frozen Corn", "Vegetable", 120, 160),
    ("Frozen Berries", "Fruit", 90, 400),
    ("Frozen Fries", "Snack", 90, 220),
    ("Frozen Pizza", "Ready Meal", 60, 380),
    ("Frozen Nuggets", "Meat", 60, 350),
    ("Frozen Fish Fillet", "Seafood", 45, 420),
    ("Ice Cream Tub", "Dessert", 30, 300),
]

DECAY = {
    "Vegetable": 0.15,
    "Fruit": 0.20,
    "Snack": 0.25,
    "Ready Meal": 0.30,
    "Meat": 0.40,
    "Seafood": 0.45,
    "Dessert": 0.50
}

# ================= STOCK =================
def generate_stock(count=160):
    stock = []
    for i in range(count):
        name, ftype, shelf, price = random.choice(ITEMS)
        frozen_days = random.randint(0, shelf + 5)
        frozen_date = SYSTEM_DATE - timedelta(days=frozen_days)
        expiry = frozen_date + timedelta(days=shelf)

        stock.append({
            "name": f"{name} #{i+1}",
            "type": ftype,
            "frozen_date": frozen_date,
            "expiry": expiry,
            "price": price
        })
    return stock

# ================= QUALITY LOGIC (UNCHANGED) =================
def calculate_quality(item, view_date):
    if view_date > item["expiry"]:
        return 0

    days_to_expiry = (item["expiry"] - view_date).days
    if days_to_expiry <= 1:
        return 30

    if view_date < item["frozen_date"]:
        return 100

    days_passed = (view_date - item["frozen_date"]).days
    q = 100 - int(days_passed * DECAY[item["type"]])
    return max(0, min(100, q))

# ================= DETAIL PAGE =================
def open_detail(item, quality, discount, final_price):
    win = tk.Toplevel()
    win.title(item["name"])
    win.geometry("520x520")
    win.configure(bg="#020617")

    tk.Label(win, text=item["name"],
             font=("Segoe UI", 16, "bold"),
             bg="#020617", fg="white").pack(pady=15)

    for line in [
        f"Food Type        : {item['type']}",
        f"Frozen Date      : {item['frozen_date'].date()}",
        f"Expiry Date      : {item['expiry'].date()}",
        f"Quality          : {quality}%",
        f"Original Price  : ₹{item['price']}",
        f"Discount        : {discount}%",
        f"Final Price     : {final_price}",
    ]:
        tk.Label(win, text=line,
                 font=("Segoe UI", 11),
                 bg="#020617", fg="#e5e7eb",
                 anchor="w").pack(fill="x", padx=40, pady=4)

# ================= PRODUCT GRID VIEW =================
def open_quality_view(title, filter_fn):
    root = tk.Toplevel()
    root.title(title)
    root.state("zoomed")
    root.configure(bg="#020617")

    stock = generate_stock()

    tk.Label(root, text=title,
             font=("Segoe UI", 22, "bold"),
             bg="#020617", fg="#38bdf8").pack(pady=10)

    date_var = tk.StringVar(value=SYSTEM_DATE.strftime("%Y-%m-%d"))
    tk.Entry(root, textvariable=date_var,
             font=("Segoe UI", 11),
             justify="center").pack(pady=6)

    container = tk.Frame(root, bg="#020617")
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg="#020617", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    holder = tk.Frame(canvas, bg="#020617")
    window = canvas.create_window((0, 0), window=holder, anchor="n")

    # ✅ CENTER ALIGNMENT FIX
    def center_window(event):
        canvas_width = event.width
        holder.update_idletasks()
        frame_width = holder.winfo_reqwidth()
        x = max((canvas_width - frame_width) // 2, 0)
        canvas.coords(window, x, 0)

    canvas.bind("<Configure>", center_window)

    holder.bind("<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.bind_all("<MouseWheel>",
        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def render():
        for w in holder.winfo_children():
            w.destroy()

        view_date = datetime.strptime(date_var.get(), "%Y-%m-%d")
        row = col = 0

        for item in stock:
            q = calculate_quality(item, view_date)
            if not filter_fn(q):
                continue

            if q >= 80:
                discount, color = 0, "#22c55e"
            elif q >= 50:
                discount, color = 30, "#facc15"
            elif q > 0:
                discount, color = 60, "#ef4444"
            else:
                discount, color = 0, "#991b1b"

            final_price = "Not for sale" if q == 0 else \
                f"₹{int(item['price'] * (100-discount)/100)}"

            card = tk.Frame(holder, bg="#020617",
                            highlightthickness=2,
                            highlightbackground=color,
                            width=280, height=200)
            card.grid(row=row, column=col, padx=25, pady=25)
            card.grid_propagate(False)

            tk.Label(card, text=item["name"],
                     bg="#020617", fg="white",
                     font=("Segoe UI", 10, "bold"),
                     wraplength=240).pack(pady=6)

            tk.Label(card, text=f"Quality: {q}%",
                     bg="#020617", fg=color).pack()

            tk.Label(card, text=f"{item['price']} → {final_price}",
                     bg="#020617", fg="#e5e7eb").pack(pady=4)

            tk.Button(card, text="View Details",
                      bg="#020617", fg=color,
                      bd=0,
                      font=("Segoe UI", 10, "bold"),
                      command=lambda x=item, qq=q,
                      d=discount, f=final_price:
                      open_detail(x, qq, d, f)).pack()

            col += 1
            if col == 4:
                col = 0
                row += 1

    tk.Button(root, text="Apply Date",
              bg="#38bdf8", fg="white",
              font=("Segoe UI", 10, "bold"),
              bd=0, padx=15, pady=6,
              command=render).pack(pady=6)

    render()

# ================= MAIN FROZEN PAGE =================
def open_frozen_foods_page():
    root = tk.Toplevel()
    root.title("Frozen Foods – Quality Monitor")
    root.state("zoomed")

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
        root.winfo_screenheight() * 0.55,
        root.winfo_screenwidth(),
        root.winfo_screenheight(),
        fill="#0f172a",
        outline=""
    )

    main = tk.Frame(root, bg="#020617")
    main.place(relx=0.5, rely=0.48, anchor="center")

    tk.Label(main, text="Frozen Foods – Quality Monitor ❄️",
             font=("Segoe UI", 26, "bold"),
             bg="#020617", fg="white").pack(pady=15)

    tk.Label(main, text="Quality-based cold storage control panel",
             font=("Segoe UI", 12),
             bg="#020617", fg="#94a3b8").pack(pady=(0, 25))

    panel = tk.Frame(main, bg="#020617")
    panel.pack()

    buttons = [
        ("🟢 High Quality", "#22c55e",
         lambda: open_quality_view("High Quality Frozen Stock", lambda q: q >= 80)),
        ("🟡 Medium Quality", "#facc15",
         lambda: open_quality_view("Medium Quality Frozen Stock", lambda q: 50 <= q < 80)),
        ("🔴 Low Quality", "#ef4444",
         lambda: open_quality_view("Low Quality Frozen Stock", lambda q: 0 < q < 50)),
        ("❌ Unsafe / Expired", "#991b1b",
         lambda: open_quality_view("Unsafe / Expired Frozen Stock", lambda q: q == 0)),
        ("📅 View by Date", "#38bdf8",
         lambda: open_quality_view("Stock by Selected Date", lambda q: True)),
        ("📊 All Frozen Stock", "#0ea5e9",
         lambda: open_quality_view("Complete Frozen Stock", lambda q: True)),
    ]

    row = col = 0
    for text, color, cmd in buttons:
        card = tk.Frame(panel, bg="#020617",
                        highlightthickness=2,
                        highlightbackground=color,
                        width=320, height=150)
        card.grid(row=row, column=col, padx=35, pady=30)
        card.grid_propagate(False)

        tk.Label(card, text=text,
                 bg="#020617", fg="white",
                 font=("Segoe UI", 12, "bold")).pack(expand=True)

        tk.Button(card, text="Open",
                  bg="#020617", fg=color,
                  bd=0,
                  font=("Segoe UI", 11, "bold"),
                  command=cmd).pack(pady=10)

        col += 1
        if col == 3:
            col = 0
            row += 1