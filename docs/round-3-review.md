# 第三轮更新：审核说明

本轮从最新 `main`（`c0f98861a1978cc51f1f9540e3e53728d5742e93`，已含合并的 PR #20）建立新分支 `feat/website-round-3`。不修改旧 PR，不合并或部署。

## 已完成

- 首页整合原有五条 FAQ，使用原生可键盘操作的手风琴；所有页面顶部导航移除 FAQ；`faq.html` 与旧书签转到 `index.html#faq`，包含无 JavaScript 的兼容跳转。
- 保留 2026 年精选活动回顾按钮，新增历史回顾入口。按用户确认，只展示已有的 2024、2025 年文章。
- 保留 TTmath、Citadel，增加四家指定支持机构；依官方英文名称排序，添加不含排名含义的说明。桌面四列、手机两列，112px 等高标志容器，图片保持原比例。六家机构及两处机构统计共用 `data/supporters.json`，通过 `scripts/render_supporters.py` 生成静态内容。
- 按原文更新 Perry、Kaylyn、Xuanyi(Prince) 的姓名和两段简介，照片、职位及其余 13 名成员保持不变。较长简介支持键盘滚动。
- 按最终澄清显示 **850+ Students Reached**；社区伙伴统计核实为 **6**。
- 审核所有九条 Programs/Livestream 视频记录，修正可靠匹配并明确部分讲解范围；错误且无法确认的目的地址改为待补充。保留完整 [旧/新链接与核实表](video-link-audit.md)。
- News、Programs、首页新闻日期显示统一为 `Mon YYYY`，保留原有完整日期和排序精度；缺少月份时不补造。
- 所有九页补齐 production domain 的 SEO、分享元数据；添加 sitemap、robots、favicon 和有用的结构化数据。拟议分享封面尚未发布或用于元数据。

## 待补充或确认

1. 请提供 **2025 COMC、2025 AMC10、Math Kangaroo 赛后讨论、Interactive Q&A** 的正确视频链接，以及 **Summer Camp Students’ Voices** 的正确系列链接。
2. 请确认 **2024 AMC10A** 原有 **Jun 2025** 标签的含义；已核实系列首集上传于 2025 年 5 月，页面保留原标签，未擅自修改活动日期。
3. 请确认 **Yingshan Xiao** 访谈候选 `https://youtu.be/Bkamz7QCS7I`（Part 1）及原有 May 2025 标签。News 目前保留频道入口，并准确标注为访问频道。
4. 请提供 **Jane Street、小月牙医、志鸿牙医 / Dr Hong Dental、BLACK BELT WORLD** 获准使用的原始标志文件。当前使用文字标志；保留既有 TTmath、Citadel 图片。Dr Hong Dental 指定的 HTTP 地址未能核实实时可达性，请确认是否仍有效。
5. 请审核聊天中提供的 **1200 × 630 分享封面提案**及其生成的标志处理。文件不在提交内容中，不会上线。当前元数据继续使用已有获准的活动照片。

## 验证与限制

本地内容、内链与锚点、SEO/sitemap、支持机构数据一致性、HTML/CSS/JavaScript 检查通过。浏览器检查覆盖 375、390、768、1440px，以及导航、FAQ 和旧链接、历史文章弹窗、支持机构布局与链接、团队键盘交互、统计与自动 Latest News 排序。桌面与手机截图见 [previews](../previews/README.md)。

五个主页面在 390、1440px 的 axe WCAG A/AA 自动检查通过；自动检查不代表完整人工无障碍认证。测试使用 Linux Chromium，未使用实体手机或 Safari。

环境网络策略限制生产图片的实时 HTTP 检查；本地图片解码、尺寸、HTTP 响应与浏览器显示可验证。新元数据和 sitemap 在批准并部署前尚未出现在生产域名。WhatsApp、WeChat 等平台的抓取、缓存与裁剪无法由本地静态测试完整重现；Instagram 也不保证所有位置提供链接预览。详见 [SEO 验证说明](seo-review.md)。
