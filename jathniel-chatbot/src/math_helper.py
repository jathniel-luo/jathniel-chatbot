import math
import re

class MathHelper:
    """数学计算助手"""
    @staticmethod
    def safe_evaluate(expression):
        """安全地评估数学表达式"""
        try:
            # 替换运算符
            expression = expression.replace('加', '+').replace('减', '-')
            expression = expression.replace('乘', '*').replace('除', '/')
            expression = expression.replace('×', '*').replace('÷', '/')
            expression = expression.replace('^', '**')
            
            # 处理特殊表达
            expression = expression.replace('的平方', '**2')
            expression = expression.replace('的立方', '**3')
            
            # 处理根号
            expression = re.sub(r'根号(\d+\.?\d*)', r'math.sqrt(\1)', expression)
            
            # 处理角度问题
            expression = expression.replace('度', '*math.pi/180')
            
            # 安全评估环境
            safe_env = {
                'math': math,
                '__builtins__': None
            }
            
            # 添加安全函数
            safe_funcs = ['sin', 'cos', 'tan', 'sqrt', 'log', 'log10', 'exp', 'radians', 'degrees', 'pi', 'e']
            for func in safe_funcs:
                if hasattr(math, func):
                    safe_env[func] = getattr(math, func)
            
            result = eval(expression, safe_env)
            
            # 格式化结果
            if isinstance(result, float) and result.is_integer():
                return int(result)
            return result
        except Exception as e:
            return f"计算错误: {str(e)}"
    
    @staticmethod
    def handle_special_math(user_input):
        """处理特殊数学问题"""
        if '圆周率' in user_input or 'π' in user_input or 'pi' in user_input:
            return f"圆周率π ≈ {math.pi}"
        
        if '自然常数' in user_input or 'e' in user_input:
            return f"自然常数e ≈ {math.e}"
        
        # 度与弧度转换
        deg_match = re.search(r'(\d+\.?\d*)度等于多少弧度', user_input)
        if deg_match:
            deg = float(deg_match.group(1))
            return f"{deg}度 ≈ {math.radians(deg)}弧度"
        
        rad_match = re.search(r'(\d+\.?\d*)弧度等于多少度', user_input)
        if rad_match:
            rad = float(rad_match.group(1))
            return f"{rad}弧度 ≈ {math.degrees(rad)}度"
        
        # 阶乘
        fact_match = re.search(r'(\d+)的阶乘', user_input)
        if fact_match:
            num = int(fact_match.group(1))
            if num <= 20:  # 避免大数阶乘
                return f"{num}! = {math.factorial(num)}"
            return f"{num}的阶乘太大，无法计算"
        
        # 最大公约数
        gcd_match = re.search(r'(\d+)和(\d+)的最大公约数', user_input)
        if gcd_match:
            a = int(gcd_match.group(1))
            b = int(gcd_match.group(2))
            return f"GCD({a}, {b}) = {math.gcd(a, b)}"
        
        # 最小公倍数
        lcm_match = re.search(r'(\d+)和(\d+)的最小公倍数', user_input)
        if lcm_match:
            a = int(lcm_match.group(1))
            b = int(lcm_match.group(2))
            lcm_val = abs(a * b) // math.gcd(a, b) if a and b else 0
            return f"LCM({a}, {b}) = {lcm_val}"
        
        return None