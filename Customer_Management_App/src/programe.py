import tkinter as tk
from tkinter import ttk, messagebox
import re
import requests
import threading
from customer import Customer
from customer_list import CustomerList
from account_manager import AccountManager

class CustomerApp:
    def __init__(self, root, user_role="regular"):
        self.root = root
        self.user_role = user_role
        self.root.title("Quản Lý Khách Hàng")
        self.root.geometry("1200x600")
        self.customer_list = CustomerList("customers.json")

        self.validate_phone = lambda sdt: re.match(r"^0\d{9}$", sdt) is not None
        self.validate_email = lambda email: re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None
        self.validate_customer_id = lambda ma_kh: re.match(r"^KH\d{3}$", ma_kh) is not None

        self.create_widgets()

    def create_widgets(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Mã KH:").grid(row=0, column=0, padx=5, pady=5)
        self.ma_kh_entry = tk.Entry(input_frame)
        self.ma_kh_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Tên:").grid(row=1, column=0, padx=5, pady=5)
        self.ten_kh_entry = tk.Entry(input_frame)
        self.ten_kh_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="SĐT:").grid(row=2, column=0, padx=5, pady=5)
        self.sdt_entry = tk.Entry(input_frame)
        self.sdt_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(input_frame)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Địa chỉ:").grid(row=4, column=0, padx=5, pady=5)
        self.dia_chi_entry = tk.Entry(input_frame)
        self.dia_chi_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Giới tính:").grid(row=5, column=0, padx=5, pady=5)
        self.gioi_tinh_var = tk.StringVar(value="Nam")
        self.gioi_tinh_combo = ttk.Combobox(input_frame, textvariable=self.gioi_tinh_var, values=["Nam", "Nữ", "Khác"], state="readonly")
        self.gioi_tinh_combo.grid(row=5, column=1, padx=5, pady=5)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Thêm", command=self.add_customer).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Sửa", command=self.update_customer).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Xóa", command=self.delete_customer).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Làm mới", command=self.display_customers).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Crawl Dữ Liệu", command=self.crawl_data).pack(side=tk.LEFT, padx=5)
        if self.user_role == "admin":
            tk.Button(button_frame, text="Quản lý tài khoản", command=self.open_account_manager).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Thoát", command=self.root.destroy).pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("Mã KH", "Tên", "SĐT", "Email", "Địa chỉ", "Giới tính"), show="headings")
        self.tree.heading("Mã KH", text="Mã KH")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("SĐT", text="SĐT")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Địa chỉ", text="Địa chỉ")
        self.tree.heading("Giới tính", text="Giới tính")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_label = tk.Label(self.root, text="", fg="red")
        self.message_label.pack(pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.display_customers()

    def open_account_manager(self):
        account_window = tk.Toplevel(self.root)
        AccountManager(account_window)

    def clear_entries(self):
        self.ma_kh_entry.delete(0, tk.END)
        self.ten_kh_entry.delete(0, tk.END)
        self.sdt_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.dia_chi_entry.delete(0, tk.END)
        self.gioi_tinh_var.set("Nam")
        self.message_label.config(text="")

    def add_customer(self):
        ma_kh = self.ma_kh_entry.get()
        ten_kh = self.ten_kh_entry.get()
        sdt = self.sdt_entry.get()
        email = self.email_entry.get()
        dia_chi = self.dia_chi_entry.get()
        gioi_tinh = self.gioi_tinh_var.get()

        if not self.validate_customer_id(ma_kh):
            self.message_label.config(text="Mã khách hàng không hợp lệ!")
            return
        if self.customer_list.customer_exists(ma_kh):
            self.message_label.config(text="Mã khách hàng đã tồn tại!")
            return
        if not ten_kh:
            self.message_label.config(text="Vui lòng nhập tên khách hàng!")
            return
        if not self.validate_phone(sdt):
            self.message_label.config(text="Số điện thoại không hợp lệ!")
            return
        if not self.validate_email(email):
            self.message_label.config(text="Email không hợp lệ!")
            return
        if not dia_chi:
            self.message_label.config(text="Vui lòng nhập địa chỉ!")
            return

        try:
            customer = Customer(ma_kh, ten_kh, sdt, email, dia_chi, gioi_tinh)
            self.customer_list.add_customer(customer)
            self.message_label.config(text="Thêm khách hàng thành công!", fg="green")
            self.clear_entries()
            self.display_customers()
        except Exception as e:
            self.message_label.config(text=f"Lỗi: {e}")

    def update_customer(self):
        ma_kh = self.ma_kh_entry.get()
        ten_kh = self.ten_kh_entry.get()
        sdt = self.sdt_entry.get()
        email = self.email_entry.get()
        dia_chi = self.dia_chi_entry.get()
        gioi_tinh = self.gioi_tinh_var.get()

        if not self.validate_customer_id(ma_kh):
            self.message_label.config(text="Mã khách hàng không hợp lệ!")
            return
        if not self.customer_list.customer_exists(ma_kh):
            self.message_label.config(text="Mã khách hàng không tồn tại!")
            return

        update_data = {}
        if ten_kh: update_data["ten_kh"] = ten_kh
        if sdt:
            if not self.validate_phone(sdt):
                self.message_label.config(text="Số điện thoại không hợp lệ!")
                return
            update_data["sdt"] = sdt
        if email:
            if not self.validate_email(email):
                self.message_label.config(text="Email không hợp lệ!")
                return
            update_data["email"] = email
        if dia_chi: update_data["dia_chi"] = dia_chi
        if gioi_tinh: update_data["gioi_tinh"] = gioi_tinh

        if update_data:
            try:
                self.customer_list.update_customer(ma_kh, **update_data)
                self.message_label.config(text="Cập nhật khách hàng thành công!", fg="green")
                self.clear_entries()
                self.display_customers()
            except Exception as e:
                self.message_label.config(text=f"Lỗi: {e}")
        else:
            self.message_label.config(text="Không có thông tin nào được cập nhật.")

    def delete_customer(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.message_label.config(text="Vui lòng chọn khách hàng để xóa!")
            return

        ma_kh = self.tree.item(selected_item)["values"][0]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa khách hàng {ma_kh}?"):
            try:
                self.customer_list.remove_customer(ma_kh)
                self.message_label.config(text="Xóa khách hàng thành công!", fg="green")
                self.clear_entries()
                self.display_customers()
            except Exception as e:
                self.message_label.config(text=f"Lỗi: {e}")

    def display_customers(self):
        self.customer_list.load_from_json()
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            if not self.customer_list.customers:
                self.message_label.config(text="Danh sách khách hàng rỗng!", fg="red")
                return
            for customer in self.customer_list.customers:
                self.tree.insert("", tk.END, text=customer.sdt, values=(
                    customer.ma_kh,
                    customer.ten_kh,
                    customer.sdt,
                    customer.email,
                    customer.dia_chi,
                    customer.gioi_tinh
                ))
        except Exception as e:
            self.message_label.config(text=f"Lỗi khi hiển thị: {e}", fg="red")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)["values"]
            sdt = self.tree.item(selected_item)["text"]
            
            if not self.validate_phone(sdt):
                self.message_label.config(text="Số điện thoại từ Treeview không hợp lệ!", fg="red")
                sdt = ""
            self.ma_kh_entry.delete(0, tk.END)
            self.ma_kh_entry.insert(0, values[0])
            self.ten_kh_entry.delete(0, tk.END)
            self.ten_kh_entry.insert(0, values[1])
            self.sdt_entry.delete(0, tk.END)
            self.sdt_entry.insert(0, sdt)
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, values[3])
            self.dia_chi_entry.delete(0, tk.END)
            self.dia_chi_entry.insert(0, values[4])
            self.gioi_tinh_var.set(values[5])

    def crawl_data(self):
        if self.user_role != "admin":
            messagebox.showerror("Lỗi", "Chỉ admin mới có quyền crawl dữ liệu!")
            return

        def fetch_and_process_data():
            try:
                self.message_label.config(text="Đang crawl dữ liệu, vui lòng đợi...", fg="blue")
                self.root.config(cursor="wait")
                self.root.update()

                with requests.Session() as session:
                    response = session.get("https://dummyjson.com/users?limit=3", timeout=5)
                    response.raise_for_status()
                    data = response.json()

                users = data.get("users", [])


                for index, user in enumerate(users, start=len(self.customer_list.customers) + 1):
                    ma_kh = f"KH{index:03d}"
                    ten_kh = f"{user.get('firstName', 'Unknown')} {user.get('lastName', '')}".strip()
                    sdt_raw = re.sub(r'\D', '', user.get("phone", ""))
                    sdt = f"0{sdt_raw[-9:]}" if len(sdt_raw) >= 9 else f"010000{index:04d}"
                    email = user.get("email", f"user{index}@example.com")
                    address = user.get("address", {})
                    dia_chi = f"{address.get('address', 'Unknown')}, {address.get('city', 'Unknown')}"
                    gioi_tinh = "Nam" if user.get("gender", "").lower() == "male" else "Nữ"

                    if not self.validate_customer_id(ma_kh):
                        continue
                    if self.customer_list.customer_exists(ma_kh):
                        continue
                    if not self.validate_phone(sdt):
                        continue
                    if not self.validate_email(email):
                        continue
                    if not dia_chi:
                        continue

                    customer = Customer(ma_kh, ten_kh, sdt, email, dia_chi, gioi_tinh)
                    self.customer_list.add_customer(customer)

               
                self.root.after(0, lambda: [
                    self.message_label.config(text="Crawl dữ liệu và lưu thành công!", fg="green"),
                    self.display_customers(),
                    self.root.config(cursor="")
                ])

            except requests.exceptions.RequestException as e:
                self.root.after(0, lambda e=e: [
                    self.message_label.config(text=f"Lỗi khi crawl dữ liệu: {e}", fg="red"),
                    self.root.config(cursor="")
                ])
            except Exception as e:
                self.root.after(0, lambda e=e: [
                    self.message_label.config(text=f"Lỗi: {e}", fg="red"),
                    self.root.config(cursor="")
                ])

        thread = threading.Thread(target=fetch_and_process_data)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerApp(root, user_role="admin")
    root.mainloop()