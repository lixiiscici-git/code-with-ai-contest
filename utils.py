def get_color(rsrp):
    """根据 RSRP 值返回 RGB 颜色列表。

    规则:
        RSRP > -90  → 绿色 (信号良好)
        RSRP > -110 → 橙色 (信号一般)
        RSRP <= -110 → 红色 (信号较差)
    """
    if rsrp > -90:
        return [0, 200, 0]
    elif rsrp > -110:
        return [255, 165, 0]
    else:
        return [255, 0, 0]
