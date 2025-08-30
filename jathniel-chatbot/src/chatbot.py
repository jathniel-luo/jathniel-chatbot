import re
import random
import time
from datetime import datetime
from .knowledge_base import KnowledgeBase
from .utils import ConversationContext, ThinkingAnimation

class JathnielChatbot:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.context = ConversationContext()
        self.thinking_animation = ThinkingAnimation()
        
    def run(self):
        """运行聊天机器人"""
        print("Jathniel：你好！我是智能小助手Jathniel，有什么我可以帮助你的吗？")
        print("Jathniel：我现在更聪明了，支持多种学习方式！")
        
        # 主动问候
        if self.context.user_name:
            print(f"Jathniel：{self.context.user_name}，很高兴再次见到你！")
        elif self.knowledge_base.conversation_history:
            print("Jathniel：欢迎回来！")
        
        while True:
            user_input = input("你: ").strip()
            if not user_input:
                continue
                
            # 检查是否要结束对话
            if any(keyword in user_input.lower() for keyword in ["再见", "退出", "结束"]):
                print(random.choice(self.knowledge_base.qa_database["再见"]))
                break
                
            # 思考动画
            self.thinking_animation.show()
            
            # 处理输入并获取回复
            bot_response = self.handle_input(user_input)
            print(f"Jathniel：{bot_response}")
    
    def handle_input(self, user_input):
        """处理用户输入"""
        # 保存对话历史
        self.knowledge_base.save_conversation(user_input, "user")
        
        # 处理特殊命令
        special_response = self.handle_special_commands(user_input)
        if special_response:
            self.knowledge_base.save_conversation(special_response, "bot")
            return special_response
        
        # 智能学习功能
        if any(keyword in user_input for keyword in ["记住", "学习", "回答"]):
            response = self.smart_learn(user_input)
            self.knowledge_base.save_conversation(response, "bot")
            return response
        
        # 理解用户意图
        intent_response = self.understand_intent(user_input)
        if intent_response:
            self.knowledge_base.save_conversation(intent_response, "bot")
            return intent_response
        
        # 使用上下文信息
        if self.context.user_name:
            personalized_input = user_input.replace("我", self.context.user_name)
        else:
            personalized_input = user_input
        
        # 记录当前问题（用于后续可能的上下文学习）
        self.context.last_question = personalized_input
        
        # 智能匹配
        best_match = self.find_best_match(personalized_input)
        if best_match:
            response = random.choice(self.knowledge_base.qa_database[best_match])
            self.context.last_topic = best_match
            response = self.personalize_response(response, user_input)
            self.knowledge_base.save_conversation(response, "bot")
            return response
        
        # 尝试基于上下文回应
        if self.context.last_topic:
            # 主动提问
            follow_up = self.ask_follow_up(self.context.last_topic)
            if follow_up:
                self.knowledge_base.save_conversation(follow_up, "bot")
                return follow_up
        
        # 如果还是没有匹配，返回默认回复并学习
        self.context.last_question = user_input
        response = "我不太明白你的意思，可以教我如何回答吗？例如：\n- 记住：问题=回答\n- 当有人问这个问题时就回答你的答案"
        self.knowledge_base.save_conversation(response, "bot")
        return response
    
    # 其他方法保持不变，只是需要调整引用方式
    # ...