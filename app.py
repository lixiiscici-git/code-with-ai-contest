import streamlit as st
import pandas as pd
import pydeck as pdk

from utils import get_color

# ============================================================
# 页面全局配置 — 必须放在所有 st. 调用之前
# ============================================================
st.set_page_config(page_title="5G 信号可视化看板", layout="wide")

st.title("📡 5G 信号可视化看板")
st.markdown("欢迎来到 **'Code with AI' 极客探索赛**！")

# ============================================================
# 数据加载
# ============================================================
df = pd.read_csv("data/signal_samples.csv")

# ============================================================
# 侧边栏 — 联动筛选器
# ============================================================
st.sidebar.header("🔍 筛选条件")

# 频段下拉筛选（含“全部”选项）
available_bands = df["Band"].unique().tolist()
available_bands.sort()
band_options = ["全部"] + available_bands
selected_band = st.sidebar.selectbox("频段 (Band)", band_options)

# RSRP 范围滑动条
rsrp_min = float(df["RSRP_dBm"].min())
rsrp_max = float(df["RSRP_dBm"].max())
rsrp_range = st.sidebar.slider(
    "RSRP 范围 (dBm)",
    min_value=rsrp_min,
    max_value=rsrp_max,
    value=(rsrp_min, rsrp_max),
    step=1.0,
)

# 根据筛选条件过滤数据
filtered_df = df.copy()
if selected_band != "全部":
    filtered_df = filtered_df[filtered_df["Band"] == selected_band]
filtered_df = filtered_df[
    (filtered_df["RSRP_dBm"] >= rsrp_range[0])
    & (filtered_df["RSRP_dBm"] <= rsrp_range[1])
]

st.sidebar.metric("筛选后样本数", len(filtered_df))

# 显示原始数据
with st.expander("查看原始数据"):
    st.dataframe(filtered_df)

# 为每条记录计算颜色
filtered_df["color"] = filtered_df["RSRP_dBm"].apply(get_color)

# ============================================================
# 3D 柱状地图 — 信号点高度随下载速率变化
# ============================================================
st.subheader("🗺️ 5G 信号 3D 柱状地图")

# 地图中心点
midpoint = (
    filtered_df["Latitude"].mean(),
    filtered_df["Longitude"].mean(),
)

# 自定义柱状 Layer：继承 ColumnLayer 并开放 get_fill_color 参数
class ColoredColumnLayer(pdk.Layer):
    """带颜色映射的 3D 柱状图层。"""
    def __init__(self, **kwargs):
        super().__init__(type="ColumnLayer", **kwargs)

# 下载速率归一化到合理柱高范围（避免过高或过低）
max_dl = filtered_df["Download_Mbps"].max()
elevation_scale = 500 / max_dl if max_dl > 0 else 1

column_layer = ColoredColumnLayer(
    data=filtered_df,
    get_position="[Longitude, Latitude]",
    get_elevation="Download_Mbps",
    elevation_scale=elevation_scale,
    radius=120,
    get_fill_color="color",
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(
    latitude=midpoint[0],
    longitude=midpoint[1],
    zoom=12,
    pitch=50,  # 倾斜视角以凸显 3D 效果
    bearing=0,
)

deck = pdk.Deck(
    layers=[column_layer],
    initial_view_state=view_state,
    tooltip={
        "html": """
        <b>小区ID:</b> {CellID}<br/>
        <b>频段:</b> {Band}<br/>
        <b>RSRP:</b> {RSRP_dBm} dBm<br/>
        <b>SINR:</b> {SINR_dB} dB<br/>
        <b>下载速率:</b> {Download_Mbps} Mbps
        """,
        "style": {"backgroundColor": "steelblue", "color": "white"},
    },
)

st.pydeck_chart(deck)

# ============================================================
# 频段统计图
# ============================================================
st.subheader("📊 各频段基站数量统计")

band_count = filtered_df["Band"].value_counts()
st.bar_chart(band_count)
