import difflib
import re
import time
import random

class ConversationContext:
    """对话上下文管理"""
    def __init__(self):
        self.user_name = None
        self.last_topic = None
        self.favorite_food = None
        self.favorite_movie = None
        self.last_question = None
        self.mood = "neutral"  # 情绪状态: neutral, happy, sad, excited
    
    def update_from_input(self, user_input):
        """从用户输入更新上下文"""
        # 提取用户姓名
        if not self.user_name:
            name_match = re.search(r"(?:我的名字是|我叫)(.+)", user_input)
            if name_match:
                self.user_name = name_match.group(1).strip()
        
        # 检测情绪
        if any(word in user_input for word in ["开心", "高兴", "快乐"]):
            self.mood = "happy"
        elif any(word in user_input for word in ["难过", "伤心", "不开心"]):
            self.mood = "sad"
        elif any(word in user_input for word in ["兴奋", "激动", "太棒了"]):
            self.mood = "excited"

class ThinkingAnimation:
    """思考动画"""
    def __init__(self, dots=3, delay=0.3):
        self.dots = dots
        self.delay = delay
        self.phrases = [
            "让我想想", 
            "思考中", 
            "这是个有趣的问题",
            "我需要考虑一下"
        ]
    
    def show(self):
        """显示思考动画"""
        phrase = random.choice(self.phrases)
        print(f"Jathniel：{phrase}", end="", flush=True)
        for _ in range(self.dots):
            time.sleep(self.delay)
            print(".", end="", flush=True)
        print()

def find_best_match(user_input, qa_database, threshold=0.6):
    """找到最佳匹配的问题"""
    # 1. 精确匹配
    for question in qa_database:
        if user_input.lower() == question.lower():
            return question
    
    # 2. 包含匹配
    for question in qa_database:
        if question.lower() in user_input.lower():
            return question
    
    # 3. 模糊匹配（使用相似度算法）
    best_match = None
    best_ratio = 0
    for question in qa_database:
        ratio = difflib.SequenceMatcher(None, user_input.lower(), question.lower()).ratio()
        if ratio > best_ratio and ratio > threshold:
            best_ratio = ratio
            best_match = question
    
    return best_match