# 账目处理与可视化程序

## 项目简介
本程序是一个自动化的账目处理与可视化工具，主要功能包括：
1. 读取用户提供的消费记录和分类标准
2. 通过AI接口对消费记录进行分类处理
3. 生成详细的消费统计报告
4. 自动创建可视化图表（饼图和柱状图）
5. 识别并展示大额消费记录
6. **新增**：支持打包为可执行文件，方便分发
7. **新增**：支持自定义输出目录和程序图标

## 依赖安装
在运行程序前，请确保已安装以下依赖：

```bash
pip install openai requests matplotlib pyqt5 pyinstaller
```

### 新增依赖说明：
- **PyQt5**：用于图形用户界面（GUI）
- **PyInstaller**：用于将程序打包为可执行文件

对于中文字体支持，不同系统需要额外配置：
- Windows：确保系统已安装微软雅黑（Microsoft YaHei）或黑体（SimHei）字体
- macOS：系统自带PingFang和STHeiti字体，无需额外安装
- Linux：建议安装文泉驿字体 `sudo apt-get install fonts-wqy-microhei`

## 配置修改
在使用前需要修改以下配置：
1. 打开 `main_gui.py` 文件
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

## 新增功能
1. **图形用户界面（GUI）**：
   - 提供更友好的用户交互界面
   - 支持文件选择和参数配置

2. **打包支持**：
   - 使用PyInstaller将程序打包为可执行文件
   - 支持Windows、macOS和Linux平台

3. **自定义输出**：
   - 支持指定输出目录
   - 自动创建输出目录（默认：`output`）

4. **程序图标**：
   - 支持自定义程序图标
   - 图标文件位于 `resources/logo.ico`

## 使用说明
### 开发环境运行
1. 准备两个输入文件：
   - `categories.md`：定义消费分类标准
   - `记账内容.md`：包含原始消费记录
2. 运行程序：
```bash
python src/main_gui.py
```

### 打包程序
1. 确保已安装PyInstaller
2. 运行打包命令：
```bash
pyinstaller main_gui.spec
```
3. 打包后的程序位于 `dist/main_gui/` 目录

### 运行打包后的程序
1. 进入 `dist/main_gui/` 目录
2. 运行 `main_gui.exe`（Windows）或 `main_gui`（macOS/Linux）
3. 程序将生成：
   - `config.txt`：处理后的格式化数据
   - `月度消费统计.png`：消费分类饼图
   - `月度5笔最高消费.png`：大额消费柱状图

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

6. **GUI扩展**：
   - 添加更多配置选项
   - 支持主题切换
   - 添加帮助文档和示例

## 注意事项
1. 确保 `resources/logo.ico` 文件存在
2. 打包前请测试所有功能
3. 如果使用自定义AI服务，请确保API地址和密钥正确