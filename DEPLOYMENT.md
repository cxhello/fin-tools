# Streamlit Cloud 部署配置说明

## ⚠️ 重要：需要在Streamlit Cloud上配置Secrets

由于 `.streamlit/secrets.toml` 文件不会提交到GitHub（出于安全考虑），需要在Streamlit Cloud上手动配置。

### 配置步骤：

1. **登录 Streamlit Cloud**
   - 访问：https://share.streamlit.io
   - 使用GitHub账号登录

2. **进入应用设置**
   - 找到你的应用：**lucisl-fin-tools**
   - 点击右上角 **Settings** ⚙️ 按钮

3. **配置 Secrets**
   - 找到 **Secrets** 部分
   - 在文本框中输入以下内容：
   
   ```toml
   api_url = "https://api.test.cinta.team/litabasic/v1/db"
   ```

4. **保存并重启**
   - 点击 **Save** 按钮
   - 应用会自动重启（大约需要几秒钟）

5. **验证配置**
   - 重启后访问应用
   - 如果能正常显示购物清单页面，说明配置成功

---

## 本地开发配置

本地开发时，使用 `.streamlit/secrets.toml` 文件：

```toml
api_url = "https://api.test.cinta.team/litabasic/v1/db"
```

这个文件已配置好，无需额外操作。

---

## 数据持久化验证

配置完成后，可以通过以下方式验证数据持久化：

1. 添加几个商品到购物清单
2. 等待应用自动休眠或手动重启应用
3. 再次访问应用，检查商品是否还在

**如果商品还在，说明数据持久化成功！**

---

## API接口说明

购物清单使用的API接口：

- `GET /ping` - 测试数据库连接
- `POST /query` - 执行SELECT查询
- `POST /execute` - 执行INSERT/UPDATE/DELETE操作

所有数据存储在你的MySQL数据库（funbit库）中。

---

## 故障排查

如果应用报错：

**错误：API调用失败**
- 检查Streamlit Cloud上的Secrets是否配置正确
- 检查Java服务是否正常运行
- 检查API地址是否正确

**错误：数据库连接失败**
- 检查Java服务的数据库连接配置
- 检查funbit数据库是否存在

---

## 技术架构

```
Streamlit Cloud (前端)
    ↓ 调用API
Java Service (API层)
    ↓ 连接数据库
MySQL Database (数据层)
```

**优势：**
- ✅ 数据永久保存，重启不丢失
- ✅ 前端无需数据库密码，更安全
- ✅ API完全通用，可支持多种应用