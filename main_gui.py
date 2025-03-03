import os

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QTextEdit, QFileDialog, QComboBox)
from PyQt5.QtGui import QIcon  # 确保正确导入 QIcon

from ai分类 import AccountProcessor
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("SherlsApp", "AccountApp")  # 新增设置对象
        self.setWindowTitle("记账程序")
        self.setGeometry(100, 100, 800, 600)
        
        # 设置窗口图标
        icon_path = self.get_resource_path('resources/logo.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"警告：未找到图标文件 {icon_path}")
        
        # 主布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # API 设置
        api_layout = QHBoxLayout()
        api_layout.addWidget(QLabel("API Key:"))
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("请输入API Key")
        api_layout.addWidget(self.api_input)
        
        api_layout.addWidget(QLabel("Base URL:"))
        self.url_input = QLineEdit("https://api.deepseek.com/v1")
        api_layout.addWidget(self.url_input)
        
        # 模型选择
        api_layout.addWidget(QLabel("模型:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(["deepseek-chat", "deepseek-ai/DeepSeek-R1", "deepseek-ai/DeepSeek-V3"])
        api_layout.addWidget(self.model_combo)
        
        layout.addLayout(api_layout)
        
        # 文件选择
        file_layout = QHBoxLayout()
        self.categories_file = QLineEdit("分类标准.md")
        self.content_file = QLineEdit("记账内容.md")
        
        file_layout.addWidget(QLabel("分类文件:"))
        file_layout.addWidget(self.categories_file)
        file_layout.addWidget(QLabel("内容文件:"))
        file_layout.addWidget(self.content_file)
        
        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self.select_files)
        file_layout.addWidget(browse_btn)
        
        layout.addLayout(file_layout)
        
        # 运行按钮
        run_btn = QPushButton("运行分类")
        run_btn.clicked.connect(self.run_classification)
        layout.addWidget(run_btn)
        
        # 添加输出目录设置
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.output_dir = QLineEdit("output")
        output_layout.addWidget(self.output_dir)
        browse_output_btn = QPushButton("浏览...")
        browse_output_btn.clicked.connect(self.select_output_dir)
        output_layout.addWidget(browse_output_btn)
        layout.addLayout(output_layout)

        # 结果输出
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)
        
        # 加载上一次的settings
        self.load_settings()

    def load_settings(self):
        """加载保存的设置"""
        self.api_input.setText(self.settings.value("api_key", ""))
        self.url_input.setText(self.settings.value("base_url", "https://api.deepseek.com/v1"))
        self.model_combo.setCurrentText(self.settings.value("model", "deepseek-chat"))
        self.categories_file.setText(self.settings.value("categories_file", "分类标准.md"))
        self.content_file.setText(self.settings.value("content_file", "记账内容.md"))
        self.output_dir.setText(self.settings.value("output_dir", "output"))

    def save_settings(self):
        """保存当前设置"""
        self.settings.setValue("api_key", self.api_input.text())
        self.settings.setValue("base_url", self.url_input.text())
        self.settings.setValue("model", self.model_combo.currentText())
        self.settings.setValue("categories_file", self.categories_file.text())
        self.settings.setValue("content_file", self.content_file.text())
        self.settings.setValue("output_dir", self.output_dir.text())


    def closeEvent(self, event):
        """窗口关闭时保存设置"""
        self.save_settings()
        event.accept()

    def get_resource_path(self, relative_path):
        """获取资源文件的绝对路径"""
        try:
            # 打包后的路径
            base_path = sys._MEIPASS
        except Exception:
            # 开发环境的路径
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        # 构建完整路径
        full_path = os.path.join(base_path, relative_path)
        return full_path
    
    def select_files(self):
        """选择分类和内容文件"""
        categories_file, _ = QFileDialog.getOpenFileName(self, "选择分类文件", "", "Markdown Files (*.md)")
        if categories_file:
            self.categories_file.setText(categories_file)
            
        content_file, _ = QFileDialog.getOpenFileName(self, "选择内容文件", "", "Markdown Files (*.md)")
        if content_file:
            self.content_file.setText(content_file)
    
    def select_output_dir(self):
        """选择输出目录"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if dir_path:
            self.output_dir.setText(dir_path)

    def run_classification(self):
        """运行分类程序"""
        self.output_area.clear()
        
        # 获取输入
        api_key = self.api_input.text()
        base_url = self.url_input.text()
        model_name = self.model_combo.currentText()
        categories_file = self.categories_file.text()
        content_file = self.content_file.text()
        output_dir = self.output_dir.text()
        
        if not api_key:
            self.output_area.append("错误：请先输入API Key")
            return
            
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # 初始化处理器
        try:
            processor = AccountProcessor(api_key, base_url, model_name, self.output_area, output_dir)
            processor.run(categories_file, content_file)
                
        except Exception as e:
            self.output_area.append(f"发生错误：{str(e)}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()