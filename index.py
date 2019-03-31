# PyQt
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
	QApplication,
	QMainWindow,
	QFrame,
	QLabel,
	QComboBox, 
	QLineEdit,
	QPushButton,
    QMessageBox,
    QDialog
)
from PyQt5 import uic

# Authentication
from authentication import Authentication

# Sys
import sys


class ParsingCleaningWindow(QDialog):

    def __init__(self, parent=None):
        super(ParsingCleaningWindow, self).__init__(parent)
        self.setWindowTitle('Iptv File Cleaner | Limpiar o cambiar formato')
        self.setWindowIcon(QIcon("img/icon.png"))
        uic.loadUi('ui/parsing_cleaning.ui')


class WindowLogin(QMainWindow):
    """Manages the graphical representation of the login."""

    def __init__(self, parent=None):
        """Handles the initialization of the class"""

        super(WindowLogin, self).__init__(parent)
        
        self.setWindowTitle("Iptv File Cleaner | Iniciar Sesion")
        self.setWindowIcon(QIcon("img/icon.png"))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(400, 380)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(243, 243, 243))
        self.setPalette(palette)

        self.parsing_cleaning_window = ParsingCleaningWindow()
        self.initUI()

    def initUI(self):
        """Sets up the graphical interphace."""

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(51, 0, 102))

        frame = QFrame(self)
        frame.setFrameShape(QFrame.NoFrame)
        frame.setFrameShadow(QFrame.Sunken)
        frame.setAutoFillBackground(True)
        frame.setPalette(palette)
        frame.setFixedWidth(400)
        frame.setFixedHeight(84)
        frame.move(0, 0)

        iconLabel = QLabel(frame)
        iconLabel.setFixedWidth(40)
        iconLabel.setFixedHeight(40)
        iconLabel.setPixmap(QPixmap("img/icon.png").scaled(40, 40, Qt.KeepAspectRatio,
                                                         Qt.SmoothTransformation))
        iconLabel.move(37, 22)

        titleFont = QFont()
        titleFont.setPointSize(16)
        titleFont.setBold(True)

        titleLabel = QLabel("<font color='white'>Iptv File Cleaner.</font>", frame)
        titleLabel.setFont(titleFont)
        titleLabel.move(83, 20)

        subtitleFont = QFont()
        subtitleFont.setPointSize(9)

        subtitleLabel = QLabel("<font color='white'>Inicia sesion usuario premium."
                                "</font>", frame)
        subtitleLabel.setFont(subtitleFont)
        subtitleLabel.move(111, 46)


        userLabel = QLabel("Usuario", self)
        userLabel.move(60, 170)

        userFrame = QFrame(self)
        userFrame.setFrameShape(QFrame.StyledPanel)
        userFrame.setFixedWidth(280)
        userFrame.setFixedHeight(28)
        userFrame.move(60, 196)

        userImage = QLabel(userFrame)
        userImage.setPixmap(QPixmap("img/user.png").scaled(20, 20, Qt.KeepAspectRatio,
                                                              Qt.SmoothTransformation))
        userImage.move(10, 4)

        self.lineEditUser = QLineEdit(userFrame)
        self.lineEditUser.setFrame(False)
        self.lineEditUser.setTextMargins(8, 0, 4, 1)
        self.lineEditUser.setFixedWidth(238)
        self.lineEditUser.setFixedHeight(26)
        self.lineEditUser.move(40, 1)


        passwordLabel = QLabel("Contraseña", self)
        passwordLabel.move(60, 224)

        passwordFrame = QFrame(self)
        passwordFrame.setFrameShape(QFrame.StyledPanel)
        passwordFrame.setFixedWidth(280)
        passwordFrame.setFixedHeight(28)
        passwordFrame.move(60, 250)

        passwordImage = QLabel(passwordFrame)
        passwordImage.setPixmap(QPixmap("img/password.png").scaled(20, 20, Qt.KeepAspectRatio,
                                                                     Qt.SmoothTransformation))
        passwordImage.move(10, 4)

        self.lineEditPassword = QLineEdit(passwordFrame)
        self.lineEditPassword.setFrame(False)
        self.lineEditPassword.setEchoMode(QLineEdit.Password)
        self.lineEditPassword.setTextMargins(8, 0, 4, 1)
        self.lineEditPassword.setFixedWidth(238)
        self.lineEditPassword.setFixedHeight(26)
        self.lineEditPassword.move(40, 1)


        loginButton = QPushButton("Iniciar sesión", self)
        loginButton.setFixedWidth(135)
        loginButton.setFixedHeight(28)
        loginButton.move(60, 286)

        cancelButton = QPushButton("Cerrar", self)
        cancelButton.setFixedWidth(135)
        cancelButton.setFixedHeight(28)
        cancelButton.move(205, 286)

        infoLink = 'https://localhost:63342/index.html'

        informationLabel = QLabel(f"<a href='{infoLink}'>Comprar</a>.", self)
        informationLabel.setOpenExternalLinks(True)
        informationLabel.setToolTip("Create una cuenta y compra el programa")
        informationLabel.move(15, 344)


        loginButton.clicked.connect(self.login)
        cancelButton.clicked.connect(self.close)

    def login(self):
        """Verifies if the user is premium

        If is premium this will open the window containing the program logic.
        If is'nt premium will send an alert saying the user buy the program.
        """
        username = self.lineEditUser.text()
        password = self.lineEditPassword.text()
        authentication = Authentication()

        msgBox = QMessageBox()
        msgBox.setWindowTitle('Error al iniciar sesion.')

        
        if authentication.login(username, password):
            if authentication.is_user_premium(username):
                self.openParsingCleaningWindow()
            else:
                msgBox.setText('No eres un usuario premium, por favor compra la aplicacion')
                msgBox.exec_()

        else:
            msgBox.setText('Credenciales invalidas :(.')
            msgBox.exec_()


        self.lineEditUser.clear()
        self.lineEditPassword.clear()

    def openParsingCleaningWindow(self):
        """Handles opening the window that contains all the logic of parsing and cleaning lists."""

        self.close()
        self.parsing_cleaning_window.exec_()


if __name__ == '__main__':

    application = QApplication(sys.argv)
    font = QFont()
    font.setPointSize(10)
    font.setFamily("Bahnschrift Light")

    application.setFont(font)
    
    window = WindowLogin()
    window.show()

sys.exit(application.exec_())
