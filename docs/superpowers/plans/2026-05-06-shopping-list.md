# 购物清单功能实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为618购物节创建一个实用的购物清单管理工具,支持商品分类管理、预算统计和导出功能

**Architecture:** 采用Streamlit框架,使用JSON文件存储数据,模块化设计分为数据持久化层、业务逻辑层和UI层,复用现有项目的架构模式

**Tech Stack:** Streamlit, Pandas, OpenPyXL, JSON

---

## 文件结构

**创建文件:**
- `pages/618购物清单.py` - 主页面文件,包含UI和业务逻辑
- `config/shopping_list.json` - 商品数据存储
- `config/categories.json` - 分类配置

**修改文件:**
- `app.py` - 添加购物清单入口

---

## Task 1: 创建配置文件和数据结构

**Files:**
- Create: `config/categories.json`
- Create: `config/shopping_list.json`

- [ ] **Step 1: 创建分类配置文件**

```json
{
  "categories": ["日用品", "食品", "电子产品", "服装", "美妆护肤", "其他"]
}
```

- [ ] **Step 2: 创建商品数据文件**

```json
[]
```

- [ ] **Step 3: 提交配置文件**

```bash
git add config/categories.json config/shopping_list.json
git commit -m "feat: add shopping list config files"
```

---

## Task 2: 创建数据持久化模块

**Files:**
- Create: `pages/618购物清单.py` (部分)

- [ ] **Step 1: 编写数据持久化模块 - load_data函数**

在`pages/618购物清单.py`文件开头添加:

```python
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from io import BytesIO
from openpyxl.styles import Font, Alignment, PatternFill

SHOPPING_LIST_PATH = "config/shopping_list.json"
CATEGORIES_PATH = "config/categories.json"


def load_data():
    """加载购物清单数据"""
    if not os.path.exists(SHOPPING_LIST_PATH):
        return []
    with open(SHOPPING_LIST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    """保存购物清单数据"""
    os.makedirs("config", exist_ok=True)
    with open(SHOPPING_LIST_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

- [ ] **Step 2: 编写export_to_excel函数**

继续在`pages/618购物清单.py`中添加:

```python
def export_to_excel(items):
    """导出购物清单到Excel"""
    df = pd.DataFrame(items)
    
    if df.empty:
        return None
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="购物清单")
        
        workbook = writer.book
        sheet = writer.sheets["购物清单"]
        
        # 设置列宽
        column_widths = {
            "A": 20,  # 商品名称
            "B": 12,  # 分类
            "C": 8,   # 数量
            "D": 8,   # 单位
            "E": 12,  # 预算价格
            "F": 10,  # 优先级
            "G": 12,  # 平台
            "H": 10,  # 状态
            "I": 12,  # 实际价格
            "J": 20,  # 备注
        }
        
        for col, width in column_widths.items():
            sheet.column_dimensions[col].width = width
        
        # 设置表头样式
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        
        for col in range(1, sheet.max_column + 1):
            cell = sheet.cell(row=1, column=col)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # 设置所有单元格垂直居中
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            for cell in row:
                cell.alignment = Alignment(vertical="center")
    
    return output.getvalue()
