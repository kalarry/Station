import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 页面标题设置
st.set_page_config(page_title="基础层：定位原理", layout="centered")
st.title("基础层项目：定位原理达标训练")

# --- 第一部分：已知条件与数学方程推导 ---
st.header("一、 项目任务与方程建立")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **已知条件：**
    * 侦察站 A：坐标 $(200, 100)$ m，测向角 $\\theta_1 = 45^\\circ$
    * 侦察站 B：坐标 $(500, 100)$ m，测向角 $\\theta_2 = 135^\\circ$
    """)

with col2:
    st.markdown("**定位原理要求：**\n1. 绘制测向交叉定位几何图\n2. 建立两条位置线方程")

st.markdown("---")
st.markdown("### 📐 位置线方程推导 (要求 2)")
st.markdown("根据点斜式直线方程 $y - y_0 = \\tan(\\theta)(x - x_0)$，我们可以建立如下方程组：")

# 使用 LaTeX 渲染标准数学公式，非常适合学术和教学展示
st.latex(r"\text{侦察站 A 位置线: } y - 100 = \tan(45^\circ)(x - 200) \implies y = x - 100")
st.latex(r"\text{侦察站 B 位置线: } y - 100 = \tan(135^\circ)(x - 500) \implies y = -x + 600")

st.markdown("联立上述方程，解得绝对理想定位点坐标为：**(350, 250)**")


# --- 第二部分：几何可视化 ---
st.markdown("---")
st.markdown("### 🗺️ 测向交叉定位几何图 (要求 1)")

# 初始化画布
fig, ax = plt.subplots(figsize=(8, 6))

# 设置中文字体 (兼容不同操作系统)
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 基站参数
Ax, Ay, angleA = 200, 100, 45
Bx, By, angleB = 500, 100, 135

# 1. 绘制基站 A 和 B
ax.plot(Ax, Ay, 'ko', markersize=8, label=f'侦察站 A ({Ax}, {Ay})')
ax.plot(Bx, By, 'bs', markersize=8, label=f'侦察站 B ({Bx}, {By})')

# 2. 绘制测向射线 (位置线)
length = 300
x_val_A = Ax + length * np.cos(np.radians(angleA))
y_val_A = Ay + length * np.sin(np.radians(angleA))
ax.plot([Ax, x_val_A], [Ay, y_val_A], 'k-', linewidth=2, label=f'A站位置线 ($\\theta_1=45^\\circ$)')

x_val_B = Bx + length * np.cos(np.radians(angleB))
y_val_B = By + length * np.sin(np.radians(angleB))
ax.plot([Bx, x_val_B], [By, y_val_B], 'b-', linewidth=2, label=f'B站位置线 ($\\theta_2=135^\\circ$)')

# 3. 绘制理想交点
ax.plot(350, 250, 'r*', markersize=15, label='理想定位点 E (350, 250)')
# 添加坐标文本注释
ax.annotate('E (350, 250)', xy=(350, 250), xytext=(10, 10), textcoords='offset points', color='red', fontsize=12, fontweight='bold')

# 图表美化与坐标系控制
ax.set_xlim(150, 550)
ax.set_ylim(50, 350)
ax.set_aspect('equal', adjustable='box') # 强制 X/Y 轴比例 1:1，保证角度视觉正确
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_xlabel("X 坐标 (m)")
ax.set_ylabel("Y 坐标 (m)")
ax.legend(loc='upper right')

# 在 Streamlit 中渲染图表
st.pyplot(fig)
