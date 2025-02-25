class FrmInputDingdan(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 绑定事件
        self.button.clicked.connect(self.on_order_confirm)  # 订单确认按钮事件
        self.btn_back_to_log.clicked.connect(self.on_exit_login)  # 退出登录按钮事件

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

    # 占位符：电机使能事件
    def on_motor_enable(self):
        """电机使能事件"""
        print("电机使能事件触发")
        # 在这里实现电机使能逻辑

    # 占位符：电机解使能事件
    def on_motor_disable(self):
        """电机解使能事件"""
        print("电机解使能事件触发")
        # 在这里实现电机解使能逻辑