# 02 Architecture

本目录负责系统架构、模块拆分、技术路线、服务边界和扩展规则。

## 架构目标

1. 支撑监管业务长期扩展。
2. 支撑 66 万房屋数据治理和后续增长。
3. 支撑银行、支付、产权登记、维修资金等外部接口。
4. 支撑审计日志、权限控制和发布回滚。
5. 支撑未来 30B、120B 模型和 GPU 推理集群接入。

## 必备文档

- `architecture_principles.md`：架构原则。
- `module_map.md`：模块地图。
- `service_boundary.md`：服务边界。
- `technology_radar.md`：技术路线。

## 责任角色

- 主责：Architect Codex
- 协作：Backend Codex、Database Codex、ServerOps Codex、AI Codex、Auditor Codex

