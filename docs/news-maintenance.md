# Latest News：数据与日期维护

`news.html` 是唯一新闻内容来源。首页通过同源 `fetch('news.html')` 读取其新闻卡片，按已知年份降序排列，只显示前三条已知年份新闻。News 页使用相同排序方法；同年有精确日期的条目按日期倒序填入原有精确日期位置，只有年份的条目保留原来从左到右的位置。没有年份的新闻保留在最后。同日新闻按稳定 ID 排序，不依赖 HTML 中的先后位置。

## 添加新闻

在 `news.html` 的 `.news-grid` 中添加一张 `.story` 卡片：

- 使用唯一、稳定的 `id`，例如 `news-event-name`。若省略，脚本会根据标题生成一致的 ID，但建议显式设置，以免标题修改导致旧书签失效。
- 设置 `data-date="YYYY-MM-DD"`，填写真实、经确认的**发布日期**，不要把活动日期、日期范围起点或 Git 提交日期当作发布时间。
- 若仅年份已知，使用 `data-year="YYYY"` 和 `data-date-status="year-only"`，不要虚构精确日期。
- 保留 `.news-image img`、`h3` 和 `.date`。完整文章使用现有 `details/summary`，视频使用现有链接。
- 不需要修改 `index.html`。首页自动复用原图和完整标题；显示日期采用 `Mon YYYY` 并以 UTC 格式化，避免时区导致前后差一天。原有完整 `data-date` 不变；对仅按年份排序的条目，可用经核实的 `data-display-month="YYYY-MM"` 显示活动月份，不改变其排序精度。

首页链接采用 `news.html#<story-id>`。有完整文章的条目自动打开对应阅读弹窗；视频条目定位到对应卡片并保留原始视频链接。JavaScript 被禁用或读取失败时，首页保留 News 页面入口。请通过 HTTP 服务或 GitHub Pages 访问，不能通过 `file://` 读取新闻。

## 当前日期精度（用户确认保留）

原网站没有区分发布日期与活动日期。当前 9 条精确日期直接取自原有新闻日期标签，未新增日期；原文未区分活动日期和发布日期，无法独立核实实际发布日。

其余 8 条未设置 `data-date`。按用户确认的规则，四条夏令营/冬令营相关新闻使用原文明确年份（`data-year`、`data-date-status="year-only"`）参与首页选择；有已知活动月份的条目显示月份与年份，只有季节时仍仅显示年份。同年这些条目保留源文件从左到右位置。另四条连年份也未提供，标记 `needs-confirmation`，不进入首页选择。没有为日期范围、月份或季节补造日期。

| 新闻 | 原有日期文字 | 当前精度依据 |
|---|---|---|
| Math Camp 2026 | August 17–21, 2026 · North York | 活动日期范围，未说明发布日期 |
| Math Winter Camp | December 2025 · Oakville | 只有月份 |
| We Pi(π)oneer Charity Math Contest（综述） | Four contests and counting | 没有日期 |
| 2025 Math Summer Camp | August 19–22, 2025 · North York | 活动日期范围，未说明发布日期 |
| Inside the Most Selective and Celebrated Math Summer Camps | Summer 2025 · video series | 只有季节 |
| What to Expect | by Kaylyn Zhang | 只有作者 |
| From Math To Quant: Houting's Inspiring Journey | Video | 没有日期 |
| From Math To AI: High Schoolers Interview Industry Experts | Video | 没有日期 |

用户已确认保留现有信息，不补造缺少的月份或发布日期。将来获得真实发布日期时，可在对应 News 卡片设置真实的 `data-date` 并移除待确认标记。自动选择无需再改首页。

## 测试

先从仓库根目录启动 `python3 -m http.server 8000 --bind 127.0.0.1`，再执行：

```sh
python3 tests/latest_news_check.py
python3 tests/browser_check.py
python3 tests/content_check.py
node --check app.js
```

新闻专项测试在浏览器中模拟新增日期更晚的条目、反转源文件顺序、无效日期和请求失败；不修改仓库新闻内容。它验证三条限制、原图/标题/日期、链接、文章弹窗和视频定位。

## 第三轮：日期显示与历史回顾

News、Programs 和首页 Latest News 的可见日期统一为英文缩写月份与年份，例如 `Sep 2026`。正文中的完整活动日期也通过 `<time datetime="原有完整日期">Sep 2026</time>` 显示；原有完整日期保留在机器可读属性中，排序用的 9 个 `data-date` 值完全不变。已知活动范围的结束日期保留为 `data-end-date`，不把活动日期伪装成发布日期。

仅知道季节与年份的新闻显示 `2025 · summer video series`，不补造月份。Programs 的 2026 Cayley、Galois、Fryer、Pascal 已按用户确认显示 Aug 2026；2025 Waterloo 和 Fermat 讲解条目已移除。已知活动月份但发布日期未确认的三个营地条目保留原有 year-only 排序规则，同时以 `data-display-month="YYYY-MM"` 供首页显示已知月份。

首页精选活动下方的历史回顾入口可展开已有的 2024 与 2025 慈善竞赛回顾链接，直接进入 News 对应原文章。News 不新增历史回顾突出区块，保留原新闻列表布局。没有新建或推测往年回顾文章、日期、统计数据或 URL。
