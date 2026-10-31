import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import random

# ================= PRODUCT GENERATOR =================
def generate_products(category):
    products = []
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    category_data = {
        "Fruits": (
            ["Apple", "Banana", "Mango", "Orange", "Papaya"],
            ["Nashik", "Ratnagiri", "Nagpur", "Malihabad"],
            90
        ),
        "Vegetables": (
            ["Tomato", "Cucumber", "Capsicum", "Brinjal", "Beans"],
            ["Pune", "Satara", "Kolhapur", "Nashik"],
            70
        ),
        "Leafy Greens & Herbs": (
            ["Spinach", "Coriander", "Mint", "Fenugreek"],
            ["Local Farm", "Vashi Mandi", "Panvel"],
            45
        ),
        "Berries & Exotics": (
            ["Strawberry", "Blueberry", "Kiwi", "Avocado"],
            ["Mahabaleshwar", "Imported", "Ooty"],
            140
        ),
        "Roots & Tubers": (
            ["Potato", "Onion", "Carrot", "Beetroot"],
            ["Agra", "Indore", "Nashik"],
            65
        ),
        "Seasonal Specials": (
            ["Pumpkin", "Sweet Corn", "Jackfruit", "Peas"],
            ["Local Market", "APMC Mandi"],
            85
        )
    }

    items, origins, base_price = category_data[category]

    for item in items:
        for i in range(1, 21):   # ~80–100 products
            mfg_offset = random.choice([-2, -1, 0, 1, 2, 3])
            mfg = today + timedelta(days=mfg_offset)

            exp_days = random.randint(7, 12)
            exp = mfg + timedelta(days=exp_days)

            products.append({
                "name": f"{item} Lot {i}",
                "category": category,
                "origin": random.choice(origins),
                "storage": "Cool & dry place",
                "mfg": mfg.strftime("%Y-%m-%d"),
                "exp": exp.strftime("%Y-%m-%d"),
                "price": base_price + random.randint(5, 30)
            })

    return products


# ================= PRODUCT LIST PAGE =================
def open_product_page(category):
    root = tk.Toplevel()
    root.title(category)
    root.state("zoomed")
    root.update_idletasks()

    # -------- BACKGROUND (DASHBOARD STYLE) --------
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

    main = tk.Frame(root, bg="#020617", padx=30, pady=20)
    main.place(relx=0.5, rely=0.52, anchor="center")

    products = generate_products(category)
    results = []

    tk.Label(main, text=category,
             font=("Segoe UI", 20, "bold"),
             bg="#020617", fg="white").pack(pady=5)

    summary = tk.Label(
        main,
        text="Total: 0 | Near Expiry: 0 | Expired: 0",
        font=("Segoe UI", 11, "bold"),
        bg="#020617", fg="#22c55e"
    )
    summary.pack(pady=5)

    tk.Label(main, text="Enter date (YYYY-MM-DD)",
             bg="#020617", fg="#94a3b8").pack()

    date_entry = tk.Entry(main)
    date_entry.pack(pady=4)

    listbox = tk.Listbox(main, width=140, height=20, font=("Segoe UI", 10))
    listbox.pack(pady=10)

    def check_expiry():
        listbox.delete(0, tk.END)
        results.clear()

        try:
            user_date = datetime.strptime(date_entry.get(), "%Y-%m-%d")
        except:
            messagebox.showerror("Error", "Invalid date format")
            return

        total = near = expired = 0

        for p in products:
            exp = datetime.strptime(p["exp"], "%Y-%m-%d")
            days_left = (exp - user_date).days

            if days_left < 0:
                status = "❌ EXPIRED"
                discount = 0
                final_price = "Not for sale"
                expired += 1
            elif days_left <= 3:
                status = "⚠ NEAR EXPIRY"
                discount = 25
                final_price = f"₹{int(p['price'] * 0.75)}"
                near += 1
            else:
                status = "✅ SAFE"
                discount = 0
                final_price = f"₹{p['price']}"

            total += 1
            results.append({
                **p,
                "days_left": days_left,
                "status": status,
                "discount": discount,
                "final_price": final_price
            })

        results.sort(key=lambda x: x["days_left"])

        for p in results:
            listbox.insert(
                tk.END,
                f"{p['name']} | EXP: {p['exp']} | {p['status']} | {p['final_price']}"
            )

        summary.config(
            text=f"Total: {total} | Near Expiry: {near} | Expired: {expired}"
        )

    def open_detail(event):
        if not listbox.curselection():
            return

        p = results[listbox.curselection()[0]]

        win = tk.Toplevel(root)
        win.title(p["name"])
        win.geometry("540x540")
        win.configure(bg="#020617")

        tk.Label(win, text=p["name"],
                 font=("Segoe UI", 16, "bold"),
                 bg="#020617", fg="white").pack(pady=15)

        details = [
            f"Category        : {p['category']}",
            f"Origin (Source): {p['origin']}",
            f"Manufacture    : {p['mfg']}",
            f"Expiry         : {p['exp']}",
            f"Days Left      : {p['days_left']}",
            f"Storage        : {p['storage']}",
            f"Status         : {p['status']}",
            f"Actual Price   : ₹{p['price']}",
            f"Discount       : {p['discount']}%",
            f"Final Price    : {p['final_price']}"
        ]

        for d in details:
            tk.Label(
                win, text=d,
                bg="#020617", fg="#e5e7eb",
                font=("Segoe UI", 11),
                anchor="w"
            ).pack(fill="x", padx=40, pady=4)

    tk.Button(
        main, text="Check Expiry",
        bg="#22c55e", fg="white",
        font=("Segoe UI", 11, "bold"),
        command=check_expiry
    ).pack(pady=6)

    listbox.bind("<Double-Button-1>", open_detail)


# ================= FRESH PRODUCE CATEGORY DASHBOARD =================
def open_fresh_produce_page():
    root = tk.Toplevel()
    root.title("Fresh Produce Categories")
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

    main = tk.Frame(root, bg="#020617", padx=30, pady=25)
    main.place(relx=0.5, rely=0.52, anchor="center")

    tk.Label(main, text="Fresh Produce",
             font=("Segoe UI", 22, "bold"),
             bg="#020617", fg="white").pack(pady=20)

    frame = tk.Frame(main, bg="#020617")
    frame.pack()

    categories = [
        ("Fruits", "#22c55e"),
        ("Vegetables", "#38bdf8"),
        ("Leafy Greens & Herbs", "#10b981"),
        ("Berries & Exotics", "#f43f5e"),
        ("Roots & Tubers", "#f59e0b"),
        ("Seasonal Specials", "#a855f7")
    ]

    row = col = 0
    for cat, color in categories:
        card = tk.Frame(
            frame,
            bg="#020617",
            highlightthickness=2,
            highlightbackground=color,
            padx=8,
            pady=8
        )
        card.grid(row=row, column=col, padx=20, pady=20)

        btn = tk.Button(
            card,
            text=cat,
            width=26,
            height=3,
            font=("Segoe UI", 12, "bold"),
            bg="#020617",
            fg="white",
            bd=0,
            command=lambda c=cat: open_product_page(c)
        )
        btn.pack()
        
        col += 1
        if col == 2:
            col = 0
            row += 1