"""
使用 Google Gemini AI 分析论文
"""

import os
import time
import sys
from typing import List, Dict
import google.generativeai as genai

from config import (
    GEMINI_MODEL,
    GEMINI_TEMPERATURE,
    GEMINI_MAX_OUTPUT_TOKENS,
    REQUEST_DELAY_SECONDS
)


def initialize_gemini(api_key: str):
    """初始化 Gemini API"""
    genai.configure(api_key=api_key)
    print(f"✅ Gemini API 已配置")


def create_analysis_prompt(paper: Dict) -> str:
    """
    为论文创建分析提示词
    
    Args:
        paper: 论文字典
    
    Returns:
        提示词字符串
    """
    # 构建机构信息字符串
    affiliations = paper.get('affiliations', {})
    institutions = affiliations.get('_institutions', []) if isinstance(affiliations, dict) else []
    institution_line = f"机构：{' · '.join(institutions)}\n" if institutions else ""
    
    prompt = f"""请分析以下无人机导航领域的学术论文，用简洁的中文回答：

论文标题：{paper['title']}

作者：{', '.join(paper['authors'])}
{institution_line}

摘要：
{paper['summary'][:3000]}

请提取以下信息：

1. **解决的核心问题**（1-2句话，说明论文针对什么具体问题或挑战）

2. **主要创新点**（3-5点，每点1句话，突出技术创新和方法论贡献）

输出格式要求：
- 使用简洁专业的语言
- 避免重复摘要内容
- 突出实质性贡献
- 不要包含"根据摘要"等引导语

输出格式示例：
【解决的问题】
针对密集障碍物环境下的无人机实时避障问题

【主要创新点】
1. 提出了基于深度强化学习的端到端避障框架
2. 设计了轻量级3D卷积神经网络用于实时感知
3. 引入了安全约束的奖励函数确保飞行安全
"""
    return prompt


def analyze_single_paper(model, paper: Dict, retry_count: int = 3) -> Dict:
    """
    分析单篇论文
    
    Args:
        model: Gemini 模型实例
        paper: 论文字典
        retry_count: 重试次数
    
    Returns:
        添加了分析结果的论文字典
    """
    prompt = create_analysis_prompt(paper)
    
    for attempt in range(retry_count):
        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    'temperature': GEMINI_TEMPERATURE,
                    'top_p': 0.95,
                    'top_k': 40,
                    'max_output_tokens': GEMINI_MAX_OUTPUT_TOKENS,
                }
            )
            
            analysis = response.text.strip()
            
            # 解析分析结果
            paper['analysis'] = analysis
            paper['analysis_success'] = True
            
            return paper
            
        except Exception as e:
            error_msg = str(e)
            print(f"   ⚠️  尝试 {attempt + 1}/{retry_count} 失败: {error_msg[:100]}")
            
            # 检测配额限制错误
            if '429' in error_msg or 'quota' in error_msg.lower() or 'rate limit' in error_msg.lower():
                wait_time = 60  # 配额限制时等待 60 秒
                print(f"   ⏳ 检测到配额限制，等待 {wait_time} 秒...")
                time.sleep(wait_time)
            elif attempt < retry_count - 1:
                time.sleep(REQUEST_DELAY_SECONDS)
            
            if attempt == retry_count - 1:
                # 所有重试失败，使用原始摘要
                paper['analysis'] = f"【解决的问题】\n{paper['summary'][:200]}...\n\n【主要创新点】\n（AI分析失败，请查看原文摘要）"
                paper['analysis_success'] = False
    
    return paper


def analyze_papers(papers: List[Dict], api_key: str) -> List[Dict]:
    """
    批量分析论文
    
    Args:
        papers: 论文列表
        api_key: Gemini API Key
    
    Returns:
        添加了分析结果的论文列表
    """
    print("\n" + "=" * 60)
    print("🤖 开始使用 Gemini AI 分析论文")
    print("=" * 60)
    
    initialize_gemini(api_key)
    
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        print(f"✅ 使用模型: {GEMINI_MODEL}")
    except Exception as e:
        print(f"❌ 初始化模型失败: {e}")
        return papers
    
    analyzed_papers = []
    success_count = 0
    
    for i, paper in enumerate(papers, 1):
        print(f"\n📄 [{i}/{len(papers)}] 分析: {paper['title'][:60]}...")
        
        analyzed_paper = analyze_single_paper(model, paper)
        analyzed_papers.append(analyzed_paper)
        
        if analyzed_paper.get('analysis_success', False):
            success_count += 1
            print(f"   ✅ 分析成功")
        else:
            print(f"   ⚠️  分析失败，使用原始摘要")
        
        # 速率控制：避免超过 Gemini API 限制（15 RPM for flash）
        if i < len(papers):
            time.sleep(REQUEST_DELAY_SECONDS)
    
    print("\n" + "=" * 60)
    print(f"✅ 分析完成: {success_count}/{len(papers)} 篇成功")
    print("=" * 60)
    
    return analyzed_papers


def main():
    """主函数 - 用于测试"""
    # 这个模块通常被 main.py 调用，这里提供测试接口
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ 错误: 未设置 GEMINI_API_KEY 环境变量")
        sys.exit(1)
    
    # 测试用的示例论文
    test_paper = {
        'title': 'Deep Reinforcement Learning for UAV Navigation',
        'authors': ['John Doe', 'Jane Smith'],
        'summary': 'This paper proposes a novel deep reinforcement learning approach for autonomous UAV navigation in complex environments...',
        'link': 'https://arxiv.org/abs/2401.00000',
        'published': '2024-01-01',
    }
    
    result = analyze_papers([test_paper], api_key)
    
    if result and result[0].get('analysis'):
        print("\n分析结果:")
        print(result[0]['analysis'])


if __name__ == "__main__":
    main()
