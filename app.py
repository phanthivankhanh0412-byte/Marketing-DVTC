import streamlit as st
import pandas as pd
import os

# =========================
# CẤU HÌNH APP
# =========================
st.set_page_config(
    page_title="Quản lý khách hàng",
    page_icon="👥",
    layout="wide"
)

st.title("👥 APP QUẢN LÝ KHÁCH HÀNG")
st.write("Nhập thông tin khách hàng vào biểu mẫu bên dưới.")

# =========================
# FILE LƯU DỮ LIỆU
# =========================
FILE_NAME = "khach_hang.csv"

columns = [
    "Số điện thoại",
    "Tên khách hàng",
    "Khu vực",
    "Ghi chú"
]

# Nếu chưa có file thì tạo DataFrame rỗng
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME, dtype=str)
else:
    df = pd.DataFrame(columns=columns)


# =========================
# FORM NHẬP KHÁCH HÀNG
# =========================
st.subheader("➕ Thêm khách hàng")

with st.form("customer_form"):

    col1, col2 = st.columns(2)

    with col1:
        phone = st.text_input(
            "Số điện thoại *",
            placeholder="Ví dụ: 0912345678"
        )

        name = st.text_input(
            "Tên khách hàng *",
            placeholder="Ví dụ: Nguyễn Văn A"
        )

    with col2:
        area = st.selectbox(
            "Khu vực",
            [
                "Hà Nội",
                "TP. Hồ Chí Minh",
                "Đà Nẵng",
                "Hải Phòng",
                "Cần Thơ",
                "Khác"
            ]
        )

        note = st.text_area(
            "Ghi chú",
            placeholder="Nhập ghi chú về khách hàng..."
        )

    submitted = st.form_submit_button(
        "💾 Thêm khách hàng",
        use_container_width=True
    )


# =========================
# XỬ LÝ THÊM KHÁCH HÀNG
# =========================
if submitted:

    # Kiểm tra dữ liệu bắt buộc
    if not phone.strip():
        st.error("⚠️ Vui lòng nhập số điện thoại.")

    elif not name.strip():
        st.error("⚠️ Vui lòng nhập tên khách hàng.")

    # Kiểm tra số điện thoại đã tồn tại
    elif phone.strip() in df["Số điện thoại"].astype(str).values:
        st.warning("⚠️ Số điện thoại này đã tồn tại.")

    else:

        new_customer = pd.DataFrame([{
            "Số điện thoại": phone.strip(),
            "Tên khách hàng": name.strip(),
            "Khu vực": area,
            "Ghi chú": note.strip()
        }])

        # Thêm khách hàng mới
        df = pd.concat(
            [df, new_customer],
            ignore_index=True
        )

        # Lưu vào CSV
        df.to_csv(
            FILE_NAME,
            index=False,
            encoding="utf-8-sig"
        )

        st.success("✅ Đã thêm khách hàng thành công!")

        # Làm mới giao diện
        st.rerun()


# =========================
# HIỂN THỊ DANH SÁCH
# =========================
st.divider()

st.subheader("📋 Danh sách khách hàng")

if len(df) == 0:

    st.info("Chưa có khách hàng nào.")

else:

    # Thống kê
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Tổng khách hàng",
            len(df)
        )

    with col2:
        st.metric(
            "Số khu vực",
            df["Khu vực"].nunique()
        )

    with col3:
        st.metric(
            "Số điện thoại",
            df["Số điện thoại"].nunique()
        )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# =========================
# TÌM KIẾM KHÁCH HÀNG
# =========================
if len(df) > 0:

    st.subheader("🔎 Tìm kiếm khách hàng")

    search = st.text_input(
        "Nhập tên hoặc số điện thoại để tìm kiếm",
        placeholder="Ví dụ: Nguyễn Văn A hoặc 0912..."
    )

    if search:

        result = df[
            df["Tên khách hàng"].str.contains(
                search,
                case=False,
                na=False
            )
            |
            df["Số điện thoại"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )


# =========================
# XÓA KHÁCH HÀNG
# =========================
st.divider()

st.subheader("🗑️ Xóa khách hàng")

if len(df) > 0:

    phone_delete = st.selectbox(
        "Chọn số điện thoại cần xóa",
        df["Số điện thoại"].tolist()
    )

    if st.button(
        "🗑️ Xóa khách hàng",
        type="secondary"
    ):

        df = df[
            df["Số điện thoại"] != phone_delete
        ]

        df.to_csv(
            FILE_NAME,
            index=False,
            encoding="utf-8-sig"
        )

        st.success("✅ Đã xóa khách hàng.")

        st.rerun()


# =========================
# TẢI DỮ LIỆU
# =========================
st.divider()

st.subheader("📥 Xuất dữ liệu")

if len(df) > 0:

    csv_data = df.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        label="📥 Tải danh sách khách hàng",
        data=csv_data,
        file_name="danh_sach_khach_hang.csv",
        mime="text/csv",
        use_container_width=True
    )
