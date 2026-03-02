"""
从 arXiv 获取最新的无人机导航相关论文
"""

import feedparser
import urllib.parse
from datetime import datetime, timedelta
from typing import List, Dict
import time
import sys
import requests

from config import (
    SEARCH_KEYWORDS,
    NAVIGATION_KEYWORDS,
    PRIORITY_INSTITUTIONS,
    MAX_PAPERS_PER_DAY
)


def build_arxiv_query() -> str:
    """构建 arXiv API 搜索查询字符串"""
    # 构建搜索词：(UAV OR drone OR ...) AND (navigation OR path planning OR ...)
    uav_terms = " OR ".join([f'all:"{kw}"' if " " in kw else f'all:{kw}' 
                              for kw in SEARCH_KEYWORDS])
    nav_terms = " OR ".join([f'all:"{kw}"' if " " in kw else f'all:{kw}' 
                              for kw in NAVIGATION_KEYWORDS])
    
    query = f"({uav_terms}) AND ({nav_terms})"
    return query


def fetch_recent_papers(days_back: int = 7, max_results: int = 100) -> List[Dict]:
    """
    从 arXiv 获取最近几天的论文
    
    Args:
        days_back: 查询最近几天的论文
        max_results: 最大返回结果数
    
    Returns:
        论文列表，每篇论文包含 title, authors, summary, link, published, affiliations
    """
    base_url = "http://export.arxiv.org/api/query?"
    
    query = build_arxiv_query()
    
    params = {
        'search_query': query,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending',
        'max_results': max_results,
    }
    
    url = base_url + urllib.parse.urlencode(params)
    
    print(f"🔍 查询 arXiv API...")
    print(f"   查询语句: {query[:100]}...")
    
    # 遵守 arXiv API 使用规范：请求之间间隔 3 秒
    time.sleep(3)
    
    try:
        feed = feedparser.parse(url)
    except Exception as e:
        print(f"❌ arXiv API 请求失败: {e}")
        return []
    
    if feed.bozo:
        print(f"⚠️  警告: RSS feed 解析可能有问题")
    
    papers = []
    cutoff_date = datetime.now() - timedelta(days=days_back)
    
    for entry in feed.entries:
        try:
            # 解析发布日期
            published = datetime.strptime(entry.published, '%Y-%m-%dT%H:%M:%SZ')
            
            # 只保留最近几天的论文
            if published < cutoff_date:
                continue
            
            # 提取作者信息（完整列表）
            authors = [author.name for author in entry.authors]
            
            # 机构信息通过 Semantic Scholar API 后续补充
            affiliations = {}
            
            paper = {
                'title': entry.title.replace('\n', ' ').strip(),
                'authors': authors,
                'summary': entry.summary.replace('\n', ' ').strip(),
                'link': entry.link,
                'pdf_link': entry.link.replace('/abs/', '/pdf/'),
                'published': published.strftime('%Y-%m-%d'),
                'arxiv_id': entry.id.split('/abs/')[-1],
                'affiliations': affiliations,
                'is_priority': False,  # 稍后判断
            }
            
            papers.append(paper)
            
        except Exception as e:
            print(f"⚠️  解析论文条目出错: {e}")
            continue
    
    print(f"✅ 获取到 {len(papers)} 篇最近 {days_back} 天的论文")
    
    # 通过 Semantic Scholar API 补充机构信息
    papers = enrich_papers_with_affiliations(papers)
    
    return papers


def fetch_affiliations_from_semantic_scholar(arxiv_id: str) -> Dict[str, list]:
    """
    通过 Semantic Scholar API 获取论文作者的机构信息
    
    Args:
        arxiv_id: arXiv 论文 ID（如 2401.12345 或 2401.12345v1）
    
    Returns:
        字典，键为作者姓名，值为机构列表；以及特殊键 '_institutions' 存储去重后的机构列表
    """
    # 去掉版本号（如 v1, v2）
    clean_id = arxiv_id.split('v')[0]
    
    url = f"https://api.semanticscholar.org/graph/v1/paper/ARXIV:{clean_id}"
    params = {"fields": "authors.name,authors.affiliations"}
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            return {}
        data = resp.json()
        
        authors_data = data.get("authors", [])
        affiliations_map: Dict[str, list] = {}
        all_institutions = []
        
        for author in authors_data:
            name = author.get("name", "")
            affils = author.get("affiliations", [])
            affiliations_map[name] = affils
            for inst in affils:
                if inst and inst not in all_institutions:
                    all_institutions.append(inst)
        
        affiliations_map["_institutions"] = all_institutions
        return affiliations_map
        
    except Exception as e:
        print(f"   ⚠️  Semantic Scholar 查询失败 ({arxiv_id}): {e}")
        return {}


