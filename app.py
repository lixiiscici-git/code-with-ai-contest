import streamlit as st
import pandas as pd
import pydeck as pdk

# 设置页面配置
st.set_page_config(page_title="5G 信号可视化看板", layout="wide")

st.title("📡 5G 信号可视化看板")
st.markdown("欢迎来到 **'Code with AI' 极客探索赛**！")
st.info("💡 **通关提示**：请打开你的 AI 助手聊天框，输入提示词让它帮你写代码。\n\n例如：*\"请帮我用 pandas 读取 data/signal_samples.csv，并在下方展示前 5 行数据。\"*")

# ==========================================
# 你的代码从这里开始... 
# (提示：不要手写，让 AI 帮你写！)
# ==========================================

# 读取数据
df = pd.read_csv("data/signal_samples.csv")

# 显示原始数据
with st.expander("查看原始数据"):
    st.dataframe(df)

# =========================
# 信号强度颜色映射
# =========================
def get_color(rsrp):
    """
    根据信号强度返回 RGB 颜色
    """
    if rsrp > -90:
        return [0, 200, 0]      # 绿色
    elif rsrp > -110:
        return [255, 165, 0]    # 橙色
    else:
        return [255, 0, 0]      # 红色

# 添加颜色列
df["color"] = df["RSRP_dBm"].apply(get_color)

# =========================
# 地图可视化
# =========================
st.subheader("🗺️ 5G 信号热力散点地图")

# 自动计算地图中心
midpoint = (
    df["Latitude"].mean(),
    df["Longitude"].mean()
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[Longitude, Latitude]',
    get_fill_color='color',
    get_radius=60,
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=midpoint[0],
    longitude=midpoint[1],
    zoom=11,
    pitch=0,
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "html": """
        <b>小区ID:</b> {CellID}<br/>
        <b>Band:</b> {Band}<br/>
        <b>RSRP:</b> {RSRP_dBm} dBm<br/>
        <b>SINR:</b> {SINR_dB} dB
        """,
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
)

st.pydeck_chart(deck)

# =========================
# 频段统计图
# =========================
st.subheader("📊 各频段基站数量统计")

band_count = df["Band"].value_counts()

st.bar_chart(band_count)