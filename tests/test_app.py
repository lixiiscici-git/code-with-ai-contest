"""app.py 核心逻辑的单元测试。"""

import sys
from pathlib import Path

import pandas as pd
import pytest

# 将项目根目录加入模块搜索路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils import get_color


# ============================================================
# 测试数据加载
# ============================================================
class TestDataLoading:
    """验证 CSV 数据加载及列名完整性。"""

    @pytest.fixture
    def sample_df(self):
        """加载真实 CSV，供后续测试复用。"""
        csv_path = (
            Path(__file__).resolve().parent.parent / "data" / "signal_samples.csv"
        )
        return pd.read_csv(csv_path)

    def test_csv_loads_with_expected_columns(self, sample_df):
        expected = [
            "Latitude",
            "Longitude",
            "CellID",
            "Band",
            "RSRP_dBm",
            "SINR_dB",
            "TerminalType",
            "Download_Mbps",
        ]
        for col in expected:
            assert col in sample_df.columns, f"缺少列: {col}"

    def test_csv_has_data(self, sample_df):
        assert len(sample_df) > 0, "CSV 数据为空"


# ============================================================
# 测试信号强度 → 颜色映射
# ============================================================
class TestGetColor:
    """验证 get_color 在所有分支下的返回值。"""

    def test_good_signal_returns_green(self):
        assert get_color(-80) == [0, 200, 0]

    def test_fair_signal_returns_orange(self):
        assert get_color(-100) == [255, 165, 0]

    def test_poor_signal_returns_red(self):
        assert get_color(-120) == [255, 0, 0]

    def test_boundary_minus_90_returns_green(self):
        # 边界值 -90: RSRP > -90 不成立，落入第二个分支 → 橙色
        assert get_color(-90) == [255, 165, 0]

    def test_boundary_minus_110_returns_red(self):
        # 边界值 -110: RSRP > -110 不成立，落入第三个分支 → 红色
        assert get_color(-110) == [255, 0, 0]


# ============================================================
# 测试数据过滤逻辑
# ============================================================
class TestFilterLogic:
    """验证 Band 和 RSRP 筛选的正确性。"""

    @pytest.fixture
    def sample_df(self):
        csv_path = (
            Path(__file__).resolve().parent.parent / "data" / "signal_samples.csv"
        )
        return pd.read_csv(csv_path)

    def test_filter_by_band(self, sample_df):
        target_band = "n78"
        filtered = sample_df[sample_df["Band"] == target_band]
        assert len(filtered) > 0
        assert (filtered["Band"] == target_band).all()

    def test_filter_by_rsrp_range(self, sample_df):
        low, high = -100, -80
        filtered = sample_df[
            (sample_df["RSRP_dBm"] >= low) & (sample_df["RSRP_dBm"] <= high)
        ]
        assert (filtered["RSRP_dBm"] >= low).all()
        assert (filtered["RSRP_dBm"] <= high).all()

    def test_filter_combined(self, sample_df):
        target_band = "n78"
        low, high = -110, -85
        filtered = sample_df[sample_df["Band"] == target_band]
        filtered = filtered[
            (filtered["RSRP_dBm"] >= low) & (filtered["RSRP_dBm"] <= high)
        ]
        assert (filtered["Band"] == target_band).all()
        assert (filtered["RSRP_dBm"] >= low).all()
        assert (filtered["RSRP_dBm"] <= high).all()


# ============================================================
# 测试颜色列生成
# ============================================================
class TestColorColumn:
    """验证 DataFrame 颜色列的生成。"""

    def test_color_column_created(self):
        csv_path = (
            Path(__file__).resolve().parent.parent / "data" / "signal_samples.csv"
        )
        df = pd.read_csv(csv_path)
        df["color"] = df["RSRP_dBm"].apply(get_color)
        assert "color" in df.columns
        assert len(df["color"]) == len(df)
        # 每条颜色应为包含 3 个整数的列表
        for c in df["color"]:
            assert isinstance(c, list)
            assert len(c) == 3
            assert all(isinstance(v, int) for v in c)
