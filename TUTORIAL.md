# 教材 / Tutorial
## 从 Python 脚本到网页应用 · From Python Script to Web App
### Glassfabriken ERP — 完整学习指南 · Complete Learning Guide

---

> **如何使用本教材 / How to use this guide**
>
> 每个概念都有 **中文解释** 和 **English explanation**，然后是代码示例。
> Every concept has a Chinese explanation and an English explanation, followed by code examples.

---

## 目录 / Table of Contents

1. [项目结构 / Project Structure](#1)
2. [Python 类 / Python Classes](#2)
3. [文件读写：CSV 和 JSON / File I/O: CSV and JSON](#3)
4. [Flask — 让 Python 变成网页服务器 / Flask — Making Python a Web Server](#4)
5. [HTML + JavaScript — 网页界面 / HTML + JavaScript — Web Interface](#5)
6. [Bootstrap — 好看的界面 / Bootstrap — Beautiful UI](#6)
7. [Font Awesome — 图标 / Font Awesome — Icons](#7)
8. [启动项目 / Starting the Project](#8)
9. [可复用的代码模式 / Reusable Code Patterns](#9)
10. [常见错误与解决方法 / Common Errors and Solutions](#10)

---

<a name="1"></a>
## 1. 项目结构 / Project Structure

### 中文
一个好的项目要把文件分门别类。我们的规则是：
- **逻辑**（计算、数据）放在 Python 文件里
- **网页**（用户看到的界面）放在 HTML 文件里
- **数据**（CSV、JSON）放在 `data/` 文件夹里

### English
A good project separates concerns. Our rule:
- **Logic** (calculations, data) goes in Python files
- **Interface** (what the user sees) goes in HTML files
- **Data** (CSV, JSON) goes in the `data/` folder

```
glassfabriken/
├── data/
│   ├── customers.csv    ← 客户列表 / customer list
│   ├── products.csv     ← 库存列表 / inventory list
│   └── orders.json      ← 已保存的订单 / saved orders
│
├── erp.py               ← 所有业务逻辑（类和函数）
│                           All business logic (classes & functions)
│
├── app.py               ← 网页服务器（Flask）
│                           Web server (Flask)
│
├── templates/
│   └── index.html       ← 用户看到的网页
│                           The webpage the user sees
│
└── requirements.txt     ← 需要安装的包 / packages to install
```

### 关键概念 / Key Concept

```
用户的浏览器  ←→  app.py (Flask)  ←→  erp.py (逻辑)  ←→  data/ (文件)
User Browser  ←→  app.py (Flask)  ←→  erp.py (Logic)  ←→  data/ (Files)
```

---

<a name="2"></a>
## 2. Python 类 / Python Classes

### 中文
**类（Class）** 是创建对象的模板。比如"客户"这个概念，每个客户都有名字、地址、折扣——用类来表示非常合适。

**为什么用类？**
- 把相关的数据打包在一起
- 可以给数据添加方法（函数）
- 代码更清晰、更容易复用

### English
A **class** is a blueprint for creating objects. The concept of "Customer" — every customer has a name, address, and discount — is a perfect fit for a class.

**Why use classes?**
- Bundle related data together
- Attach methods (functions) to the data
- Code becomes cleaner and reusable

```python
# ── 定义类 / Define a class ──────────────────────
class Customer:
    # __init__ 在创建对象时自动调用
    # __init__ is called automatically when creating an object
    def __init__(self, customer_id, name, address, discount_pct):
        self.customer_id = customer_id    # self. 表示"属于这个对象"
        self.name = name                  # self. means "belongs to this object"
        self.address = address
        self.discount_pct = float(discount_pct)

    # to_dict() 把对象转成字典，方便发送给网页
    # to_dict() converts the object to a dict, easy to send to web
    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "address": self.address,
            "discount_pct": self.discount_pct,
        }

    # __str__ 决定 print() 显示什么
    # __str__ decides what print() shows
    def __str__(self):
        return f"{self.customer_id} – {self.name}"


# ── 使用类 / Using a class ───────────────────────
kund = Customer("C1001", "Alfa Livs", "Alfavägen 1", 10)

print(kund.name)          # → Alfa Livs
print(kund.discount_pct)  # → 10.0
print(kund)               # → C1001 – Alfa Livs
print(kund.to_dict())     # → {"customer_id": "C1001", ...}
```

### 继承的思路 / Inheritance idea（扩展知识）

```python
# 如果以后想创建"VIP客户"，可以继承 Customer
# If you later want a "VIP Customer", you can inherit from Customer
class VIPCustomer(Customer):
    def __init__(self, customer_id, name, address):
        super().__init__(customer_id, name, address, discount_pct=20)
        self.is_vip = True
```

---

<a name="3"></a>
## 3. 文件读写：CSV 和 JSON / File I/O: CSV and JSON

### CSV 文件

#### 中文
CSV（逗号分隔值）是最简单的表格格式，用 Excel 也能打开。

#### English
CSV (Comma-Separated Values) is the simplest table format, also openable in Excel.

```python
import csv

# ── 读取 CSV / Read CSV ──────────────────────────
with open("data/customers.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)      # 第一行自动变成 key
                                    # First row automatically becomes keys
    for row in reader:
        print(row["name"])          # → Alfa Livs, Bravo Kiosk, ...
        print(row["discount_pct"])  # → 10, 0, 5, ...


# ── 写入 CSV / Write CSV ─────────────────────────
with open("data/customers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["customer_id", "name", "address", "discount_pct"])  # 标题行 / Header
    writer.writerow(["C1001", "Alfa Livs", "Alfavägen 1", 10])
    writer.writerow(["C1002", "Bravo Kiosk", "Brunnsgatan 7", 0])
```

### JSON 文件

#### 中文
JSON 是网络上最常用的数据格式。Python 的列表/字典可以直接转成 JSON。

#### English
JSON is the most common data format on the web. Python lists/dicts convert directly to JSON.

```python
import json

# ── 读取 JSON / Read JSON ────────────────────────
with open("data/orders.json", encoding="utf-8") as f:
    orders = json.load(f)    # JSON → Python 列表或字典 / list or dict
    print(orders[0]["order_id"])   # → O-2026-0001


# ── 写入 JSON / Write JSON ───────────────────────
orders = [
    {"order_id": "O-2026-0001", "customer_id": "C1001"},
    {"order_id": "O-2026-0002", "customer_id": "C1003"},
]
with open("data/orders.json", "w", encoding="utf-8") as f:
    json.dump(orders, f, indent=2, ensure_ascii=False)
    # indent=2        → 漂亮的缩进格式 / pretty formatting
    # ensure_ascii=False → 允许中文/瑞典语 / allow non-ASCII characters
```

### 重要：总是用 encoding="utf-8" / Always use encoding="utf-8"

```python
# ✅ 正确 / Correct
with open("file.csv", encoding="utf-8") as f: ...

# ❌ 可能出错（Windows 默认 cp1252）/ May break on Windows
with open("file.csv") as f: ...
```

---

<a name="4"></a>
## 4. Flask — 让 Python 变成网页服务器 / Flask — Making Python a Web Server

### 中文
Flask 是一个轻量级的 Python 网页框架。它让你的 Python 函数变成可以通过浏览器访问的"地址"（URL）。

### English
Flask is a lightweight Python web framework. It turns your Python functions into "addresses" (URLs) accessible via a browser.

```bash
# 安装 / Install
pip install flask
```

### 基础概念 / Basic Concepts

```python
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)   # 创建应用 / Create the app


# ── @app.route 装饰器 / decorator ────────────────
# 把函数绑定到一个 URL 地址
# Binds a function to a URL address

@app.route("/")                    # 访问 http://localhost:5000/ 时调用
def index():                       # Called when visiting http://localhost:5000/
    return render_template("index.html")   # 返回 HTML 文件 / Return HTML file


# ── GET 请求：返回数据 / Return data ─────────────
@app.route("/api/customers")
def get_customers():
    data = [{"id": "C1001", "name": "Alfa Livs"}]
    return jsonify(data)    # 自动转成 JSON / Auto-converts to JSON
    # 浏览器收到: [{"id": "C1001", "name": "Alfa Livs"}]


# ── POST 请求：接收数据 / Receive data ────────────
@app.route("/api/customers", methods=["POST"])
def add_customer():
    data = request.get_json()    # 读取浏览器发来的 JSON / Read JSON from browser
    name = data["name"]
    # ... 保存客户 / save customer ...
    return jsonify({"ok": True}), 201    # 201 = "已创建" / "Created"


# ── 启动服务器 / Start server ────────────────────
if __name__ == "__main__":
    app.run(debug=True)    # debug=True → 保存文件后自动重启 / auto-restart on save
```

### HTTP 方法 / HTTP Methods

| 方法/Method | 用途/Purpose | 例子/Example |
|-------------|-------------|-------------|
| `GET`    | 获取数据 / Fetch data | 查看所有客户 / View all customers |
| `POST`   | 创建新数据 / Create new data | 添加客户 / Add customer |
| `PUT`    | 更新数据 / Update data | 修改客户信息 / Edit customer |
| `DELETE` | 删除数据 / Delete data | 删除客户 / Delete customer |

### HTTP 状态码 / HTTP Status Codes

| 代码/Code | 含义/Meaning |
|-----------|-------------|
| `200` | 成功 / OK |
| `201` | 已创建 / Created |
| `400` | 请求有误 / Bad request |
| `404` | 未找到 / Not found |
| `500` | 服务器错误 / Server error |

---

<a name="5"></a>
## 5. HTML + JavaScript — 网页界面 / Web Interface

### 中文
HTML 决定网页的**结构**，CSS 决定**外观**，JavaScript 决定**行为**（比如按钮点击后发生什么）。

### English
HTML defines the **structure**, CSS defines the **appearance**, JavaScript defines the **behavior** (e.g., what happens when you click a button).

### fetch() — 浏览器和 Flask 之间的桥梁 / The bridge between browser and Flask

```javascript
// ── GET：从服务器获取数据 / Fetch data from server ──
async function loadCustomers() {
    // fetch() 发送 HTTP 请求 / sends an HTTP request
    const response = await fetch('/api/customers');
    const customers = await response.json();   // JSON → JS 数组 / array

    // 把数据填入表格 / Fill data into table
    const tbody = document.querySelector('#my-table tbody');
    tbody.innerHTML = customers.map(c => `
        <tr>
            <td>${c.customer_id}</td>
            <td>${c.name}</td>
            <td>${c.discount_pct}%</td>
        </tr>
    `).join('');
}


// ── POST：发送数据到服务器 / Send data to server ──
async function addCustomer() {
    const newCustomer = {
        customer_id: document.getElementById('input-id').value,
        name: document.getElementById('input-name').value,
        discount_pct: 10
    };

    const response = await fetch('/api/customers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },  // 告诉服务器格式 / Tell server the format
        body: JSON.stringify(newCustomer)                  // JS对象 → JSON字符串 / Object → JSON string
    });

    if (response.ok) {
        alert('客户添加成功！/ Customer added!');
        loadCustomers();    // 刷新列表 / Refresh list
    } else {
        const error = await response.json();
        alert('错误：' + error.error);
    }
}
```

### 完整数据流程 / Complete Data Flow

```
用户点击"添加"按钮
User clicks "Add" button
        ↓
JavaScript 的 addCustomer() 运行
JavaScript's addCustomer() runs
        ↓
fetch() 发送 POST 请求到 /api/customers
fetch() sends POST request to /api/customers
        ↓
Flask 的 add_customer() 函数运行
Flask's add_customer() function runs
        ↓
erp.add_customer() 验证并保存数据
erp.add_customer() validates and saves data
        ↓
Flask 返回 JSON {"customer_id": ..., "name": ...}
Flask returns JSON
        ↓
JavaScript 收到结果，更新网页
JavaScript receives result, updates page
```

---

<a name="6"></a>
## 6. Bootstrap 5 — 好看的界面无需写大量 CSS / Beautiful UI Without Writing Lots of CSS

### 中文
Bootstrap 是一个 CSS 框架。只需在 HTML 元素上加上特定的 class 名称，就能得到漂亮的样式，不用自己写 CSS。

### English
Bootstrap is a CSS framework. Just add specific class names to HTML elements to get beautiful styling — no need to write CSS yourself.

### 引入 Bootstrap / Include Bootstrap

```html
<!-- 放在 <head> 里 / Put inside <head> -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- 放在 </body> 前 / Put before </body> -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
```

### 常用组件 / Common Components

```html
<!-- ── 按钮 / Buttons ── -->
<button class="btn btn-primary">蓝色按钮 / Blue</button>
<button class="btn btn-success">绿色按钮 / Green</button>
<button class="btn btn-danger">红色按钮 / Red</button>
<button class="btn btn-outline-secondary">边框按钮 / Outline</button>
<button class="btn btn-sm btn-primary">小按钮 / Small button</button>
<button class="btn btn-lg btn-primary">大按钮 / Large button</button>

<!-- ── 输入框 / Input fields ── -->
<input class="form-control" placeholder="输入文字 / Enter text">
<select class="form-select">
    <option>选项1 / Option 1</option>
</select>

<!-- ── 表格 / Table ── -->
<table class="table table-hover table-striped">
    <thead class="table-dark">
        <tr><th>列1 / Col1</th><th>列2 / Col2</th></tr>
    </thead>
    <tbody>
        <tr><td>数据 / Data</td><td>数据 / Data</td></tr>
    </tbody>
</table>

<!-- ── 网格布局（自动分列）/ Grid layout ── -->
<div class="row">
    <div class="col-md-6">左半边 / Left half</div>
    <div class="col-md-6">右半边 / Right half</div>
</div>

<div class="row g-3">   <!-- g-3 = 间距 / spacing -->
    <div class="col-md-4">三分之一 / One third</div>
    <div class="col-md-4">三分之一 / One third</div>
    <div class="col-md-4">三分之一 / One third</div>
</div>

<!-- ── 卡片 / Card ── -->
<div class="card shadow-sm">
    <div class="card-body">
        <h5 class="card-title">标题 / Title</h5>
        <p class="card-text">内容 / Content</p>
    </div>
</div>

<!-- ── 徽章 / Badge ── -->
<span class="badge bg-primary">新 / New</span>
<span class="badge bg-success">库存充足 / In stock</span>
<span class="badge bg-danger">库存不足 / Low stock</span>

<!-- ── 弹窗 / Modal ── -->
<button data-bs-toggle="modal" data-bs-target="#myModal">打开弹窗 / Open modal</button>

<div class="modal fade" id="myModal">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">标题 / Title</h5>
                <button class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">内容 / Content</div>
        </div>
    </div>
</div>
```

### 常用工具类 / Utility Classes

```html
<!-- 文字 / Text -->
<p class="fw-bold">粗体 / Bold</p>
<p class="text-muted">灰色文字 / Muted text</p>
<p class="text-center">居中 / Center</p>
<p class="text-end">右对齐 / Right-align</p>
<p class="text-primary">蓝色 / Blue</p>
<p class="text-danger">红色 / Red</p>

<!-- 间距（m=margin外边距, p=padding内边距, 数字0-5）/ Spacing -->
<div class="mt-3">上方外边距 / Margin top</div>
<div class="mb-2">下方外边距 / Margin bottom</div>
<div class="p-3">内边距 / Padding</div>
<div class="px-4">左右内边距 / Horizontal padding</div>

<!-- 显示 / Display -->
<div class="d-flex gap-2">   <!-- 横向排列 / Horizontal layout -->
    <button>A</button>
    <button>B</button>
</div>
<div class="d-grid">         <!-- 全宽按钮 / Full-width button -->
    <button class="btn btn-primary">全宽 / Full width</button>
</div>
```

---

<a name="7"></a>
## 7. Font Awesome — 图标 / Icons

### 中文
Font Awesome 提供数千个矢量图标，用 `<i>` 标签引入。

### English
Font Awesome provides thousands of vector icons, added with an `<i>` tag.

```html
<!-- 引入 / Include (放在 <head>) -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">

<!-- 使用方式 / Usage -->
<i class="fa-solid fa-[图标名]"></i>
```

### 常用图标 / Common Icons

```html
<i class="fa-solid fa-users"></i>           <!-- 用户/客户 / Users/Customers -->
<i class="fa-solid fa-boxes-stacked"></i>   <!-- 库存 / Inventory -->
<i class="fa-solid fa-cart-plus"></i>       <!-- 新订单 / New order -->
<i class="fa-solid fa-receipt"></i>         <!-- 收据 / Receipt -->
<i class="fa-solid fa-plus"></i>            <!-- 加号 / Plus -->
<i class="fa-solid fa-trash"></i>           <!-- 删除 / Delete -->
<i class="fa-solid fa-eye"></i>             <!-- 查看 / View -->
<i class="fa-solid fa-pen-to-square"></i>   <!-- 编辑 / Edit -->
<i class="fa-solid fa-check"></i>           <!-- 确认 / Confirm -->
<i class="fa-solid fa-xmark"></i>           <!-- 关闭 / Close -->
<i class="fa-solid fa-magnifying-glass"></i><!-- 搜索 / Search -->
<i class="fa-solid fa-gauge-high"></i>      <!-- 仪表盘 / Dashboard -->
<i class="fa-solid fa-ice-cream"></i>       <!-- 冰淇淋 / Ice cream -->
<i class="fa-solid fa-clock-rotate-left"></i><!-- 历史 / History -->

<!-- 搜索更多图标 / Find more icons: https://fontawesome.com/icons -->
```

### 结合 Bootstrap 使用 / Combine with Bootstrap

```html
<!-- 图标 + 文字按钮 / Icon + text button -->
<button class="btn btn-success">
    <i class="fa-solid fa-plus me-2"></i>添加 / Add
</button>

<!-- 纯图标按钮 / Icon-only button -->
<button class="btn btn-outline-primary btn-sm">
    <i class="fa-solid fa-eye"></i>
</button>

<!-- 带图标的标题 / Title with icon -->
<h5><i class="fa-solid fa-users me-2 text-primary"></i>客户列表 / Customer List</h5>
```

---

<a name="8"></a>
## 8. 启动项目 / Starting the Project

### 第一次启动 / First time

```bash
# 1. 打开终端，进入项目文件夹
#    Open terminal, navigate to project folder
cd C:\Users\hkdse\Desktop\glassfabriken

# 2. 安装 Flask（只需一次）
#    Install Flask (only once)
pip install flask

# 3. 启动服务器
#    Start the server
python app.py
```

### 你会看到 / You will see

```
==================================================
  Glassfabriken ERP startar...
  Öppna: http://localhost:5000
==================================================
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 4. 打开浏览器 / Open browser

```
http://localhost:5000
```

### 停止服务器 / Stop server

```
按 Ctrl + C / Press Ctrl + C
```

---

<a name="9"></a>
## 9. 可复用的代码模式 / Reusable Code Patterns

这些模式可以用在你未来的任何项目里。
These patterns can be used in any of your future projects.

---

### 模式 1：类 + to_dict() / Pattern 1: Class + to_dict()

#### 中文
系统里每种"东西"（客户、产品、订单）都应该有自己的类。
永远都加一个 `to_dict()` 方法，这样就能轻松转成 JSON 发给网页。

#### English
Every "thing" in the system (customer, product, order) should have its own class.
Always add a `to_dict()` method — this makes it easy to convert to JSON for the web.

```python
class AnyThing:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):           # ← 始终添加这个 / Always add this
        return {"id": self.id, "name": self.name}
```

---

### 模式 2：管理类 / Pattern 2: Manager Class

#### 中文
创建一个"总管理"类，负责加载数据、查找、添加、保存。
其他代码只需要和这个类打交道，不需要直接操作文件。

#### English
Create one "manager" class responsible for loading, finding, adding, and saving data.
Other code only needs to interact with this class — not directly with files.

```python
class SystemManager:
    def __init__(self):
        self.items = {}
        self.load()             # 启动时加载 / Load on startup

    def load(self):
        # 读文件 / Read file
        ...

    def save(self):
        # 写文件 / Write file
        ...

    def find(self, identifier):
        # 查找 / Find
        return self.items.get(identifier)

    def add(self, id, name):
        if id in self.items:
            return False, "已存在 / Already exists"
        self.items[id] = AnyThing(id, name)
        self.save()
        return True, self.items[id]
```

---

### 模式 3：先验证，后执行 / Pattern 3: Validate First, Act Later

#### 中文
在修改任何数据之前，先检查所有可能的错误。
一旦发现问题就立即返回错误，不要继续执行。

#### English
Before modifying any data, check all possible errors first.
Once a problem is found, return the error immediately — don't continue.

```python
def process(self, customer_id, product_id, qty):
    # ── 第一步：验证所有输入 / Step 1: Validate all inputs ──
    customer = self.find_customer(customer_id)
    if not customer:
        return None, f"客户 {customer_id} 不存在 / Customer not found"

    product = self.find_product(product_id)
    if not product:
        return None, f"产品 {product_id} 不存在 / Product not found"

    if product.stock < qty:
        return None, f"库存不足 / Insufficient stock: {product.stock} < {qty}"

    # ── 第二步：所有验证通过，执行操作 / Step 2: All valid, execute ──
    product.stock -= qty
    self.save()
    return result, None    # None 表示没有错误 / None means no error


# ── 调用方式 / How to call ──────────────────────
result, error = system.process("C1001", "10001", 5)
if error:
    print(f"错误 / Error: {error}")
else:
    print(f"成功 / Success: {result}")
```

---

### 模式 4：Flask API + fetch() 流水线 / Pattern 4: Flask API + fetch() Pipeline

#### 中文
这是 Python 网页应用最核心的模式：Python 处理逻辑，JavaScript 更新界面。

#### English
This is the core pattern for Python web apps: Python handles logic, JavaScript updates the UI.

```
Python 类 (erp.py)
    ↓ 提供数据 / Provides data
Flask 路由 (app.py)
    ↓ 返回 JSON / Returns JSON
fetch() 请求 (index.html)
    ↓ 更新 HTML / Updates HTML
用户看到结果 / User sees result
```

```python
# app.py 里 / In app.py
@app.route("/api/items", methods=["GET"])
def get_items():
    return jsonify([i.to_dict() for i in manager.items.values()])

@app.route("/api/items", methods=["POST"])
def add_item():
    data = request.get_json()
    ok, result = manager.add(data["id"], data["name"])
    if ok:
        return jsonify(result.to_dict()), 201
    return jsonify({"error": result}), 400
```

```javascript
// index.html 里 / In index.html
async function loadItems() {
    const items = await fetch('/api/items').then(r => r.json());
    document.querySelector('tbody').innerHTML =
        items.map(i => `<tr><td>${i.id}</td><td>${i.name}</td></tr>`).join('');
}

async function addItem(id, name) {
    const res = await fetch('/api/items', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id, name})
    });
    const data = await res.json();
    if (res.ok) {
        loadItems();          // 刷新列表 / Refresh list
    } else {
        alert(data.error);    // 显示错误 / Show error
    }
}
```

---

### 模式 5：自动生成 ID / Pattern 5: Auto-generate IDs

#### 中文
让系统自动生成唯一 ID，避免重复和手动输入错误。

#### English
Let the system auto-generate unique IDs to avoid duplicates and manual input errors.

```python
from datetime import datetime

def generate_order_id(self):
    year = datetime.now().year     # 当前年份 / Current year
    prefix = f"O-{year}-"
    max_num = 0

    for order in self.get_all_orders():
        oid = order.get("order_id", "")
        if oid.startswith(prefix):
            num = int(oid[len(prefix):])      # 提取数字部分 / Extract the number
            max_num = max(max_num, num)

    return f"{prefix}{max_num + 1:04d}"       # :04d → 4位数字，不足补0
                                              # :04d → 4 digits, zero-padded
# 结果 / Results: O-2026-0001, O-2026-0002, O-2026-0003 ...
```

---

<a name="10"></a>
## 10. 常见错误与解决方法 / Common Errors and Solutions

| 错误 / Error | 原因 / Cause | 解决方法 / Solution |
|-------------|-------------|-------------------|
| `ModuleNotFoundError: flask` | Flask 未安装 / Not installed | `pip install flask` |
| 网页无法打开 / Page won't load | 服务器没运行 / Server not running | 运行 `python app.py` |
| `UnicodeDecodeError` | 文件编码问题 / Encoding issue | 加上 `encoding="utf-8"` |
| `JSONDecodeError` | JSON 文件格式错误 / Bad JSON | 检查括号是否匹配 / Check brackets |
| 端口被占用 / Port in use | 另一个程序占用了5000 / Another app uses 5000 | 改成 `app.run(port=5001)` |
| 修改 Python 代码后无效 / Changes not taking effect | 服务器缓存 / Server cache | 重启 `python app.py` |
| 浏览器显示旧数据 / Browser shows old data | 浏览器缓存 / Browser cache | 按 `Ctrl + Shift + R` 强制刷新 |
| `KeyError` 在 CSV 读取时 / on CSV read | 列名拼写错误 / Column name typo | 检查 CSV 第一行的列名 / Check header row |

### 调试技巧 / Debugging Tips

```python
# Python 端：打印中间结果 / Print intermediate results
print(f"[DEBUG] 找到客户 / Found customer: {customer}")
print(f"[DEBUG] 库存 / Stock: {product.stock}")

# Flask 开启 debug 模式（自动显示详细错误）
# Flask debug mode (shows detailed errors)
app.run(debug=True)
```

```javascript
// JavaScript 端：打开浏览器控制台 (F12)
// Open browser console (F12)
console.log('收到数据 / Received data:', data);
console.error('发生错误 / Error occurred:', error);
```

---

## 快速参考卡 / Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│            Python 网页应用速查 / Python Web App Cheatsheet  │
├──────────────────┬──────────────────────────────────────┤
│ 读取 CSV         │ csv.DictReader(open(file))            │
│ 写入 CSV         │ csv.writer(f).writerow([...])         │
│ 读取 JSON        │ json.load(open(file))                 │
│ 写入 JSON        │ json.dump(data, f, indent=2)          │
│ Flask GET 路由   │ @app.route("/api/x")                  │
│ Flask POST 路由  │ @app.route("/api/x", methods=["POST"])│
│ 返回 JSON        │ return jsonify(data)                  │
│ 读取请求数据     │ request.get_json()                    │
│ fetch GET        │ fetch('/api/x').then(r => r.json())   │
│ fetch POST       │ fetch('/api/x', {method:'POST', ...}) │
│ 更新 HTML 表格   │ tbody.innerHTML = items.map(...).join │
│ Bootstrap 按钮   │ class="btn btn-primary"               │
│ Font Awesome 图标│ <i class="fa-solid fa-[name]"></i>    │
└──────────────────┴──────────────────────────────────────┘
```

---

*本教材基于 Glassfabriken ERP 项目编写 · Based on the Glassfabriken ERP project*
*适用于任何 Python Flask 网页项目 · Applicable to any Python Flask web project*
