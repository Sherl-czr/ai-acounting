import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import platform
import os

class ConsoleOutput:
    def __init__(self, output_widget):
        self.output_widget = output_widget
        
    def log(self, message):
        if self.output_widget is not None:
            self.output_widget.append(message)
        print(message)  # 同时输出到控制台

def get_system_font():
    """根据操作系统返回合适的字体设置"""
    system = platform.system()
    
    if system == 'Windows':
        font_list = ['Microsoft YaHei', 'SimHei', 'SimSun']
        for font in font_list:
            try:
                FontProperties(fname=font)
                return font
            except:
                continue
    elif system == 'Darwin':  # macOS
        font_paths = [
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/STHeiti Light.ttc',
            '/System/Library/Fonts/STHeiti Medium.ttc'
        ]
        for path in font_paths:
            if os.path.exists(path):
                return path
    
    return 'sans-serif'

def setup_matplotlib_fonts():
    """设置matplotlib的字体和负号显示"""
    font = get_system_font()
    
    if platform.system() == 'Windows':
        plt.rcParams['font.sans-serif'] = [font]
    else:  # macOS
        if font != 'sans-serif':
            plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
            try:
                FontProperties(fname=font)
            except:
                plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    
    plt.rcParams['axes.unicode_minus'] = False

def parse_config_file(file_path, console):
    # 初始化空字典
    expenses = {}
    large_expenses = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        console.log(f"读取配置文件失败: {str(e)}")
        return None, None
        
    is_reading = False
    for line in lines:
        line = line.strip()
        if line == '# start':
            is_reading = True
            continue
        elif line == '# end':
            break
        
        if is_reading and line:
            try:
                parts = line.split(' ')
                date = parts[0].split(':')[1]
                type_name = parts[1].split(':')[1]
                name = parts[2].split(':')[1]
                cost = float(parts[3].split(':')[1])
                
                # 动态添加分类
                if type_name not in expenses:
                    expenses[type_name] = []
                
                expense_detail = {
                    'date': date,
                    'name': name,
                    'amount': cost,
                    'description': ' '.join(parts[4:]) if len(parts) > 4 else '无描述'
                }
                
                expenses[type_name].append(expense_detail)
                
                if cost >= 30:
                    large_expenses.append({
                        "date": date.replace('-', '月') + '日',
                        "name": name,
                        "amount": cost,
                        "description": expense_detail['description']
                    })
            except Exception as e:
                console.log(f"解析行 '{line}' 失败: {str(e)}")
                continue
    
    return expenses, large_expenses

def create_visualizations(config_file, console, output_dir):
    """创建可视化图表"""
    try:
        # 设置字体
        setup_matplotlib_fonts()
        
        # 解析配置文件
        expenses, large_expenses = parse_config_file(config_file, console)
        if expenses is None:
            return
            
        # 打印分类详情
        console.log("\n=== 详细分类消费记录 ===")
        for category, records in expenses.items():
            if records:
                console.log(f"\n分类: {category}")
                console.log(f"总金额: {sum(r['amount'] for r in records):.2f}元")
                console.log(f"交易次数: {len(records)}")
                console.log("具体消费记录:")
                for record in records:
                    console.log(f"  - 日期: {record['date']}")
                    console.log(f"    项目: {record['name']}")
                    console.log(f"    金额: {record['amount']:.2f}元")
                    console.log(f"    描述: {record['description']}")
                    console.log("    -------------------")
        console.log("\n=== 分类详情结束 ===")
        
        # 计算每个类别的总金额和百分比
        categories = list(expenses.keys())
        expenses_totals = [sum(r['amount'] for r in records) for records in expenses.values()]
        total_expense = sum(expenses_totals)
        
        # 计算每个类别的百分比
        percentages = [(amount / total_expense) * 100 for amount in expenses_totals]
        
        # 设置阈值（比如3%）
        THRESHOLD = 3
        
        # 将小于阈值的类别合并为"其他"
        other_mask = [p < THRESHOLD for p in percentages]
        if any(other_mask):
            other_total = sum(amount for amount, is_small in zip(expenses_totals, other_mask) if is_small)
            new_categories = [cat for cat, is_small in zip(categories, other_mask) if not is_small] + ['其他']
            new_expenses = [amount for amount, is_small in zip(expenses_totals, other_mask) if not is_small] + [other_total]
        else:
            new_categories = categories
            new_expenses = expenses_totals

        # 绘制饼图
        plt.figure(figsize=(10, 8))
        start_angle = 90
        plt.pie(
            new_expenses,
            labels=new_categories,
            autopct=lambda pct: f'{pct:.1f}%\n({pct/100.*total_expense:.2f}元)',
            startangle=start_angle
        )
        plt.title('月度消费统计', fontsize=16, pad=20)
        plt.text(-1.5, -1.2, f"总计: {total_expense:.2f}元", fontsize=12)
        # 保存饼图
        output_pie = os.path.join(output_dir, '月度消费统计.png')
        plt.savefig(output_pie, dpi=300, bbox_inches='tight')
        plt.close()
        console.log(f"饼图已保存为: {output_pie}")

        # 绘制最大5笔消费柱状图
        consumptions = sorted(large_expenses, key=lambda x: x['amount'], reverse=True)[:5]
        labels = [f"{item['date']}\n{item['name']}" for item in consumptions]
        values = [item['amount'] for item in consumptions]
        bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(values)), values, color=bar_colors)
        plt.xticks(range(len(labels)), labels, rotation=0)
        plt.ylabel('金额 (元)')
        plt.title('月度消费最高的前五笔内容', pad=20)

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}元',
                    ha='center', va='bottom')

        max_value = max(values)
        plt.ylim(0, max_value * 1.15)
        plt.tight_layout()
        # 保存柱状图
        output_bar = os.path.join(output_dir, '月度5笔最高消费.png')
        plt.savefig(output_bar, format='png', bbox_inches='tight', dpi=300)
        plt.close()
        console.log(f"柱状图已保存为: {output_bar}")

    except Exception as e:
        console.log(f"可视化过程出错: {str(e)}")