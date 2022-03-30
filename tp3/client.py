from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt5.Qt import QUrl, QDesktopServices
import requests
import sys
import webbrowser



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()



    def initUI(self):
        self.setWindowTitle("Client")
        self.setFixedSize(400, 400)
        self.label1 = QLabel("Enter your hostname:", self)
        self.label1.move(10, 0)
        self.text1 = QLineEdit(self)
        self.text1.move(10, 30)

        self.label5 = QLabel("Enter your api_key:", self)
        self.label5.move(10, 60)
        self.text2 = QLineEdit(self)
        self.text2.move(10, 90)
        self.label3 = QLabel("Enter your IP:", self)
        self.label3.move(10, 120)
        self.text3 = QLineEdit(self)
        self.text3.move(10, 150)

        self.label2 = QLabel("Answer:", self)
        self.label2.move(10, 180)
        self.button = QPushButton("Send", self)
        self.button.move(10, 210)

        self.button.clicked.connect(self.on_click)
        self.button.pressed.connect(self.on_click)

        self.show()

    def on_click(self):
        hostname = self.text1.text()
        api_key = self.text2.text()
        ip = self.text3.text()
        if (hostname == "") or (api_key=="") or (ip == ""):
            QMessageBox.about(self, "Error", "Please fill the field")
        else:
            res = self.__query(hostname, api_key, ip)
            if res:
                self.label2.setText("Answer%s" % (res["latitude"]))
                self.label2.adjustSize()
                self.show()
                url2 = "https://www.openstreetmap.org/?mlat=%s&mlon=%s#map=12" %(res["latitude"],res["longitude"])
                #requests.get(url2)
                webbrowser.open(url2)
    def __query(self, hostname, api_key, ip):
        #print(type(hostname))
        #print(type(api_key))
        #print(type(ip))
        url = "http://%s/ip/%s?key=%s" %(hostname, ip, api_key)
        r = requests.get(url)
        if r.status_code == requests.codes.NOT_FOUND:
            QMessageBox.about(self, "Error", "IP not found")
        if r.status_code == requests.codes.OK:
            
            return r.json()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()