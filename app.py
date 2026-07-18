import streamlit as st
import pandas as pd
import numpy as np
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

#خريطة المنازل بعد الفلترة، ملوّنة فعلياً حسب السعر (أصفر=رخيص، أحمر=غالي)
st.subheader("Map (colored by MedHouseVal)")
price_min, price_max = df["MedHouseVal"].min(), df["MedHouseVal"].max()
norm_price = (filtered["MedHouseVal"] - price_min) / (price_max - price_min)

map_df = filtered.rename(columns={"Latitude": "lat", "Longitude": "lon"})[["lat", "lon"]].copy()
map_df["color"] = norm_price.apply(lambda v: f"#ff{int(255 * (1 - v)):02x}00")

st.map(map_df, color="color")

#توزيع الأسعار للبيانات المفلترة (نبني تسميات نظيفة بدل Interval objects)
st.subheader("MedHouseVal Distribution")
counts, bin_edges = np.histogram(filtered["MedHouseVal"], bins=10)
labels = [f"{bin_edges[i]:.2f}-{bin_edges[i + 1]:.2f}" for i in range(len(bin_edges) - 1)]
hist_series = pd.Series(counts, index=labels, name="Count")

st.bar_chart(hist_series)
