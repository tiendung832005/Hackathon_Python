from tabulate import tabulate

danh_sach_hoa_don = []
FILE_DATA = "hoa_don_data.json"
DON_GIA = 3000


def tinh_toan_hoa_don(so_cu, so_moi):
    tieu_thu = so_moi - so_cu
    thanh_tien = tieu_thu * DON_GIA

    if tieu_thu < 100:
        muc_ap_dung = "Mức 1"
    elif tieu_thu < 200:
        muc_ap_dung = "Mức 2"
    else:
        muc_ap_dung = "Mức 3 (Cao)"
    return tieu_thu, thanh_tien, muc_ap_dung


def tim_hoa_don_theo_ma(ma_cong_to):
    for i, hoa_don in enumerate(danh_sach_hoa_don):
        if hoa_don['ma_cong_to'] == ma_cong_to:
            return i, hoa_don
    return -1, None

# 1. Hiển thị danh sách hóa đơn


def hien_thi_danh_sach():
    """1. Hiển thị danh sách hóa đơn"""
    if not danh_sach_hoa_don:
        print("Chưa có hóa đơn nào trong danh sách.")
        return

    headers = ["STT", "Mã công tơ", "Tên chủ hộ", "Số cũ",
               "Số mới", "Tiêu thụ", "Thành tiền", "Mức áp dụng"]
    table_data = []

    for i, hoa_don in enumerate(danh_sach_hoa_don, 1):
        row = [
            i,
            hoa_don['ma_cong_to'],
            hoa_don['ten_chu_ho'],
            hoa_don['so_dien_tu'],
            hoa_don['so_dien_moi'],
            hoa_don['tieu_thu'],
            f"{hoa_don['thanh_tien']:,} VNĐ",
            hoa_don['muc_ap_dung']
        ]
        table_data.append(row)

    print("\n" + "="*100)
    print("DANH SÁCH HÓA ĐƠN TIỀN ĐIỆN")
    print("="*100)
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print(f"\nTổng số hóa đơn: {len(danh_sach_hoa_don)}")


# 2. Thêm chỉ số điện
def them_chi_so_dien():
    """2. Thêm chỉ số điện"""
    print("\n--- THÊM CHỈ SỐ ĐIỆN MỚI ---")

    try:
        ma_cong_to = input("Nhập mã công tơ: ").strip()
        if not ma_cong_to:
            print("Mã công tơ không được để tróngo")
            return

        index, existing = tim_hoa_don_theo_ma(ma_cong_to)
        if existing:
            print(f"Mã công tơ {ma_cong_to} đã tồn tại.")
            return

        ten_chu_ho = input("Nhập tên chủ hộ: ").strip()
        if not ten_chu_ho:
            print("Tên chủ hộ không được để trống.")
            return

        so_cu = int(input("Nhập chỉ số điện cũ: "))
        so_moi = int(input("Nhập chỉ số điện mới: "))

        if so_moi < so_cu:
            print("Số mới phải lớn hơn hoặc bằng số cũ")
            return

        tieu_thu, thanh_tien, muc_ap_dung = tinh_toan_hoa_don(so_cu, so_moi)

        hoa_don_moi = {
            "ma_cong_to": ma_cong_to,
            "ten_chu_ho": ten_chu_ho,
            "so_dien_tu": so_cu,
            "so_dien_moi": so_moi,
            "tieu_thu": tieu_thu,
            "thanh_tien": thanh_tien,
            "muc_ap_dung": muc_ap_dung
        }

        danh_sach_hoa_don.append(hoa_don_moi)
        print("Đã thêm hóa đơn thành công!")
        print(f"Tiêu thụ: {tieu_thu} kWh")
        print(f"Thành tiền: {thanh_tien:,} VNĐ")
        print(f"Mức áp dụng: {muc_ap_dung}")

    except ValueError:
        print("Lỗi: Vui lòng nhập số hợp lệ cho chỉ số điện.")
    except Exception as e:
        print(f"Lỗi không xác định: {e}")


