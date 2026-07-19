import streamlit as st
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing

st.set_page_config(page_title="California Housing Dashboard", layout="wide")

#بطاقة تعريفية عصرية بالمشروع والفريق (RTL صحيح، أسماء المشاركين واضحة)
st.markdown("""
<style>
.project-hero{
    direction: rtl; text-align: right;
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    border-radius: 18px; padding: 28px 32px; color: #fff;
    margin-bottom: 22px; box-shadow: 0 8px 28px rgba(30,60,114,.28);
}
.project-hero .eyebrow{ font-size: .8rem; letter-spacing: 2px; opacity: .8; text-transform: uppercase; }
.project-hero h1{ margin: 4px 0 2px; font-size: 1.9rem; font-weight: 800; line-height: 1.25; }
.project-hero .sub{ opacity: .9; font-size: 1rem; margin-bottom: 20px; }
.hero-chips{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 22px; }
.hero-chip{ background: rgba(255,255,255,.14); border: 1px solid rgba(255,255,255,.28);
    border-radius: 999px; padding: 7px 16px; font-size: .9rem; }
.hero-chip b{ font-weight: 700; }
.team-grid{ display: flex; flex-wrap: wrap; gap: 14px; }
.member{ background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.22);
    border-radius: 14px; padding: 14px 18px; min-width: 220px; }
.member .name{ font-weight: 700; font-size: 1.08rem; margin-bottom: 3px; }
.member .sid{ direction: ltr; text-align: right; opacity: .82; font-size: .82rem;
    font-family: ui-monospace, monospace; }
.hero-chip b{ margin-left: 6px; }
/* جعل الشريط الجانبي بالكامل RTL */
section[data-testid="stSidebar"]{ direction: rtl; text-align: right; }
</style>
<div class="project-hero">
    <div class="eyebrow">WML · F25 Project</div>
    <h1>California Housing Dashboard</h1>
    <div class="sub">لوحة تفاعلية لاستكشاف بيانات أسعار المنازل في كاليفورنيا</div>
    <div class="hero-chips">
        <span class="hero-chip"><b>الجهة</b> الجامعة الافتراضية السورية (SVU)</span>
        <span class="hero-chip"><b>الفصل</b> F25</span>
        <span class="hero-chip"><b>المادة</b> WML</span>
        <span class="hero-chip"><b>بإشراف</b> د. باسل الخطيب</span>
    </div>
    <div class="team-grid">
        <div class="member"><div class="name">حمزة سايحة</div><div class="sid">Hamza_423996</div></div>
        <div class="member"><div class="name">محمد زيد النحاس</div><div class="sid">MHDZAID_461549</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return fetch_california_housing(as_frame=True).frame

df = load_data()

#فلاتر مبسّطة عبر قوائم منسدلة بفئات جاهزة (أسهل من سحب منزلق النطاق)
st.sidebar.header("الفلاتر")

income_option = st.sidebar.selectbox(
    "دخل السكان",
    ["الكل", "منخفض — أقل من $30,000", "متوسط — $30,000 إلى $70,000", "مرتفع — أكثر من $70,000"],
    help="اختر فئة متوسط دخل سكان المنطقة",
)
income_bounds = {
    "الكل": (df.MedInc.min(), df.MedInc.max()),
    "منخفض — أقل من $30,000": (df.MedInc.min(), 3.0),
    "متوسط — $30,000 إلى $70,000": (3.0, 7.0),
    "مرتفع — أكثر من $70,000": (7.0, df.MedInc.max()),
}[income_option]

age_option = st.sidebar.selectbox(
    "عمر المنزل",
    ["الكل", "حديثة — أقل من 15 سنة", "متوسطة — 15 إلى 35 سنة", "قديمة — أكثر من 35 سنة"],
    help="اختر فئة عمر المنازل",
)
age_bounds = {
    "الكل": (df.HouseAge.min(), df.HouseAge.max()),
    "حديثة — أقل من 15 سنة": (df.HouseAge.min(), 15.0),
    "متوسطة — 15 إلى 35 سنة": (15.0, 35.0),
    "قديمة — أكثر من 35 سنة": (35.0, df.HouseAge.max()),
}[age_option]

filtered = df[
    df.MedInc.between(*income_bounds) & df.HouseAge.between(*age_bounds)
]

col1, col2 = st.columns(2)
col1.metric("عدد المنازل المطابقة", f"{len(filtered):,}")
col2.metric("من إجمالي", f"{len(df):,}")

#خريطة المنازل بعد الفلترة، ملوّنة فعلياً حسب السعر (أصفر=رخيص، أحمر=غالي)
st.markdown('<h3 dir="rtl" style="text-align:right">خريطة توزيع المنازل</h3>', unsafe_allow_html=True)
st.caption(
    '<div dir="rtl">كل نقطة = منزل واحد على موقعه الجغرافي الحقيقي في كاليفورنيا. '
    'اللون: أصفر = سعر منخفض، أحمر = سعر مرتفع.</div>',
    unsafe_allow_html=True,
)

price_min, price_max = df["MedHouseVal"].min(), df["MedHouseVal"].max()
norm_price = (filtered["MedHouseVal"] - price_min) / (price_max - price_min)

map_df = filtered.rename(columns={"Latitude": "lat", "Longitude": "lon"})[["lat", "lon"]].copy()
map_df["color"] = norm_price.apply(lambda v: f"#ff{int(255 * (1 - v)):02x}00")

st.map(map_df, color="color")

#توزيع الأسعار للبيانات المفلترة، بالدولار الفعلي بدل الوحدة المُقيّسة (×100,000$)
st.markdown('<h3 dir="rtl" style="text-align:right">توزيع أسعار المنازل</h3>', unsafe_allow_html=True)
st.caption(
    '<div dir="rtl">كل عمود = عدد المنازل التي يقع سعرها ضمن هذا النطاق (بالدولار الفعلي). '
    'ملاحظة: أعلى قيمة في الداتاست الأصلي مقفولة عند 500,001$ (top-coding)، '
    'لذلك قد يظهر تجمّع عند هذا الحد.</div>',
    unsafe_allow_html=True,
)

counts, bin_edges = np.histogram(filtered["MedHouseVal"], bins=10)
labels = [f"${bin_edges[i] * 100000:,.0f}–${bin_edges[i + 1] * 100000:,.0f}" for i in range(len(bin_edges) - 1)]
hist_series = pd.Series(counts, index=labels, name="عدد المنازل")

st.bar_chart(hist_series)