def enrich_papers_with_affiliations(papers: List[Dict]) -> List[Dict]:
    """
    批量为论文补充机构信息
    
    Args:
        papers: 论文列表
    
    Returns:
        添加了机构信息的论文列表
    """
    print(f"\n🏛️  正在通过 Semantic Scholar 获取机构信息...")
    success_count = 0
    
    for i, paper in enumerate(papers):
        arxiv_id = paper.get("arxiv_id", "")
        if not arxiv_id:
            continue
        
        affiliations_map = fetch_affiliations_from_semantic_scholar(arxiv_id)
        
        if affiliations_map:
            paper["affiliations"] = affiliations_map
            institutions = affiliations_map.get("_institutions", [])
            if institutions:
                success_count += 1
                print(f"   [{i+1}/{len(papers)}] ✅ {paper['title'][:50]}... → {', '.join(institutions[:3])}")
            else:
                print(f"   [{i+1}/{len(papers)}] ℹ️  {paper['title'][:50]}... → 未找到机构信息")
        else:
            print(f"   [{i+1}/{len(papers)}] ❌ {paper['title'][:50]}... → 查询失败")
        
        # 遵守 Semantic Scholar API 限速（无 key：1 req/s）
        time.sleep(1.2)
    
    print(f"✅ 机构信息补充完成（{success_count}/{len(papers)} 篇成功）")
    return papers


def check_priority_institution(paper: Dict) -> bool:
    """
    检查论文是否来自优先研究机构
    
    Args:
        paper: 论文字典
    
    Returns:
        是否为优先机构
    """
    # 优先使用 Semantic Scholar 获取的机构信息
    institutions = []
    affiliations = paper.get('affiliations', {})
    if isinstance(affiliations, dict):
        institutions = affiliations.get('_institutions', [])
    
    # 如果有 Semantic Scholar 机构数据则优先使用
    if institutions:
        search_text = ' '.join(institutions).lower()
    else:
        # 备用：在标题、作者列表、摘要中搜索机构名称
        search_text = f"{paper['title']} {' '.join(paper['authors'])} {paper['summary']}".lower()
    
    for institution in PRIORITY_INSTITUTIONS:
        if institution.lower() in search_text:
            return True
    
    return False


def prioritize_papers(papers: List[Dict]) -> List[Dict]:
    """
    给论文排序，优先机构的论文排在前面
    
    Args:
        papers: 论文列表
    
    Returns:
        排序后的论文列表
    """
    for paper in papers:
        paper['is_priority'] = check_priority_institution(paper)
    
    # 按优先级排序（优先机构在前），然后按日期
    sorted_papers = sorted(
        papers,
        key=lambda x: (not x['is_priority'], x['published']),
        reverse=True
    )
    
    priority_count = sum(1 for p in sorted_papers if p['is_priority'])
    print(f"⭐ {priority_count} 篇来自优先研究机构")
    
    return sorted_papers


def filter_papers(papers: List[Dict], max_papers: int = MAX_PAPERS_PER_DAY) -> List[Dict]:
    """
    过滤并限制论文数量
    
    Args:
        papers: 论文列表
        max_papers: 最大保留论文数
    
    Returns:
        过滤后的论文列表
    """
    # 先排序
    papers = prioritize_papers(papers)
    
    # 限制数量
    if len(papers) > max_papers:
        print(f"📊 限制论文数量: {len(papers)} -> {max_papers}")
        papers = papers[:max_papers]
    
    return papers


def main():
    """主函数 - 获取并过滤论文"""
    print("=" * 60)
    print("📚 开始获取 arXiv 无人机导航论文")
    print("=" * 60)
    
    # 获取最近 3 天的论文（避免遗漏周末更新）
    papers = fetch_recent_papers(days_back=3, max_results=100)
    
    if not papers:
        print("❌ 没有找到相关论文")
        return []
    
    # 过滤和排序
    filtered_papers = filter_papers(papers)
    
    print("\n" + "=" * 60)
    print(f"✅ 最终筛选出 {len(filtered_papers)} 篇论文待分析")
    print("=" * 60)
    
    # 显示前几篇论文标题
    print("\n📑 论文预览:")
    for i, paper in enumerate(filtered_papers[:5], 1):
        priority_mark = "⭐" if paper['is_priority'] else "  "
        print(f"{priority_mark} {i}. {paper['title'][:80]}...")
    
    if len(filtered_papers) > 5:
        print(f"   ... 还有 {len(filtered_papers) - 5} 篇论文")
    
    return filtered_papers


if __name__ == "__main__":
    papers = main()
    
    # 返回论文数量作为退出码（用于调试）
    sys.exit(0 if papers else 1)
