import pandas as pd


class Data_Deal(object):
    def __init__(self, data_str):
        self.target = data_str
        self.flag = ""
        self.pressure = 0

    # 解码各数据要素，便于显示和绘图
    def get_num(self):
        print('在数据解析函数中')
        self.flag = self.target[0:3]
        self.pressure1 = float(self.target[3:10])
        self.pressure2 = float(self.target[10:17])
        self.pressure3 = float(self.target[17:24])
        self.pressure4 = float(self.target[24:31])
        return self.flag, self.pressure1, self.pressure2, self.pressure3, self.pressure4


    def store_to_txt(self):
        file = open("Data.txt", "a")
        file.write(self.target + "\n")
        file.close()

    def create_csv(self, file_name):
        df = pd.DataFrame({'Time': self.time[2:],
                           'Temperature': [self.temp],
                           'Humidity': self.humidity,
                           'Speed': self.speed,
                           'Direc_num': self.disp_direction[0],
                           'Direc_str': self.disp_direction[2],
                           'Pressure': self.pressure})
        df.to_csv(file_name, index=False)

    def store_to_csv(self, file_name):
        data_buff = pd.DataFrame({'Time': self.time[2:],
                                  'Temperature': self.temp,
                                  'Humidity': self.humidity,
                                  'Speed': self.speed,
                                  'Direc_num': self.disp_direction[0],
                                  'Direc_str': self.disp_direction[2],
                                  'Pressure': self.pressure}, index=[1])
        data_buff.to_csv(file_name, mode='a', encoding='utf-8',
                         header=False, index=False)
