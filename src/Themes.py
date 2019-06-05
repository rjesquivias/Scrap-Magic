import abc
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
abstractstaticmethod = abc.abstractmethod

class Theme(object, metaclass=abc.ABCMeta):
    @abstractstaticmethod
    def toolbar_color_style(self):
        pass

    @abstractstaticmethod
    def toolbar_color(self):
        pass

    @abstractstaticmethod
    def textbox_color_style(self):
        pass

    @abstractstaticmethod
    def textbox_color(self):
        pass

    @abstractstaticmethod
    def background_color_style(self):
        pass

    @abstractstaticmethod
    def background_color(self):
        pass

    @abstractstaticmethod
    def text_color_style(self):
        pass

    @abstractstaticmethod
    def text_color(self):
        pass
        
class DefaultTheme(Theme):
    @staticmethod
    def toolbar_color_style():
        return "color: rgb(218, 221, 226);"

    @staticmethod
    def toolbar_color():
        return QColor(218, 221, 226)

    @staticmethod
    def textbox_color_style():
        return "background-color: rgb(237, 242, 246);"

    @staticmethod
    def textbox_color():
        return QColor(237, 242, 246)

    @staticmethod
    def background_color_style():
        return "background-color: rgb(255, 255, 255);"

    @staticmethod
    def background_color():
        return QColor(255, 255, 255)

    @staticmethod
    def text_color_style():
        return "color: rgb(26, 25, 30);"

    @staticmethod
    def text_color():
        return QColor(26, 25, 30)

class DarkTheme(Theme):
    @staticmethod
    def toolbar_color_style():
        return "color: rgb(50, 50, 50);"

    @staticmethod
    def toolbar_color():
        return QColor(50, 50, 50)

    @staticmethod
    def textbox_color_style():
        return "background-color: rgb(30, 30, 30);"

    @staticmethod
    def textbox_color():
        return QColor(30, 30, 30)

    @staticmethod
    def background_color_style():
        return "background-color: rgb(37, 37, 38);"

    @staticmethod
    def background_color():
        return QColor(37, 37, 38)

    @staticmethod
    def text_color_style():
        return "color: rgb(228, 228, 228);"

    @staticmethod
    def text_color():
        return QColor(228, 228, 228)