#!/usr/bin/env python3

import os
import time
from playwright.sync_api import sync_playwright

# 配置参数
save_path = os.path.dirname(__file__) + '/pdf_paper_edu/'
limit = 20  # 每页论文数量
total_pages = 3  # 爬取的总页数

def main():
    # 创建保存目录
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)  # 调试时可以设置为False
        page = browser.new_page()
        
        for page_num in range(total_pages):
            print(f"\n=== 爬取第 {page_num + 1} 页 ===")
            
            # 构建页码链接
            # 注意：paper.edu.cn的分页可能是通过其他方式实现，这里假设是简单的page参数
            # 实际使用时可能需要根据网站的分页机制调整
            url = f"https://www.paper.edu.cn/releasepaper/subject.shtml?page={page_num + 1}"
            
            try:
                # 访问页面
                page.goto(url)
                page.wait_for_load_state('networkidle')
                
                # 等待论文列表加载完成
                page.wait_for_selector('.mylmchooseBox')
                
                # 获取所有论文卡片
                paper_cards = page.locator('.mylmchooseBox').all()
                print(f"找到 {len(paper_cards)} 篇论文")
                
                for index, card in enumerate(paper_cards):
                    try:
                        # 提取论文标题
                        title_element = card.locator('.llxarticle-title a')
                        title = title_element.inner_text().strip()
                        
                        # 提取论文详情页链接
                        paper_url = title_element.get_attribute('href')
                        
                        if not paper_url.startswith('http'):
                            paper_url = f"https://www.paper.edu.cn{paper_url}"
                        
                        print(f"\n{index + 1}. 处理论文: {title}")
                        print(f"   详情页: {paper_url}")
                        
                        # 访问论文详情页
                        detail_page = browser.new_page()
                        detail_page.goto(paper_url)
                        detail_page.wait_for_load_state('networkidle')
                        
                        # 获取隐藏的paper_id
                        paper_id_element = detail_page.locator('input[name="paper_id"]')
                        paper_id = paper_id_element.get_attribute('value')
                        
                        if paper_id:
                            print(f"   Paper ID: {paper_id}")
                            
                            # 构建PDF下载链接
                            pdf_url = f"https://www.paper.edu.cn/download/downpdf/paper/{paper_id}"
                            print(f"   PDF链接: {pdf_url}")
                            
                            # 下载PDF
                            response = detail_page.request.get(pdf_url)
                            
                            if response.ok:
                                # 生成保存文件名（使用paper_id作为文件名）
                                pdf_filename = f"{paper_id}.pdf"
                                pdf_path = os.path.join(save_path, pdf_filename)
                                
                                with open(pdf_path, "wb") as f:
                                    f.write(response.body())
                                
                                print(f"   ✓ 下载成功: {pdf_filename}")
                            else:
                                print(f"   ✗ 下载失败，状态码: {response.status}")
                        else:
                            print(f"   ✗ 未找到Paper ID")
                        
                        # 关闭详情页
                        detail_page.close()
                        
                        # 避免请求过快
                        time.sleep(1)
                        
                    except Exception as e:
                        print(f"   ✗ 处理论文时出错: {str(e)}")
                        continue
                
                print(f"\n=== 第 {page_num + 1} 页爬取完成 ===")
                print("=" * 50)
                
            except Exception as e:
                print(f"✗ 爬取第 {page_num + 1} 页时出错: {str(e)}")
                continue
        
        # 关闭浏览器
        browser.close()
        print(f"\n=== 所有页面爬取完成 ===")
        print(f"PDF文件保存在: {save_path}")

if __name__ == "__main__":
    main()
