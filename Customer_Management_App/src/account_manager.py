
import tkinter as tk
from tkinter import ttk, messagebox
import json

class AccountManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản Lý Tài Khoản")
        self.root.geometry("600x400")
        self.accounts_file = "account_db.json"
        self.accounts = self.load_accounts()

        self.create_widgets()

    def load_accounts(self):
        try:
            with open(self.accounts_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            default_accounts = [
                {"username": "admin", "password": "admin123", "role": "admin"},
                {"username": "user1", "password": "user123", "role": "regular"}
            ]
            with open(self.accounts_file, 'w', encoding='utf-8') as file:
                json.dump(default_accounts, file, ensure_ascii=False, indent=4)
            return default_accounts
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi đọc file tài khoản: {e}")
            return []

    def save_accounts(self):
        try:
            with open(self.accounts_file, 'w', encoding='utf-8') as file:
                json.dump(self.accounts, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu file tài khoản: {e}")

    def create_widgets(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(input_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(input_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Role:").grid(row=2, column=0, padx=5, pady=5)
        self.role_var = tk.StringVar(value="regular")
        self.role_combo = ttk.Combobox(input_frame, textvariable=self.role_var, values=["admin", "regular"], state="readonly")
        self.role_combo.grid(row=2, column=1, padx=5, pady=5)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Thêm", command=self.add_account).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Sửa", command=self.update_account).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Xóa", command=self.delete_account).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Hiển thị", command=self.display_accounts).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Thoát", command=self.root.destroy).pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("Username", "Password", "Role"), show="headings")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        self.tree.heading("Role", text="Role")
        self.tree.column("Username", width=150)
        self.tree.column("Password", width=150)
        self.tree.column("Role", width=100)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        self.message_label = tk.Label(self.root, text="", fg="red")
        self.message_label.pack(pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.display_accounts()

    def clear_entries(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.role_var.set("regular")
        self.message_label.config(text="")

    def add_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()

        if not username or not password:
            self.message_label.config(text="Vui lòng nhập username và password!")
            return
        if any(account["username"] == username for account in self.accounts):
            self.message_label.config(text="Username đã tồn tại!")
            return

        try:
            self.accounts.append({"username": username, "password": password, "role": role})
            self.save_accounts()
            self.message_label.config(text="Thêm tài khoản thành công!", fg="green")
            self.clear_entries()
            self.display_accounts()
        except Exception as e:
            self.message_label.config(text=f"Lỗi: {e}")

    def update_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()

        if not username:
            self.message_label.config(text="Vui lòng nhập username!")
            return

        for account in self.accounts:
            if account["username"] == username:
                if password:
                    account["password"] = password
                if role:
                    account["role"] = role
                try:
                    self.save_accounts()
                    self.message_label.config(text="Cập nhật tài khoản thành công!", fg="green")
                    self.clear_entries()
                    self.display_accounts()
                except Exception as e:
                    self.message_label.config(text=f"Lỗi: {e}")
                return
        self.message_label.config(text="Username không tồn tại!")

    def delete_account(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.message_label.config(text="Vui lòng chọn tài khoản để xóa!")
            return

        username = self.tree.item(selected_item)["values"][0]
        if username == "admin":
            self.message_label.config(text="Không thể xóa tài khoản admin!", fg="red")
            return
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa tài khoản {username}?"):
            try:
                self.accounts = [account for account in self.accounts if account["username"] != username]
                self.save_accounts()
                self.message_label.config(text="Xóa tài khoản thành công!", fg="green")
                self.clear_entries()
                self.display_accounts()
            except Exception as e:
                self.message_label.config(text=f"Lỗi: {e}")

    def display_accounts(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            for account in self.accounts:
                self.tree.insert("", tk.END, values=(
                    account["username"],
                    account["password"],  # Hiển thị mật khẩu dạng plain text
                    account["role"]
                ))
            self.message_label.config(text="Danh sách tài khoản đã được làm mới!", fg="green")
        except Exception as e:
            self.message_label.config(text=f"Lỗi khi hiển thị: {e}", fg="red")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)["values"]
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, values[0])
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, values[1])
            self.role_var.set(values[2])
