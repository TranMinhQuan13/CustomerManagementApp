import tkinter as tk
from tkinter import messagebox
import json
from programe import CustomerApp
from register import RegisterApp

class LoginApp:
    def __init__(self, root):
        self.accounts_file = "account_db.json"

        self.root = root
        self.root.title("Đăng Nhập Tài Khoản")
        self.root.geometry("350x300")

        self.label_title = tk.Label(root, text="Đăng Nhập", font=("Arial", 16, "bold"))
        self.label_title.pack(pady=20)

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.username = tk.Label(self.frame, text="Tên đăng nhập:", font=("Arial", 10))
        self.username.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.username_inp = tk.Entry(self.frame, width=25)
        self.username_inp.grid(row=0, column=1, padx=10, pady=5)

        self.password = tk.Label(self.frame, text="Mật Khẩu:", font=("Arial", 10))
        self.password.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.password_inp = tk.Entry(self.frame, width=25, show="*")
        self.password_inp.grid(row=1, column=1, padx=10, pady=5)

        self.button_login = tk.Button(root, text="Đăng Nhập", font=("Arial", 10), command=self.login)
        self.button_login.pack(pady=20)
        self.button_register = tk.Button(root, text="Đăng Ký", font=("Arial", 10), command=self.open_register)
        self.button_register.pack(pady=5)

    def open_register(self):
        register_window = tk.Toplevel(self.root)
        RegisterApp(register_window)

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

    def login(self):
        username = self.username_inp.get()
        password = self.password_inp.get()

        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
            return

        accounts = self.load_accounts()
        for account in accounts:
            if account["username"] == username and account["password"] == password:
                try:
                    messagebox.showinfo("Thông báo", "Đăng nhập thành công")
                    self.root.destroy()
                    root = tk.Tk()
                    app = CustomerApp(root, user_role=account["role"])
                    root.mainloop()
                    return
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Lỗi khi mở ứng dụng: {e}")
                    return
        messagebox.showerror("Lỗi", "Username hoặc password không đúng!")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()