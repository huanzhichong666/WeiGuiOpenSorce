import sys

from PyQt5.QtSensors import QSensor

from ParaMeters import *
from Functions import *
from PyQt5 import QtWidgets, uic
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
import os
import datetime
from PyQt5.QtWidgets import QMessageBox
import matplotlib.pyplot as plt
# from MachineAction import *
from matplotlib.font_manager import FontProperties
# 设置支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体（SimHei）
plt.rcParams['axes.unicode_minus'] = False    # 解决负号 '-' 显示为方块的问题
# 设置支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体（SimHei）
plt.rcParams['axes.unicode_minus'] = False    # 解决负号 '-' 显示为方块的问题

# 设置支持中文的字体
# label.setFont(QFont("SimSun"))
#region 根地址
#####参数赋值Start########
filenameAccountConfig="D:\Projects\PythonProject\TheLatetesedVersion\AccountInfos.txt"#预设的账号密码信息
filenameDates="D:\Projects\PythonProject\TheLatetesedVersion\Dates.txt"#预设的运动参数
folderAddr="D:\Projects\PythonProject\date"#数据存储的文件夹目录
folder_path2="D:\Projects\PythonProject\date2"
AccountInfos=AccountParas()#用来存储用户的账号信息
DatesPreInos=usrDefineParas()#用来存储一些提前预设的数据
#####参数赋值End########
#endregion
#region 全局变量
########全局变量start###########
product_id=0
orderName=0
# 全局变量，用于存储从 FrmParameterSet 传递的数据
global_slider_type = ""
global_slider_series = ""
global_preload_size = ""
########全局变量end#############
#endregion
#region 参数初始化
#####Init参数Start########
dataAccount = functions.read_data(filenameAccountConfig)
if dataAccount is not None and len(dataAccount) == 6:
    AccountInfos.usrAccount,AccountInfos.usrPwd,AccountInfos.adAccount,AccountInfos.adPwd,AccountInfos.anyAccount,AccountInfos.anyPwd=dataAccount
dataAccount=functions.read_data(filenameDates)
if dataAccount is not None and len(dataAccount) == 4:
    DatesPreInos.runtimesPre,AccountInfos.checkTimesPre,AccountInfos.runSpeedPre,AccountInfos.anglePre=dataAccount
#####Init参数End########
#endregion
# region 硬件初始化
###########硬件初始化start####################
#     #led灯初始化
# Leds.enable_Led(22,0)#红灯灭
# Leds.enable_Led(23,1)#绿灯亮
#     #传感器初始化
# Sensors.sensor_servor_clean()
# Sensors.sensor_pressure_clean()
# Sensors.sensor_distance_clean()
#     #直线电机初始化
# LinerMotor.enable_motor(16,0)#电机解使能
###########硬件初始化end######################
#endregion
#登录界面
class FrmLog(QtWidgets.QMainWindow):  ##用户登录界面设计，一般里面设计控件的事件函数，事件连接在__init__函数里面
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('Frm_log.ui', self)
        self.ui.lblAcountWarn.hide()#账号不能为空
        self.ui.lblPwdWarn.hide()#密码不能为空
        self.ui.lblError.hide()#账号密码错误提示
        self.ui.LogButton.clicked.connect(self.check_acount)  ##事件 --登录
        self.center_on_screen()
    #屏幕居中
    def center_on_screen(self):
        """将窗口居中显示"""
        # 获取屏幕的几何信息
        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # 计算窗口左上角的坐标5
        window_width = self.ui.width()
        window_height = self.ui.height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # 设置窗口位置
        self.ui.move(x, y)
        # 创建网格布局用于显示参数
    #登录事件
    def check_acount(self):
        # 获取用户输入的账号和密码
        input_account = self.ui.LineCount.text()
        input_password = self.ui.LinePassword.text()

        # 检查账号和密码是否为空
        if not input_account:
            self.ui.lblAcountWarn.show()  # 显示“账号不能为空”提示
            return
        else:
            self.ui.lblAcountWarn.hide()  # 隐藏“账号不能为空”提示

        if not input_password:
            self.ui.lblPwdWarn.show()  # 显示“密码不能为空”提示
            return
        else:
            self.ui.lblPwdWarn.hide()  # 隐藏“密码不能为空”提示

        # 验证用户输入的账号和密码
        if input_account == str(AccountInfos.usrAccount) and input_password == str(AccountInfos.usrPwd):
            # 普通用户登录成功
            self.frmInputDingdan = FrmInputDingdan()
            self.frmInputDingdan.show()
            self.ui.close()
        elif input_account == str(AccountInfos.adAccount) and input_password == str(AccountInfos.adPwd):
            # 管理员登录成功
            self.frmAdmin = FrmAdministrator()  # 加载管理员界面
            self.frmAdmin.show()
            self.ui.close()
        elif input_account == str(AccountInfos.anyAccount) and input_password == str(AccountInfos.anyPwd):
            # 其他账户登录成功
            self.frmInputDingdan = FrmInputDingdan()
            self.frmInputDingdan.ui.show()
            self.ui.close()
        else:
            # 账号或密码错误
            self.ui.lblError.show()  # 显示“账号密码错误提示”
            self.ui.LinePassword.clear()  # 清空密码输入框
