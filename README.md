# tool-dependabot-sentinel

> **Dependabot 智能配置与 PR 降噪哨兵**  
> Universal CLI Facade (UCFS v1.0) 标准实现 | 100% 离线自省 | 语义成组与反疲劳巡检

> [!NOTE]
> **第一性原理架构收敛声明 (Evolution Notice)**:  
> 本工具所包含的 Dependabot 依赖守护配置与降噪模板，已正式通过第一性原理仲裁并收敛归入高内聚特种技能 [skill-github-ops](file:///D:/github/skill-github-ops)（三级渐进式披露架构）。  
> 存量代码已冻结并归档保留。在现代 AI 协同中，推荐直接调用 `skill-github-ops` 享受更轻量、零 Token 浪费的最佳实践。


---

## 🌟 核心价值与实用性痛点解答

在使用 GitHub 官方 Dependabot 时，开发者和团队常常遭遇两大极端：
1. **依赖遗忘与安全腐化**：完全没有配置 `.github/dependabot.yml`，导致引用的第三方库漏洞在数年内无人问津，甚至不知道 GitHub Actions 的版本早已过时。
2. **PR 轰炸与告警疲劳 (Alert Fatigue)**：开启 Dependabot 后，系统每天自动弹出 20~30 个独立的拉取请求，CI 队列瞬间被塞满，团队 review 成本剧增，最终导致维护者被迫关闭 Dependabot。

`tool-dependabot-sentinel` 通过两项核心能力终结此困境：
- **语义成组降噪 (Semantic Grouping)**：自动扫描项目栈（Python/Node/Rust/Go/Docker/Actions），将开发工具链（linter/test runner）和微小补丁聚合至单一每周 PR，消灭 80% 以上的无谓通知。
- **配置健康度审计 (Anti-Spam Audit)**：一键检查现存 `dependabot.yml`，精准揪出遗漏的生态（如忘记添加 `github-actions`）与未限额配置。

---

## ⚡ 极速开始 (Quick Start in 3 Seconds)

```bash
# 1. 环境校验
python main.py setup

# 2. 对当前项目生成降噪版 Dependabot 配置 (.github/dependabot.yml)
python main.py run

# 3. 运行离线单元测试
python main.py test

# 4. 核心健康自检
python main.py health

# 5. 清理缓存
python main.py clean
```

### 高级功能：定制配置与静态审计
```bash
# 审计当前工程已有的 Dependabot 隐患与遗漏生态
python main.py audit --target D:\github\my-project

# 定制生成频率（如每周一执行，限制最大并发 PR 为 3）
python main.py generate --target D:\github\my-project --interval weekly --day monday --limit 3
```

---

## 🛡️ 架构与不变式

- **独立职责**：专职负责 Dependabot 策略推导与配置文件生成，不发起任何网络请求或拉取云端 Issue。
- **离线确定性**：依赖分析基于本地清单文件（`requirements.txt`, `package.json`, `Cargo.toml` 等），全离线零外部调用。

---

## 🚫 Non-Goals (明确非目标)

1. **不自动合并 PR**：本工具不提供直接合入 GitHub PR 的特权行为（应由人工 Review 或受保护分支检查决定）。
2. **不替代包管理器**：本工具不直接执行 `npm update` 或 `pip install --upgrade`，版本解析由 GitHub 云端引擎完成。
3. **不越权修改源码**：除生成 `.github/dependabot.yml` 外，绝不触碰任何代码文件。
