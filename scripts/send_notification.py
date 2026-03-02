"""
通过 Server 酱发送微信通知
"""

import os
import sys
import requests
from datetime import datetime
from typing import List, Dict
import urllib3

# 禁用 SSL 警告（解决某些网络环境的 SSL 问题）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def format_paper_card(paper: Dict, index: int) -> str:
    """
    格式化单篇论文为 Markdown 卡片
    
    Args:
        paper: 论文字典
        index: 论文编号
    
    Returns:
        Markdown 格式的论文卡片
    """
    # 优先机构标记
    priority_mark = "⭐ " if paper.get('is_priority', False) else ""
    
    # 完整作者列表
    all_authors = paper.get('authors', [])
    author_str = ', '.join(all_authors)
    
    # 机构信息
    affiliations = paper.get('affiliations', {})
    institutions = []
    if isinstance(affiliations, dict):
        institutions = affiliations.get('_institutions', [])
    
    if institutions:
        institution_str = f"**机构**: {' · '.join(institutions)}  "
    else:
        institution_str = ""
    
    # 构建卡片
    card = f"""### {priority_mark}{index}. {paper['title']}

**作者**: {author_str}  
{institution_str}
**发布日期**: {paper['published']}  
**arXiv**: [{paper['arxiv_id']}]({paper['link']})

{paper.get('analysis', paper['summary'][:300] + '...')}

---

"""
    return card


def build_notification_message(papers: List[Dict]) -> tuple:
    """
    构建完整的通知消息
    
    Args:
        papers: 论文列表
    
    Returns:
        (title, content) 元组
    """
    today = datetime.now().strftime('%Y年%m月%d日')
    
    # 统计信息
    total_count = len(papers)
    priority_count = sum(1 for p in papers if p.get('is_priority', False))
    success_count = sum(1 for p in papers if p.get('analysis_success', False))
    
    # 消息标题
    title = f"📚 arXiv无人机导航论文日报 ({today})"
    
    # 消息内容
    content = f"""# 📚 今日 arXiv 无人机导航论文精选

**日期**: {today}  
**论文总数**: {total_count} 篇  
**优先机构**: {priority_count} 篇 ⭐  
**AI分析成功**: {success_count}/{total_count} 篇

---

"""
    
    # 添加每篇论文
    for i, paper in enumerate(papers, 1):
        card = format_paper_card(paper, i)
        content += card
    
    # 添加页脚
    content += f"""

---

🤖 *本报告由 GitHub Actions + Gemini AI 自动生成*  
📅 *生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return title, content


def send_to_serverchan(sendkey: str, title: str, content: str, retry_count: int = 3) -> bool:
    """
    发送消息到 Server 酱
    
    Args:
        sendkey: Server 酱 SendKey
        title: 消息标题
        content: 消息内容（支持 Markdown）
        retry_count: 重试次数
    
    Returns:
        是否发送成功
    """
    url = f"https://sctapi.ftqq.com/{sendkey}.send"
    
    # Server 酱消息长度限制：标题 ≤ 100字，内容 ≤ 64KB
    if len(title) > 100:
        title = title[:97] + "..."
    
    if len(content.encode('utf-8')) > 64 * 1024:
        print("⚠️  消息内容超过 64KB，进行截断...")
        # 简单截断（保留前 60KB）
        while len(content.encode('utf-8')) > 60 * 1024:
            content = content[:-1000]
        content += "\n\n...(内容过长已截断)"
    
    data = {
        "title": title,
        "desp": content
    }
    
    for attempt in range(retry_count):
        try:
            print(f"\n📤 发送微信通知 (尝试 {attempt + 1}/{retry_count})...")
            
            # 自动检测代理环境变量
            proxies = {}
            http_proxy = os.getenv('http_proxy') or os.getenv('HTTP_PROXY')
            https_proxy = os.getenv('https_proxy') or os.getenv('HTTPS_PROXY')
            if http_proxy:
                proxies['http'] = http_proxy
            if https_proxy:
                proxies['https'] = https_proxy
            
            response = requests.post(url, data=data, timeout=15, verify=False, proxies=proxies if proxies else None)
            result = response.json()
            
            # 检查返回结果
            if result.get('code') == 0:
                print(f"✅ 消息发送成功!")
                print(f"   Push ID: {result.get('data', {}).get('pushid', 'N/A')}")
                return True
            else:
                print(f"❌ 发送失败: {result.get('message', '未知错误')}")
                print(f"   完整响应: {result}")
                
        except requests.exceptions.Timeout:
            print(f"⚠️  请求超时")
        except Exception as e:
            print(f"❌ 发送出错: {str(e)}")
        
        # 重试延迟
        if attempt < retry_count - 1:
            import time
            time.sleep(2)
    
    print(f"❌ 所有尝试均失败")
    return False


def send_notification(papers: List[Dict], sendkey: str) -> bool:
    """
    发送论文分析通知
    
    Args:
        papers: 论文列表
        sendkey: Server 酱 SendKey
    
    Returns:
        是否发送成功
    """
    print("\n" + "=" * 60)
    print("📱 准备发送微信通知")
    print("=" * 60)
    
    if not papers:
        print("⚠️  没有论文需要推送")
        # 发送一条简单的通知
        title = "📭 今日无新论文"
        content = f"今天没有找到符合条件的无人机导航论文。\n\n生成时间: {datetime.now()}"
        return send_to_serverchan(sendkey, title, content)
    
    # 构建消息
    title, content = build_notification_message(papers)
    
    print(f"📝 消息标题: {title}")
    print(f"📝 消息长度: {len(content)} 字符 ({len(content.encode('utf-8'))} 字节)")
    
    # 发送
    success = send_to_serverchan(sendkey, title, content)
    
    return success


def main():
    """主函数 - 用于测试"""
    sendkey = os.getenv('SERVERCHAN_KEY')
    
    if not sendkey:
        print("❌ 错误: 未设置 SERVERCHAN_KEY 环境变量")
        sys.exit(1)
    
    # 测试用的示例论文
    test_papers = [
        {
            'title': 'Deep Learning for Autonomous Drone Navigation',
            'authors': ['Zhang Wei', 'Li Ming', 'Wang Hua'],
            'published': '2024-02-11',
            'link': 'https://arxiv.org/abs/2402.00001',
            'arxiv_id': '2402.00001',
            'is_priority': True,
            'analysis_success': True,
            'analysis': """【解决的问题】
针对复杂动态环境下无人机实时导航的挑战

【主要创新点】
1. 提出了端到端的深度强化学习导航框架
2. 设计了轻量级视觉感知模块适应嵌入式平台
3. 引入了安全约束确保飞行可靠性"""
        }
    ]
    
    success = send_notification(test_papers, sendkey)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
