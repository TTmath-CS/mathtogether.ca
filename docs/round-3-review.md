# 第三轮更新：审核说明

本轮从最新 `main`（`c0f98861a1978cc51f1f9540e3e53728d5742e93`，已含合并的 PR #20）建立新分支 `feat/website-round-3`。不修改旧 PR，不合并或部署。

## 已完成

- 首页整合原有五条 FAQ，使用原生可键盘操作的手风琴；所有页面顶部导航移除 FAQ；`faq.html` 与旧书签转到 `index.html#faq`，包含无 JavaScript 的兼容跳转。
- 保留 2026 年精选活动回顾按钮。首页历史回顾入口可展开 2024、2025 年原文章链接；News 移除新增的历史回顾突出区块，维持原有新闻列表布局与全部 17 条文章内容。
- 保留 TTmath、Citadel，增加四家指定支持机构；依官方英文名称排序，添加不含排名含义的说明。四个新增 logo 已从用户提供的 `logos.zip` 原样接入，未裁剪、重绘或重新编码。桌面和平板每行三家、共两行，手机每行两家；112px 等高容器与原图比例保持不变。BLACK BELT WORLD 的白色字样使用深色底以确保清晰。六家机构及两处机构统计共用 `data/supporters.json`，通过 `scripts/render_supporters.py` 生成静态内容。
- 按原文更新 Perry、Kaylyn、Xuanyi(Prince) 的姓名和两段简介，照片、职位及其余 13 名成员保持不变。较长简介支持键盘滚动。
- 按最终澄清显示 **850+ Students Reached**；社区伙伴统计核实为 **6**。首页每个数字居中置于说明文字上方，保留装饰图标；FAQ 使用与其他首页区块相同的左边缘和左对齐标题。 首页 About、Featured Event、Our Programs、Latest News、FAQ 五处红字标签恢复原来的小字号。
- 审核全部九条原有 Programs/Livestream 记录；按用户确认移除五条旧记录，包括 2025 Fermat。当前八条记录、20 个独立视频链接，涵盖 2026 慈善竞赛、Cayley、Galois、Fryer、Pascal 和 2025 COMC、AMC10、AMC12。原先没有月份的四条 2026 记录统一为用户确认的 Aug 2026，机器日期为 2026-08。视频讲解标题统一去除末尾长横线，2025 COMC、AMC10、AMC12 使用与 2026 年一致的年份加竞赛名称格式；Watch 链接继续另起一行。News 原有 17 条新闻内容和布局保留，已确认的视频链接继续有效。完整 [旧/新链接与核实表](video-link-audit.md)记录变更。
- News、Programs、首页新闻日期显示统一为 `Mon YYYY`，保留原有完整日期和排序精度；用户已确认缺少月份或发布日期的内容保留现有信息，不补造。
- 视频讲解链接（含 News 阅读弹窗）与首页 Watch on YouTube 在新标签页打开，保留当前网站页面；链接包含新标签页的无障碍提示及外链安全属性。
- 所有九页补齐 production domain 的 SEO、分享元数据；添加 sitemap、robots、favicon 和有用的结构化数据。拟议分享封面尚未发布或用于元数据。

## 待补充或确认

**1200 × 630 分享封面提案**仍等待批准，包括其中生成的标志处理。文件不在提交内容中，不会上线。当前元数据继续使用已有获准的活动照片。四家新增支持者的原始 logo 已接入；Dr Hong Dental 指定的 HTTP 官网已获用户确认有效，链接保持原样。

## 验证与限制

本地内容、内链与锚点、SEO/sitemap、支持机构数据一致性、HTML/CSS/JavaScript 检查通过。浏览器检查覆盖 375、390、768、1440px，以及导航、FAQ 和旧链接、历史文章弹窗、支持机构布局与链接、团队键盘交互、统计与自动 Latest News 排序。桌面与手机截图见 [previews](../previews/README.md)。

五个主页面在 390、1440px 的 axe WCAG A/AA 自动检查通过；自动检查不代表完整人工无障碍认证。测试使用 Linux Chromium，未使用实体手机或 Safari。

环境网络策略限制生产图片的实时 HTTP 检查；本地图片解码、尺寸、HTTP 响应与浏览器显示可验证。新元数据和 sitemap 在批准并部署前尚未出现在生产域名。WhatsApp、WeChat 等平台的抓取、缓存与裁剪无法由本地静态测试完整重现；Instagram 也不保证所有位置提供链接预览。详见 [SEO 验证说明](seo-review.md)。
