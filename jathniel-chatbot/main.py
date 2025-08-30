#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import JathnielChatbot
from math_helper import MathHelper

def main():
    """主函数"""
    print("请选择模式:")
    print("1. Jath - 聊天模式")
    print("2. Niel - 数学模式")
    
    choice = input("请输入选择 (1 或 2): ").strip()
    
    if choice == "1":
        chatbot = JathnielChatbot()
        chatbot.run()
    elif choice == "2":
        run_math_mode()
    else:
        print("输入错误，请重新运行程序并输入1或2。")

def run_math_mode():
    """运行数学模式"""
    math_helper = MathHelper()
    
    print("Niel：你好！我是数学助手Niel，我可以帮你解决各种数学问题。")
    print("Niel：支持的操作：+ - * / ** sin cos tan sqrt")
    print("Niel：例如：sin(30) 或 2+3*4 或 根号16")
    
    while True:
        user_input = input("你: ").strip()
        if not user_input:
            continue
            
        # 检查是否要结束对话
        if any(keyword in user_input.lower() for keyword in ["再见", "退出", "结束"]):
            print("Niel：再见！下次有数学问题再来找我。")
            break
            
        # 处理基本问候
        if "你好" in user_input:
            print("Niel：你好！有什么数学问题需要解决吗？")
            continue
            
        if "谢谢" in user_input:
            print("Niel：不客气！随时为你效劳。")
            continue
            
        # 处理特殊数学问题
        special_result = math_helper.handle_special_math(user_input)
        if special_result:
            print(f"Niel：{special_result}")
            continue
            
        # 处理数学表达式
        try:
            result = math_helper.safe_evaluate(user_input)
            print(f"Niel：计算结果: {result}")
        except Exception as e:
            print(f"Niel：计算错误: {str(e)}")

if __name__ == "__main__":
    main()