
import pandas
import shutil
import sys
import time
import os
from tqdm import tqdm
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton

# 读取txt文件,并根据间隔的空格分割，用pandas
def read_txt(path):
    # 读取txt文件
    data = pandas.read_csv(path, sep=" ", header=None,encoding='gb18030')
    # 分割txt文件
    data = data[0].str.split("\\t", expand=True)
    # 选取第一列
    data = data.iloc[:,-1].to_list()
    print("获取路径完成")
    return data

# 将data的图片路径拷贝到output_path文件夹中
def copy_image(data, output_path, progress):
    # 创建一个空的错误列表
    error_list = []
    # 创建一个进度条
    pbar = tqdm(total=len(data))

    # 遍历data
    for i, item in enumerate(data):
        # 判断路径是否存在
        if not os.path.exists(item):
            # 添加到错误列表
            error_list.append(item)
        else:
            # 拷贝图片
            shutil.copy(item, output_path)
        # 更新进度条
        pbar.update(1)
        progress.setValue((i + 1) / len(data) * 100)

    # 关闭进度条
    pbar.close()
    # 如果有错误，弹出错误消息
    if error_list:
        long_message = "文件路径不存在:\n" + ', '.join(error_list)
        msg = ErrorDialog(long_message)
        msg.exec_()
    else:
        print("拷贝完成")


def copy_images_main(path, output_path, progress):
    # 记录时间
    start = time.time()
    #查看read_txt函数的返回值
    img_paths = read_txt(path)
    #查看copy_image函数的返回值
    copy_image(img_paths, output_path, progress)
    #结束时间
    end = time.time()
    # 输出运行时间
    print("运行时间：",end-start)
    #暂停2秒
    time.sleep(2)
    # 返回，而不是退出程序
    return 0
    # # 推出程序
    # sys.exit(0)

class ErrorDialog(QDialog):
    def __init__(self, long_message):
        super().__init__()

        self.initUI(long_message)

    def initUI(self, long_message):
        self.setWindowTitle('错误')

        layout = QVBoxLayout(self)

        # 创建一个QTextEdit并设置为只读
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setText(long_message)
        layout.addWidget(self.textEdit)

        # 创建一个关闭按钮
        self.closeButton = QPushButton('关闭', self)
        self.closeButton.clicked.connect(self.close)
        layout.addWidget(self.closeButton)

if __name__ == "__main__":
    # 设置一个txt文件路径，这个文件是用户输入的txt文件路径
    if len(sys.argv) > 1:
        path=sys.argv[1]
    else:
        path = input("请输入inital_pose.txt文件路径：")
        # path = r'E:\PIE-UAV\PIE-Smart-2D-dom-xqx-test\prj\test202304261315\SfM\Adjustment\main_reconstruction\inital_pose.txt'

    #设置一个输出文件夹路径，用于存放拷贝的图片
    if len(sys.argv) > 1:
        output_path=sys.argv[2]
    else:
        output_path = input("请输入输出文件夹路径：")
        # output_path = r'E:\PIE-UAV\PIE-Smart-2D-dom-xqx-test\prj\test202304261315\SfM\Adjustment\main_reconstruction\output'

    copy_images_main(path, output_path)