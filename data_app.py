import sys
import serial
import serial.tools.list_ports
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QMessageBox
import pyqtgraph as pg
from data_deal import Data_Deal
from MainWindow import Ui_MainWindow


class Data_App(QWidget, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # 创建串口实例对象
        self.ser = serial.Serial()
        # 创建 QTimer 实例对象
        self.timer = QTimer()
        # 创建显示窗口
        self.main_window = QMainWindow()
        self.setupUi(self.main_window)
        self.retranslateUi(self.main_window)

        # 储存所有存在的串口 字典
        self.Com_Dict = {}
        # 串口开关标志
        self.open_flag = False
        # 创建新csv文件标志
        self.create_file_flag = True
        # 要保存的当前的文件名
        self.now_file_name = None
        # 串口接收的字符串
        self.receive_bit_data = None
        self.receive_data = None
        # 图像对象
        self.flow = None
        self.temp = None
        self.pressure1 = None
        self.pressure2 = None
        self.pressure3 = None
        self.pressure4 = None
        self.conductor = None
        self.ph = None
        # 绘图相关数据
        self.x = 0
        self.y1 = []
        self.y2 = []
        self.y3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.y4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.y5 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.y6 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.y7 = []
        self.y8 = []
        # 接收数据处理后的元组
        self.display_value = ()
        # 发送数据
        self.data1 = ''
        self.data2 = ''
        self.data3 = ''
        self.data4 = ''

        self.init()
        self.port_check()

        # 按键关联

    def init(self):
        # 串口开关按钮
        self.Button_Open.clicked.connect(self.port_opreation)
        # 数据接收按钮
        self.Button_Rec.clicked.connect(self.data_begin)
        # 数据发送按钮
        self.Button_send1.clicked.connect(self.data_send1)
        self.Button_send2.clicked.connect(self.data_send2)
        self.Button_send3.clicked.connect(self.data_send3)
        self.Button_send4.clicked.connect(self.data_send4)
        # 退出程序
        self.Button_quit.clicked.connect(self.app_close)
        # 串口检测按钮
        self.Button_FindPort.clicked.connect(self.port_check)
        # 定时器接收数据
        self.timer.timeout.connect(self.data_receive)
        # PlotWidget 实例初始化
        self.plotView_1_init()
        self.plotView_2_init()
        self.plotView_3_init()
        self.plotView_4_init()
        self.plotView_5_init()
        self.plotView_6_init()
        self.plotView_7_init()
        self.plotView_8_init()

    def plotView_1_init(self):
        self.plotView_1.setTitle("流量趋势",
                                 color='008080',
                                 size='12pt')
        # 设置上下左右的label
        self.plotView_1.setLabel("left", "流量(单位)")
        self.plotView_1.setLabel("bottom", "采样点")

        # 设置自适应刻度范围
        self.plotView_1.enableAutoRange()

        # 显示表格线
        self.plotView_1.showGrid(x=True, y=True)

        # 背景色改为白色
        self.plotView_1.setBackground('w')

        # 实时显示应该获取 plotItem， 调用setData，
        # 这样只重新plot该曲线，性能更高
        self.flow = self.plotView_1.getPlotItem().plot(
            pen=pg.mkPen('r', width=1)
        )

    def plotView_2_init(self):
        self.plotView_2.setTitle("温度趋势",
                                 color='008080',
                                 size='12pt')
        # 设置上下左右的label
        self.plotView_2.setLabel("left", "温度(摄氏度)")
        self.plotView_2.setLabel("bottom", "采样点")

        # 设置自适应刻度范围
        self.plotView_2.enableAutoRange()

        # 显示表格线
        self.plotView_2.showGrid(x=True, y=True)

        # 背景色改为白色
        self.plotView_2.setBackground('w')

        # 实时显示应该获取 plotItem， 调用setData，
        # 这样只重新plot该曲线，性能更高
        self.temp = self.plotView_2.getPlotItem().plot(
            pen=pg.mkPen('r', width=1)
        )

    def plotView_3_init(self):
        self.plotView_3.setTitle("动脉压趋势",
                                 color='008080',
                                 size='12pt')
        # 设置上下左右的label
        self.plotView_3.setLabel("left", "动脉压(单位)")
        self.plotView_3.setLabel("bottom", "采样点")

        # 设置自适应刻度范围
        self.plotView_3.enableAutoRange()

        # 显示表格线
        self.plotView_3.showGrid(x=True, y=True)

        # 背景色改为白色
        self.plotView_3.setBackground('w')

        # 实时显示应该获取 plotItem， 调用setData，
        # 这样只重新plot该曲线，性能更高
        self.pressure1 = self.plotView_3.getPlotItem().plot(
            pen=pg.mkPen('r', width=1)
        )

    def plotView_4_init(self):
        self.plotView_4.setTitle("静脉压趋势",
                                 color='008080',
                                 size='12pt')
        # 设置上下左右的label
        self.plotView_4.setLabel("left", "静脉压(单位)")
        self.plotView_4.setLabel("bottom", "采样点")

        # 设置自适应刻度范围
        self.plotView_4.enableAutoRange()

        # 显示表格线
        self.plotView_4.showGrid(x=True, y=True)

        # 背景色改为白色
        self.plotView_4.setBackground('w')

        # 实时显示应该获取 plotItem， 调用setData，
        # 这样只重新plot该曲线，性能更高
        self.pressure2 = self.plotView_4.getPlotItem().plot(
            pen=pg.mkPen('r', width=1)
        )

    def plotView_5_init(self):
        self.plotView_5.setTitle("新鲜液压力趋势",
                                 color='008080',
                                 size='12pt')
        # 设置上下左右的label
        self.plotView_5.setLabel("left", "新鲜液液(单位)")
        self.plotView_5.setLabel("bottom", "采样点")

        # 设置自适应刻度范围
        self.plotView_5.enableAutoRange()

        # 显示表格线
        self.plotView_5.showGrid(x=True, y=True)

        # 背景色改为白色
        self.plotView_5.setBackground('w')

        # 实时显示应该获取 plotItem， 调用setData，
        # 这样只重新plot该曲线，性能更高
        self.pressure3 = self.plotView_5.getPlotItem().plot(
            pen=pg.mkPen('r', width=1)
        )

    def plotView_6_init(self):
        self.plotView_6.setTitle("废液压力趋势",
                                 color='008080',
                                 size='12pt')
        # 设置上下左右的label
        self.plotView_6.setLabel("left", "废液压力(单位)")
        self.plotView_6.setLabel("bottom", "采样点")

        # 设置自适应刻度范围
        self.plotView_6.enableAutoRange()

        # 显示表格线
        self.plotView_6.showGrid(x=True, y=True)

        # 背景色改为白色
        self.plotView_6.setBackground('w')

        # 实时显示应该获取 plotItem， 调用setData，
        # 这样只重新plot该曲线，性能更高
        self.pressure4 = self.plotView_6.getPlotItem().plot(
            pen=pg.mkPen('r', width=1)
        )

    def plotView_7_init(self):
        self.plotView_7.setTitle("电导率趋势",
                                 color='008080',
                                 size='12pt')
        # 设置上下左右的label
        self.plotView_7.setLabel("left", "电导(单位)")
        self.plotView_7.setLabel("bottom", "采样点")

        # 设置自适应刻度范围
        self.plotView_7.enableAutoRange()

        # 显示表格线
        self.plotView_7.showGrid(x=True, y=True)

        # 背景色改为白色
        self.plotView_7.setBackground('w')

        # 实时显示应该获取 plotItem， 调用setData，
        # 这样只重新plot该曲线，性能更高
        self.conductor = self.plotView_7.getPlotItem().plot(
            pen=pg.mkPen('r', width=1)
        )

    def plotView_8_init(self):
        self.plotView_8.setTitle("PH趋势",
                                 color='008080',
                                 size='12pt')
        # 设置上下左右的label
        self.plotView_8.setLabel("left", "PH(单位)")
        self.plotView_8.setLabel("bottom", "采样点")

        # 设置自适应刻度范围
        self.plotView_8.enableAutoRange()

        # 显示表格线
        self.plotView_8.showGrid(x=True, y=True)

        # 背景色改为白色
        self.plotView_8.setBackground('w')

        # 实时显示应该获取 plotItem， 调用setData，
        # 这样只重新plot该曲线，性能更高
        self.ph = self.plotView_8.getPlotItem().plot(
            pen=pg.mkPen('r', width=1)
        )

        # 串口检测

    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        port_list = list(serial.tools.list_ports.comports())
        self.Box_get_port.clear()
        if len(port_list) == 0:
            self.Box_get_port.addItem("无串口")
            QMessageBox.information(self, "信息", "未检测到串口！")
        else:
            self.Box_get_port.clear()
            for port in port_list:
                self.Com_Dict["%s" % port[0]] = "%s" % port[1]
                self.Box_get_port.addItem(port[0])

        # 串口开关操作

    def port_opreation(self):
        self.open_flag = ~self.open_flag
        if self.open_flag:
            self.port_open()
        else:
            self.port_close()

    def data_begin(self):
        if self.ser.isOpen():
            # 打开串口接收定时器，周期为100ms
            if not self.timer.isActive():
                self.timer.start(100)
                self.Button_Rec.setText("接收中")
            else:
                return None
        else:
            QMessageBox.information(self, 'Port', '串口未打开！')

        # 打开串口

    def port_open(self):
        # 从QComboBox的当前值获取端口号
        self.ser.port = self.Box_get_port.currentText()
        # self.ser.port = 'COM1'
        # 设置串口通信参数
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.parity = "N"
        # timeout默认为None，若不设置timeout，当使用read()时，一直会等到读取指定的字节数为止
        self.ser.timeout = 2
        self.ser.write_timeout = 2
        try:
            self.ser.open()
        except:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            return None
        # 判断是否有串口打开
        if self.ser.isOpen():
            # 打开串口接收定时器，周期为100ms
            self.statusbar.showMessage("打开串口成功")
            # self.timer.start(100)
            self.Button_Open.setText("关闭")

        # 关闭串口

    def port_close(self):
        self.timer.stop()
        try:
            self.ser.close()
        except:
            pass

        if not self.ser.isOpen():
            self.Button_Open.setText("打开")
            self.Button_Rec.setText("接收")
            self.statusbar.showMessage("串口已关闭")

        # 接收数据

    def data_receive(self):
        try:
            num = self.ser.inWaiting()
        except:
            self.port_close()
            QMessageBox.critical(self, "Read Error", "读取输入缓存区数据的字节数失败！")
            return None

        print(num)
        self.receive_bit_data = self.ser.read(31)
        print(self.receive_bit_data)
        self.receive_data = self.receive_bit_data.decode('ascii')
        print(self.receive_data)
        self.statusbar.showMessage("数据读取成功，准备处理数据")
        self.data_operation()

        # 处理接收的数据

    def data_operation(self):
        # 这里的receive_data指的是发送端发送的字符串
        print('开始数据处理')
        if len(self.receive_data) == 31:
            try:
                # 使用获得的数据字符串创建一个对象
                print('读取数据长度没问题')
                data = Data_Deal(self.receive_data)
                # 对数据进行分析处理，并获得一个元祖类型的返回值，以便后面更新显示
                print('数据解析对象生成')
                self.display_value = data.get_num()
                print('数据解析完成，准备处理数据')
                print(self.display_value)
                print(self.display_value[0])
            except ValueError:
                self.statusbar.showMessage('数据解析失败！准备重新接收')
                self.ser.reset_input_buffer()
                return None
            # 判断需要创建一个新的csv还是直接存入当前csv(每次数据接收成功都会为之创建一个csv文件)
            # if self.create_file_flag:
            #    self.create_file_flag = False
            #    # 当前成功接收的数据所存放的文件名
            #    self.now_file_name = self.receive_data[4:6] + "_" + \
            #                         self.receive_data[6:8] + "_" + \
            #                         self.receive_data[8:10] + ".csv"
            #    data.create_csv(self.now_file_name)
            # else:
            #    data.store_to_csv(self.now_file_name)
            if self.display_value[0] == 'tmp':
                print('数据格式没问题')
                self.show_update()
                self.statusbar.showMessage("数据格式正确，更新数据完毕")
            else:
                self.statusbar.showMessage('数据格式不正确！准备重新接收')
                # QMessageBox.information(self, "信息", "数据格式不正确！准备重新接收")
                self.ser.reset_input_buffer()
                return None
        elif len(self.receive_data) == 0:
            self.port_close()
            QMessageBox.information(self, "信息", "没有读到数据！")
            return None
        else:
            self.statusbar.showMessage("读取的数据的字节数不对！准备重新接收")
            # QMessageBox.information(self, "信息", "读取的数据的字节数不对！准备重新接收")
            self.ser.reset_input_buffer()
            return None
            # pass #self.textBrowser.insertPlainText("Data Receive Error: Wrong Data Length!\r\n")
            # QMessageBox.critical(self, "Data Length Error", "从输入缓存区读取数据的字节数不对！")

        # 更新所有显示

    def show_update(self):
        # 更新文本显示区域的数据
        self.label_value_3.setText(str(self.display_value[1]))
        self.label_value_4.setText(str(self.display_value[2]))
        self.label_value_5.setText(str(self.display_value[3]))
        self.label_value_6.setText(str(self.display_value[4]))
        # 更新数据
        self.x += 1
        # self.y1.append(self.display[0])
        # self.y2.append(self.display[1])
        self.y3[:-1] = self.y3[1:]
        self.y3[-1] = self.display_value[1]
        self.y4[:-1] = self.y4[1:]
        self.y4[-1] = self.display_value[2]
        self.y5[:-1] = self.y5[1:]
        self.y5[-1] = self.display_value[3]
        self.y6[:-1] = self.y6[1:]
        self.y6[-1] = self.display_value[4]
        # self.y7.append(self.display[6])
        # 更新图形
        # self.statusBar.showMessage("绘图对象：实时数据，当前数据保存文件为 %s" % self.now_file_name)
        # self.flow.setData(self.x, self.y1)
        # self.temp.setData(self.x, self.y2)
        self.pressure1.setData(self.y3)
        self.pressure1.setPos(self.x, 0)
        self.pressure2.setData(self.y4)
        self.pressure2.setPos(self.x, 0)
        self.pressure3.setData(self.y5)
        self.pressure3.setPos(self.x, 0)
        self.pressure4.setData(self.y6)
        self.pressure4.setPos(self.x, 0)
        # self.ph.setData(self.x, self.y7)

    def data_send1(self):
        # print('按钮1')
        try:
            if self.ser.isOpen():
                self.data1 = 'rec' + self.input_1.text()
                # print(self.data1)
                if len(self.data1) == 6:
                    try:
                        int(self.input_1.text())
                    except ValueError:
                        QMessageBox.information(self, '提示', '请输入3位整数')
                        return None
                    else:
                        data = (self.data1+"\r\n").encode('ascii')
                        self.ser.write(data)
                        # self.input_1.setText('')
                        return None
                elif len(self.data1) == 3:
                    QMessageBox.information(self, '提示', '发送数据不能为空！')
                    return None
                else:
                    QMessageBox.information(self, '提示', '请输入3位整数')
                    return None
            else:
                QMessageBox.information(self, 'Port', '串口未打开')
                return None
        except ValueError:
            QMessageBox.critical(self, 'Input Error', '请输入合法数据')
            return None

    def data_send2(self):
        # print('按钮2')
        try:
            if self.ser.isOpen():
                self.data2 = 'hec' + self.input_2.text()
                if len(self.data2) == 6:
                    try:
                        int(self.input_2.text())
                    except ValueError:
                        QMessageBox.information(self, '提示', '请输入三位整数')
                        return None
                    else:
                        data = (self.data2+"\r\n").encode('ascii')
                        self.ser.write(data)
                        # self.input_2.setText('')
                        return None
                elif len(self.data2) == 3:
                    QMessageBox.information(self, '提示', '发送数据不能为空！')
                    return None
                else:
                    QMessageBox.information(self, '提示', '请输入三位整数')
                    return None
            else:
                QMessageBox.information(self, 'Port', '串口未打开')
                return None
        except ValueError:
            QMessageBox.critical(self, 'Input Error', '请输入合法数据')
            return None

    def data_send3(self):
        print('按钮3')
        try:
            if self.ser.isOpen():
                self.data3 = 'cmd' + self.input_3.text()
                if len(self.data3) == 12:
                    try:
                        int(self.input_3.text())
                    except ValueError:
                        QMessageBox.information(self, '提示', '请输入八位整数')
                        return None
                    else:
                        print(self.data3)
                        data = (self.data3+"\r\n").encode('ascii')
                        self.ser.write(data)
                        # self.input_3.setText('')
                        return None
                elif len(self.data3) == 3:
                    QMessageBox.information(self, '提示', '发送数据不能为空！')
                    return None
                else:
                    QMessageBox.information(self, '提示', '请输入三位整数')
                    return None
            else:
                QMessageBox.information(self, 'Port', '串口未打开')
                return None
        except ValueError:
            QMessageBox.critical(self, 'Input Error', '请输入合法数据')
            return None

    def data_send4(self):
        # print('按钮4')
        try:
            if self.ser.isOpen():
                self.data4 = 'bec' + self.input_4.text()
                if len(self.data4) == 6:
                    try:
                        int(self.input_4.text())
                    except ValueError:
                        QMessageBox.information(self, '提示', '请输入三位整数')
                        return None
                    else:
                        data = (self.data4+"\r\n").encode('ascii')
                        self.ser.write(data)
                        # self.input_4.setText('')
                        return None
                elif len(self.data4) == 3:
                    QMessageBox.information(self, '提示', '发送数据不能为空！')
                    return None
                else:
                    QMessageBox.information(self, '提示', '请输入三位整数')
                    return None
            else:
                QMessageBox.information(self, 'Port', '串口未打开')
                return None
        except ValueError:
            QMessageBox.critical(self, 'Input Error', '请输入合法数据')
            return None

        # 关闭系统

    def app_close(self):
        self.port_close()
        quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myShow = Data_App()
    myShow.main_window.show()
    sys.exit(app.exec_())
