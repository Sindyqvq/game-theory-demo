import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm 

# --- 1. 加载字体 (只加载，不使用) ---
# 尝试加载 SimHei.ttf，如果找不到则忽略（避免报错）
try:
    font_prop = fm.FontProperties(fname='SimHei.ttf')
except:
    font_prop = None

# --- 2. 网页标题 ---
st.title("博弈论互动演示：策略演化实验室 🧬")
st.markdown("物理系博弈论期末作业演示 | 基于 Python Streamlit")

# --- 3. 侧边栏设置 ---
st.sidebar.header("实验参数设置")
st.sidebar.write("调整下方的滑块，观察曲线变化")

# 设定博弈的四个数值
st_t = st.sidebar.slider("诱惑 (T) - 我背叛/对方合作", 0, 10, 5)
st_r = st.sidebar.slider("奖励 (R) - 双方合作", 0, 10, 3)
st_p = st.sidebar.slider("惩罚 (P) - 双方背叛", 0, 10, 1)
st_s = st.sidebar.slider("傻瓜 (S) - 我合作/对方背叛", 0, 10, 0)

# --- 4. 显示矩阵 ---
st.subheader("当前收益矩阵 (Payoff Matrix)")
st.info(f"""
- 如果你合作，对方合作：得 {st_r} 分
- 如果你背叛，对方合作：得 {st_t} 分
- 如果你合作，对方背叛：得 {st_s} 分
- 如果你背叛，对方背叛：得 {st_p} 分
""")

# --- 5. 演化模拟逻辑 ---
st.subheader("📊 随时间演化的结果")
st.write("假设群体中一部分人选合作，一部分人选背叛，随时间推移，谁会活下来？")

init_coop = st.slider("初始合作者比例", 0.0, 1.0, 0.5, step=0.01)
steps = 50 

x = init_coop
history = [x]
dt = 0.1 

for _ in range(steps):
    f_c = x * st_r + (1 - x) * st_s
    f_d = x * st_t + (1 - x) * st_p
    avg_f = x * f_c + (1 - x) * f_d
    dx = x * (f_c - avg_f) * dt
    x = x + dx
    if x > 1: x = 1
    if x < 0: x = 0
    history.append(x)

# --- 6. 画图展示 (关键修改在这里！) ---
fig, ax = plt.subplots() # ax 在这里才出生！
ax.plot(history, label="合作者比例 (Cooperators)", color='blue', linewidth=2)
ax.plot([1-h for h in history], label="背叛者比例 (Defectors)", color='red', linestyle='--', linewidth=2)

# --- 现在才可以给 ax 设置字体 ---
ax.set_title("策略演化动力学", fontproperties=font_prop, fontsize=15)
ax.set_xlabel("时间 (Time)", fontproperties=font_prop, fontsize=12)
ax.set_ylabel("人口比例 (Ratio)", fontproperties=font_prop, fontsize=12)
ax.legend(prop=font_prop) # 图例字体
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# --- 7. 结论 ---
st.subheader("💡 实验结论")
if history[-1] > 0.95:
    st.success("结果：合作占领了世界！(演化稳定策略是合作)")
elif history[-1] < 0.05:
    st.error("结果：世界陷入了背叛的深渊。(演化稳定策略是背叛)")
else:
    st.warning("结果：合作与背叛共存。(混合均衡)")