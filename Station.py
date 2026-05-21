import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 网页标题和说明
st.title("📡 测向交叉定位：误差包络模拟器")
st.markdown("通过调整下方滑块，实时观察**工程典型误差**对最终定位精度的影响范围（红色阴影区域）。")

# 侧边栏：放置交互滑块
st.sidebar.header("控制面板")
t1 = st.sidebar.slider('A站基础角 (°)', min_value=0, max_value=90, value=45, step=1)
t2 = st.sidebar.slider('B站基础角 (°)', min_value=90, max_value=180, value=135, step=1)
delta = st.sidebar.slider('工程误差偏差 (±°)', min_value=0.0, max_value=10.0, value=3.0, step=0.5)

# 核心计算函数
def calc_intersection(x1, y1, angle1, x2, y2, angle2):
    a1, a2 = np.radians(angle1), np.radians(angle2)
    if np.isclose(np.tan(a1), np.tan(a2)):
        return None, None
    t1_tan, t2_tan = np.tan(a1), np.tan(a2)
    x = (y2 - y1 + x1 * t1_tan - x2 * t2_tan) / (t1_tan - t2_tan)
    y = y1 + t1_tan * (x - x1)
    return x, y

def plot_ray(ax, x0, y0, angle, color, style, label=None):
    length = 600
    rad = np.radians(angle)
    x1 = x0 + length * np.cos(rad)
    y1 = y0 + length * np.sin(rad)
    ax.plot([x0, x1], [y0, y1], color=color, linestyle=style, alpha=0.5, label=label)

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

# 绘制基础射线与交点
plot_ray(ax, 200, 100, t1, 'black', '--')
plot_ray(ax, 500, 100, t2, 'blue', '--')
ex, ey = calc_intersection(200, 100, t1, 500, 100, t2)
if ex is not None:
    ax.plot(ex, ey, 'k*', markersize=10, label=f'理想点 ({ex:.1f}, {ey:.1f})')

# 计算四种误差组合并绘制包络区域
err_A = [t1 + delta, t1 + delta, t1 - delta, t1 - delta]
err_B = [t2 + delta, t2 - delta, t2 - delta, t2 + delta]
poly_x, poly_y = [], []

for ea, eb in zip(err_A, err_B):
    px, py = calc_intersection(200, 100, ea, 500, 100, eb)
    if px is not None:
        poly_x.append(px)
        poly_y.append(py)

if len(poly_x) == 4:
    ax.fill(poly_x, poly_y, color='red', alpha=0.25, label=f'±{delta}° 误差包络区域')
    for px, py in zip(poly_x, poly_y):
        ax.plot(px, py, 'ro', markersize=5)

ax.legend(loc='upper right')

# 将 matplotlib 图表渲染到 Streamlit 网页中
st.pyplot(fig)