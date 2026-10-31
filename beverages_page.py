import tkinter as tk
from datetime import datetime, timedelta
import random

# ================= BASE DATE =================
BASE_DATE = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

# ================= BEVERAGE CONFIG =================
BEVERAGE_TYPES = {
    "Soft Drink": {"shelf": 180, "sugar": "High", "caffeine": "Sometimes"},
    "Fruit Juice": {"shelf": 90, "sugar": "Medium", "caffeine": "No"},
    "Energy Drink": {"shelf": 365, "sugar": "High", "caffeine": "Yes"},
    "Milk-based Drink": {"shelf": 30, "sugar": "Medium", "caffeine": "No"},
    "Packaged Water": {"shelf": 365, "sugar": "None", "caffeine": "No"},
    "Tea / Coffee Drink": {"shelf": 120, "sugar": "Low", "caffeine": "Yes"}
}

PRICES = {
    "Soft Drink": (40, 90),
    "Fruit Juice": (60, 120),
    "Energy Drink": (80, 180),
    "Milk-based Drink": (50, 100),
    "Packaged Water": (20, 50),
    "Tea / Coffee Drink": (70, 150)
}

# ================= PRODUCT GENERATOR =================
def generate_beverages(count=180):
    products = []
    for i in range(count):
        btype = random.choice(list(BEVERAGE_TYPES.keys()))
        shelf = BEVERAGE_TYPES[btype]["shelf"]

        mfg_offset = random.randint(0, shelf + 20)
        mfg = BASE_DATE - timedelta(days=mfg_offset)
        exp = mfg + timedelta(days=shelf)

        batch = f"BATCH-{random.randint(100,999)}"
        price = random.randint(*PRICES[btype])

        products.append({
            "name": f"{btype} Item {i+1}",
            "type": btype,
            "batch": batch,
            "mfg": mfg,
            "exp": exp,
            "price": price
        })
    return products

# ================= STATUS LOGIC =================
def get_timeline_status(expiry, view_date):
    days_left = (expiry - view_date).days
    if days_left < 0:
        return "EXPIRED"
    elif days_left <= 5:
        return "NEAR EXPIRY"
    elif days_left <= 20:
        return "WARNING"
    else:
        return "SAFE"

# ================= DETAIL PAGE =================
def open_detail(item, status, view_date):
    win = tk.Toplevel()
    win.title(item["name"])
    win.geometry("540x520")
    win.configure(bg="#020617")

    info = BEVERAGE_TYPES[item["type"]]
    days_left = (item["exp"] - view_date).days

    tk.Label(win, text=item["name"],
             font=("Segoe UI", 16, "bold"),
             bg="#020617", fg="white").pack(pady=12)

    details = [
        f"Type               : {item['type']}",
        f"Batch No           : {item['batch']}",
        f"Manufactured Date  : {item['mfg'].date()}",
        f"Expiry Date        : {item['exp'].date()}",
        f"Days Remaining     : {days_left}",
        f"Status             : {status}",
        "",
        "Drink Information:",
        f"Sugar Content      : {info['sugar']}",
        f"Caffeine           : {info['caffeine']}",
        "",
        "System Suggestion:",
        "Apply discount and push sales"
        if status in ["WARNING", "NEAR EXPIRY"]
        else "Safe for normal sale"
    ]

    for d in details:
        tk.Label(win, text=d,
                 font=("Segoe UI", 11),
                 bg="#020617", fg="#e5e7eb",
                 anchor="w").pack(fill="x", padx=30, pady=4)

