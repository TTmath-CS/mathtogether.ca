# -*- coding: utf-8 -*-
REPLACEMENTS = [
 ('<span class="wordmark">AI WORKSHOP</span>', '<span class="wordmark">AI 实战工作坊</span>'),
 ('Build Real AI Projects.<br>Learn Skills That Matter.',
  '做真实的 AI 项目。<br>学真正有用的技能。'),
 ('In-person classroom course &middot; 8 weeks', '线下教室课 &middot; 共 8 次课'),
 ('<em>More than theory.</em> Real tools, real experience, real&nbsp;projects.',
  '<em>不只是理论。</em>真实的工具、真实的体验、真实的项目。'),
 ('This workshop focuses on project-based learning. We&rsquo;ll cover key concepts, but more importantly, you&rsquo;ll gain hands-on <b>tools, workflows and real-world experience</b> that textbooks rarely teach.',
  '本课程以项目式学习为核心。我们会讲清关键概念，但更重要的是，<br>你将获得课本很少教的<b>实用工具、开发流程与真实项目经验</b>。'),
 ('<div class="c1">From idea<br>to live project.</div>', '<div class="c1">从一个想法<br>到一个上线项目</div>'),
 ('<div class="c2">You build it.<br>You launch it.</div>', '<div class="c2">你亲手做<br>你亲手上线</div>'),
 ('<span>WHAT YOU WILL LEARN</span>', '<span>你将学到什么</span>'),

 ('AI Tools in Real Use', 'AI 工具实战'),
 ('Learn Claude, ChatGPT and more. Use AI to write code, find bugs, understand and refactor code, and brainstorm ideas. Learn how to evaluate and verify AI outputs.',
  '学会用 Claude、ChatGPT 等 AI 工具写代码、找 Bug、<br>读懂并重构代码、激发思路，并学会评估和验证 AI 的输出。'),
 ('Developer Essentials', '开发者必备技能'),
 ('Master the tools real developers use every day: command line, Git, GitHub, version control, and collaboration. Practical skills rarely covered in regular courses.',
  '掌握真实开发者每天在用的工具：命令行、Git、GitHub、<br>版本控制与团队协作。这些是常规课程很少涉及的实用技能。'),
 ('Software Project Management', '软件项目管理'),
 ('Learn the professional development workflow: requirements &rarr; planning &rarr; development &rarr; testing &rarr; iteration &rarr; documentation. Track tasks, manage versions, and work like real developers.',
  '学习专业的开发流程：<br>需求 &rarr; 规划 &rarr; 开发 &rarr; 测试 &rarr; 迭代 &rarr; 文档。<br>管理任务、管理版本，像真正的开发者一样工作。'),
 ('Deployment &amp; Basics of DevOps', '部署与 DevOps 基础'),
 ('Learn how to deploy your project online. Understand servers, domains, environment setup, and how to make your project publicly accessible.',
  '学会把项目部署上线，理解服务器、域名、环境配置，<br>以及如何让自己的项目对外可访问。'),
 ('Build, Test &amp; Launch Your AI Project', '构建、测试并发布 AI 项目'),
 ('Apply everything you learn to build a complete AI project from start to finish. Test, deploy, and share your work with a clean GitHub repository.',
  '把学到的一切用于从零到一完成一个完整的 AI 项目：<br>测试、部署，并用一个规范的 GitHub 仓库展示你的作品。'),

 ('<h2>YOU WILL GAIN</h2>', '<h2>你将收获</h2>'),
 ('<span>Practical AI tools you can use immediately</span>', '<span>可以立刻上手使用的 AI 工具</span>'),
 ('<span>Real-world developer skills and workflows</span>', '<span>真实的开发者技能与工作流程</span>'),
 ('<span>Experience managing a complete software project</span>', '<span>完整管理一个软件项目的经验</span>'),
 ('<span>Confidence to deploy and share your work online</span>', '<span>独立部署并对外展示作品的信心</span>'),
 ('<span>A finished AI project you can run, show, and be proud of</span>', '<span>一个能运行、能展示、值得骄傲的 AI 项目</span>'),
 ('<span>A strong portfolio piece for high school, college applications and beyond</span>',
  '<span>一份能用于高中、大学申请的<br>高含金量作品集</span>'),

 ('>Class time<', '>上课时间<'),
 ('Saturday<br>4:45 PM &ndash; 6:15 PM', '每周六<br>下午 4:45 &ndash; 6:15'),
 ('In person &middot; TTMath classroom', '线下上课 &middot; TTMath 教室'),
 ('>Fee<', '>学费<'),
 ('<p class="fee-sub">8 classes</p>', '<p class="fee-sub">共 8 次课</p>'),
 ('>Prerequisites<', '>入学要求<'),
 ('<li>Completed TTMath CS1 or equivalent, with strong programming skills</li>',
  '<li>已完成 TTMath CS1 或同等水平，<br>具备扎实的编程基础</li>'),
 ('<li>Starting 8th grade and above in September</li>', '<li>九月起就读 8 年级及以上</li>'),
 ('<li>Strong interest in AI</li>', '<li>对 AI 有浓厚兴趣</li>'),

 ('<p class="t1">This is more than an AI course.</p>', '<p class="t1">这不只是一门 AI 课。</p>'),
 ('<p class="t2">It&rsquo;s an in-person workshop that gives you the experience to turn ideas into real AI projects.</p>',
  '<p class="t2">这是一次线下工作坊，<br>让你真正拥有把想法变成 AI 项目的经验。</p>'),
 ('<span>IDEA</span>', '<span>想法</span>'),
 ('<span>CODE</span>', '<span>编码</span>'),
 ('<span>TEST</span>', '<span>测试</span>'),
 ('<span>DEPLOY</span>', '<span>部署</span>'),
 ('<span>SHARE</span>', '<span>分享</span>'),
]

ZH_CSS = """
/* ---------- Chinese edition overrides ---------- */
body{font-family:Archivo,"Noto Sans SC","WenQuanYi Zen Hei","Microsoft YaHei",sans-serif;}
.wordmark{font-size:50px;letter-spacing:-0.5px;}
.subhead{line-height:1.42;letter-spacing:.01em;}
.pill{letter-spacing:.08em;font-size:12px;}
.highlight{font-size:15.4px;line-height:1.95;}
.lede{font-size:13.6px;line-height:1.66;}
.hero .circle .c1{font-size:12.6px;line-height:1.5;}
.hero .circle .c2{font-size:13.4px;line-height:1.5;margin-top:7px;}
.sec-head span{letter-spacing:.16em;font-size:17px;}
.item h3{font-size:16.5px;letter-spacing:.01em;}
.item p{font-size:13.6px;line-height:1.58;}
.gain h2{letter-spacing:.14em;}
.gain li{font-size:13.4px;line-height:1.54;}
.info .lbl{letter-spacing:.14em;}
.info .val{font-size:14px;line-height:1.5;}
.info .sub{font-size:12.4px;}
.info .fee-sub{font-size:12.6px;}
.info ul li{font-size:12.8px;line-height:1.5;margin-bottom:4px;}
.band .t1{font-size:14.6px;}
.band .t2{font-size:12.8px;line-height:1.45;}
.flow .step span{font-size:10.4px;letter-spacing:.08em;}
"""
