
import tkinter as tk
from tkinter import ttk, messagebox
import json

class RegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng Ký Tài Khoản")
        self.root.geometry("350x350")

        self.label_title = tk.Label(root, text="Đăng Ký", font=("Arial", 16, "bold"))
        self.label_title.pack(pady=20)

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.label_username = tk.Label(self.frame, text="Tên Đăng Nhập:", font=("Arial", 10))
        self.label_username.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_username = tk.Entry(self.frame, width=25)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)

        self.label_password = tk.Label(self.frame, text="Mật Khẩu:", font=("Arial", 10))
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_password = tk.Entry(self.frame, width=25, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)

        self.label_confirm_password = tk.Label(self.frame, text="Nhập Lại Mật Khẩu:", font=("Arial", 10))
        self.label_confirm_password.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_confirm_password = tk.Entry(self.frame, width=25, show="*")
        self.entry_confirm_password.grid(row=2, column=1, padx=10, pady=5)

        self.label_role = tk.Label(self.frame, text="Vai Trò:", font=("Arial", 10))
        self.label_role.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.role_var = tk.StringVar(value="regular")
        self.role_combo = ttk.Combobox(self.frame, textvariable=self.role_var, values=["admin", "regular"], state="readonly", width=22)
        self.role_combo.grid(row=3, column=1, padx=10, pady=5)

        self.button_register = tk.Button(root, text="Đăng Ký", font=("Arial", 10), command=self.register)
        self.button_register.pack(pady=20)
        self.button_out = tk.Button(root, text="Hủy", font=("Arial", 10), command=root.destroy)
        self.button_out.pack()

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()
        role = self.role_var.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu không khớp!")
            return
        if len(password) < 6:
            messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
            return

        try:
            try:
                with open("account_db.json", "r") as file:
                    users = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                users = []

            if any(user["username"] == username for user in users):
                messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!")
                return

            users.append({"username": username, "password": password, "role": role})
            with open("account_db.json", "w") as file:
                json.dump(users, file, ensure_ascii=False, indent=4)
            messagebox.showinfo("Thành Công", "Đăng ký thành công!")
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.entry_confirm_password.delete(0, tk.END)
            self.role_var.set("regular")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã có lỗi xảy ra: {str(e)}")
if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterApp(root)
    root.mainloop()