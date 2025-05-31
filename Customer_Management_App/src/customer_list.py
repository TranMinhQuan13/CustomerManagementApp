import json
from customer import Customer

class CustomerList:
    def __init__(self, json_file="customers.json"):
        self.json_file = json_file
        self.customers = []
        self.load_from_json()

    def load_from_json(self):
        try:
            with open(self.json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.customers = [
                    Customer(
                        item["ma_kh"],
                        item["ten_kh"],
                        item["sdt"],
                        item["email"],
                        item["dia_chi"],
                        item["gioi_tinh"]
                    ) for item in data
                ]
        except FileNotFoundError:
            print(f"File {self.json_file} không tồn tại, tạo danh sách rỗng.")
        except Exception as e:
            print(f"Lỗi khi đọc file JSON: {e}")

    def save_to_json(self):
        try:
            with open(self.json_file, 'w', encoding='utf-8') as file:
                json.dump([customer.to_dict() for customer in self.customers], file, ensure_ascii=False, indent=4)
            print("Lưu file JSON thành công.")
        except Exception as e:
            print(f"Lỗi khi lưu file JSON: {e}")

    def add_customer(self, customer):
        if any(c.ma_kh == customer.ma_kh for c in self.customers):
            print(f"Khách hàng với mã {customer.ma_kh} đã tồn tại.")
            return False
        self.customers.append(customer)
        self.save_to_json()
        print(f"Đã thêm khách hàng {customer.ten_kh}.")
        return True

    def remove_customer(self, ma_kh):
        for customer in self.customers:
            if customer.ma_kh == ma_kh:
                self.customers.remove(customer)
                self.save_to_json()
                print(f"Đã xóa khách hàng với mã {ma_kh}.")
                return True
        print(f"Không tìm thấy khách hàng với mã {ma_kh}.")
        return False

    def update_customer(self, ma_kh, **kwargs):
        for customer in self.customers:
            if customer.ma_kh == ma_kh:
                for key, value in kwargs.items():
                    if hasattr(customer, key):
                        setattr(customer, key, value)
                    else:
                        print(f"Thuộc tính {key} không tồn tại.")
                self.save_to_json()
                print(f"Đã cập nhật khách hàng với mã {ma_kh}.")
                return True
        print(f"Không tìm thấy khách hàng với mã {ma_kh}.")
        return False

    def display_customers(self):
        if not self.customers:
            print("Danh sách khách hàng rỗng.")
        else:
            for customer in self.customers:
                print(customer)
    def customer_exists(self, ma_kh):
        return any(customer.ma_kh == ma_kh for customer in self.customers)

