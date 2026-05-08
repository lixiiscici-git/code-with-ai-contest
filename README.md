# 📡 5G 信号可视化看板

"Code with AI" 极客探索赛参赛作品 —— 基于 Streamlit + Pydeck 的 5G 路测数据交互式 3D 看板。

## 一、看板功能

### 🔍 侧边栏联动筛选

左侧边栏提供实时筛选器，拖动后地图与图表立即更新：

- **频段筛选**：下拉菜单按 Band（n28/n41/n78/n79 等）过滤
- **RSRP 范围筛选**：滑动条按信号强度 (dBm) 范围过滤
- **样本计数**：实时显示当前筛选条件下的数据条数

### 🗺️ 3D 柱状地图

- 每个信号点以 **3D 柱体** 渲染，柱体高度随 `Download_Mbps`（下载速率）变化
- 柱体颜色按 RSRP 信号强度着色：
  - **绿色**：> -90 dBm（信号良好）
  - **橙色**：-110 ~ -90 dBm（信号一般）
  - **红色**：< -110 dBm（信号较差）
- 支持鼠标悬停查看详情：CellID、Band、RSRP、SINR、下载速率
- 支持拖拽旋转、缩放等 3D 视角操作

### 📊 频段统计图表

- 柱状图展示各频段基站数量分布
- 随筛选条件自动更新

## 二、项目结构

```
code-with-ai-contest/
├── app.py                  # Streamlit 主应用入口
├── utils.py                # 核心工具函数（信号颜色映射）
├── requirements.txt        # Python 依赖清单
├── data/
│   └── signal_samples.csv  # 5G 路测模拟数据集
├── tests/
│   └── test_app.py         # 单元测试（11 项）
├── AI_PROMPTS.md           # AI Agent 交互日志
└── README.md               # 本文件
```

## 三、运行方法

### 环境要求

- Python 3.11+
- Windows / macOS / Linux

### 1. 克隆仓库

```bash
git clone <repo-url>
cd code-with-ai-contest
```

### 2. 创建虚拟环境

```bash
python -m venv .env
```

### 3. 激活环境并安装依赖

**Windows (PowerShell):**

```powershell
.env\Scripts\activate
pip install -r requirements.txt
```

**macOS / Linux:**

```bash
source .env/bin/activate
pip install -r requirements.txt
```

### 4. 启动看板

```bash
streamlit run app.py
```

浏览器将自动打开 `http://localhost:8501`。

### 5. 运行单元测试

```bash
python -m pytest tests/ -v
```

预期输出：`11 passed`。

## 四、数据集说明


| 字段            | 类型     | 说明                            |
| ------------- | ------ | ----------------------------- |
| Latitude      | float  | 纬度                            |
| Longitude     | float  | 经度                            |
| CellID        | int    | 基站小区 ID                       |
| Band          | string | 频段 (n28/n41/n78/n79)          |
| RSRP_dBm      | float  | 参考信号接收功率 (dBm)                |
| SINR_dB       | float  | 信噪比 (dB)                      |
| TerminalType  | string | 终端类型 (Smartphone/CPE/Vehicle) |
| Download_Mbps | float  | 下行速率 (Mbps)                   |


## 五、技术栈


| 组件        | 版本     | 用途       |
| --------- | ------ | -------- |
| Streamlit | 1.57.0 | Web 看板框架 |
| Pydeck    | 0.9.2  | 3D 地图渲染  |
| Pandas    | 3.0.2  | 数据处理     |
| NumPy     | 2.4.4  | 数值计算     |
| Pytest    | 9.0.3  | 单元测试     |


