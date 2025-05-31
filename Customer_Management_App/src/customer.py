
class Customer:
    def __init__(self, ma_kh, ten_kh, sdt, email, dia_chi, gioi_tinh):
        self.ma_kh = ma_kh
        self.ten_kh = ten_kh
        self.sdt = sdt
        self.email = email
        self.dia_chi = dia_chi
        self.gioi_tinh = gioi_tinh

    def to_dict(self):
        return {
            "ma_kh": self.ma_kh,
            "ten_kh": self.ten_kh,
            "sdt": self.sdt,
            "email": self.email,
            "dia_chi": self.dia_chi,
            "gioi_tinh": self.gioi_tinh
        }

    def __str__(self):
        return f"Ma KH: {self.ma_kh}, Ten: {self.ten_kh}, SDT: {self.sdt}, Email: {self.email}, Dia chi: {self.dia_chi}, Gioi tinh: {self.gioi_tinh}"