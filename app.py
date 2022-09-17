# -*- coding: utf-8 -*-
import os
import platform
import shutil
import qrcode
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets

qr_constructor = qrcode.QRCode(
    version=10,
    box_size=12,
    border=3,
    error_correction=qrcode.constants.ERROR_CORRECT_H
)

class Ui_MainWindow(object):
    color = ''
    icon = ''
    qr_code = ''

    def link_changed(self):
        qr_constructor.clear()
        qr_constructor.add_data(self.txt_link.text())
        qr_constructor.make()

        if self.color == '':
            qr_image = qr_constructor.make_image(
                fill_color='black', back_color='white').convert('RGBA')
        else:
            qr_image = qr_constructor.make_image(
                fill_color=self.color, back_color='white').convert('RGBA')

        if self.icon != '':
            logo = Image.open(self.icon).convert('RGBA').resize((256, 256))

            pos = ((qr_image.size[0] - logo.size[0]) // 2,
                   (qr_image.size[1] - logo.size[1]) // 2)

            qr_image.paste(logo, pos, logo)

        path = os.path.expanduser('~') + '/.cache/codetalker/'
        
        if not os.path.exists(path):
            os.makedirs(path)

        if platform.system() == 'Windows':
            path.replace('/', '\\')

        self.qr_code = qr_image.save(path + 'temp_code.png')

        image = QtGui.QPixmap(path + 'temp_code.png')
        self.img_box.setPixmap(image)

    def icon_clicked(self):
        dialog = QtWidgets.QFileDialog()
        choose_icon = dialog.getOpenFileName(
            dialog, 'Selecionar imagem', os.path.expanduser('~'), 'Arquivos de imagem (*.png)')

        self.icon = choose_icon[0]

        self.link_changed()

    def color_clicked(self):
        self.color = QtWidgets.QColorDialog.getColor().getRgb()

        self.link_changed()

    def clear_clicked(self):
        self.icon = ''
        self.color = ''

        self.link_changed()

    def save_clicked(self):
        path = os.path.expanduser('~') + '/Downloads'
        tmp_path = os.path.expanduser('~') + '/.cache/codetalker/temp_code.png'

        if platform.system() == 'Windows':
            path.replace('/', '\\')
            tmp_path.replace('/', '\\')

        dialog = QtWidgets.QFileDialog()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            dialog, "Salvar arquivo", path, "Arquivos de Imagem (*.png)")

        if not filename.endswith('.png'):
            filename += '.png'

        shutil.copy(tmp_path, filename)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(787, 302)
        MainWindow.setWindowTitle("CODE TALKER - CRIADOR DE QR CODES")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_color = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_color.sizePolicy().hasHeightForWidth())
        self.btn_color.setSizePolicy(sizePolicy)
        self.btn_color.setText("CLIQUE PARA ESCOLHER UMA COR")
        self.btn_color.setObjectName("btn_color")
        self.gridLayout.addWidget(self.btn_color, 6, 0, 1, 1)
        self.img_box = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.img_box.sizePolicy().hasHeightForWidth())
        self.img_box.setSizePolicy(sizePolicy)
        self.img_box.setMinimumSize(QtCore.QSize(250, 250))
        self.img_box.setMaximumSize(QtCore.QSize(250, 250))
        self.img_box.setFrameShape(QtWidgets.QFrame.Box)
        self.img_box.setText("")
        self.img_box.setScaledContents(True)
        self.img_box.setObjectName("img_box")
        self.gridLayout.addWidget(self.img_box, 0, 1, 8, 1)
        self.txt_link = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(False)
        self.txt_link.setFont(font)
        self.txt_link.setText("")
        self.txt_link.setPlaceholderText("Insira o link aqui")
        self.txt_link.setObjectName("txt_link")
        self.gridLayout.addWidget(self.txt_link, 4, 0, 1, 1)
        self.btn_save = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_save.sizePolicy().hasHeightForWidth())
        self.btn_save.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.btn_save.setFont(font)
        self.btn_save.setText("SALVAR QR CODE")
        self.btn_save.setObjectName("btn_save")
        self.gridLayout.addWidget(self.btn_save, 7, 0, 2, 1)
        self.btn_clear = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setItalic(True)
        self.btn_clear.setFont(font)
        self.btn_clear.setText("LIMPAR QR CODE")
        self.btn_clear.setObjectName("btn_clear")
        self.gridLayout.addWidget(self.btn_clear, 8, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setText("CODE TALKER")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 2, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setText("Criador de QR Codes")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.btn_icon = QtWidgets.QPushButton(self.centralwidget)
        self.btn_icon.setText("CLIQUE PARA ESCOLHER UM ÍCONE")
        self.btn_icon.setObjectName("btn_icon")
        self.gridLayout.addWidget(self.btn_icon, 5, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.txt_link.textChanged.connect(self.link_changed)
        self.btn_icon.clicked.connect(self.icon_clicked)
        self.btn_color.clicked.connect(self.color_clicked)
        self.btn_clear.clicked.connect(self.clear_clicked)
        self.btn_save.clicked.connect(self.save_clicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
