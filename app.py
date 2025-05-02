
import streamlit as st
from PIL import Image

# Logo
logo = Image.open("logo_kla_krang.jpg")

# Page config
st.set_page_config(page_title="ระบบฟางข้าว - กล้าแกร่ง", layout="wide")

# Header
col1, col2 = st.columns([1, 4])
with col1:
    st.image(logo, width=120)
with col2:
    st.title("ระบบประเมินปริมาณฟางข้าวเพื่อบริหารจัดการชีวมวล")
    st.subheader("บริษัท กล้า-แกร่ง จำกัด")

# Input section
st.sidebar.header("พารามิเตอร์")
area = st.sidebar.selectbox("จังหวัด", ["นครสวรรค์"])
date_range = st.sidebar.date_input("ช่วงวันที่เก็บเกี่ยว", [])

# Static output (replace with real analysis later)
st.markdown("### 🔍 ผลการประเมินเบื้องต้น")
st.metric("พื้นที่ข้าว (ไร่)", "21,500")
st.metric("ปริมาณฟางข้าว (ตัน)", "3,870")
st.metric("จำนวนรถเกี่ยวที่ต้องใช้", "12 คัน")

# Placeholder for map
st.markdown("---")
st.markdown("#### 🗺️ แผนที่ GCVI (จำลอง)")
st.image("https://i.imgur.com/gcvi_map_example.jpg", use_column_width=True)

# Export CSV (simulate)
import pandas as pd
df = pd.DataFrame({
    "ตำบล": ["ท่าตะโก", "บรรพตพิสัย", "ชุมแสง"],
    "พื้นที่ข้าว (ไร่)": [8500, 7000, 6000],
    "ปริมาณฟาง (ตัน)": [1530, 1260, 1080]
})
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 ดาวน์โหลด .CSV", data=csv, file_name="biomass_estimate.csv", mime="text/csv")
