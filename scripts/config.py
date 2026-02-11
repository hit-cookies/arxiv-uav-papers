"""
配置文件 - 定义优先研究机构和搜索参数
"""

# 顶尖无人机导航研究机构列表
PRIORITY_INSTITUTIONS = [
    # 北美
    "MIT", "Massachusetts Institute of Technology",
    "CMU", "Carnegie Mellon University",
    "Stanford", "Stanford University",
    "UC Berkeley", "University of California, Berkeley",
    "Caltech", "California Institute of Technology",
    "University of Pennsylvania", "UPenn", "GRASP",
    
    # 欧洲
    "ETH Zurich", "ETH Zürich",
    "University of Zurich", "UZH",
    "TUM", "Technical University of Munich",
    "Imperial College London",
    
    # 亚洲
    "Tsinghua", "清华大学",
    "HKUST", "Hong Kong University of Science and Technology",
    "NUS", "National University of Singapore",
    "Zhejiang University", "浙江大学",
    "BUAA", "北京航空航天大学", "Beihang University",
    "SJTU", "Shanghai Jiao Tong University", "上海交通大学",
]

# arXiv 搜索关键词
SEARCH_KEYWORDS = [
    "UAV",
    "drone",
    "unmanned aerial vehicle",
    "quadrotor",
    "multirotor",
]

# 导航相关关键词
NAVIGATION_KEYWORDS = [
    "navigation",
    "path planning",
    "trajectory",
    "obstacle avoidance",
    "SLAM",
    "localization",
    "mapping",
    "motion planning",
    "autonomous flight",
]

# 搜索的 arXiv 分类
ARXIV_CATEGORIES = [
    "cs.RO",  # Robotics
    "cs.AI",  # Artificial Intelligence
    "cs.CV",  # Computer Vision
    "cs.LG",  # Machine Learning
]

# 每天处理的最大论文数量
MAX_PAPERS_PER_DAY = 20

# Gemini API 配置
GEMINI_MODEL = "gemini-2.5-flash"  # 最新可用的 flash 模型
GEMINI_TEMPERATURE = 0.4
GEMINI_MAX_OUTPUT_TOKENS = 1024

# 速率控制
REQUEST_DELAY_SECONDS = 5  # Gemini API 请求间隔
