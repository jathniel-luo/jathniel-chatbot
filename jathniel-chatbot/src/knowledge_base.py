import json
import os

class KnowledgeBase:
    def __init__(self):
        self.learning_data_file = "data/jathniel_knowledge.json"
        self.conversation_history_file = "data/jathniel_conversation.json"
        self.qa_database_file = "data/jathniel_database.json"
        
        # 确保数据目录存在
        os.makedirs("data", exist_ok=True)
        
        self.learned_data = self.load_learned_data()
        self.conversation_history = self.load_conversation_history()
        self.qa_database = self.load_qa_database()
    
    def load_learned_data(self):
        """加载学习数据"""
        if os.path.exists(self.learning_data_file):
            try:
                with open(self.learning_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_learned_data(self):
        """保存学习数据"""
        with open(self.learning_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.learned_data, f, ensure_ascii=False, indent=2)
    
    def load_conversation_history(self):
        """加载对话历史"""
        if os.path.exists(self.conversation_history_file):
            try:
                with open(self.conversation_history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_conversation_history(self):
        """保存对话历史"""
        with open(self.conversation_history_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
    
    def save_conversation(self, message, role):
        """保存单条对话"""
        self.conversation_history.append({
            "role": role,
            "message": message,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        if len(self.conversation_history) > 100:  # 最多保存100条
            self.conversation_history.pop(0)
        self.save_conversation_history()
    
    def load_qa_database(self):
        """加载问答数据库"""
        # 如果数据库文件不存在，创建并初始化默认数据库
        if not os.path.exists(self.qa_database_file):
            default_data = self.get_default_knowledge()
            with open(self.qa_database_file, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
            return default_data
        
        # 如果文件存在，加载数据
        try:
            with open(self.qa_database_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self.get_default_knowledge()
    
    def get_default_knowledge(self):
        """获取默认知识库"""
        # 这里包含原有的默认知识库内容
        # 为了简洁，这里只显示一部分
        return {
            "你好": ["你好！很高兴认识你。", "嗨！你好啊！", "你好，很高兴和你聊天。", "你好！我是Jathniel，有什么我可以帮你的吗？"],
            "早上好": ["早上好！新的一天开始了，祝你有个好心情。", "早安！今天有什么计划吗？", "早上好！希望今天对你来说是美好的一天。"],
            # ... 其他知识
        }
    
    def merge_learned_knowledge(self):
        """合并学习到的知识到数据库"""
        for question, answers in self.learned_data.items():
            if question in self.qa_database:
                # 确保不添加重复的回答
                for answer in answers:
                    if answer not in self.qa_database[question]:
                        self.qa_database[question].append(answer)
            else:
                self.qa_database[question] = answers
        self.save_learned_data()