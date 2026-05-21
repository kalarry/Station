import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 网页标题和说明
st.title("测向交叉定位：±3°误差包络模拟器")

# 侧边栏：放置交互滑块
st.sidebar.header("控制面板")
t1 = st.sidebar.slider('A站理想角 (°)', min_value=0, max_value=90, value=45, step=1)
t2 = st.sidebar.slider('B站理想角 (°)', min_value=90, max_value=180, value=135, step=1)
delta = st.sidebar.slider('工程误差偏差 (±°)', min_value=0.0, max_value=10.0, value=3.0, step=0.5)

# 核心计算函数
def calc_intersection(x1, y1, angle1, x2, y2, angle2):
    """计算两条射线的交点"""
    a1, a2 = np.radians(angle1), np.radians(angle2)
    # 避免平行情况
    if np.isclose(np.tan(a1), np.tan(a2)):
        return None, None
    t1_tan, t2_tan = np.tan(a1), np.tan(a2)
    x = (y2 - y1 + x1 * t1_tan - x2 * t2_tan) / (t1_tan - t2_tan)
    y = y1 + t1_tan * (x - x1)
    return x, y

def plot_ray(ax, x0, y0, angle, color, style, label=None, linewidth=1):
    """从 station 绘制一条射线"""
    length = 600
    rad = np.radians(angle)
    x1 = x0 + length * np.cos(rad)
    y1 = y0 + length * np.sin(rad)
    ax.plot([x0, x1], [y0, y1], color=color, linestyle=style, alpha=0.5, label=label, linewidth=linewidth)

def annotate_angle_offset(ax, x0, y0, angle, base_angle, color):
    """在线的垂直方向上偏移标注文字，使其远离线体"""
    dist_along = 250   # 文字沿着射线方向的距离
    offset_perp = 25   # 文字垂直远离射线的距离 (数值越大越远)
    
    rad = np.radians(angle)
    # 判断是 +delta 还是 -delta 的边界线，决定向哪一侧推开
    sign = 1 if angle > base_angle else -1
    
    # 利用法向量计算垂直偏移后的坐标
    lx = x0 + dist_along * np.cos(rad) - sign * offset_perp * np.sin(rad)
    ly = y0 + dist_along * np.sin(rad) + sign * offset_perp * np.cos(rad)
    
    # 添加文字，并设置半透明白色背景边框，防止被网格遮挡
    bbox_props = dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8)
    ax.text(lx, ly, f"{angle:.1f}°", color=color, fontsize=10, fontweight='bold',
            ha='center', va='center', bbox=bbox_props)

# 初始化图表
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(100, 600)
ax.set_ylim(50, 450)
ax.grid(True, linestyle=':', alpha=0.7)
ax.set_aspect('equal', adjustable='box')
ax.set_xlabel("X 坐标 (m)")
ax.set_ylabel("Y 坐标 (m)")

# 绘制基站
ax.plot(200, 100, 'ko', markersize=8, label='侦察站 A (200, 100)')
ax.plot(500, 100, 'bs', markersize=8, label='侦察站 B (500, 100)')

# 计算并绘制理想定位点
ex, ey = calc_intersection(200, 100, t1, 500, 100, t2)
if ex is not None:
    ax.plot(ex, ey, 'k*', markersize=
