import streamlit as st
from underthesea import word_tokenize, pos_tag
import pandas as pd
import base64

st.set_page_config(page_title="Demo POS Tagging Tiếng Việt", layout="wide")

st.title("Demo POS Tagging Tiếng Việt với Streamlit")
st.write("Nhập một câu tiếng Việt, ứng dụng sẽ tách từ và gán nhãn từ loại.")

# Input
text = st.text_area(
    "Nhập câu tiếng Việt ở đây:",
    "Hệ thống phân loại bình luận tiếng Việt rất chính xác.",
    height=100
)

analyze_clicked = st.button("🔍 Phân tích", type="primary", width="stretch")

col1, col2 = st.columns(2)

# Bảng giải thích nhãn từ loại
POS_TAGS_EXPLANATION = {
    "N": "Danh từ",
    "Np": "Danh từ riêng",
    "Nc": "Danh từ chỉ loại",
    "Nu": "Danh từ đơn vị",
    "V": "Động từ",
    "A": "Tính từ",
    "P": "Đại từ",
    "R": "Phó từ",
    "L": "Định từ",
    "M": "Số từ",
    "E": "Giới từ",
    "C": "Liên từ",
    "I": "Thán từ",
    "T": "Trợ từ, tiểu từ",
    "B": "Từ gốc Hán-Việt",
    "Y": "Từ viết tắt",
    "S": "Từ ngoại lai",
    "X": "Từ không phân loại",
    "CH": "Dấu câu",
}

# Màu cho từng loại từ loại
POS_COLORS = {
    "N": "#FF6B6B",
    "Np": "#FF4444",
    "Nc": "#FF8888",
    "Nu": "#FFAAAA",
    "V": "#4ECDC4",
    "A": "#FFE66D",
    "P": "#A8E6CF",
    "R": "#95E1D3",
    "L": "#DDA0DD",
    "M": "#87CEEB",
    "E": "#FFA07A",
    "C": "#98D8C8",
    "I": "#F7DC6F",
    "T": "#BB8FCE",
    "B": "#F0B27A",
    "Y": "#AED6F1",
    "S": "#F5B7B1",
    "X": "#D5DBDB",
    "CH": "#BDC3C7",
}

# Hàm highlight
def highlight_text(tagged_words):
    html = ""
    for word, tag in tagged_words:
        color = POS_COLORS.get(tag, "#FFFFFF")
        html += f'<span style="background-color:{color}; padding:4px; margin:2px; border-radius:4px">{word} ({tag})</span> '
    return html

if analyze_clicked:
    # ✅ TODO: xử lý input rỗng
    if not text.strip():
        st.warning("⚠️ Vui lòng nhập câu trước khi phân tích!")
    else:
        # ✅ Tokenize
        tokens = word_tokenize(text)

        # ✅ POS tagging
        tagged = pos_tag(text)

        # =========================
        # COL1: TOKENIZE
        # =========================
        with col1:
            st.subheader("🔹 Kết quả Tokenize")
            st.write(tokens)

        # =========================
        # COL2: POS TAGGING
        # =========================
        with col2:
            st.subheader("🔹 Kết quả POS Tagging")

            df = pd.DataFrame(tagged, columns=["Từ", "Nhãn"])
            st.dataframe(df, use_container_width=True)

            # ✅ Highlight màu
            st.markdown("### 🌈 Highlight từ loại")
            st.markdown(highlight_text(tagged), unsafe_allow_html=True)

        # =========================
        # ✅ Export CSV
        # =========================
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Tải kết quả CSV",
            data=csv,
            file_name="pos_tagging_result.csv",
            mime="text/csv"
        )

# =========================
# ✅ Bảng giải thích POS tags
# =========================
st.markdown("---")
st.subheader("📘 Bảng giải thích nhãn từ loại")

pos_df = pd.DataFrame(
    [(k, v) for k, v in POS_TAGS_EXPLANATION.items()],
    columns=["Nhãn", "Ý nghĩa"]
)

st.table(pos_df)

# TODO: Thêm xử lý POS tagging và hiển thị kết quả ở col2
# TODO: Thêm bảng giải thích các nhãn từ loại (POS tags)
# TODO: Thêm xử lý lỗi khi input rỗng
# TODO: Thêm tính năng export kết quả ra file CSV
# TODO: Thêm highlight màu cho từng loại từ loại khác nhau