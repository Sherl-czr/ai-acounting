from 可视化 import ConsoleOutput
from openai import OpenAI
import os

class AccountProcessor:
    def __init__(self, api_key, base_url, model_name, output_widget, output_dir):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.console = ConsoleOutput(output_widget)
        self.output_dir = output_dir
        
    def read_file(self, file_path):
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            self.console.log(f"读取文件 {file_path} 失败: {str(e)}")
            return ""
    def get_prompt_template(self):
        return """

请将以下消费记录转换为标准格式。

【输出格式要求】
1. 每条记录使用格式：DATE:年-月-日 TYPE:类别 NAME:具体内容 COST:金额
2. 输出时在"# start"和"# end"之间展示结果
3. 金额保留两位小数

【分类标准】


【示例输出】
# start
DATE:2024-01-01 TYPE:饮料 NAME:咖啡 COST:32.00
DATE:2024-01-01 TYPE:食物 NAME:午餐 COST:45.00
# end

【需要转换的消费记录】


        """

    def create_prompt(self, categories_file, content_file):
        """组合 prompt"""
        categories = self.read_file(categories_file)
        content = self.read_file(content_file)
        prompt_template = self.get_prompt_template()


        prompt = prompt_template.replace(
            "【分类标准】\n", f"【分类标准】\n{categories}\n"
        ).replace(
            "【需要转换的消费记录】\n", f"【需要转换的消费记录】\n{content}\n"
        )

        self.console.log("\n=== 生成的 Prompt ===")
        self.console.log(prompt)
        self.console.log("=== Prompt 结束 ===\n")

        return prompt
    
        
    def process_accounts(self, prompt):
        """使用 AI 处理账目"""
        self.console.log("\n开始处理账目...")
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            self.console.log("AI 处理完成")
            return response.choices[0].message.content
        except Exception as e:
            self.console.log(f"API调用失败:")
            self.console.log(f"错误类型: {type(e).__name__}")
            self.console.log(f"错误信息: {str(e)}")
            return None
            
    def extract_formatted_content(self, ai_response):
        """从 AI 响应中提取格式化的内容"""
        if not ai_response:
            return None

        try:
            start_idx = ai_response.find('# start')
            end_idx = ai_response.find('# end')

            if start_idx != -1 and end_idx != -1:
                formatted_content = ai_response[start_idx:end_idx + len('# end')]
                return formatted_content
            return None
        except Exception as e:
            self.console.log(f"提取内容出错: {str(e)}")
            return None
            
    def save_to_config(self, content, output_file):
        """保存到配置文件"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            self.console.log(f"数据已保存到 {output_file}")
            return True
        except Exception as e:
            self.console.log(f"保存文件出错: {str(e)}")
            return False
            
    def run(self, categories_file, content_file):
        """运行整个流程"""
        output_file = os.path.join(self.output_dir, "config.txt")
        
        # 检查文件是否存在
        for file in [categories_file, content_file]:
            if not os.path.exists(file):
                self.console.log(f"错误: 找不到文件 {file}")
                return
                
        # 创建 prompt
        self.console.log("正在生成处理提示...")
        prompt = self.create_prompt(categories_file, content_file)
        
        # 处理账目
        self.console.log("正在处理账目...")
        ai_response = self.process_accounts(prompt)
        
        if ai_response:
            formatted_content = self.extract_formatted_content(ai_response)
            if formatted_content:
                if self.save_to_config(formatted_content, output_file):
                    self.console.log("\n开始生成可视化...")
                    try:
                        from 可视化 import create_visualizations
                        create_visualizations(output_file, self.console, self.output_dir)
                        self.console.log("可视化完成！")
                    except Exception as e:
                        self.console.log(f"可视化过程出错: {str(e)}")
                else:
                    self.console.log("保存文件失败！")
            else:
                self.console.log("无法提取格式化内容！")
        else:
            self.console.log("AI 处理失败！")