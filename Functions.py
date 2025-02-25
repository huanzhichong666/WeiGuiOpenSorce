import os
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime

folderAddr = "D:\Projects\PythonProject\date"  # 数据存储根目录
orderName = "1111"  # 当前订单号
product_id = 1  # 当前产品编号


header_data = [
    ["", "", "检验参数", "", "", ""],
    ["订单编号", "", "跑合次数", "", "测量次数", ""],
    ["滑块型号", "", "预压等级", "", "合格预压范围", ""],
    ["", "", "检测数据", "", "", ""],
    ["编号", "平均预压(N)", "测量预压最大值(N)", "测量预压最小值(N)", "客制/标准", "合格/不合格"],
]


class functions:
    @staticmethod
    # 定义一个函数来读取文件并返回数据
    def read_data(filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                # 将读取的每一行数据分割成数字，并转换为整数
                data = [int(num) for num in lines[0].split()]
                return data
        except FileNotFoundError:
            print(f"文件 {filename} 未找到。")
            return None
    @staticmethod
    #定义一个函数来写入数据
    def write_data(filename, data):
        with open(filename, 'w') as file:
            file.write(' '.join(map(str, data)))

    @staticmethod
    #读产品编号
    def read_product_id( file_path):
        """
        读取 data.txt 文件中的产品编号
        :param file_path: data.txt 文件路径
        :return: 产品编号（整数）
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if len(lines) > 1:  # 确保有数据行
                    last_line = lines[-1].strip()  # 获取最后一行
                    parts = last_line.split(",")
                    if len(parts) >= 3:  # 确保有产品编号字段
                        return int(parts[2])  # 返回产品编号
        except Exception as e:
            print(f"读取产品编号失败：{str(e)}")
        return 1  # 默认返回 1
    #读产品编号
    @staticmethod
    def update_product_id(file_path, new_product_id):
        """
        修改 data.txt 文件中的产品编号
        :param file_path: data.txt 文件路径
        :param new_product_id: 新的产品编号
        """
        try:
            with open(file_path, "r+", encoding="utf-8") as f:
                lines = f.readlines()
                if len(lines) > 1:  # 确保有数据行
                    last_line = lines[-1].strip()  # 获取最后一行
                    parts = last_line.split(",")
                    if len(parts) >= 3:  # 确保有产品编号字段
                        parts[2] = str(new_product_id)  # 更新产品编号
                        lines[-1] = ",".join(parts) + "\n"  # 替换最后一行
                        f.seek(0)  # 回到文件开头
                        f.writelines(lines)  # 写回文件
                        f.truncate()  # 截断多余内容
                        print(f"产品编号已更新为：{new_product_id}")
                        return
        except Exception as e:
            print(f"更新产品编号失败：{str(e)}")

    @staticmethod
    def saveDateToPdf(new_data_list, addr, sdCardAddr,header_data):
        """
        保存数据到 PDF 文件。
        :param new_data_list: 新数据列表，格式为二维列表，例如 [[row1], [row2]]
        :param addr: 订单号
        :param sdCardAddr: 数据存储根目录
        """
        # 设置字体
        song = "simfang"
        pdfmetrics.registerFont(TTFont(song, "D:\Projects\PythonProject\TheLatetesedVersion\STZHONGS.TTF"))

        # 定义页面尺寸
        PAGE_HEIGHT = A4[1]
        PAGE_WIDTH = A4[0]

        # PDF 文件路径
        pdf_folder = os.path.join(sdCardAddr, addr, "pdfVersion")
        os.makedirs(pdf_folder, exist_ok=True)  # 确保文件夹存在
        pdf_file = os.path.join(pdf_folder, f"{addr}.pdf")

        # 读取现有数据（如果 PDF 文件已存在）
        existing_data = []
        if os.path.exists(pdf_file):
            # 假设我们有一个函数可以从 PDF 中提取数据（这里简化处理）
            pass

        # 合并表头、现有数据和新数据
        full_data = header_data + existing_data
        for new_data in new_data_list:  # 遍历新数据列表，逐行添加
            full_data.append(new_data)

        # 创建表格
        colWidths = [100, 100, 100, 100, 100, 100]  # 列宽
        table = Table(full_data, colWidths=colWidths)

        # 设置表格样式
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # 表头背景颜色
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # 字体颜色
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ("FONT", (0, 0), (-1, -1), song, 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('SPAN', (0, 0), (1, 0)),  # 表格合并单元格
            ('SPAN', (1, 0), (2, 0)),
            ('SPAN', (2, 0), (3, 0)),
            ('SPAN', (3, 0), (4, 0)),
            ('SPAN', (4, 0), (5, 0)),
            ('SPAN', (0, 3), (1, 3)),
            ('SPAN', (1, 3), (2, 3)),
            ('SPAN', (2, 3), (3, 3)),
            ('SPAN', (3, 3), (4, 3)),
            ('SPAN', (4, 3), (5, 3)),
        ])
        table.setStyle(style)

        # 创建 PDF 文档
        doc = SimpleDocTemplate(pdf_file, pagesize=letter)

        # 添加表格到文档
        elements = [table]

        def DrawPageInfo(c, date=datetime.date.today()):
            """绘制页脚"""
            c.setStrokeColor(colors.dimgrey)
            c.line(30, PAGE_HEIGHT - 790, 570, PAGE_HEIGHT - 790)
            c.setFont(song, 8)
            c.setFillColor(colors.black)
            c.drawString(30, PAGE_HEIGHT - 810, f"生成日期：{date.isoformat()}")

        def myFirstPage(c, doc):
            """第一页的布局"""
            c.saveState()
            c.setFillColor(colors.green)
            c.setFont(song, 30)
            img = Image("D:\Projects\PythonProject\TheLatetesedVersion\logo.png")
            img.drawWidth = 82
            img.drawHeight = 54
            img.drawOn(c, 40, A4[1] - 120)
            c.drawCentredString(300, PAGE_HEIGHT - 100, "预压检测报告")
            DrawPageInfo(c)
            c.restoreState()

        def myLaterPages(c, doc):
            """后续页的布局"""
            c.saveState()
            DrawPageInfo(c)
            c.restoreState()

        # 构建 PDF
        doc.build(elements, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

    @staticmethod
    def read_data_from_txt(file_path):
        """
        从指定的 txt 文件中读取数据。
        :param file_path: 文件路径
        :return: 数据的二维列表
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            # 将每行数据分割为列表
            data = [line.strip().split(",") for line in lines if line.strip()]
            return data
        except Exception as e:
            print(f"读取数据失败：{str(e)}")
            return []

    @staticmethod
    def update_data_in_txt(file_path, new_data_list, append=True):
        """
        向指定的 txt 文件中追加或覆盖数据。
        :param file_path: 文件路径
        :param new_data_list: 要写入的数据（二维列表）
        :param append: 是否追加数据（True 表示追加，False 表示覆盖）
        """
        try:
            mode = "a" if append else "w"
            with open(file_path, mode, encoding="utf-8") as f:
                for row in new_data_list:
                    f.write(",".join(row) + "\n")
            print("数据已成功写入文件！")
        except Exception as e:
            print(f"写入数据失败：{str(e)}")