# ================= MAIN PAGE =================
def open_beverages_page():
    root = tk.Toplevel()
    root.title("Beverages – Expiry Timeline Monitor")
    root.state("zoomed")

    canvas_bg = tk.Canvas(root, highlightthickness=0)
    canvas_bg.pack(fill="both", expand=True)

    canvas_bg.create_rectangle(
        0, 0,
        root.winfo_screenwidth(),
        root.winfo_screenheight(),
        fill="#020617", outline=""
    )
    canvas_bg.create_rectangle(
        0,
        root.winfo_screenheight() * 0.55,
        root.winfo_screenwidth(),
        root.winfo_screenheight(),
        fill="#0f172a", outline=""
    )

    main = tk.Frame(root, bg="#020617")
    main.place(relx=0.5, rely=0.48, anchor="center")

    tk.Label(main, text="Beverages – Expiry Timeline",
             font=("Segoe UI", 24, "bold"),
             bg="#020617", fg="white").pack()

    tk.Label(main,
             text="Batch-based beverage monitoring with dynamic timeline",
             font=("Segoe UI", 11),
             bg="#020617", fg="#94a3b8").pack(pady=10)

    # ---------- DATE ----------
    date_var = tk.StringVar(value=BASE_DATE.strftime("%Y-%m-%d"))
    tk.Entry(main, textvariable=date_var, width=15,
             justify="center").pack(pady=4)

    products = generate_beverages()

    # ---------- FILTER BUTTONS ----------
    filter_frame = tk.Frame(main, bg="#020617")
    filter_frame.pack(pady=8)

    selected_type = tk.StringVar(value="ALL")

    def set_filter(t):
        selected_type.set(t)
        render()

    for t in ["ALL"] + list(BEVERAGE_TYPES.keys()):
        tk.Button(
            filter_frame,
            text=t,
            bg="#020617",
            fg="#38bdf8",
            bd=1,
            highlightbackground="#38bdf8",
            padx=10,
            pady=4,
            command=lambda x=t: set_filter(x)
        ).pack(side="left", padx=6)

    # ---------- APPLY DATE ----------
    tk.Button(
        main, text="Apply Date",
        bg="#22c55e", fg="white",
        font=("Segoe UI", 11, "bold"),
        bd=0, padx=20, pady=6,
        command=lambda: render()
    ).pack(pady=8)

    # ---------- TIMELINE ----------
    timeline = tk.Frame(main, bg="#020617")
    timeline.pack(pady=15)

    columns = {
        "SAFE": ("🟢 SAFE", "#22c55e"),
        "WARNING": ("🟡 WARNING", "#facc15"),
        "NEAR EXPIRY": ("🟠 NEAR EXPIRY", "#fb923c"),
        "EXPIRED": ("🔴 EXPIRED", "#ef4444")
    }

    frames = {}
    scroll_canvases = []

    for key, (label, color) in columns.items():
        outer = tk.Frame(
            timeline,
            bg="#020617",
            highlightthickness=2,
            highlightbackground=color,
            width=260,
            height=420
        )
        outer.pack(side="left", padx=12)
        outer.pack_propagate(False)

        tk.Label(outer, text=label,
                 bg="#020617", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=6)

        canvas = tk.Canvas(outer, bg="#020617", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        scroll_canvases.append(canvas)

        inner = tk.Frame(canvas, bg="#020617")
        window = canvas.create_window((0, 0), window=inner, anchor="nw")

        def on_configure(e, c=canvas, w=window):
            c.configure(scrollregion=c.bbox("all"))
            c.itemconfig(w, width=260)

        inner.bind("<Configure>", on_configure)

        frames[key] = inner

    # ---------- GLOBAL TOUCHPAD SCROLL (FINAL FIX) ----------
    def global_scroll(event):
        for c in scroll_canvases:
            c.yview_scroll(int(-1 * (event.delta / 120)), "units")

    root.bind_all("<MouseWheel>", global_scroll)

    # ---------- RENDER ----------
    def render():
        view_date = datetime.strptime(date_var.get(), "%Y-%m-%d")

        for f in frames.values():
            for w in f.winfo_children():
                w.destroy()

        for item in products:
            if selected_type.get() != "ALL" and item["type"] != selected_type.get():
                continue

            status = get_timeline_status(item["exp"], view_date)
            frame = frames[status]

            tk.Button(
                frame,
                text=f"{item['name']}\n{item['batch']}",
                bg="#020617",
                fg="white",
                bd=0,
                wraplength=220,
                justify="center",
                command=lambda x=item, s=status:
                open_detail(x, s, view_date)
            ).pack(pady=4)

    render()