# 3. Cập nhật hóa đơn
def cap_nhat_hoa_don():
    """3. Cập nhật hóa đơn"""
    print("\n--- CẬP NHẬT HÓA ĐƠN ---")

    ma_cong_to = input("Nhập mã công tơ cần cập nhật: ").strip()
    if not ma_cong_to:
        print("Mã công tơ không được để trống.")
        return

    index, hoa_don = tim_hoa_don_theo_ma(ma_cong_to)
    if not hoa_don:
        print(f"Không tìm thấy hóa đơn với mã công tơ {ma_cong_to}")
        return

    print("Thông tin hiện tại:")
    print(f"Tên chủ hộ: {hoa_don['ten_chu_ho']}")
    print(f"Số điện cũ: {hoa_don['so_dien_tu']}")
    print(f"Số điện mới: {hoa_don['so_dien_moi']}")
    print(f"Tiêu thụ: {hoa_don['tieu_thu']} kWh")

    try:
        so_moi_moi = int(input("Nhập số mới (mới):"))

        if so_moi_moi < hoa_don['so_dien_tu']:
            print("Số mới phải lớn hơn hoặc bằng số cũ.")
            return

        tieu_thu, thanh_tien, muc_ap_dung = tinh_toan_hoa_don(
            hoa_don['so_dien_tu'], so_moi_moi)
        danh_sach_hoa_don[index]['so_dien_moi'] = so_moi_moi
        danh_sach_hoa_don[index]['tieu_thu'] = tieu_thu
        danh_sach_hoa_don[index]['thanh_tien'] = thanh_tien
        danh_sach_hoa_don[index]['muc_ap_dung'] = muc_ap_dung

        print("Đã cập nhật hóa đơn thành công!")
        print(f"Tiêu thụ mới: {tieu_thu} kWh")
        print(f"Thành tiền mới: {thanh_tien:,} VNĐ")
        print(f"Mức áp dụng mới: {muc_ap_dung}")

    except ValueError:
        print("Lỗi: Vui lòng nhập số hợp lệ cho chỉ số điện.")

    # 4. Xóa hóa đơn


def xoa_hoa_don():
    """4. Xóa hóa đơn"""
    print("\n--- XÓA HÓA ĐƠN ---")

    ma_cong_to = input("Nhập mã công tơ cần xóa: ").strip()
    if not ma_cong_to:
        print("Mã công tơ không được để trống.")
        return

    index, hoa_don = tim_hoa_don_theo_ma(ma_cong_to)
    if not hoa_don:
        print(f"Không tìm thấy hóa đơn với mã công tơ {ma_cong_to}")
        return

    print("Thông tin hóa đơn sẽ bị xóa:")
    print(f"- Mã công tơ: {hoa_don['ma_cong_to']}")
    print(f"- Tên chủ hộ: {hoa_don['ten_chu_ho']}")
    print(f"- Tiêu thụ: {hoa_don['tieu_thu']} kWh")
    print(f"- Thành tiền: {hoa_don['thanh_tien']:,} VNĐ")

    xac_nhan = input("Bạn có chắc muốn xóa? (y/n): ").strip().lower()
    if xac_nhan in ['y', 'yes']:
        danh_sach_hoa_don.pop(index)
        print("Đã xóa hóa đơn thành công!")
    else:
        print("Đã hủy thao tác xóa.")


# 5. Tìm kiếm hóa đơn
def tim_kiem_hoa_don():
    """5. Tìm kiếm hóa đơn"""
    print("\n--- TÌM KIẾM HÓA ĐƠN ---")

    tu_khoa = input("Nhập tên chủ hộ hoặc mã công tơ: ").strip().lower()
    if not tu_khoa:
        print("Từ khóa tìm kiếm không được để trống!")
        return

    ket_qua = []
    for hoa_don in danh_sach_hoa_don:
        if (tu_khoa in hoa_don['ten_chu_ho'].lower() or
                tu_khoa in hoa_don['ma_cong_to'].lower()):
            ket_qua.append(hoa_don)

    if not ket_qua:
        print("Không tìm thấy kết quả nào!")
        return

    print(f"\nTìm thấy {len(ket_qua)} kết quả:")
    headers = ["STT", "Mã công tơ", "Tên chủ hộ",
               "Tiêu thụ", "Thành tiền", "Mức áp dụng"]
    table_data = []

    for i, hoa_don in enumerate(ket_qua, 1):
        row = [
            i,
            hoa_don['ma_cong_to'],
            hoa_don['ten_chu_ho'],
            hoa_don['tieu_thu'],
            f"{hoa_don['thanh_tien']:,} VNĐ",
            hoa_don['muc_ap_dung']
        ]
        table_data.append(row)

    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# 6. Sắp xếp danh sách hóa đơn


