import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 设置 Matplotlib 的字体为支持中文的字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为 SimHei（黑体）
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题

# 加载数据
data = pd.read_csv("ecommerce_data.csv", parse_dates=["日期"])

# 页面标题
st.title("电商月报数据看板")

# 数据过滤功能
st.sidebar.header("数据筛选")
start_date = st.sidebar.date_input("开始日期", value=data["日期"].min())
end_date = st.sidebar.date_input("结束日期", value=data["日期"].max())
filtered_data = data[(data["日期"] >= pd.Timestamp(start_date)) & (data["日期"] <= pd.Timestamp(end_date))]

# 核心指标
st.header("核心指标")
total_sales = filtered_data["销售额"].sum()
total_orders = filtered_data["订单量"].sum()
avg_order_value = filtered_data["客单价"].mean()

st.metric(label="总销售额", value=f"{total_sales} 元")
st.metric(label="总订单量", value=f"{total_orders} 单")
st.metric(label="平均客单价", value=f"{avg_order_value:.2f} 元")

# 销售额趋势图
st.header("每日销售额趋势")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(filtered_data["日期"], filtered_data["销售额"], marker='o', linestyle='-', label="销售额")
ax.set_title("每日销售额趋势", fontsize=16)
ax.set_xlabel("日期", fontsize=14)
ax.set_ylabel("销售额 (元)", fontsize=14)  # 添加单位
ax.legend()
plt.xticks(rotation=45, fontsize=12)  # 旋转日期，避免重叠
plt.yticks(fontsize=12)
st.pyplot(fig)

# 商品分类销售额占比
st.header("商品分类销售额占比")
category_sales = filtered_data.groupby("商品分类")["销售额"].sum()

# 解决标签堆叠问题：将部分标签移到图外
fig, ax = plt.subplots(figsize=(8, 8))
explode = [0.05] * len(category_sales)  # 每块区域突出
wedges, texts, autotexts = ax.pie(
    category_sales,
    labels=category_sales.index,
    autopct='%1.1f%%',
    explode=explode,
    startangle=140,
    textprops={'fontsize': 12},
)

# 调整标签位置，防止堆叠
for text in texts:
    text.set_fontsize(12)
for autotext in autotexts:
    autotext.set_fontsize(12)
    autotext.set_color("black")
    autotext.set_text(f"{float(autotext.get_text().strip('%')) * sum(category_sales) / 100:.2f} 元")  # 显示单位

ax.set_title("商品分类销售额占比", fontsize=16)
st.pyplot(fig)

# 地区销售额分布
st.header("地区销售额分布")
region_sales = filtered_data.groupby("地区")["销售额"].sum()
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(region_sales.index, region_sales.values, color='skyblue')
ax.set_title("地区销售额分布", fontsize=16)
ax.set_xlabel("地区", fontsize=14)
ax.set_ylabel("销售额 (元)", fontsize=14)  # 添加单位

# 为每个条形图添加销售额数值
for i, value in enumerate(region_sales.values):
    ax.text(i, value + 10, f'{value:.2f} 元', ha='center', va='bottom', fontsize=12)

plt.xticks(rotation=45, fontsize=12)  # 让地区名称更清晰
plt.yticks(fontsize=12)
st.pyplot(fig)

# 数据表格展示
st.header("数据预览")
st.dataframe(filtered_data)
