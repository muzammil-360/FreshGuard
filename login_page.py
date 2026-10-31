import tkinter as tk
from tkinter import messagebox
import dashboard

# ---------------- LOGIN FUNCTION ----------------
users = {
    "muzammil": "muz_17",
    "tanish": "tanish_19",
    "manthan": "manthan_21"
}

def login():
    u = username_entry.get()
    p = password_entry.get()

    if u in users and users[u] == p:
        messagebox.showinfo("Welcome", f"Welcome {u}")
        root.withdraw()
        dashboard.open_dashboard(u)
    else:
        messagebox.showerror("Error", "Invalid username or password")


def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        show_btn.config(text="Hide")
    else:
        password_entry.config(show="*")
        show_btn.config(text="Show")

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Food Expiry Management System - Login")
root.state("zoomed")
root.update_idletasks()

# ---------------- BACKGROUND CANVAS ----------------
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

# ---------------- CENTER CONTENT FRAME ----------------
content_frame = tk.Frame(
    root,
    bg="#020617",
    padx=45,
    pady=35
)
content_frame.place(relx=0.5, rely=0.5, anchor="center")

# ---------------- CONTENT ----------------
tk.Label(
    content_frame,
    text="Food Expiry\nManagement System",
    font=("Segoe UI", 22, "bold"),
    fg="white",
    bg="#020617",
    justify="center"
).pack(pady=(0, 10))

tk.Label(
    content_frame,
    text="Inventory & expiry tracking system",
    font=("Segoe UI", 11),
    fg="#94a3b8",
    bg="#020617"
).pack(pady=(0, 20))

tk.Label(
    content_frame,
    text="Username",
    fg="white",
    bg="#020617",
    anchor="w"
).pack(fill="x")

username_entry = tk.Entry(
    content_frame,
    font=("Segoe UI", 11)
)
username_entry.pack(fill="x", pady=(5, 15))

tk.Label(
    content_frame,
    text="Password",
    fg="white",
    bg="#020617",
    anchor="w"
).pack(fill="x")

password_frame = tk.Frame(content_frame, bg="#020617")
password_frame.pack(fill="x", pady=(5, 20))

password_entry = tk.Entry(
    password_frame,
    font=("Segoe UI", 11),
    show="*"
)
password_entry.pack(side="left", fill="x", expand=True)

show_btn = tk.Button(
    password_frame,
    text="Show",
    command=toggle_password
)
show_btn.pack(side="right", padx=5)

tk.Button(
    content_frame,
    text="LOGIN",
    font=("Segoe UI", 12, "bold"),
    bg="#22c55e",
    fg="white",
    relief="flat",
    command=login
).pack(fill="x", pady=(10, 0))

root.mainloop()