def sap_xep_hoa_don():
    """6. Sắp xếp danh sách hóa đơn"""
    print("\n--- SẮP XẾP DANH SÁCH HÓA ĐƠN ---")
    print("1. Theo tiêu thụ (giảm dần)")
    print("2. Theo tên chủ hộ (A-Z)")

    try:
        lua_chon = int(input("Chọn cách sắp xếp (1-2): "))

        if lua_chon == 1:
            danh_sach_hoa_don.sort(key=lambda x: x['tieu_thu'], reverse=True)
            print("Đã sắp xếp theo tiêu thụ (giảm dần)")
        elif lua_chon == 2:
            danh_sach_hoa_don.sort(key=lambda x: x['ten_chu_ho'])
            print("Đã sắp xếp theo tên chủ hộ (A-Z)")
        else:
            print("Lựa chọn không hợp lệ!")
            return

        hien_thi_danh_sach()

    except ValueError:
        print("Lỗi: Vui lòng nhập số hợp lệ!")

# 7. Thống kê doanh thu


def thong_ke_doanh_thu():
    """7. Thống kê doanh thu"""
    print("\n--- THỐNG KÊ DOANH THU ---")

    if not danh_sach_hoa_don:
        print("Danh sách hóa đơn trống!")
        return

    muc_1 = sum(1 for hd in danh_sach_hoa_don if hd['muc_ap_dung'] == "Mức 1")
    muc_2 = sum(1 for hd in danh_sach_hoa_don if hd['muc_ap_dung'] == "Mức 2")
    muc_3 = sum(
        1 for hd in danh_sach_hoa_don if hd['muc_ap_dung'] == "Mức 3 (Cao)")

    tong_doanh_thu = sum(hd['thanh_tien'] for hd in danh_sach_hoa_don)
    tong_tieu_thu = sum(hd['tieu_thu'] for hd in danh_sach_hoa_don)

    print(f"Số hộ dùng điện Mức 1 (< 100 kWh): {muc_1}")
    print(f"Số hộ dùng điện Mức 2 (100-199 kWh): {muc_2}")
    print(f"Số hộ dùng điện Mức 3 (≥ 200 kWh): {muc_3}")
    print(f"Tổng số hộ: {len(danh_sach_hoa_don)}")
    print(f"Tổng tiêu thụ: {tong_tieu_thu:,} kWh")
    print(f"Tổng doanh thu: {tong_doanh_thu:,} VNĐ")

    return {"Mức 1": muc_1, "Mức 2": muc_2, "Mức 3": muc_3}


def hien_thi_menu():
    """Hiển thị menu chính"""
    print("\n" + "="*60)
    print("CHƯƠNG TRÌNH QUẢN LÝ HÓA ĐƠN TIỀN ĐIỆN 🏠")
    print("="*60)
    print("1.  Hiển thị danh sách hóa đơn")
    print("2.  Thêm chỉ số điện")
    print("3.  Cập nhật thông tin hóa đơn")
    print("4.  Xóa hóa đơn")
    print("5.  Tìm kiếm hóa đơn")
    print("6.  Sắp xếp danh sách hóa đơn")
    print("7.  Thống kê doanh thu")
    print("8.  Vẽ biểu đồ thống kê mức tiêu thụ")
    print("9.  Lưu vào file CSV")
    print("10. Thoát")
    print("="*60)


def chuong_trinh_chinh():
    """Chương trình chính với menu CLI"""

    while True:
        hien_thi_menu()

        try:
            lua_chon = input("Nhập lựa chọn của bạn (1-10): ").strip()

            if lua_chon == "1":
                hien_thi_danh_sach()
            elif lua_chon == "2":
                them_chi_so_dien()
            elif lua_chon == "3":
                cap_nhat_hoa_don()
            elif lua_chon == "4":
                xoa_hoa_don()
            elif lua_chon == "5":
                tim_kiem_hoa_don()
            elif lua_chon == "6":
                sap_xep_hoa_don()
            elif lua_chon == "7":
                thong_ke_doanh_thu()
            elif lua_chon == "8":
                break
            elif lua_chon == "9":
                break
            elif lua_chon == "10":
                print("\n--- ĐANG THOÁT CHƯƠNG TRÌNH ---")
                print("Cảm ơn bạn đã sử dụng chương trình")
                break
            else:
                print("Lựa chọn không hợp lệ! Vui lòng chọn từ 1-10.")

        except KeyboardInterrupt:
            print("\n\nChương trình bị ngắt bởi người dùng.")
            break

        except Exception as e:
            print(f"Lỗi: {e}")

        input("\nNhấn Enter để tiếp tục...")


print(" Chương trình quản lý hóa đơn tiền điện đã sẵn sàng")
print(" Tất cả chức năng đã được load thành công")
print("\n" + "="*50)

chuong_trinh_chinh()