```

- [ ] **Step 3: 提交数据持久化模块**

```bash
git add pages/618购物清单.py
git commit -m "feat: add data persistence functions"
```

---

## Task 3: 创建商品管理模块

**Files:**
- Modify: `pages/618购物清单.py`

- [ ] **Step 1: 编写商品管理函数 - add_item**

继续在`pages/618购物清单.py`中添加:

```python
def add_item(name, category, quantity, unit, budget_price, priority, platform, notes=""):
    """新增商品"""
    items = load_data()
    new_item = {
        "id": str(datetime.now().timestamp()),
        "name": name,
        "category": category,
        "quantity": quantity,
        "unit": unit,
        "budget_price": budget_price,
        "priority": priority,
        "platform": platform,
        "status": "待购买",
        "actual_price": 0,
        "notes": notes,
        "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    items.append(new_item)
    save_data(items)
    return new_item
```

- [ ] **Step 2: 编写商品管理函数 - update_item**

继续添加:

```python
def update_item(item_id, **kwargs):
    """更新商品信息"""
    items = load_data()
    for item in items:
        if item["id"] == item_id:
            item.update(kwargs)
            item["updated_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    save_data(items)
```

- [ ] **Step 3: 编写商品管理函数 - delete_item**

继续添加:

```python
def delete_item(item_id):
    """删除商品"""
    items = load_data()
    items = [item for item in items if item["id"] != item_id]
    save_data(items)
```

- [ ] **Step 4: 编写商品管理函数 - toggle_status**

继续添加:

```python
def toggle_status(item_id):
    """切换购买状态"""
    items = load_data()
    status_cycle = ["待购买", "已购买", "已取消"]
    for item in items:
        if item["id"] == item_id:
            current_index = status_cycle.index(item["status"])
            next_index = (current_index + 1) % len(status_cycle)
            item["status"] = status_cycle[next_index]
            item["updated_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    save_data(items)
```

- [ ] **Step 5: 编写商品管理函数 - get_items**

继续添加:

```python
def get_items(category=None, priority=None, status=None):
    """获取商品列表,支持筛选"""
    items = load_data()
    
    if category and category != "全部":
        items = [item for item in items if item["category"] == category]
    
    if priority and priority != "全部":
        items = [item for item in items if item["priority"] == priority]
    
    if status and status != "全部":
        items = [item for item in items if item["status"] == status]
    
    return items
```

- [ ] **Step 6: 提交商品管理模块**

```bash
git add pages/618购物清单.py
git commit -m "feat: add item management functions"
```

---

## Task 4: 创建分类管理模块

**Files:**
- Modify: `pages/618购物清单.py`

- [ ] **Step 1: 编写分类管理函数 - load_categories**

继续添加:

```python
def load_categories():
    """加载分类列表"""
    if not os.path.exists(CATEGORIES_PATH):
        return []
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("categories", [])
```

- [ ] **Step 2: 编写分类管理函数 - save_categories**

继续添加:

```python
def save_categories(categories):
    """保存分类列表"""
    os.makedirs("config", exist_ok=True)
    with open(CATEGORIES_PATH, "w", encoding="utf-8") as f:
        json.dump({"categories": categories}, f, ensure_ascii=False, indent=2)
```

- [ ] **Step 3: 编写分类管理函数 - add_category**

继续添加:

```python
def add_category(category_name):
    """新增分类"""
    categories = load_categories()
    if category_name not in categories:
        categories.append(category_name)
        save_categories(categories)
        return True
    return False
```

- [ ] **Step 4: 编写分类管理函数 - delete_category**

继续添加:

```python
def delete_category(category_name):
    """删除分类"""
    items = load_data()
    # 检查是否有关联商品
    has_items = any(item["category"] == category_name for item in items)
    if has_items:
        return False
    
    categories = load_categories()
    if category_name in categories:
        categories.remove(category_name)
        save_categories(categories)
        return True
    return False
```

- [ ] **Step 5: 提交分类管理模块**

```bash
git add pages/618购物清单.py
git commit -m "feat: add category management functions"
```

---

## Task 5: 创建统计分析模块

**Files:**
- Modify: `pages/618购物清单.py`

- [ ] **Step 1: 编写统计分析函数 - calculate_budget_summary**

继续添加:

```python
def calculate_budget_summary(items):
    """计算预算汇总"""
    total_budget = sum(item.get("budget_price", 0) * item.get("quantity", 1) for item in items)
    spent = sum(item.get("actual_price", 0) for item in items if item["status"] == "已购买")
    remaining = total_budget - spent
    return {
        "total_budget": total_budget,
        "spent": spent,
        "remaining": remaining
    }
```

- [ ] **Step 2: 编写统计分析函数 - calculate_category_stats**

继续添加:

```python
def calculate_category_stats(items):
    """按分类统计"""
    stats = {}
    for item in items:
        category = item.get("category", "未分类")
        if category not in stats:
            stats[category] = {
                "count": 0,
                "budget": 0,
                "spent": 0
            }
        stats[category]["count"] += 1
        stats[category]["budget"] += item.get("budget_price", 0) * item.get("quantity", 1)
        if item["status"] == "已购买":
            stats[category]["spent"] += item.get("actual_price", 0)
    return stats
```

- [ ] **Step 3: 编写统计分析函数 - calculate_priority_stats**

继续添加:

```python
def calculate_priority_stats(items):
    """按优先级统计"""
    stats = {
        "必须": {"count": 0, "budget": 0, "spent": 0},
        "想买": {"count": 0, "budget": 0, "spent": 0},
        "可选": {"count": 0, "budget": 0, "spent": 0}
    }
    
    for item in items:
        priority = item.get("priority", "可选")
        if priority in stats:
            stats[priority]["count"] += 1
            stats[priority]["budget"] += item.get("budget_price", 0) * item.get("quantity", 1)
            if item["status"] == "已购买":
                stats[priority]["spent"] += item.get("actual_price", 0)
    
    return stats
```

- [ ] **Step 4: 编写统计分析函数 - calculate_completion_rate**

继续添加:

```python
def calculate_completion_rate(items):
    """计算购买完成率"""
    if not items:
        return 0
    
    completed = sum(1 for item in items if item["status"] == "已购买")
    return (completed / len(items)) * 100
```

- [ ] **Step 5: 提交统计分析模块**

```bash
git add pages/618购物清单.py
git commit -m "feat: add statistics functions"
```

---

## Task 6: 创建UI界面 - 页面框架和侧边栏

**Files:**
- Modify: `pages/618购物清单.py`

- [ ] **Step 1: 创建页面标题和侧边栏筛选**

继续在`pages/618购物清单.py`中添加UI代码:

```python
# ======================================
#               Web UI
# ======================================
st.title("🛒 618购物清单")

# 侧边栏筛选
st.sidebar.header("🔍 筛选条件")

# 加载分类
categories = load_categories()
category_filter = st.sidebar.selectbox("按分类筛选", ["全部"] + categories)

# 按优先级筛选
priority_filter = st.sidebar.selectbox("按优先级筛选", ["全部", "必须", "想买", "可选"])

# 按状态筛选
status_filter = st.sidebar.selectbox("按状态筛选", ["全部", "待购买", "已购买", "已取消"])

# 获取筛选后的商品
filtered_items = get_items(
    category=category_filter,
    priority=priority_filter,
    status=status_filter
)

# 侧边栏预算统计
st.sidebar.markdown("---")
st.sidebar.header("💰 预算统计")
budget_summary = calculate_budget_summary(load_data())
st.sidebar.metric("总预算", f"¥{budget_summary['total_budget']:.2f}")
st.sidebar.metric("已花费", f"¥{budget_summary['spent']:.2f}")
st.sidebar.metric("剩余预算", f"¥{budget_summary['remaining']:.2f}")
```

- [ ] **Step 2: 提交页面框架**

```bash
git add pages/618购物清单.py
git commit -m "feat: add page framework and sidebar"
```

---

## Task 7: 创建UI界面 - 清单管理Tab

**Files:**
- Modify: `pages/618购物清单.py`

- [ ] **Step 1: 创建Tab结构和新增商品弹窗**

继续添加:

```python
# 创建Tab
tab1, tab2, tab3 = st.tabs(["📝 清单管理", "📊 统计分析", "📥 导出"])

with tab1:
    st.markdown("### 商品列表")
    
    # 新增商品弹窗
    @st.dialog("新增商品")
    def add_item_dialog():
        name = st.text_input("商品名称 *")
        categories = load_categories()
        category = st.selectbox("分类 *", categories)
        col1, col2 = st.columns(2)
        quantity = col1.number_input("数量 *", min_value=1, value=1)
        unit = col2.text_input("单位", value="个")
        budget_price = st.number_input("预算价格 *", min_value=0.0, step=0.01)
        priority = st.selectbox("优先级 *", ["必须", "想买", "可选"])
        platform = st.selectbox("购买平台", ["淘宝", "天猫", "京东", "拼多多", "其他"])
        notes = st.text_area("备注")
        
        col1, col2 = st.columns(2)
        if col1.button("保存", use_container_width=True):
            if not name.strip():
                st.error("商品名称不能为空")
            else:
                add_item(name, category, quantity, unit, budget_price, priority, platform, notes)
                st.success("新增成功!")
                st.rerun()
        
        if col2.button("取消", use_container_width=True):
            st.rerun()
    
    if st.button("➕ 新增商品", use_container_width=True):
        add_item_dialog()
    
    st.markdown("---")
```

- [ ] **Step 2: 创建商品卡片展示**

继续添加:

```python
    # 商品列表展示
    if not filtered_items:
        st.info("暂无商品,请点击上方按钮新增")
    else:
        for item in filtered_items:
            # 优先级标识
            priority_emoji = {"必须": "🔴", "想买": "🟡", "可选": "⚪"}
            # 状态标识
            status_emoji = {"待购买": "🛒", "已购买": "✅", "已取消": "❌"}
            
            with st.container():
                cols = st.columns([4, 3, 3])
                
                # 左侧: 商品信息
                with cols[0]:
                    st.write(f"**{item['name']}**")
                    st.caption(f"📦 {item['quantity']}{item['unit']} | 💰 ¥{item['budget_price']:.2f}")
                    st.caption(f"📂 {item['category']} | 🏪 {item['platform']}")
                
                # 中间: 状态和优先级
                with cols[1]:
                    st.write(f"{status_emoji.get(item['status'], '')} {item['status']}")
                    st.write(f"{priority_emoji.get(item['priority'], '')} {item['priority']}")
                
                # 右侧: 操作按钮
                with cols[2]:
                    c1, c2, c3 = st.columns(3)
                    
                    # 状态切换按钮
                    if c1.button("🔄", key=f"toggle_{item['id']}", help="切换状态"):
                        toggle_status(item['id'])
                        st.rerun()
                    
                    # 编辑按钮
                    if c2.button("✏️", key=f"edit_{item['id']}", help="编辑"):
                        st.session_state.edit_item_id = item['id']
                        st.rerun()
                    
                    # 删除按钮
                    if c3.button("🗑️", key=f"delete_{item['id']}", help="删除"):
                        st.session_state.delete_item_id = item['id']
                        st.rerun()
                
                st.markdown("---")
```

- [ ] **Step 3: 创建编辑商品弹窗**

继续添加:

```python
# 编辑商品弹窗
if "edit_item_id" in st.session_state:
    item_to_edit = next((item for item in load_data() if item["id"] == st.session_state.edit_item_id), None)
    
    if item_to_edit:
        @st.dialog("编辑商品")
        def edit_item_dialog(item):
            name = st.text_input("商品名称", value=item["name"])
            categories = load_categories()
            category_index = categories.index(item["category"]) if item["category"] in categories else 0
            category = st.selectbox("分类", categories, index=category_index)
            
            col1, col2 = st.columns(2)
            quantity = col1.number_input("数量", min_value=1, value=item["quantity"])
            unit = col2.text_input("单位", value=item["unit"])
            
            budget_price = st.number_input("预算价格", min_value=0.0, value=item["budget_price"], step=0.01)
            priority_index = ["必须", "想买", "可选"].index(item["priority"]) if item["priority"] in ["必须", "想买", "可选"] else 0
            priority = st.selectbox("优先级", ["必须", "想买", "可选"], index=priority_index)
            
            platforms = ["淘宝", "天猫", "京东", "拼多多", "其他"]
            platform_index = platforms.index(item["platform"]) if item["platform"] in platforms else 0
            platform = st.selectbox("购买平台", platforms, index=platform_index)
            
            notes = st.text_area("备注", value=item.get("notes", ""))
            
            # 如果已购买,显示实际价格输入
            if item["status"] == "已购买":
                actual_price = st.number_input("实际价格", min_value=0.0, value=item.get("actual_price", 0), step=0.01)
            else:
                actual_price = item.get("actual_price", 0)
            
            col1, col2 = st.columns(2)
            if col1.button("保存修改", use_container_width=True):
                update_item(
                    item["id"],
                    name=name,
                    category=category,
                    quantity=quantity,
                    unit=unit,
                    budget_price=budget_price,
                    priority=priority,
                    platform=platform,
                    notes=notes,
                    actual_price=actual_price
                )
                st.success("修改成功!")
                del st.session_state.edit_item_id
                st.rerun()
            
            if col2.button("取消", use_container_width=True):
                del st.session_state.edit_item_id
                st.rerun()
        
        edit_item_dialog(item_to_edit)
```

- [ ] **Step 4: 创建删除确认弹窗**

继续添加:

```python
# 删除确认弹窗
if "delete_item_id" in st.session_state:
    item_to_delete = next((item for item in load_data() if item["id"] == st.session_state.delete_item_id), None)
    
    if item_to_delete:
        @st.dialog("确认删除")
        def delete_item_dialog(item):
            st.warning(f"⚠️ 确定要删除商品 **{item['name']}** 吗? 删除后不可恢复!")
            
            col1, col2 = st.columns(2)
            if col1.button("确认删除", use_container_width=True):
                delete_item(item["id"])
                st.success("删除成功!")
                del st.session_state.delete_item_id
                st.rerun()
            
            if col2.button("取消", use_container_width=True):
                del st.session_state.delete_item_id
                st.rerun()
        
        delete_item_dialog(item_to_delete)
```

- [ ] **Step 5: 提交清单管理Tab**

```bash
git add pages/618购物清单.py
git commit -m "feat: add item management UI with dialogs"
```

---

## Task 8: 创建UI界面 - 统计分析Tab

**Files:**
- Modify: `pages/618购物清单.py`

- [ ] **Step 1: 创建统计分析Tab内容**

继续添加:

```python
with tab2:
    st.markdown("### 📊 统计分析")
    
    all_items = load_data()
    
    if not all_items:
        st.info("暂无数据,请先添加商品")
    else:
        # 预算使用情况
        st.markdown("#### 💰 预算使用情况")
        budget_summary = calculate_budget_summary(all_items)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("总预算", f"¥{budget_summary['total_budget']:.2f}")
        col2.metric("已花费", f"¥{budget_summary['spent']:.2f}")
        col3.metric("剩余预算", f"¥{budget_summary['remaining']:.2f}")
        
        # 进度条
        if budget_summary['total_budget'] > 0:
            progress = budget_summary['spent'] / budget_summary['total_budget']
            st.progress(min(progress, 1.0))
            st.caption(f"预算使用率: {progress*100:.1f}%")
        
        st.markdown("---")
        
        # 购买完成率
        st.markdown("#### ✅ 购买完成率")
        completion_rate = calculate_completion_rate(all_items)
        st.metric("完成率", f"{completion_rate:.1f}%")
        
        st.markdown("---")
        
        # 按分类统计
        st.markdown("#### 📂 按分类统计")
        category_stats = calculate_category_stats(all_items)
        
        for category, stats in category_stats.items():
            with st.expander(f"{category} ({stats['count']}件)"):
                col1, col2, col3 = st.columns(3)
                col1.metric("预算", f"¥{stats['budget']:.2f}")
                col2.metric("已花费", f"¥{stats['spent']:.2f}")
                col3.metric("商品数", stats['count'])
        
        st.markdown("---")
        
        # 按优先级统计
        st.markdown("#### 🎯 按优先级统计")
        priority_stats = calculate_priority_stats(all_items)
        
        for priority, stats in priority_stats.items():
            priority_emoji = {"必须": "🔴", "想买": "🟡", "可选": "⚪"}
            with st.expander(f"{priority_emoji.get(priority, '')} {priority} ({stats['count']}件)"):
                col1, col2, col3 = st.columns(3)
                col1.metric("预算", f"¥{stats['budget']:.2f}")
                col2.metric("已花费", f"¥{stats['spent']:.2f}")
                col3.metric("商品数", stats['count'])
```

- [ ] **Step 2: 提交统计分析Tab**

```bash
git add pages/618购物清单.py
git commit -m "feat: add statistics analysis tab"
```

---

## Task 9: 创建UI界面 - 导出功能Tab

**Files:**
- Modify: `pages/618购物清单.py`

- [ ] **Step 1: 创建导出功能Tab内容**

继续添加:

```python
with tab3:
    st.markdown("### 📥 导出购物清单")
    
    all_items = load_data()
    
    if not all_items:
        st.info("暂无数据,无法导出")
    else:
        st.write(f"当前清单共 **{len(all_items)}** 件商品")
        
        # 显示筛选后的商品数量
        if filtered_items and len(filtered_items) != len(all_items):
            st.write(f"筛选后共 **{len(filtered_items)}** 件商品")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        # 导出全部商品
        with col1:
            st.markdown("#### 导出全部商品")
            excel_data = export_to_excel(all_items)
            if excel_data:
                st.download_button(
                    label="📥 下载全部清单",
                    data=excel_data,
                    file_name=f"购物清单_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        # 导出筛选后商品
        with col2:
            st.markdown("#### 导出筛选后商品")
            if filtered_items and len(filtered_items) != len(all_items):
                excel_data_filtered = export_to_excel(filtered_items)
                if excel_data_filtered:
                    st.download_button(
                        label="📥 下载筛选清单",
                        data=excel_data_filtered,
                        file_name=f"购物清单_筛选_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            else:
                st.info("未应用筛选条件")
```

- [ ] **Step 2: 提交导出功能Tab**

```bash
git add pages/618购物清单.py
git commit -m "feat: add export functionality tab"
```

---

## Task 10: 创建分类管理UI

**Files:**
- Modify: `pages/618购物清单.py`

- [ ] **Step 1: 在侧边栏添加分类管理**

修改侧边栏部分,在预算统计下方添加:

```python
# 在侧边栏预算统计下方添加
st.sidebar.markdown("---")
st.sidebar.header("📂 分类管理")

# 新增分类弹窗
@st.dialog("新增分类")
def add_category_dialog():
    new_category = st.text_input("分类名称")
    
    col1, col2 = st.columns(2)
    if col1.button("保存", use_container_width=True):
        if not new_category.strip():
            st.error("分类名称不能为空")
        else:
            if add_category(new_category):
                st.success("新增成功!")
                st.rerun()
            else:
                st.warning("该分类已存在")
    
    if col2.button("取消", use_container_width=True):
        st.rerun()

if st.sidebar.button("➕ 新增分类", use_container_width=True):
    add_category_dialog()

# 显示分类列表
categories = load_categories()
for cat in categories:
    cols = st.sidebar.columns([3, 1])
    cols[0].write(f"• {cat}")
    
    # 删除分类按钮
    if cols[1].button("🗑️", key=f"del_cat_{cat}", help="删除分类"):
        if delete_category(cat):
            st.success(f"已删除分类: {cat}")
            st.rerun()
        else:
            st.error("该分类下有关联商品,无法删除")
```

- [ ] **Step 2: 提交分类管理UI**

```bash
git add pages/618购物清单.py
git commit -m "feat: add category management UI in sidebar"
```

---

## Task 11: 更新主页面入口

**Files:**
- Modify: `app.py`

- [ ] **Step 1: 在app.py中添加购物清单入口**

修改`app.py`文件:

```python
import streamlit as st

st.title("财务自动化工具合集")

st.markdown("""
欢迎使用自动化工具平台!请选择左侧菜单进入具体工具。

当前支持:

- 🧾 **支付宝账单对账工具**
- 📊 **服务费率维护工具**
- 🛒 **618购物清单**

如需新增功能,请联系开发同学 😄
""")
```

- [ ] **Step 2: 提交主页面更新**

```bash
git add app.py
git commit -m "feat: add shopping list entry in main page"
```

---

## 实施说明

本计划按照模块化设计,分为以下步骤:
1. 创建配置文件和数据结构
2. 实现数据持久化模块
3. 实现商品管理核心功能
4. 实现分类管理功能
5. 实现统计分析功能
6. 构建UI界面(页面框架、清单管理、统计分析、导出功能)
7. 添加分类管理UI
8. 更新主页面入口

每个任务都是独立的,可以逐个实现和测试。所有功能都遵循现有项目的代码风格和架构模式。