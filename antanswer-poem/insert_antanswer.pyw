import sys
import _anwfunction.read_antanswer as readOpt
from PyQt5.QtWidgets import *

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("anw Selector 0.1a")

        self.pushButton = QPushButton("실행할 파일 선택")
        self.pushButton.clicked.connect(self.pushButtonClicked)

        self.acceptButton = QPushButton("확인")
        self.acceptButton.clicked.connect(self.fnameAccept)
        self.label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.pushButton)
        layout.addWidget(self.label)
        layout.addWidget(self.acceptButton)

        self.setLayout(layout)

    def pushButtonClicked(self):
        self.fname = QFileDialog.getOpenFileName(caption='Open File', directory='answer_data_pack\\', filter='텍스트 파일 (*.txt);;antanswer 파일 (*.anw);;atanswer Crypted 파일 (*.awt)')
        self.label.setText(self.fname[0])

    def fnameAccept(self):
        with open("anwOpt.json", "r", encoding='utf-8-sig') as f:
            print(f)
            self.imsiOpt = readOpt.readOpt(f)
        print(self.imsiOpt)
        with open("anwOpt.json", "w", encoding="utf-8-sig") as f:
            readOpt.writePathOpt(f, self.imsiOpt, self.fname[0])


        quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()