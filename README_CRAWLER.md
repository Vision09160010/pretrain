# Paper.edu.cn 论文爬虫使用说明

## 功能介绍

本爬虫脚本用于从 `https://www.paper.edu.cn` 网站爬取论文信息并下载PDF文件。

## 文件说明

1. `paper_edu_crawler.py` - 主要爬虫脚本
2. `test_playwright.py` - Playwright环境测试脚本
3. `parse_warc.py` - Common Crawl WARC文件解析工具（之前创建）
4. `process_robotstxt.py` - Common Crawl robots.txt路径处理工具（之前创建）

## 环境准备

### 1. 安装Python依赖

```bash
pip install playwright
```

### 2. 安装浏览器驱动

```bash
playwright install
```

## 使用步骤

### 1. 测试Playwright环境

首先运行测试脚本确保Playwright正常工作：

```bash
python test_playwright.py
```

如果输出类似以下内容，则表示环境正常：
```
测试Playwright是否正常工作...
页面标题: 论文发布系统 - 中国科技论文在线
找到 XX 篇论文
✓ Playwright测试成功！
```

### 2. 配置爬虫参数

在 `paper_edu_crawler.py` 文件中可以修改以下参数：

```python
# 配置参数
save_path = os.path.dirname(__file__) + '/pdf_paper_edu/'  # PDF保存目录
limit = 20  # 每页论文数量（根据网站实际情况调整）
total_pages = 3  # 爬取的总页数（根据需要调整）
```

### 3. 运行爬虫

```bash
python paper_edu_crawler.py
```

### 4. 查看结果

爬取的PDF文件将保存在 `pdf_paper_edu` 文件夹中，文件名使用论文的 `paper_id` 命名。

## 工作原理

1. 访问论文列表页面
2. 提取每篇论文的标题和详情页链接
3. 访问详情页获取隐藏的 `paper_id`
4. 使用 `paper_id` 构建PDF下载链接
5. 下载PDF文件并保存

## 注意事项

1. **网站限制**：请遵守网站的robots.txt规则，不要过度爬取
2. **请求频率**：脚本中已经加入了适当的延迟（1秒），请不要修改过小
3. **页面结构**：如果网站更新了页面结构，脚本可能需要相应调整
4. **存储空间**：下载大量PDF文件会占用较多存储空间
5. **网络问题**：如果遇到网络问题，脚本可能会抛出异常，建议逐步测试

## 常见问题

### 1. Playwright安装失败

尝试使用代理或更换镜像源：

```bash
pip install playwright -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 浏览器驱动安装失败

尝试指定浏览器版本：

```bash
playwright install chromium
```

### 3. 无法找到论文元素

检查网站页面结构是否发生变化，可能需要更新CSS选择器。

### 4. 下载的PDF文件为空

检查网络连接或网站是否需要登录才能下载PDF。

## 示例输出

```
=== 爬取第 1 页 ===
找到 20 篇论文

1. 处理论文: 促红细胞生成素在结直肠癌小鼠模型中诱导脾脏Ter和EDMC细胞生成
   详情页: https://www.paper.edu.cn/releasepaper/content/202512-7
   Paper ID: NUDGcF2QNRzVII4eQOQeQeQ
   PDF链接: https://www.paper.edu.cn/download/downpdf/paper/NUDGcF2QNRzVII4eQOQeQeQ
   ✓ 下载成功: NUDGcF2QNRzVII4eQOQeQeQ.pdf

2. 处理论文: ...
```

## 自定义扩展

您可以根据需要扩展脚本功能：

1. 增加多线程/异步支持提高爬取速度
2. 添加错误重试机制
3. 提取更多论文元数据（作者、机构、摘要等）
4. 实现增量爬取，避免重复下载
5. 添加日志记录功能

## 版权声明

本脚本仅用于学习和研究目的，请遵守相关法律法规和网站使用条款。
