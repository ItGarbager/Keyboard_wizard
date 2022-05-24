import sys
import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from pynput import keyboard

'''桌面宠物'''
KEY = 'init'


# 监听按压
def on_press(key):
    global KEY
    try:
        KEY = key.char

    except AttributeError:
        key = "%s" % key
        KEY = key.rsplit(".", 1)[-1]


# 监听释放
def on_release(key):
    global KEY
    KEY = 'init'


class DesktopPet(QWidget):
    ROOT_DIR = 'images'

    def __init__(self, parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)
        # 初始化
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()

        # 加载图标
        icon_path = self.load_icon()

        # 设置退出选项
        quit_action = QAction('退出', self, triggered=self.quit)
        quit_action.setIcon(QIcon(icon_path))
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icon_path))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()

        # 当前显示的图片
        self.image = QLabel(self)

        # 是否跟随鼠标
        self.is_follow_mouse = False
        # 拖拽时避免鼠标直接跳到左上角
        self.mouse_drag_pos = self.pos()
        # 显示
        self.image = QLabel(self)  # 实例化图片对象
        self.init_image()

        self.show()

        # 定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.runFrame)
        self.timer.start(2)  # 每2毫秒更新一次 runFrame 动作

    def load_icon(self):
        """随机导入一个桌面宠物的所有图片，在py相同文件夹中新建图片文件夹命名为‘resources’,
            再新建文件夹名‘pet_1’,将图片保存在‘pet_1’中,也可以多设置几个文件夹，将不同类型的图片保存在里面
            """
        icon_path = os.path.join(self.ROOT_DIR, 'icon.png')
        return icon_path

    def runFrame(self):
        """完成动作的每一帧"""
        self.set_image()

    def mousePressEvent(self, event):
        """鼠标左键按下时, 宠物将和鼠标位置绑定"""
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        """鼠标移动, 则宠物也移动"""
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        """
        鼠标释放时, 取消绑定
        """
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def init_image(self):
        """初始化图像"""
        # 设置布局
        myLayout = QGridLayout()

        # 设置布局没有边缘空白
        myLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(myLayout)

        # 设置显示图片
        self.set_image()
        myLayout.addWidget(self.image)

    def set_image(self):
        """设置更新当前图片"""
        image_path = os.path.join(self.ROOT_DIR, KEY + ".png")
        if not os.path.isfile(image_path):
            image_path = os.path.join(self.ROOT_DIR, "init.png")

        self.image.setPixmap(QPixmap(image_path))

        self.image.setScaledContents(True)
        # 设置label最大大小
        self.image.setMaximumSize(194, 120)

    def quit(self):
        """退出程序"""
        self.close()
        sys.exit()


if __name__ == '__main__':
    listener = keyboard.Listener(
        on_press=on_press, on_release=on_release
    )
    listener.start()  # 启动键盘监听线程
    app = QApplication(sys.argv)
    pet = DesktopPet()

    sys.exit(app.exec_())
