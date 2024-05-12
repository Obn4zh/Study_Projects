import sys
import LSB
import hashlib
import steg_on_hamming

from addit_functs import read_color, get_size, save_color, generate_alphanum_crypt_string

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QGraphicsScene
from PyQt6.QtGui import QPixmap
from main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.new_container_color = 0
        self.full_container_color = 0

        self.full_container_name = 0
        self.status = "hide"

        self.ui.exit.triggered.connect(QApplication.instance().quit)
        self.ui.open_new_container.triggered.connect(self.openNewcontainer)
        self.ui.open_full_container.triggered.connect(self.openFullcontainer)

        self.ui.button_hide_message.clicked.connect(self.hideMassageClicked)
        self.ui.button_extract_message.clicked.connect(self.extractMassageClicked)

        # self.ui.textEdit_password.setText(generate_alphanum_crypt_string(15)) #vU!%?b`U=Rbrc}V
        # self.ui.textEdit_m_start.setText(generate_alphanum_crypt_string(15)) #bRg/H}#O=2G=c>V
        # self.ui.textEdit_m_end.setText(generate_alphanum_crypt_string(15)) #Ld{p2:dUw$`+09#

        self.ui.textEdit_password.setText('vU!%?b`U=Rbrc}V')
        self.ui.textEdit_m_start.setText('bRg/H}#O=2G=c>V')
        self.ui.textEdit_m_end.setText('Ld{p2:dUw$`+09#')

    def hideMassageClicked(self):
        if self.new_container_color:
            self.ui.statusbar.showMessage("Начинаем процесс заполнения контейнера")
            key = self.ui.textEdit_password.toPlainText()
            text = self.ui.textEdit_message.toPlainText()
            print(self.ui.stego_reid.currentText())

            try:
                reid = float(self.ui.stego_reid.currentText())
                sdvig = int(self.ui.textEdit_sdvig.toPlainText())
                m_start = self.ui.textEdit_m_start.toPlainText().encode("utf-8")
                m_end = self.ui.textEdit_m_end.toPlainText().encode("utf-8")
                metod = self.ui.stego_metod.currentIndex()

                # text = AES_cript.encrypt(text, key)
                m_start = hashlib.sha256(m_start).hexdigest()
                m_end = hashlib.sha256(m_end).hexdigest()

                new_image = ""
                if metod == 0:
                    new_image = LSB.LSB_R_enc(self.new_container_color, text, m_start, m_end, sdvig, reid)
                elif metod == 1:
                    new_image = LSB.LSB_M_enc(self.new_container_color, text, m_start, m_end, sdvig, reid)
                elif metod == 2:
                    new_image = steg_on_hamming.SoH_enc(self.new_container_color, text, m_start, m_end, sdvig)

                name_file = QFileDialog.getSaveFileName(self, "Сохранить файл", "./"
                                                             , filter="Изображения (*.bmp)")[0]

                save_color(self.new_container_name, name_file, new_image, 'pixels')
                self.full_container_name = name_file
                self.openFullcontainer()

                self.ui.statusbar.showMessage("Сообщение скрыто")
            except Exception as err:
                print(err)
        else:
            self.ui.statusbar.showMessage("Ожидание открытия файла")


    def extractMassageClicked(self):
        if self.full_container_name:
            key = self.ui.textEdit_password.toPlainText()
            text = self.ui.textEdit_message.toPlainText()
            reid = float(self.ui.stego_reid.currentText())
            m_start = self.ui.textEdit_m_start.toPlainText().encode("utf-8")
            m_end = self.ui.textEdit_m_end.toPlainText().encode("utf-8")
            metod = self.ui.stego_metod.currentIndex()

            m_start = hashlib.sha256(m_start).hexdigest()
            m_end = hashlib.sha256(m_end).hexdigest()

            try:
                private_text = ""
                if metod == 0 or metod == 1:
                    private_text = LSB.LSB_dec(self.full_container_color, m_start, m_end, reid)
                elif metod == 2:
                    private_text = steg_on_hamming.SoH_dec(self.full_container_color, m_start, m_end)

                # text = AES_cript.decrypt(private_text, key)
                text = private_text
                self.ui.textEdit_message.setText(text)
                self.ui.statusbar.showMessage("Сообщение извлечено")
            except Exception as err:
                print(err)
                self.ui.statusbar.showMessage("Ошибка!!!")


        else:
            self.ui.statusbar.showMessage("Ожидание открытия файла")

        return 0

    def openNewcontainer(self):
        self.new_container_name = QFileDialog.getOpenFileName(self, "Открыть файл", "./"
                                                         , filter="Изображения (*.png *.jpg *.bmp)")[0]
        width, height = get_size(self.new_container_name)
        k = 0
        if width > height:
            k = width / 468
        else:
            k = height / 298
        new_width = round(width / k)
        new_height = round(height / k)

        self.new_container_color = read_color(self.new_container_name, 'pixels')

        self.scene_new_container = QGraphicsScene()
        pic = QGraphicsPixmapItem()
        pic.setPixmap(QPixmap(self.new_container_name).scaled(new_width, new_height))
        self.scene_new_container.addItem(pic)
        self.ui.original_image.setScene(self.scene_new_container)

        self.ui.statusbar.showMessage("Файл " + self.new_container_name + " открыт")

    def openFullcontainer(self):
        if self.full_container_name == 0:
            self.full_container_name = QFileDialog.getOpenFileName(self, "Открыть файл", "./"
                                                            , filter="Изображение без сжатия (*.bmp)")[0]
            self.status = "show"


        width, height = get_size(self.full_container_name)
        k = 0
        if width > height:
            k = width / 468
        else:
            k = height / 298
        new_width = round(width / k)
        new_height = round(height / k)

        self.full_container_color = read_color(self.full_container_name, 'pixels')

        self.scene_full_container = QGraphicsScene()
        pic = QGraphicsPixmapItem()
        pic.setPixmap(QPixmap(self.full_container_name).scaled(new_width, new_height))
        self.scene_full_container.addItem(pic)
        self.ui.stego_image.setScene(self.scene_full_container)

        if self.status == "show":
            self.ui.statusbar.showMessage("Файл " + self.full_container_name + " открыт")


def main():
    app = QApplication([])
    application = MainWindow()
    application.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