#订单查询界面
class FrmOrderQuery(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("订单查询界面")
        self.setGeometry(100, 100, 800, 500)  # 设置窗口大小为 800x500
        self.setFixedSize(800, 500)  # 固定窗口大小

        # 创建主布局
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)  # 设置边距
        main_layout.setSpacing(15)  # 设置控件之间的间距

        # 上半部分：订单查询结果表格
        self.create_order_table(main_layout)

        # 下半部分：查询条件和按钮
        self.create_query_panel(main_layout)
        #居中显示界面
        self.center_on_screen()
    #界面居中显示
    def center_on_screen(self):
        """将窗口居中显示"""
        # 获取屏幕的几何信息
        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # 计算窗口左上角的坐标
        window_width = self.width()
        window_height = self.height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # 设置窗口位置
        self.move(x, y)
        # 创建网格布局用于显示参数
    def create_order_table(self, layout):
        """创建订单查询结果表格"""
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)  # 设置列数
        self.table.setHorizontalHeaderLabels(["订单编号", "订单日期","物料信息", "订单状态", "备注"])
        self.table.setRowCount(0)  # 初始行数为 0
        self.table.horizontalHeader().setStretchLastSection(True)  # 最后一列自动拉伸
        self.table.setAlternatingRowColors(True)  # 隔行变色
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #ccc;
                background-color: #f9f9f9;
            }
            QHeaderView::section {
                background-color: #eaeaea;
                padding: 4px;
                border: 1px solid #ccc;
            }
        """)  # 设置表格样式

        layout.addWidget(self.table)

    def create_query_panel(self, layout):
        """创建查询条件和按钮区域"""
        query_layout = QtWidgets.QGridLayout()
        query_layout.setSpacing(10)  # 设置控件之间的间距

        # 查询条件标签和输入框
        labels = ["订单编号："]
        self.inputs = {}  # 存储输入框的字典

        font = QtGui.QFont("Arial", 10)  # 设置字体

        for i, label_text in enumerate(labels):
            label = QtWidgets.QLabel(label_text)
            label.setFont(font)
            label.setStyleSheet("color: #333;")  # 设置文字颜色

            line_edit = QtWidgets.QLineEdit()
            line_edit.setFont(font)
            line_edit.setStyleSheet("""
                QLineEdit {
                    background-color: #f9f9f9;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 5px;
                }
            """)  # 设置样式

            query_layout.addWidget(label, 0, i * 2)       # 标签放在偶数列
            query_layout.addWidget(line_edit, 0, i * 2 + 1)  # 输入框放在奇数列
            self.inputs[label_text] = line_edit

        # 按钮区域
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)  # 设置按钮之间的间距

        # 定义按钮名称
        button_names = ["查询", "重置", "返回"]

        # 创建按钮并添加到布局中
        self.buttons = {}  # 存储按钮的字典

        for name in button_names:
            button = QtWidgets.QPushButton(name)
            button.setFont(font)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
            """)  # 设置按钮样式

            # 绑定按钮事件
            if name == "查询":
                button.clicked.connect(self.on_query)
            elif name == "重置":
                button.clicked.connect(self.on_reset)
            elif name == "返回":
                button.clicked.connect(self.on_back)

            button_layout.addWidget(button)
            self.buttons[name] = button

        # 将按钮布局添加到查询条件布局
        query_layout.addLayout(button_layout, 1, 0, 1, len(labels) * 2)

        # 将查询条件布局添加到主布局
        layout.addLayout(query_layout)

    # 按钮事件处理函数
    def on_query(self):
        """查询按钮事件"""
        order_id = self.inputs["订单编号："].text()

        # 模拟查询结果（实际应从数据库或文件中获取）
        data = []
        if order_id:
            data.append(["ORD12345", "2023-10-01", "已完成", "无"])
            data.append(["ORD67890", "2023-10-02", "进行中", "需要确认"])

        # 更新表格数据
        self.update_table(data)

    def on_reset(self):
        """重置按钮事件"""
        for input_box in self.inputs.values():
            input_box.clear()

    def on_back(self):
        """返回按钮事件"""
        # self.frmlog = FrmLog()
        # self.frmlog.ui.show()
        # self.close()

    def update_table(self, data):
        """更新表格数据"""
        self.table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, cell_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(cell_data)
                item.setTextAlignment(QtCore.Qt.AlignCenter)  # 居中对齐
                self.table.setItem(row, col, item)
