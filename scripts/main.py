"""
主执行脚本 - 协调所有模块完成每日论文分析任务
"""

import os
import sys
from datetime import datetime

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fetch_papers import fetch_recent_papers, filter_papers
from analyze_papers import analyze_papers
from send_notification import send_notification


def print_banner():
    """打印启动横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     arXiv 无人机导航论文自动分析与推送系统                ║
║     Powered by Gemini AI + Server 酱                      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)
    print(f"🕐 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def check_environment() -> tuple:
    """
    检查环境变量配置
    
    Returns:
        (gemini_key, serverchan_key) 元组
    """
    print("🔧 检查环境配置...")
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    serverchan_key = os.getenv('SERVERCHAN_KEY')
    
    if not gemini_key:
        print("❌ 错误: 未设置 GEMINI_API_KEY 环境变量")
        sys.exit(1)
    else:
        print(f"✅ GEMINI_API_KEY: {gemini_key[:20]}...")
    
    if not serverchan_key:
        print("❌ 错误: 未设置 SERVERCHAN_KEY 环境变量")
        sys.exit(1)
    else:
        print(f"✅ SERVERCHAN_KEY: {serverchan_key[:15]}...")
    
    print()
    return gemini_key, serverchan_key


def main():
    """主函数"""
    print_banner()
    
    # 1. 检查环境
    gemini_key, serverchan_key = check_environment()
    
    try:
        # 2. 获取论文
        papers = fetch_recent_papers(days_back=3, max_results=100)
        
        if not papers:
            print("\n⚠️  未找到相关论文，发送空报告...")
            send_notification([], serverchan_key)
            print("\n✅ 任务完成")
            return 0
        
        # 3. 过滤和排序
        filtered_papers = filter_papers(papers)
        
        # 4. AI 分析
        analyzed_papers = analyze_papers(filtered_papers, gemini_key)
        
        # 5. 发送通知
        success = send_notification(analyzed_papers, serverchan_key)
        
        # 6. 总结
        print("\n" + "=" * 60)
        print("📊 执行总结")
        print("=" * 60)
        print(f"✅ 获取论文: {len(papers)} 篇")
        print(f"✅ 筛选后: {len(filtered_papers)} 篇")
        print(f"✅ 分析成功: {sum(1 for p in analyzed_papers if p.get('analysis_success', False))} 篇")
        print(f"{'✅' if success else '❌'} 微信推送: {'成功' if success else '失败'}")
        print(f"🕐 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断执行")
        return 130
    
    except Exception as e:
        print(f"\n\n❌ 执行过程中出现错误:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
