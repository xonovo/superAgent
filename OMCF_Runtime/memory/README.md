# Runtime Memory Adapter

本目录是 Runtime V1 的记忆适配层。

V1 不直接修改 `MCP/17_Memory_Center`，只在运行产物中生成项目记忆建议和决策登记建议。

后续版本可以把本适配层扩展为：

1. 读取全局 Memory Center。
2. 按需创建 Project Memory。
3. 写入 Decision Registry。
4. 写入 Failure Log 和 Lessons Learned。
