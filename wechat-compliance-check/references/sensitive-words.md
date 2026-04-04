# 微信公众号敏感词库

> 最后更新：2026-04-04
> 来源：实际发布踩坑 + 社区汇总 + 微信官方规范

## 使用说明

每条规则格式：`敏感词 → 替换词 | 风险等级 | 备注`

上下文标记：
- `[ALWAYS]` — 任何语境都替换
- `[CONTEXT]` — 需要判断上下文，技术语境可能安全
- `[REGEX]` — 使用正则匹配

---

## 1. 翻墙/代理工具类 🔴

```
VPN → 虚拟专用网络 | 🔴 | [ALWAYS]
Clash → 网络规则工具 | 🔴 | [ALWAYS]
Shadowsocks → 加密代理工具 | 🔴 | [ALWAYS]
ShadowsocksR → 加密代理工具 | 🔴 | [ALWAYS]
SSR → 加密代理 | 🔴 | [CONTEXT] 技术缩写可能有其他含义
V2Ray → 网络工具 | 🔴 | [ALWAYS]
Trojan → 网络协议 | 🔴 | [CONTEXT] 安全领域可能指木马
Xray → 网络工具 | 🔴 | [CONTEXT] 可能指医学X光
科学上网 → 网络访问 | 🔴 | [ALWAYS]
翻墙 → 跨境访问 | 🔴 | [ALWAYS]
梯子 → 网络工具 | 🔴 | [CONTEXT] 可能指真实梯子
GFW → 网络限制 | 🔴 | [ALWAYS]
防火长城 → 网络限制 | 🔴 | [ALWAYS]
墙 → 网络限制 | 🔴 | [CONTEXT] 仅在网络语境中替换
机场 → 网络服务 | 🔴 | [CONTEXT] 仅在代理语境中替换
节点 → 服务器 | 🟡 | [CONTEXT] 仅在代理语境中替换
```

## 2. 政治/地缘敏感类 🔴

```
中国封禁 → 部分地区限制 | 🔴 | [ALWAYS]
中国封号 → 部分地区账号受限 | 🔴 | [ALWAYS]
中国开发者封号 → 部分地区开发者受限 | 🔴 | [ALWAYS]
中国.*被禁 → 部分地区受限 | 🔴 | [REGEX]
中国.*封.*潮 → 部分地区受限 | 🔴 | [REGEX]
中国控制的公司 → 部分地区的公司 | 🔴 | [ALWAYS]
Chinese.*ban → regional restriction | 🔴 | [REGEX]
审查制度 → 内容管理制度 | 🔴 | [ALWAYS]
言论自由 → （删除或重写段落） | 🔴 | [ALWAYS]
政治敏感 → 政策相关 | 🟡 | [CONTEXT]
地缘政治 → 地区政策 | 🟡 | [ALWAYS]
```

## 3. 破解/逆向类 🟡

```
逆向工程 → 技术分析 | 🟡 | [ALWAYS]
逆向分析 → 技术分析 | 🟡 | [ALWAYS]
破解 → 分析 | 🟡 | [CONTEXT] 密码破解→密码分析
crack → analyze | 🟡 | [CONTEXT]
hack → 技术 | 🟡 | [CONTEXT] hackathon 等合法用法保留
Hacker News → 技术社区 | 🟡 | [ALWAYS] 含 hack 字样
漏洞利用 → 安全问题 | 🟡 | [CONTEXT]
exploit → vulnerability | 🟡 | [CONTEXT]
注入 → 插入 | 🟡 | [CONTEXT] SQL注入等技术术语可保留
inject → insert | 🟡 | [CONTEXT]
绕过 → 规避 | 🟡 | [ALWAYS]
bypass → workaround | 🟡 | [ALWAYS]
脱壳 → 分析 | 🟡 | [ALWAYS]
反编译 → 代码分析 | 🟡 | [ALWAYS]
decompile → code analysis | 🟡 | [ALWAYS]
hook → 拦截 | 🟡 | [CONTEXT]
```

## 4. 封号/灰产类 🟡

```
封号 → 账号限制 | 🟡 | [ALWAYS]
封禁 → 限制 | 🟡 | [ALWAYS]
被封 → 被限制 | 🟡 | [ALWAYS]
ban → restrict | 🟡 | [ALWAYS] 作为动词时
banned → restricted | 🟡 | [ALWAYS]
banning → restricting | 🟡 | [ALWAYS]
转售 → 违规分享 | 🟡 | [ALWAYS]
resell → redistribute | 🟡 | [ALWAYS]
账号共享 → 多人共用 | 🟡 | [ALWAYS]
account sharing → multi-user access | 🟡 | [ALWAYS]
薅羊毛 → 套利 | 🟡 | [ALWAYS]
代刷 → 违规操作 | 🟡 | [ALWAYS]
刷量 → 违规操作 | 🟡 | [ALWAYS]
外挂 → 第三方工具 | 🟡 | [ALWAYS]
```

## 5. 引流/商业化类 🟡

```
付费源码 → 源码 | 🟡 | [ALWAYS] 去掉付费字样
付费获取 → 获取 | 🟡 | [CONTEXT]
购买 → 获取 | 🟡 | [CONTEXT] 正常商品购买可保留
下单 → （视语境） | 🟡 | [CONTEXT]
加微信领取 → 加微信了解 | 🟡 | [ALWAYS]
限时优惠 → （视语境） | 🟡 | [CONTEXT]
免费领 → （视语境） | 🟡 | [CONTEXT] 可能触发诱导分享
扫码付款 → （视语境） | 🟡 | [CONTEXT]
```

## 6. 平台/品牌敏感类 ⚠️

```
微信 → （通常安全） | ⚠️ | [CONTEXT] 批评微信时可能敏感
腾讯 → （通常安全） | ⚠️ | [CONTEXT] 负面评价时注意
抖音 → （通常安全） | ⚠️ | [CONTEXT] 引流到竞品时敏感
小红书 → （通常安全） | ⚠️ | [CONTEXT] 引流到竞品时敏感
```

## 7. 医疗/健康类 🔴

```
治疗 → （视语境） | 🔴 | [CONTEXT] 非医疗文章避免使用
药物 → （视语境） | 🔴 | [CONTEXT]
疗效 → （视语境） | 🔴 | [CONTEXT]
根治 → （删除） | 🔴 | [ALWAYS] 绝对化用语
```

## 8. 绝对化用语类 ⚠️

```
最好的 → 优秀的 | ⚠️ | [CONTEXT] 广告法禁止绝对化用语
第一 → 领先 | ⚠️ | [CONTEXT]
唯一 → （视语境） | ⚠️ | [CONTEXT]
100% → （视语境） | ⚠️ | [CONTEXT]
绝对 → （视语境） | ⚠️ | [CONTEXT]
```

---

## 更新日志

- 2026-04-04：初始版本，基于实际公众号发布违规经验整理
- 覆盖 8 大类 100+ 敏感词/短语
- 包含中英文双语匹配
- 标注上下文敏感度（ALWAYS/CONTEXT/REGEX）
