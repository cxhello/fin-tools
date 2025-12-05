import streamlit as st
import json
import os

CONFIG_PATH = "config/rate_map.json"


# =============================
# JSON 读写
# =============================
def load_rate_map():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rate_map(data):
    os.makedirs("config", exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


st.title("🧾 服务费率维护工具")


rate_map = load_rate_map()

st.markdown("---")


# =============================
# 新增企业（使用 st.dialog）
# =============================
@st.dialog("新增企业服务费率")
def add_dialog():
    new_name = st.text_input("企业名称")
    new_rate = st.number_input("服务费率（%）", step=0.01)

    col1, col2 = st.columns(2)
    if col1.button("保存"):
        if not new_name.strip():
            st.error("企业名称不能为空")
        else:
            rate_map[new_name] = new_rate
            save_rate_map(rate_map)
            st.success("新增成功！")
            st.rerun()

    if col2.button("取消"):
        st.rerun()


# 点击按钮打开弹窗
if st.button("➕ 新增企业服务费率"):
    add_dialog()


st.markdown("### 📋 企业服务费率列表")

# =============================
# 编辑弹窗
# =============================
@st.dialog("编辑企业服务费率")
def edit_dialog(edit_name):
    st.write(f"正在编辑：**{edit_name}**")

    new_rate = st.number_input(
        "服务费率（%）",
        value=float(rate_map[edit_name]),
        step=0.01
    )

    col1, col2 = st.columns(2)
    if col1.button("保存修改"):
        rate_map[edit_name] = new_rate
        save_rate_map(rate_map)
        st.success("修改成功！")
        st.rerun()

    if col2.button("取消"):
        st.rerun()


# =============================
# 删除弹窗
# =============================
@st.dialog("确认删除")
def delete_dialog(delete_name):
    st.error(f"⚠ 确定要删除 {delete_name} 吗？删除后不可恢复！")

    col1, col2 = st.columns(2)
    if col1.button("确认删除"):
        del rate_map[delete_name]
        save_rate_map(rate_map)
        st.success("删除成功！")
        st.rerun()

    if col2.button("取消"):
        st.rerun()


# =============================
# 列表展示
# =============================
if not rate_map:
    st.info("暂无企业费率数据，请点击上方按钮新增。")
else:
    for name, rate in rate_map.items():
        st.write("---")
        cols = st.columns([4, 2, 2, 2])

        cols[0].write(f"**{name}**")
        cols[1].write(f"{rate}%")

        if cols[2].button("✏ 编辑", key=f"edit_{name}"):
            edit_dialog(name)

        if cols[3].button("🗑 删除", key=f"delete_{name}"):
            delete_dialog(name)