# 管理员界面
class FrmAdministrator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("管理员界面")
        self.setGeometry(100, 100, 800, 500)  # 设置窗口大小为 800x500
        self.setFixedSize(800, 500)  # 固定窗口大小
        self.center_on_screen()

        # 设置全局样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #f3f4f6, stop:1 #e5e7eb
                ); /* 浅灰色渐变背景 */
            }
            QGroupBox {
                background-color: #ffffff; /* 白色背景 */
                border: 1px solid #ccc; /* 灰色边框 */
                border-radius: 8px; /* 圆角 */
                padding: 10px; /* 内边距 */
            }
            QLabel {
                color: #333333; /* 深灰色文字 */
                font-size: 13px;
            }
            QLineEdit, QDoubleSpinBox, QComboBox {
                background-color: #ffffff; /* 白色背景 */
                border: 1px solid #ccc; /* 灰色边框 */
                border-radius: 4px;
                padding: 5px;
                color: #333333; /* 深灰色文字 */
                font-size: 13px;
            }
            QPushButton {
                background-color: #007BFF; /* 蓝色按钮 */
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #0056b3; /* 鼠标悬停时变深 */
            }
        """)

        # 创建主布局
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)  # 设置边距
        main_layout.setSpacing(15)  # 设置控件之间的间距

        # 添加运动参数修改区域
        self.create_motion_parameters(main_layout)

        # 添加账户信息修改区域
        self.create_account_management(main_layout)

        # 添加退出按钮
        self.create_exit_button(main_layout)

    def center_on_screen(self):
        """将窗口居中显示"""
        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        window_width = self.width()
        window_height = self.height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.move(x, y)

    def create_motion_parameters(self, layout):
        """创建运动参数修改区域"""
        group_box = QtWidgets.QGroupBox("运动参数修改")
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSpacing(10)  # 设置控件之间的间距

        # 参数数据
        labels = [
            "跑和次数：", "测量次数：", "速度：", "舵机角度修正："
        ]
        units = ["次", "次", "mm/s", ""]
        min_values = [1.0, 1.0, 50.0, -100.0]
        max_values = [15.0, 6.0, 400.0, 100.0]
        step_values = [1.0, 1.0, 50.0, 1.0]
        init_values=[DatesPreInos.runtimesPre,AccountInfos.checkTimesPre,AccountInfos.runSpeedPre,AccountInfos.anglePre]

        self.spin_boxes = []  # 存储所有 QDoubleSpinBox 控件
        self.data = []  # 存储 spinbox 的值

        for i, (label_text, unit, min_val, max_val, step_val,init_val) in enumerate(zip(labels, units, min_values, max_values, step_values,init_values)):
            row = i
            label = QtWidgets.QLabel(label_text)
            label.setFont(QtGui.QFont("Arial", 13))
            spin_box = QtWidgets.QDoubleSpinBox()
            spin_box.setFont(QtGui.QFont("Arial", 13))
            spin_box.setDecimals(0 if unit != "" else 1)
            spin_box.setMinimum(min_val)
            spin_box.setMaximum(max_val)
            spin_box.setSingleStep(step_val)
            spin_box.setValue(init_val)
            self.spin_boxes.append(spin_box)
            # 将初始值存储到 data 数组中
            self.data.append(init_val)
            grid_layout.addWidget(label, row, 0)
            grid_layout.addWidget(spin_box, row, 1)

            if unit:
                unit_label = QtWidgets.QLabel(unit)
                unit_label.setFont(QtGui.QFont("Arial", 13))
                grid_layout.addWidget(unit_label, row, 2)

        # 添加确定按钮
        btn_revise = QtWidgets.QPushButton("确定")
        btn_revise.setFont(QtGui.QFont("Arial", 13))
        grid_layout.addWidget(btn_revise, len(labels), 1)
        group_box.setLayout(grid_layout)
        layout.addWidget(group_box)
        btn_revise.clicked.connect(self.btnReviseDate)
    def btnReviseDate(self):
        try:
            # 获取当前 spinbox 的值并存储到 self.data
            self.data = [int(spin_box.value()) for spin_box in self.spin_boxes]
            print("当前的运动参数已保存到 data 数组:", self.data)
            # 将数据写入文件
            functions.write_data(filenameDates, self.data)

            # 显示成功提示框
            msg_box = QMessageBox()
            msg_box.setWindowTitle("提示")
            msg_box.setText("运动参数修改成功")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f9f9f9;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                }
                QLabel {
                    color: #333333;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
            """)
            msg_box.exec_()
        except Exception as e:
            # 显示错误提示框
            error_box = QMessageBox()
            error_box.setWindowTitle("错误")
            error_box.setText(f"运动参数修改失败：{str(e)}")
            error_box.setIcon(QMessageBox.Critical)
            error_box.setStandardButtons(QMessageBox.Ok)
            error_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f9f9f9;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                }
                QLabel {
                    color: #333333;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #a71d2a;
                }
            """)
            error_box.exec_()
    def create_account_management(self, layout):
        """创建账户信息修改区域"""
        group_box = QtWidgets.QGroupBox("账户信息修改")
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSpacing(10)  # 设置控件之间的间距

        # 参数数据
        labels = [
            "原用户名：", "新用户名：", "原密码：", "新密码：", "用户权限："
        ]

        self.line_edits = []  # 存储所有 QLineEdit 控件
        self.combo_box = None  # 存储 QComboBox 控件

        for i, label_text in enumerate(labels):
            row = i
            label = QtWidgets.QLabel(label_text)
            label.setFont(QtGui.QFont("Arial", 13))

            if label_text == "用户权限：":
                combo_box = QtWidgets.QComboBox()
                combo_box.addItems(["管理员", "用户"])
                combo_box.setFont(QtGui.QFont("Arial", 13))
                self.combo_box = combo_box
                grid_layout.addWidget(label, row, 0)
                grid_layout.addWidget(combo_box, row, 1)
            else:
                line_edit = QtWidgets.QLineEdit()
                line_edit.setFont(QtGui.QFont("Arial", 13))
                if "密码" in label_text:
                    line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
                self.line_edits.append(line_edit)
                grid_layout.addWidget(label, row, 0)
                grid_layout.addWidget(line_edit, row, 1)

        # 添加确定按钮
        btn_check = QtWidgets.QPushButton("确定")
        btn_check.setFont(QtGui.QFont("Arial", 13))
        btn_check.clicked.connect(self.btnAccountRevise)
        grid_layout.addWidget(btn_check, len(labels), 1)

        group_box.setLayout(grid_layout)
        layout.addWidget(group_box)

    def btnAccountRevise(self):
        try:
            # 获取用户输入的值
            original_username = self.line_edits[0].text().strip()  # 原用户名
            new_username = self.line_edits[1].text().strip() or original_username  # 新用户名（如果为空则保持不变）
            original_password = self.line_edits[2].text().strip()  # 原密码
            new_password = self.line_edits[3].text().strip() or original_password  # 新密码（如果为空则保持不变）
            user_role = self.combo_box.currentText()  # 用户权限
            # 根据用户权限更新管理员或其他账户信息
            if user_role == "管理员":
                if(original_username == str(AccountInfos.adAccount) and original_password == str(AccountInfos.adPwd)):
                    AccountInfos.adAccount = new_username
                    AccountInfos.adPwd = new_password
                else:
                    error_box = QMessageBox()
                    error_box.setWindowTitle("错误")
                    error_box.setText("原用户名或原密码错误，请重新输入！")
                    error_box.setIcon(QMessageBox.Critical)
                    error_box.setStandardButtons(QMessageBox.Ok)
                    error_box.setStyleSheet("""
                                        QMessageBox {
                                            background-color: #f9f9f9;
                                            border: 1px solid #ccc;
                                            border-radius: 8px;
                                        }
                                        QLabel {
                                            color: #333333;
                                            font-size: 14px;
                                        }
                                        QPushButton {
                                            background-color: #dc3545;
                                            color: white;
                                            border: none;
                                            border-radius: 4px;
                                            padding: 8px 16px;
                                        }
                                        QPushButton:hover {
                                            background-color: #a71d2a;
                                        }
                                    """)
                    error_box.exec_()
                    return
            elif user_role == "用户":
                if (original_username == str(AccountInfos.usrAccount) and original_password == str(AccountInfos.usrPwd)):
                    AccountInfos.usrAccount = new_username
                    AccountInfos.usrPwd = new_password
                else:
                    error_box = QMessageBox()
                    error_box.setWindowTitle("错误")
                    error_box.setText("原用户名或原密码错误，请重新输入！")
                    error_box.setIcon(QMessageBox.Critical)
                    error_box.setStandardButtons(QMessageBox.Ok)
                    error_box.setStyleSheet("""
                                        QMessageBox {
                                            background-color: #f9f9f9;
                                            border: 1px solid #ccc;
                                            border-radius: 8px;
                                        }
                                        QLabel {
                                            color: #333333;
                                            font-size: 14px;
                                        }
                                        QPushButton {
                                            background-color: #dc3545;
                                            color: white;
                                            border: none;
                                            border-radius: 4px;
                                            padding: 8px 16px;
                                        }
                                        QPushButton:hover {
                                            background-color: #a71d2a;
                                        }
                                    """)
                    error_box.exec_()
                    return

            # 将更新后的账户信息保存到文件
            account_data = [
                AccountInfos.usrAccount,
                AccountInfos.usrPwd,
                AccountInfos.adAccount,
                AccountInfos.adPwd,
                AccountInfos.anyAccount,
                AccountInfos.anyPwd
            ]
            functions.write_data(filenameAccountConfig, account_data)

            # 显示成功提示框
            msg_box = QMessageBox()
            msg_box.setWindowTitle("提示")
            msg_box.setText("账户信息修改成功")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f9f9f9;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                }
                QLabel {
                    color: #333333;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
            """)
            msg_box.exec_()

        except Exception as e:
            # 显示错误提示框
            error_box = QMessageBox()
            error_box.setWindowTitle("错误")
            error_box.setText(f"账户信息修改失败：{str(e)}")
            error_box.setIcon(QMessageBox.Critical)
            error_box.setStandardButtons(QMessageBox.Ok)
            error_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f9f9f9;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                }
                QLabel {
                    color: #333333;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #a71d2a;
                }
            """)
            error_box.exec_()

    def create_exit_button(self, layout):
        """创建退出按钮"""
        btn_quick = QtWidgets.QPushButton("退出")
        btn_quick.setFont(QtGui.QFont("Arial", 13))
        btn_quick.clicked.connect(self.btnBackToLog)
        layout.addWidget(btn_quick)

    # 返回登录界面
    def btnBackToLog(self):
        print("退出按钮被点击")
        self.frmlog = FrmLog()
        self.frmlog.show()
        self.close()
#订单输入界面
class FrmInputDingdan(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 默认电机状态为解使能
        self.motor_enabled = False  # 电机是否使能的状态标志

        # 绑定事件
        self.button.clicked.connect(self.on_order_confirm)  # 订单确认按钮事件
        self.btn_back_to_log.clicked.connect(self.on_exit_login)  # 退出登录按钮事件
        self.btn_enable.clicked.connect(self.on_motor_enable)  # 电机使能按钮事件
        self.btn_disable.clicked.connect(self.on_motor_disable)  # 电机解使能按钮事件

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(811, 480)
        Form.setFixedSize(811, 480)  # 固定窗口大小
        self.center_on_screen(Form)

        # 设置全局样式
        Form.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #f3f4f6, stop:1 #e5e7eb
                ); /* 浅灰色渐变背景 */
            }
            QGroupBox {
                background-color: #ffffff; /* 白色背景 */
                border: 1px solid #ccc; /* 灰色边框 */
                border-radius: 8px; /* 圆角 */
                padding: 10px; /* 内边距 */
            }
            QLabel {
                color: #333333; /* 深灰色文字 */
                font-size: 12px;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #ffffff; /* 白色背景 */
                border: 1px solid #ccc; /* 灰色边框 */
                border-radius: 4px;
                padding: 5px;
                color: #333333; /* 深灰色文字 */
            }
            QPushButton {
                background-color: #007BFF; /* 蓝色按钮 */
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #0056b3; /* 鼠标悬停时变深 */
            }
        """)

        # 主布局
        main_layout = QtWidgets.QVBoxLayout(Form)
        main_layout.setContentsMargins(20, 20, 20, 20)  # 设置边距
        main_layout.setSpacing(15)  # 设置控件之间的间距

        # 订单信息区域
        self.create_order_input(main_layout)

        # 功能按键区域
        self.create_function_buttons(main_layout)

        # 检测模式选择区域
        self.create_detection_mode(main_layout)

        # 自定义预压上下限区域
        self.create_pressure_limits(main_layout)

        # 操作按钮区域
        self.create_button_panel(main_layout)

        # 默认设置
        self.rb_standard.setChecked(True)  # 默认选中“标准模式”
        self.pressure_group_box.setVisible(False)  # 默认隐藏“自定义预压上下限”

        # 绑定事件
        self.rb_standard.toggled.connect(self.on_mode_changed)
        self.rb_customer.toggled.connect(self.on_mode_changed)

    def center_on_screen(self, Form):
        """将窗口居中显示"""
        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        window_width = Form.width()
        window_height = Form.height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        Form.move(x, y)

    def create_order_input(self, layout):
        """创建订单信息区域"""
        group_box = QtWidgets.QGroupBox("订单信息")
        hbox_layout = QtWidgets.QHBoxLayout()
        hbox_layout.setSpacing(10)  # 设置控件之间的间距

        label = QtWidgets.QLabel("请输入订单号：")
        label.setFont(QtGui.QFont("Arial", 12))
        text_edit = QtWidgets.QTextEdit()
        text_edit.setPlaceholderText("请输入订单号……")
        text_edit.setMaximumHeight(40)  # 限制高度
        text_edit.setFont(QtGui.QFont("Arial", 12))

        button = QtWidgets.QPushButton("确定")
        button.setFont(QtGui.QFont("Arial", 12))

        hbox_layout.addWidget(label)
        hbox_layout.addWidget(text_edit)
        hbox_layout.addWidget(button)

        group_box.setLayout(hbox_layout)
        layout.addWidget(group_box)

        self.text_edit = text_edit  # 保存引用以便后续使用
        self.button = button

    def create_function_buttons(self, layout):
        """创建功能按键区域"""
        group_box = QtWidgets.QGroupBox("功能按键")
        hbox_layout = QtWidgets.QHBoxLayout()
        hbox_layout.setSpacing(10)  # 设置控件之间的间距

        btn_enable = QtWidgets.QPushButton("电机使能")
        btn_enable.setFont(QtGui.QFont("Arial", 12))

        btn_disable = QtWidgets.QPushButton("电机解使能")
        btn_disable.setFont(QtGui.QFont("Arial", 12))

        hbox_layout.addWidget(btn_enable)
        hbox_layout.addWidget(btn_disable)

        group_box.setLayout(hbox_layout)
        layout.addWidget(group_box)

        self.btn_enable = btn_enable
        self.btn_disable = btn_disable

    def create_detection_mode(self, layout):
        """创建检测模式选择区域"""
        group_box = QtWidgets.QGroupBox("检测模式选择")
        hbox_layout = QtWidgets.QHBoxLayout()
        hbox_layout.setSpacing(10)  # 设置控件之间的间距

        rb_standard = QtWidgets.QRadioButton("标准模式")
        rb_standard.setFont(QtGui.QFont("Arial", 12))

        rb_customer = QtWidgets.QRadioButton("客制模式")
        rb_customer.setFont(QtGui.QFont("Arial", 12))

        hbox_layout.addWidget(rb_standard)
        hbox_layout.addWidget(rb_customer)

        group_box.setLayout(hbox_layout)
        layout.addWidget(group_box)

        self.rb_standard = rb_standard
        self.rb_customer = rb_customer

    def create_pressure_limits(self, layout):
        """创建自定义预压上下限区域"""
        group_box = QtWidgets.QGroupBox("自定义预压上下限")
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSpacing(10)  # 设置控件之间的间距

        lbl_upper = QtWidgets.QLabel("上限：")
        lbl_upper.setFont(QtGui.QFont("Arial", 12))
        txt_upper = QtWidgets.QLineEdit()
        txt_upper.setPlaceholderText("_________ N")
        txt_upper.setFont(QtGui.QFont("Arial", 12))

        lbl_lower = QtWidgets.QLabel("下限：")
        lbl_lower.setFont(QtGui.QFont("Arial", 12))
        txt_lower = QtWidgets.QLineEdit()
        txt_lower.setPlaceholderText("_________ N")
        txt_lower.setFont(QtGui.QFont("Arial", 12))

        grid_layout.addWidget(lbl_upper, 0, 0)
        grid_layout.addWidget(txt_upper, 0, 1)
        grid_layout.addWidget(lbl_lower, 1, 0)
        grid_layout.addWidget(txt_lower, 1, 1)

        group_box.setLayout(grid_layout)
        layout.addWidget(group_box)

        self.pressure_group_box = group_box  # 保存引用以便后续使用
        self.txt_upper = txt_upper
        self.txt_lower = txt_lower

    def create_button_panel(self, layout):
        """创建操作按钮区域"""
        hbox_layout = QtWidgets.QHBoxLayout()
        hbox_layout.setSpacing(10)  # 设置按钮之间的间距

        btn_back_to_log = QtWidgets.QPushButton("退出登录")
        btn_back_to_log.setFont(QtGui.QFont("Arial", 12))

        hbox_layout.addStretch(1)  # 添加伸缩空间，使按钮靠右对齐
        hbox_layout.addWidget(btn_back_to_log)

        layout.addLayout(hbox_layout)

        self.btn_back_to_log = btn_back_to_log

    def on_mode_changed(self):
        """检测模式切换事件"""
        if self.rb_standard.isChecked():
            self.pressure_group_box.setVisible(False)  # 隐藏“自定义预压上下限”
        elif self.rb_customer.isChecked():
            self.pressure_group_box.setVisible(True)  # 显示“自定义预压上下限”

    def on_order_confirm(self):
        global orderName

        # 获取用户输入的订单号
        order_id = self.text_edit.toPlainText().strip()

        # 检查电机是否使能
        if not self.motor_enabled:
            self.show_message_box("错误", "电机未使能，请先使能电机！", icon=QtWidgets.QMessageBox.Critical)
            return

        if not order_id:
            # 如果订单号为空，提示用户
            self.show_message_box("错误", "订单号不能为空！", icon=QtWidgets.QMessageBox.Critical)
            return

        # 提示用户是否确认订单号
        reply = self.show_message_box(
            "确认订单号",
            f"您输入的订单号是：{order_id}\n是否确认？",
            buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            default_button=QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            folder_path = os.path.join(folderAddr, order_id)
            data_file_path = os.path.join(folder_path, "data.txt")

            if os.path.exists(folder_path):
                # 如果订单号已存在，提示用户
                reply = self.show_message_box(
                    "订单号已存在",
                    f"订单号 {order_id} 已存在。\n是否继续？",
                    buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                    default_button=QtWidgets.QMessageBox.No
                )
                if reply == QtWidgets.QMessageBox.No:
                    return  # 用户选择重新输入订单号

                # 读取现有的产品编号
                product_id = functions.read_product_id(data_file_path)
            else:
                # 创建订单号目录及子文件夹
                os.makedirs(os.path.join(folder_path, "pdfVersion"), exist_ok=True)
                os.makedirs(os.path.join(folder_path, "pictureVersion"), exist_ok=True)

                # 默认产品编号为 1
                product_id = 1

                # 创建或更新 data.txt 文件
                with open(data_file_path, "w", encoding="utf-8") as f:
                    f.write("订单号,创建时间,产品编号\n")
                    f.write(f"{order_id},{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{product_id}\n")

            # 新增：创建另一个 txt 文件用于存储 new_data_list 数据
            global data_storage_path
            data_storage_path = os.path.join(folder_path2, f"{order_id}_data.txt")  # 留出文件地址供自定义
            if not os.path.exists(data_storage_path):
                with open(data_storage_path, "w", encoding="utf-8") as f:
                    f.write("")  # 初始化为空文件

            # 检查是否为客制模式
            if self.rb_customer.isChecked():
                upper_limit = self.txt_upper.text().strip()
                lower_limit = self.txt_lower.text().strip()

                # 检查上限和下限是否为空
                if not upper_limit or not lower_limit:
                    self.show_message_box("错误", "预压上下限设定值不能为空！", icon=QtWidgets.QMessageBox.Critical)
                    return

                try:
                    upper_limit = float(upper_limit)
                    lower_limit = float(lower_limit)
                except ValueError:
                    self.show_message_box("错误", "预压上下限必须为数字！", icon=QtWidgets.QMessageBox.Critical)
                    return

                # 检查下限是否小于 0
                if lower_limit < 0:
                    self.show_message_box("错误", "预压下限不能小于 0！", icon=QtWidgets.QMessageBox.Critical)
                    return

                # 检查上限是否小于下限
                if upper_limit <= lower_limit:
                    self.show_message_box("错误", "预压下限需小于预压上限！", icon=QtWidgets.QMessageBox.Critical)
                    return

            # 进入下一个界面（例如参数设置界面）
            orderName = order_id
            self.frm_parameter_set = FrmParameterSet()
            self.frm_parameter_set.show()
            self.close()

    def on_exit_login(self):
        """退出登录按钮事件"""
        self.frm_log = FrmLog()
        self.frm_log.show()
        self.close()

    def show_message_box(self, title, message, buttons=QtWidgets.QMessageBox.Ok, icon=QtWidgets.QMessageBox.Information, default_button=None):
        """美化版 QMessageBox"""
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setStandardButtons(buttons)
        if default_button:
            msg_box.setDefaultButton(default_button)

        # 美化样式
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #f9f9f9;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        return msg_box.exec_()

    def on_motor_enable(self):
        """电机使能事件"""
        self.motor_enabled = True
        print("电机使能事件触发")
        # 在这里实现电机使能逻辑
        # Leds.enable_Led(23, 1)  # 绿灯亮
        # Leds.enable_Led(22, 0)  # 红灯灭
        # LinerMotor.enable_motor(16, 1)  # 电机使能
        self.show_message_box("成功", "电机使能成功！", icon=QtWidgets.QMessageBox.Information)
    def on_motor_disable(self):
        """电机解使能事件"""
        self.motor_enabled = False
        print("电机解使能事件触发")
        self.show_message_box("成功", "电机解使能成功！", icon=QtWidgets.QMessageBox.Information)
        # 在这里实现电机解使能逻辑
        # Leds.enable_Led(22, 1)  # 红灯亮
        # Leds.enable_Led(23, 0)  # 绿灯灭
        # LinerMotor.enable_motor(16, 0)  # 电机解使能
#参数确定界面
class FrmParameterSet(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("参数检测界面")
        self.setGeometry(100, 100, 800, 500)  # 设置窗口大小为 800x500
        self.setFixedSize(800, 500)  # 固定窗口大小
        self.center_on_screen()

        # 设置全局样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #f3f4f6, stop:1 #e5e7eb
                ); /* 浅灰色渐变背景 */
            }
            QGroupBox {
                background-color: #ffffff; /* 白色背景 */
                border: 1px solid #ccc; /* 灰色边框 */
                border-radius: 8px; /* 圆角 */
                padding: 10px; /* 内边距 */
            }
            QLabel {
                color: #333333; /* 深灰色文字 */
                font-size: 12px;
            }
            QLineEdit, QComboBox {
                background-color: #ffffff; /* 白色背景 */
                border: 1px solid #ccc; /* 灰色边框 */
                border-radius: 4px;
                padding: 5px;
                color: #333333; /* 深灰色文字 */
            }
            QPushButton {
                background-color: #007BFF; /* 蓝色按钮 */
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #0056b3; /* 鼠标悬停时变深 */
            }
        """)

        # 创建主布局
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)  # 设置边距
        main_layout.setSpacing(15)  # 设置控件之间的间距

        # 添加基本参数区域
        self.create_basic_parameters(main_layout)

        # 添加检测参数区域
        self.create_detection_parameters(main_layout)

        # 添加操作按钮区域
        self.create_button_panel(main_layout)

    def center_on_screen(self):
        """将窗口居中显示"""
        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        window_width = self.width()
        window_height = self.height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.move(x, y)

    def create_basic_parameters(self, layout):
        """创建基本参数区域"""
        basic_group = QtWidgets.QGroupBox("基本参数")
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSpacing(10)  # 设置控件之间的间距

        # 参数数据
        labels = [
            "跑和次数：", "跑和速度：", "产品编号：",
            "测量次数：", "平均预压："
        ]
        global orderName
        global product_id
        product_id = functions.read_product_id(f"{folderAddr}\\{orderName}\\data.txt")
        dataAccount = functions.read_data(filenameDates)
        if dataAccount is not None and len(dataAccount) == 4:
            DatesPreInos.runtimesPre, AccountInfos.checkTimesPre, AccountInfos.runSpeedPre, AccountInfos.anglePre = dataAccount
        default_values = [f"{DatesPreInos.runtimesPre} 次", f"{AccountInfos.runSpeedPre} mm/s", f"{product_id}", f"{AccountInfos.checkTimesPre} 次", "_________"]
        font = QtGui.QFont("Arial", 10)  # 设置字体

        # 将参数分为两列显示
        for i, (label_text, default_value) in enumerate(zip(labels, default_values)):
            row = i // 2  # 每行最多显示 2 个参数
            col = i % 2   # 列索引
            label = QtWidgets.QLabel(label_text)
            label.setFont(font)
            line_edit = QtWidgets.QLineEdit(default_value)
            line_edit.setFont(font)
            line_edit.setReadOnly(True)  # 设置为只读模式
            grid_layout.addWidget(label, row, col * 2)       # 标签放在偶数列
            grid_layout.addWidget(line_edit, row, col * 2 + 1)  # 输入框放在奇数列

        # 将网格布局添加到分组框
        basic_group.setLayout(grid_layout)
        layout.addWidget(basic_group)

    def create_detection_parameters(self, layout):
        """创建检测参数区域（调整为网格布局）"""
        global global_slider_type, global_slider_series, global_preload_size

        detection_group = QtWidgets.QGroupBox("检测参数")
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSpacing(10)  # 设置控件间距

        # 参数数据
        labels = ["滑块型号：", "滑块系列：", "预压力大小：", "导轨长度："]
        options = [["MGN3", "MGN7", "MGN9", "MGN12", "MGN15", "MGW2", "MGW3", "MGW7", "MGW9", "MGW12", "MGW14", "MGW15"], ["HSlider","CSlider"], ["Z0","Z1","ZF"], []]  # 空列表表示使用输入框
        default_values = ["MGN7", "HSlider", "Z0", "_________"]
        font = QtGui.QFont("Arial", 10)

        # 使用网格布局排列参数（与基本参数一致）
        for i, (label_text, opts, default) in enumerate(zip(labels, options, default_values)):
            row = i // 2  # 每行显示2个参数
            col = i % 2  # 列索引
            label = QtWidgets.QLabel(label_text)
            label.setFont(font)

            # 创建控件（组合框或输入框）
            if opts:  # 有选项时使用组合框
                combo = QtWidgets.QComboBox()
                combo.addItems(opts)
                combo.setCurrentText(default)
                combo.setFont(font)
                grid_layout.addWidget(label, row, col * 2)  # 标签在偶数列
                grid_layout.addWidget(combo, row, col * 2 + 1)  # 控件在奇数列

                # 将组合框引用保存，方便后续获取值
                if label_text == "滑块型号：":
                    self.combo_slider_type = combo
                elif label_text == "滑块系列：":
                    self.combo_slider_series = combo
                elif label_text == "预压力大小：":
                    self.combo_preload_size = combo
            else:  # 无选项时使用输入框
                line_edit = QtWidgets.QLineEdit(default)
                line_edit.setFont(font)
                line_edit.setReadOnly(True)
                grid_layout.addWidget(label, row, col * 2)
                grid_layout.addWidget(line_edit, row, col * 2 + 1)

        detection_group.setLayout(grid_layout)
        layout.addWidget(detection_group)

    def create_button_panel(self, layout):
        """创建操作按钮区域"""
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)  # 设置按钮之间的间距

        # 定义按钮名称
        button_names = ["自动检测", "开始检测", "修改订单号", "订单查询"]

        # 创建按钮并添加到布局中
        self.buttons = {}  # 存储按钮的字典
        font = QtGui.QFont("Arial", 10)  # 设置字体
        for name in button_names:
            button = QtWidgets.QPushButton(name)
            button.setFont(font)

            # 绑定按钮事件
            if name == "自动检测":
                button.clicked.connect(self.btnEveAutoCheck)
            elif name == "开始检测":
                button.clicked.connect(self.btnEveStartCheck)
            elif name == "修改订单号":
                button.clicked.connect(self.btnEveBackPas)
            elif name == "订单查询":
                button.clicked.connect(self.btnEveBackQuery)

            button_layout.addWidget(button)
            self.buttons[name] = button

        # 将按钮布局添加到主布局
        layout.addLayout(button_layout)

    # 按钮事件处理函数
    def btnEveAutoCheck(self):
        print("自动检测按钮被点击")

    def btnEveStartCheck(self):
        global global_slider_type, global_slider_series, global_preload_size

        # 获取用户选择的值
        global_slider_type = self.combo_slider_type.currentText()
        global_slider_series = self.combo_slider_series.currentText()
        global_preload_size = self.combo_preload_size.currentText()

        print(f"滑块类型: {global_slider_type}, 滑块系列: {global_slider_series}, 预压力大小: {global_preload_size}")

        # 进入下一个界面（例如 MainWindow）
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()  # 关闭当前界面

    def btnEveBackPas(self):
        print("修改订单号按钮被点击")
        self.frmInputDingdan = FrmInputDingdan()
        self.frmInputDingdan.show()
        self.close()

    def btnEveBackQuery(self):
        print("订单查询按钮被点击")
        self.frm_order_query = FrmOrderQuery()
        self.frm_order_query.show()
        self.close()
#结果输出界面
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据显示界面")
        self.setGeometry(100, 100, 800, 600)  # 增加窗口高度以容纳更多内容
        self.setFixedSize(800, 600)  # 固定窗口大小
        self.center_on_screen()
        # 设置全局样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #f3f4f6, stop:1 #e5e7eb
                ); /* 浅灰色渐变背景 */
            }
            QLabel {
                color: #333333; /* 深灰色文字 */
                font-size: 12px;
            }
            QLineEdit {
                background-color: #ffffff; /* 白色背景 */
                border: 1px solid #ccc; /* 灰色边框 */
                border-radius: 4px;
                padding: 5px;
                color: #333333; /* 深灰色文字 */
            }
            QPushButton {
                background-color: #007BFF; /* 蓝色按钮 */
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #0056b3; /* 鼠标悬停时变深 */
            }
        """)
        # 创建主布局
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)  # 设置边距
        main_layout.setSpacing(15)  # 设置控件之间的间距
        # 上半部分：Matplotlib 曲线图
        self.canvas = PlotCanvas(self, width=6, height=4)  # 增加高度
        main_layout.addWidget(self.canvas)
        # 下半部分：参数显示区域
        self.create_parameter_panel(main_layout)
        # 最下面：添加按钮区域
        self.create_button_panel(main_layout)
        # 初始化保存数据按钮状态
        self.save_data_enabled = True  # 控制“保存数据”按钮是否可用

    def center_on_screen(self):
        """将窗口居中显示"""
        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        window_width = self.width()
        window_height = self.height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.move(x, y)

    def create_parameter_panel(self, layout):
        global product_id, global_slider_type, global_slider_series, global_preload_size
        dataAccount = functions.read_data(filenameDates)
        if dataAccount is not None and len(dataAccount) == 4:
            DatesPreInos.runtimesPre, AccountInfos.checkTimesPre, AccountInfos.runSpeedPre, AccountInfos.anglePre = dataAccount

        # 使用全局变量生成 test_data，并添加“合格与否”字段
        test_data = [
            f"{DatesPreInos.runtimesPre}次",
            f"{AccountInfos.runSpeedPre} mm/s",
            f"{product_id}",
            global_slider_type,
            global_slider_series,
            global_preload_size,
            f"{AccountInfos.checkTimesPre}次",
            "合格"  # 默认值为“合格”
        ]

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSpacing(10)  # 设置控件之间的间距

        # 参数数据
        labels = [
            "跑和次数：", "跑和速度：", "产品编号：",
            "滑块型号：", "滑块系列：", "预压力大小：", "测量次数：",
            "合格与否："  # 新增的标签
        ]
        default_values = test_data
        font = QtGui.QFont("Arial", 10)  # 设置字体

        # 将参数分为两列显示
        for i, (label_text, default_value) in enumerate(zip(labels, default_values)):
            row = i // 4  # 每行最多显示 4 个参数
            col = i % 4   # 列索引
            label = QtWidgets.QLabel(label_text)
            label.setFont(font)
            label.setStyleSheet("color: #333;")  # 设置文字颜色
            line_edit = QtWidgets.QLineEdit(default_value)
            line_edit.setFont(font)
            line_edit.setReadOnly(True)  # 设置为只读模式
            line_edit.setStyleSheet("""
                QLineEdit {
                    background-color: #ffffff;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 5px;
                }
            """)  # 设置样式
            grid_layout.addWidget(label, row, col * 2)  # 标签放在偶数列
            grid_layout.addWidget(line_edit, row, col * 2 + 1)  # 输入框放在奇数列

        # 将网格布局添加到主布局
        layout.addLayout(grid_layout)

    def create_button_panel(self, layout):
        # 创建水平布局用于放置按钮
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)  # 设置按钮之间的间距
        button_layout.setContentsMargins(0, 0, 0, 0)  # 移除边距

        # 定义按钮名称
        button_names = ["再次测量", "保存数据", "修改参数"]

        # 创建按钮并添加到布局中
        self.buttons = {}  # 存储按钮的字典
        font = QtGui.QFont("Arial", 10)  # 设置字体
        for name in button_names:
            button = QtWidgets.QPushButton(name)
            button.setFont(font)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
            """)  # 设置按钮样式

            # 绑定按钮事件
            if name == "再次测量":
                button.clicked.connect(self.on_remeasure)
            elif name == "保存数据":
                button.clicked.connect(self.on_save_date)
            elif name == "修改参数":
                button.clicked.connect(self.on_back)
            button_layout.addWidget(button)
            self.buttons[name] = button

        # 将按钮布局添加到主布局
        layout.addLayout(button_layout)

    # 按钮事件处理函数
    def on_remeasure(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()  # 关闭当前界面

    def on_save_date(self):
        global orderName
        global product_id
        if dataAccount is not None and len(dataAccount) == 4:
            DatesPreInos.runtimesPre, AccountInfos.checkTimesPre, AccountInfos.runSpeedPre, AccountInfos.anglePre = dataAccount
        header_data = [
            ["", "", "检验参数", "", "", ""],
            ["订单编号", f"{orderName}", "跑合次数", f"{DatesPreInos.runtimesPre}", "测量次数", f"{AccountInfos.checkTimesPre}"],
            ["滑块型号", "", "预压等级", "", "合格预压范围", ""],
            ["", "", "检测数据", "", "", ""],
            ["编号", "平均预压(N)", "测量预压最大值(N)", "测量预压最小值(N)", "客制/标准", "合格/不合格"],
        ]
        # 弹出确认对话框
        reply = self.show_message_box(
            "保存数据",
            "是否确定要保存当前数据？",
            buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            default_button=QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            # 截图保存路径
            folder_path = os.path.join(folderAddr, orderName, "pictureVersion")
            image_path = os.path.join(folder_path, f"{product_id}.png")
            # 截取当前窗口截图
            screenshot = self.grab()
            screenshot.save(image_path)
            # 更新产品编号
            product_id += 1
            functions.update_product_id(f"{folderAddr}\\{orderName}\\data.txt", product_id)
            global data_storage_path
            new_data = [["1", "100N", "最大值", "最小值", "标准", "不合格"]]
            functions.update_data_in_txt(data_storage_path, new_data, append=True)
            # 调用 saveDateToPdf 保存数据到 PDF
            new_data_list = functions.read_data_from_txt(data_storage_path)
            try:
                functions.saveDateToPdf(new_data_list, orderName, folderAddr, header_data)
                print("PDF 文件已成功生成！")
            except Exception as e:
                print(f"生成 PDF 文件失败：{str(e)}")
            # 提示保存成功
            self.show_message_box(
                "保存成功",
                f"数据已保存!",
                icon=QtWidgets.QMessageBox.Information
            )
            # 禁用“保存数据”按钮
            self.buttons["保存数据"].setEnabled(False)
            self.save_data_enabled = False

    def on_back(self):
        """修改参数按钮被点击"""
        self.frm_parameter_set = FrmParameterSet()
        self.frm_parameter_set.show()
        self.close()

    def show_message_box(self, title, message, buttons=QtWidgets.QMessageBox.Ok, icon=QtWidgets.QMessageBox.Information, default_button=None):
        """美化版 QMessageBox"""
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setStandardButtons(buttons)
        if default_button:
            msg_box.setDefaultButton(default_button)
        # 美化样式
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #f9f9f9;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        return msg_box.exec_()
#曲线图界面
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=6, height=4, dpi=100):
        # 创建 Matplotlib 图形
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

        # 设置背景颜色
        self.setStyleSheet("""
            background-color: qlineargradient(
                spread:pad, 
                x1:0, y1:0, x2:1, y2:1, 
                stop:0 #f9f9f9, stop:1 #e5e5e5
            ); /* 浅灰色渐变背景 */
            border: 1px solid #ccc; /* 边框 */
            border-radius: 8px; /* 圆角 */
            padding: 10px; /* 内边距 */
        """)

        # 调整 Matplotlib 布局，避免标签被遮挡
        fig.tight_layout(pad=3.0)  # 自动调整布局，增加 padding

        # 绘制初始曲线图
        self.plot()

    def plot(self):
        # 示例数据
        x = [i * 0.1 for i in range(100)]
        y = [i**2 for i in x]

        # 绘制曲线图
        self.axes.clear()  # 清除之前的图形
        self.axes.plot(x, y, 'r-', linewidth=2)
        self.axes.set_title("压力显示图", fontsize=12, color="#333")
        self.axes.set_xlabel("时间 (s)", fontsize=10, color="#555", labelpad=10)  # 增加 labelpad 避免遮挡
        self.axes.set_ylabel("值", fontsize=10, color="#555", labelpad=10)  # 增加 labelpad
        self.axes.grid(True, linestyle='--', alpha=0.6)  # 添加网格线

        # 设置 Matplotlib 背景颜色
        self.axes.set_facecolor("#f9f9f9")  # 浅灰色背景
        self.axes.spines['top'].set_visible(False)  # 隐藏顶部边框
        self.axes.spines['right'].set_visible(False)  # 隐藏右侧边框
        self.draw()
if __name__ == '__main__':
    app =QtWidgets.QApplication(sys.argv)
    frmlog = MainWindow()
    frmlog.show()

    sys.exit(app.exec_())