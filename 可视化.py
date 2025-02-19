import os
import platform

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def get_system_font():
    """
    根据操作系统返回合适的字体设置
    """
    system = platform.system()
    
    if system == 'Windows':
        # Windows 常用中文字体
        font_list = ['Microsoft YaHei', 'SimHei', 'SimSun']
        for font in font_list:
            try:
                FontProperties(fname=font)
                return font
            except:
                continue
    elif system == 'Darwin':  # macOS
        # macOS 常用中文字体
        font_paths = [
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/STHeiti Light.ttc',
            '/System/Library/Fonts/STHeiti Medium.ttc'
        ]
        for path in font_paths:
            if os.path.exists(path):
                return path
    
    # 如果没有找到合适的字体，返回默认值
    return 'sans-serif'

def setup_matplotlib_fonts():
    """
    设置matplotlib的字体和负号显示
    """
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

def parse_config_file(file_path):
    expenses = {
        '食物': [],
        '饮料': [],
        '交通': [],
        '电费和燃气费': [],
        '用车费用': [],
        '日常': [],
        '消费': [],
        '娱乐': [],
        '超前消费': []
    }
    
    large_expenses = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    is_reading = False
    for line in lines:
        line = line.strip()
        if line == '# start':
            is_reading = True
            continue
        elif line == '# end':
            break
        
        if is_reading and line:
            # 解析每一行记录
            parts = line.split(' ')
            date = parts[0].split(':')[1]
            type_name = parts[1].split(':')[1]
            name = parts[2].split(':')[1]
            cost = float(parts[3].split(':')[1])
            
            # 存储详细信息
            expense_detail = {
                'date': date,
                'name': name,
                'amount': cost,
                'description': ' '.join(parts[4:]) if len(parts) > 4 else '无描述'
            }
            
            # 添加到对应类别
            if type_name in expenses:
                expenses[type_name].append(expense_detail)
            
            # 如果金额大于等于30，添加到large_expenses
            if cost >= 30:
                large_expenses.append({
                    "date": date.replace('-', '月') + '日',
                    "name": name,
                    "amount": cost,
                    "description": expense_detail['description']
                })
    
    return expenses, large_expenses

def create_visualizations(expenses, large_expenses):
    # 设置字体
    setup_matplotlib_fonts()
    font = get_system_font()
    
    # 打印分类详情
    print("\n=== 详细分类消费记录 ===")
    for category, records in expenses.items():
        if records:  # 只打印有内容的分类
            print(f"\n分类: {category}")
            print(f"总金额: {sum(r['amount'] for r in records):.2f}元")
            print(f"交易次数: {len(records)}")
            print("具体消费记录:")
            for record in records:
                print(f"  - 日期: {record['date']}")
                print(f"    项目: {record['name']}")
                print(f"    金额: {record['amount']:.2f}元")
                print(f"    描述: {record['description']}")
                print("    -------------------")
    print("\n=== 分类详情结束 ===")
    
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
        # 获取需要合并的类别的总额
        other_total = sum(amount for amount, is_small in zip(expenses_totals, other_mask) if is_small)
        
        # 创建新的数据列表
        new_categories = [cat for cat, is_small in zip(categories, other_mask) if not is_small] + ['其他']
        new_expenses = [amount for amount, is_small in zip(expenses_totals, other_mask) if not is_small] + [other_total]
    else:
        new_categories = categories
        new_expenses = expenses_totals

    # 绘制饼图
    plt.figure(figsize=(10, 8))
    
    # 设置饼图的起始角度
    start_angle = 90
    
    # 绘制饼图
    plt.pie(
        new_expenses,
        labels=new_categories,
        autopct=lambda pct: f'{pct:.1f}%\n({pct/100.*total_expense:.2f}元)',
        startangle=start_angle
    )

    plt.title('月度消费统计', fontsize=16, pad=20)
    
    # 添加总计金额的文本
    plt.text(-1.5, -1.2, f"总计: {total_expense:.2f}元", fontsize=12)

    # 保存饼图
    output_pie = '月度消费统计.png'
    plt.savefig(output_pie, dpi=300, bbox_inches='tight')
    plt.close()

    # 绘制最大5笔消费柱状图
    consumptions = sorted(large_expenses, key=lambda x: x['amount'], reverse=True)[:5]
    labels = [f"{item['date']}\n{item['name']}" for item in consumptions]  # 将标签分成两行
    values = [item['amount'] for item in consumptions]
    bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    plt.figure(figsize=(12, 6))  # 加宽图形
    
    # 创建柱状图
    bars = plt.bar(range(len(values)), values, color=bar_colors)

    # 设置坐标轴
    plt.xticks(range(len(labels)), labels, rotation=0)  # 移除旋转
    
    # 根据操作系统创建字体属性
    if platform.system() == 'Darwin' and font != 'sans-serif':  # macOS
        font_prop = FontProperties(fname=font, size=12)  # 减小字体大小
    else:  # Windows 或其他
        font_prop = FontProperties(family=font, size=12)

    plt.ylabel('金额 (元)', fontproperties=font_prop)
    plt.title('月度消费最高的前五笔内容', fontproperties=font_prop, pad=20)

    # 显示数值
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}元',
                ha='center', va='bottom')

    # 设置y轴的刻度间隔
    max_value = max(values)
    plt.ylim(0, max_value * 1.15)  # 给顶部数值留出15%的空间
    
    # 自动调整布局
    plt.tight_layout()

    # 保存柱状图
    output_bar = '月度5笔最高消费.png'
    plt.savefig(output_bar, format='png', bbox_inches='tight', dpi=300)
    plt.close()

    return output_pie, output_bar

def calculate_total_expenses(expenses):
    """计算总支出"""
    total = 0
    for category, records in expenses.items():
        total += sum(r['amount'] for r in records)
    return total

def main():
    # 解析配置文件
    expenses, large_expenses = parse_config_file('config.txt')
    
    # 打印总支出
    total = calculate_total_expenses(expenses)
    print(f"\n总支出: {total:.2f}元")
    
    # 创建可视化
    output_pie, output_bar = create_visualizations(expenses, large_expenses)
    print(f"\n饼图已保存为: '{output_pie}'")
    print(f"柱状图已保存为: '{output_bar}'")

if __name__ == "__main__":
    main()