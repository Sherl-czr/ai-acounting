from openai import OpenAI
import requests
import json
import os



class AccountProcessor:
    def __init__(self, api_key):
        print("初始化客户端...")
        self.api_key = api_key
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
        print(f"客户端初始化完成，使用base_url: {self.client.base_url}")

    def test_connection(self):
        """测试API连接"""
        print("\n=== API 测试开始 ===")
        print(f"API Key: {'*' * (len(self.api_key) - 4) + self.api_key[-4:]}")

        try:
            print("\n测试API调用...")
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": "你好"}
                ]
            }
            print("发送请求...")
            print(f"请求头: {headers}")
            print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")

            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            print(f"API响应状态码: {response.status_code}")
            print(f"API响应内容: {response.text}")

            return response.status_code == 200

        except Exception as e:
            print(f"连接测试失败: {str(e)}")
            return False

    def read_file(self, file_path):
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"读取文件 {file_path} 失败: {str(e)}")
            return ""

    def create_prompt(self, categories_file, content_file):
        """组合 prompt"""
        categories = self.read_file(categories_file)
        content = self.read_file(content_file)
        prompt_template = self.read_file('prompt.md')

        prompt = prompt_template.replace(
            "【分类标准】\n",
            "【分类标准】\n" + categories + "\n"
        ).replace(
            "【需要转换的消费记录】\n",
            "【需要转换的消费记录】\n" + content + "\n"
        )

        print("\n=== 生成的 Prompt ===")
        print(prompt)
        print("=== Prompt 结束 ===\n")

        return prompt
    def process_accounts(self, prompt):
        """使用 AI 处理账目"""
        print("\n开始处理账目...")
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                result = response.json()
                print("AI 处理完成")
                return result['choices'][0]['message']['content']
            else:
                print(f"API 请求失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                return None

        except Exception as e:
            print(f"API调用失败:")
            print(f"错误类型: {type(e).__name__}")
            print(f"错误信息: {str(e)}")
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
            print(f"提取内容出错: {str(e)}")
            return None

    def save_to_config(self, content, output_file):
        """保存到配置文件"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"数据已保存到 {output_file}")
            return True
        except Exception as e:
            print(f"保存文件出错: {str(e)}")
            return False


def main():
    print("=== 账目处理程序启动 ===")

    # 初始化处理器
    api_key = ""
    processor = AccountProcessor(api_key)

    # 文件路径
    print("\n1. 开始处理账目")
    categories_file = "分类标准.md"
    content_file = "记账内容.md"
    output_file = "config.txt"

    # 检查文件是否存在
    for file in [categories_file, content_file]:
        if not os.path.exists(file):
            print(f"错误: 找不到文件 {file}")
            return

    # 创建 prompt
    print("正在生成处理提示...")
    prompt = processor.create_prompt(categories_file, content_file)

    # 处理账目
    print("正在处理账目...")
    ai_response = processor.process_accounts(prompt)
    if ai_response:
        formatted_content = processor.extract_formatted_content(ai_response)
        if formatted_content:
            if processor.save_to_config(formatted_content, output_file):
                print("\n3. 开始生成可视化...")
                try:
                    from 可视化 import main as visualize_main
                    visualize_main()
                    print("可视化完成！")
                except Exception as e:
                    print(f"可视化过程出错: {str(e)}")
            else:
                print("保存文件失败！")
        else:
            print("无法提取格式化内容！")
    else:
        print("AI 处理失败！")


if __name__ == "__main__":
    main()