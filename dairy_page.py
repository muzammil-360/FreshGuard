import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# ---------- GENERATE DAIRY PRODUCTS ----------
def generate_dairy_products():
    base_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    milk_types = ["Full Cream", "Toned", "Skimmed"]
    brands = ["Amul", "Mother Dairy", "Britannia", "Nestle"]
    sizes = ["500ml", "1L", "2L"]

    products = []

    for brand in brands:
        for mtype in milk_types:
            for size in sizes:
                products.append({
                    "name": f"{brand} Milk ({mtype}, {size})",
                    "category": "Dairy",
                    "storage": "Keep refrigerated at 4°C",
                    "mfg": base_date.strftime("%Y-%m-%d"),
                    "exp": (base_date + timedelta(days=7)).strftime("%Y-%m-%d"),
                    "price": 90
                })

    cheese_types = ["Cheddar", "Mozzarella", "Processed", "Slice"]
    for brand in brands:
        for c in cheese_types:
            products.append({
                "name": f"{brand} {c} Cheese",
                "category": "Dairy",
                "storage": "Refrigerated storage required",
                "mfg": base_date.strftime("%Y-%m-%d"),
                "exp": (base_date + timedelta(days=30)).strftime("%Y-%m-%d"),
                "price": 180
            })

    flavors = ["Vanilla", "Chocolate", "Strawberry", "Mango"]
    packs = ["Cup", "Cone", "Family Pack"]

    for brand in brands:
        for f in flavors:
            for p in packs:
                products.append({
                    "name": f"{brand} Ice Cream ({f}, {p})",
                    "category": "Frozen Dairy",
                    "storage": "Store below -18°C",
                    "mfg": base_date.strftime("%Y-%m-%d"),
                    "exp": (base_date + timedelta(days=45)).strftime("%Y-%m-%d"),
                    "price": 120
                })

    return products


# ================== MAIN DAIRY PAGE ==================
def open_dairy_page():
    root = tk.Toplevel()
    root.title("Dairy Products - Expiry Management")
    root.state("zoomed")
    root.configure(bg="#020617")

    dairy_products = generate_dairy_products()
    filtered_results = []

    # ---------- HEADER ----------
    tk.Label(root, text="Dairy Products",
             font=("Segoe UI", 20, "bold"),
             bg="#020617", fg="white").pack(pady=5)

    # ---------- SUMMARY BAR ----------
    summary_label = tk.Label(
        root,
        text="Total: 0 | Near Expiry: 0 | Expired: 0",
        font=("Segoe UI", 11, "bold"),
        bg="#020617",
        fg="#22c55e"
    )
    summary_label.pack(pady=5)

    # ---------- DATE INPUT ----------
    tk.Label(root, text="Enter date (YYYY-MM-DD)",
             font=("Segoe UI", 11),
             bg="#020617", fg="#94a3b8").pack()

    date_entry = tk.Entry(root, font=("Segoe UI", 11))
    date_entry.pack(pady=4)

    # ---------- SEARCH BOX ----------
    tk.Label(root, text="Search product",
             font=("Segoe UI", 10),
             bg="#020617", fg="#94a3b8").pack()

    search_entry = tk.Entry(root, font=("Segoe UI", 11))
    search_entry.pack(pady=4)

    # ---------- LISTBOX ----------
    listbox = tk.Listbox(
        root,
        width=150,
        height=22,
        font=("Segoe UI", 10)
    )
    listbox.pack(pady=10)

    # ---------- EXPIRY LOGIC ----------
    def check_expiry():
        listbox.delete(0, tk.END)
        filtered_results.clear()

        try:
            user_date = datetime.strptime(date_entry.get(), "%Y-%m-%d")
        except:
            messagebox.showerror("Error", "Date format must be YYYY-MM-DD")
            return

        total = near = expired = 0

        for item in dairy_products:
            exp_date = datetime.strptime(item["exp"], "%Y-%m-%d")
            days_left = (exp_date - user_date).days

            if days_left < 0:
                status = "❌ EXPIRED"
                discount = 0
                final_price = "Not for sale"
                expired += 1
            elif days_left <= 3:
                status = "⚠ NEAR EXPIRY"
                discount = 30
                final_price = f"₹{int(item['price'] * 0.7)}"
                near += 1
            else:
                status = "✅ SAFE"
                discount = 0
                final_price = f"₹{item['price']}"

            total += 1

            filtered_results.append({
                **item,
                "days_left": days_left,
                "status": status,
                "discount": discount,
                "final_price": final_price
            })

        filtered_results.sort(key=lambda x: x["days_left"])

        for p in filtered_results:
            listbox.insert(
                tk.END,
                f"{p['name']} | Exp: {p['exp']} | {p['status']} | Price: {p['final_price']}"
            )

        summary_label.config(
            text=f"Total: {total} | Near Expiry: {near} | Expired: {expired}"
        )

    # ---------- SEARCH FILTER ----------
    def filter_products(event):
        query = search_entry.get().lower()
        listbox.delete(0, tk.END)

        for p in filtered_results:
            if query in p["name"].lower():
                listbox.insert(
                    tk.END,
                    f"{p['name']} | Exp: {p['exp']} | {p['status']} | Price: {p['final_price']}"
                )

    search_entry.bind("<KeyRelease>", filter_products)

    # ---------- PRODUCT DETAIL PAGE ----------
    def open_product_detail(event):
        if not listbox.curselection():
            return

        p = filtered_results[listbox.curselection()[0]]

        win = tk.Toplevel(root)
        win.title(p["name"])
        win.geometry("520x520")
        win.configure(bg="#020617")

        tk.Label(win, text=p["name"],
                 font=("Segoe UI", 16, "bold"),
                 bg="#020617", fg="white").pack(pady=15)

        details = [
            f"Category           : {p['category']}",
            f"Manufacture Date   : {p['mfg']}",
            f"Expiry Date        : {p['exp']}",
            f"Days Remaining     : {p['days_left']}",
            f"Storage Condition  : {p['storage']}",
            f"Status             : {p['status']}",
            f"Actual Price       : ₹{p['price']}",
            f"Discount Applied   : {p['discount']}%",
            f"Final Price        : {p['final_price']}"
        ]

        for d in details:
            tk.Label(win, text=d,
                     font=("Segoe UI", 11),
                     bg="#020617", fg="#e5e7eb",
                     anchor="w").pack(fill="x", padx=40, pady=4)

    # ---------- BUTTON ----------
    tk.Button(
        root, text="Check Expiry",
        font=("Segoe UI", 11, "bold"),
        bg="#22c55e", fg="white",
        command=check_expiry
    ).pack(pady=6)

    listbox.bind("<Double-Button-1>", open_product_detail)