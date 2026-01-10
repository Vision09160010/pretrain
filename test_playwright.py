#!/usr/bin/env python3

from playwright.sync_api import sync_playwright

print("测试Playwright是否正常工作...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.paper.edu.cn/releasepaper/subject.shtml")
    
    # 检查页面标题
    title = page.title()
    print(f"页面标题: {title}")
    
    # 检查是否能找到论文列表
    paper_cards = page.locator('.mylmchooseBox').all()
    print(f"找到 {len(paper_cards)} 篇论文")
    
    browser.close()

print("✓ Playwright测试成功！")
print("您可以开始使用paper_edu_crawler.py脚本了")
