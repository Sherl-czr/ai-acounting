# 账目处理与可视化程序

## 项目简介
本程序是一个自动化的账目处理与可视化工具，主要功能包括：
1. 读取用户提供的消费记录和分类标准
2. 通过AI接口对消费记录进行分类处理
3. 生成详细的消费统计报告
4. 自动创建可视化图表（饼图和柱状图）
5. 识别并展示大额消费记录

## 依赖安装
在运行程序前，请确保已安装以下依赖：

```bash
pip install openai requests matplotlib
```

对于中文字体支持，不同系统需要额外配置：
- Windows：确保系统已安装微软雅黑（Microsoft YaHei）或黑体（SimHei）字体
- macOS：系统自带PingFang和STHeiti字体，无需额外安装
- Linux：建议安装文泉驿字体 `sudo apt-get install fonts-wqy-microhei`

## 配置修改
在使用前需要修改以下配置：
1. 打开 `accounting_processor.py` 文件
2. 找到以下代码并进行修改：
```python
# ... existing code ...
api_key = ""  # 替换为你的API Key
processor = AccountProcessor(api_key)
# ... existing code ...
```
3. 如果需要使用其他AI服务，可以修改base_url：
```python
# ... existing code ...
self.client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1"  # 修改为你的服务地址
)
# ... existing code ...
```

## 可扩展性
本程序具有良好的扩展性，以下是一些可扩展的方向：

1. **分类扩展**：
   - 修改 `categories.md` 文件添加新的消费分类
   - 在 `可视化.py` 的 `parse_config_file` 函数中添加对应的分类处理

2. **可视化扩展**：
   - 在 `create_visualizations` 函数中添加新的图表类型
   - 修改现有图表的样式和布局

3. **数据处理扩展**：
   - 在 `process_accounts` 方法中添加额外的数据处理逻辑
   - 修改 `extract_formatted_content` 方法以支持不同的输出格式

4. **输入格式扩展**：
   - 修改 `read_file` 方法以支持更多文件格式（如Excel、CSV等）
   - 添加新的文件解析逻辑

5. **报告生成**：
   - 添加PDF报告生成功能
   - 增加更多统计指标（如月度对比、趋势分析等）

## 使用说明
1. 准备两个输入文件：
   - `categories.md`：定义消费分类标准
   - `记账内容.md`：包含原始消费记录
2. 运行程序：
```bash
python accounting_processor.py
```
3. 程序将生成：
   - `config.txt`：处理后的格式化数据
   - `月度消费统计.png`：消费分类饼图
   - `月度5笔最高消费.png`：大额消费柱状图

这个README文件包含了项目介绍、依赖安装说明、配置修改指南和可扩展性说明。你可以根据实际需求进一步调整内容。