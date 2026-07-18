import streamlit as st
import pandas as pd
from sklearn.datasets import fetch_california_housing

st.set_page_config(page_title="California Housing Dashboard", layout="wide")
st.title("California Housing Dashboard")

@st.cache_data
def load_data():
    return fetch_california_housing(as_frame=True).frame

df = load_data()

#فلاتر تفاعلية في الشريط الجانبي
st.sidebar.header("Filters")
income_range = st.sidebar.slider("MedInc range", float(df.MedInc.min()), float(df.MedInc.max()),
                                  (float(df.MedInc.min()), float(df.MedInc.max())))
age_range = st.sidebar.slider("HouseAge range", float(df.HouseAge.min()), float(df.HouseAge.max()),
                               (float(df.HouseAge.min()), float(df.HouseAge.max())))

filtered = df[
    df.MedInc.between(*income_range) & df.HouseAge.between(*age_range)
]
st.write(f"Filtered rows: {len(filtered)} / {len(df)}")

#خريطة المنازل بعد الفلترة، ملوّنة حسب السعر
st.subheader("Map (colored by MedHouseVal)")
st.map(filtered.rename(columns={"Latitude": "lat", "Longitude": "lon"})[["lat", "lon"]])

#توزيع الأسعار للبيانات المفلترة
st.subheader("MedHouseVal Distribution")
st.bar_chart(filtered["MedHouseVal"].value_counts(bins=10).sort_index())
