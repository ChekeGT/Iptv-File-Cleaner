"""Manages all the graphicals represntations."""

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
    QDialog,
    QCheckBox,
    QFileDialog
)

# Authentication
from authentication import Authentication

# Sys
import sys

# Cleaners
from cleaners import M3UFileCleaner

# Readers
from readers import M3UFileReader

# Utilities
from utilites import ParseAndWriteM3UToSimpleText


class ParsingCleaningWindow(QDialog):
    """Manages the graphical representation of changing iptv lists."""

    def __init__(self, parent=None):
        """Handles initialization of the class."""
        super(ParsingCleaningWindow, self).__init__(parent)

        self.setWindowTitle('Iptv File Cleaner | Limpiar o cambiar formato')
        self.setWindowIcon(QIcon("img/icon.png"))

        self.setFixedSize(450, 450)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)

        self.patterns = [
        ]

        self.input_file = None
        self.output_file = None

        self.initUi()

    def initUi(self):
        """Handles the initialization of all the graphical interphace"""

        # Headers

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(51, 0, 102))

        frame = QFrame(self)
        frame.setFrameShape(QFrame.NoFrame)
        frame.setFrameShadow(QFrame.Sunken)
        frame.setAutoFillBackground(True)
        frame.setPalette(palette)
        frame.setFixedWidth(450)
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

        subtitleLabel = QLabel("<font color='white'>Limpia o cambia de formato tu lista de iptv."
                                "</font>", frame)
        subtitleLabel.setFont(subtitleFont)
        subtitleLabel.move(111, 46)
        
        # Input File

        # Label

        inputFileLabel = QLabel("Selecciona tu lista:", self)
        inputFileLabel.move(40, 95)

        # Button

        inputFileSelectorButton = QPushButton("Seleccionar Archivo:", self)
        inputFileSelectorButton.setFixedWidth(170)
        inputFileSelectorButton.setFixedHeight(30)
        inputFileSelectorButton.move(180, 90)

        # Patterns

        # Common Patterns

        # Series

        deleteSeriesLabel = QLabel("Eliminar Series?", self)
        deleteSeriesLabel.move(60, 150)

        self.deleteSeries = QCheckBox(self)
        self.deleteSeries.move(40, 150)

        # Movies

        deleteMoviesLabel = QLabel("Eliminar Peliculas?", self)
        deleteMoviesLabel.move(60, 170)

        self.deleteMovies = QCheckBox(self)
        self.deleteMovies.move(40, 170)

        # Custom patterns

        patternsLabel = QLabel("Introduce un patron, y da ok para agregarlo a la lista.", self)
        patternsLabel.move(40, 210)

        patternsFrame = QFrame(self)
        patternsFrame.setFrameShape(QFrame.StyledPanel)
        patternsFrame.setFixedWidth(280)
        patternsFrame.setFixedHeight(28)
        patternsFrame.move(40, 236)

        self.patternLineEdit = QLineEdit(patternsFrame)
        self.patternLineEdit.setFrame(False)
        self.patternLineEdit.setTextMargins(8, 0, 4, 1)
        self.patternLineEdit.setFixedWidth(238)
        self.patternLineEdit.setFixedHeight(26)
        self.patternLineEdit.move(40, 1)

        # Image
        patternsImage = QLabel(patternsFrame)
        patternsImage.setPixmap(QPixmap("img/book.jpg").scaled(
                30,
                30, 
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )
        patternsImage.move(10, 4)

        # Confirm pattern button

        confirmPatternButton = QPushButton("Ok", self)
        confirmPatternButton.setFixedWidth(50)
        confirmPatternButton.setFixedHeight(30)
        confirmPatternButton.move(330, 240)

        # Decoder Type

        decoderTypeLabel = QLabel("Tipo de decodificador", self)
        decoderTypeLabel.move(40, 290)

        self.decoderType = QComboBox(self)
        self.decoderType.addItems(["OpenBox", "Freesat | GT Media"])
        self.decoderType.setCurrentIndex(-1)
        self.decoderType.setFixedWidth(280)
        self.decoderType.setFixedHeight(26)
        self.decoderType.move(40, 306)

        # Output File

        # Label

        outputFileLabel = QLabel("Archivo de Salida:", self)
        outputFileLabel.move(40, 360)

        # Button

        outputFileSelectorButton = QPushButton("Seleccionar Archivo:", self)
        outputFileSelectorButton.setFixedWidth(170)
        outputFileSelectorButton.setFixedHeight(30)
        outputFileSelectorButton.move(180, 355)

        # Change list button

        changeIptvListButton = QPushButton("Limpiar y/o cambiar lista.", self)
        changeIptvListButton.setFixedWidth(300)
        changeIptvListButton.setFixedHeight(30)
        changeIptvListButton.move(70, 415)

        # Buttons Signals

        confirmPatternButton.clicked.connect(self.add_pattern)
        changeIptvListButton.clicked.connect(self.changeIptvList)
        inputFileSelectorButton.clicked.connect(self.get_input_file)
        outputFileSelectorButton.clicked.connect(self.get_output_file)

    def add_pattern(self):
        """Handles adding patterns to the patterns list."""

        pattern = self.patternLineEdit.text()
        self.patterns.append(pattern)

        self.patternLineEdit.clear()

    def get_input_file(self):
        """Manages getting the input file."""

        try:
            filename, file_type = QFileDialog.getOpenFileName(self)
            
            file = open(filename, 'r+', encoding='utf-8')

            self.input_file = file

        except Exception as e:
            pass

    def get_output_file(self):
        """Manages getting the input file."""

        try:
            filename, file_type = QFileDialog.getOpenFileName(self)
            
            file = open(filename, 'w', encoding='utf-8')

            self.output_file = file

        except Exception as e:
            pass

    def changeIptvList(self):
        """Handles the parsing or/and cleaning of an IptvList"""

        try:

            input_file = self.input_file
            output_file = self.output_file
            msgBox = QMessageBox()

            if input_file and output_file:

                patterns = self.patterns

                if self.deleteMovies.isChecked():
                    patterns += [
                        'movie',
                        'movies',
                        'peliculas',
                        'pelicula'
                    ]

                if self.deleteSeries.isChecked():
                    patterns += [
                        'serie',
                        'series'
                    ]

                decoder_type = self.decoderType.currentText()
                if decoder_type:

                    if len(patterns) >= 1:

                        cleaner = M3UFileCleaner(patterns)
                        cleaned_lines = cleaner.delete_unneeded_lines(input_file)

                        segment_list = M3UFileReader.cut_lines(cleaned_lines)

                    else:
                        segment_list, length = M3UFileReader.read(input_file)
                    
                    ParseAndWriteM3UToSimpleText(output_file, decoder_type, segment_list)

                    msgBox.setWindowTitle('Lineas borradas y cambiadas exitosamente.')
                    msgBox.setText('Todas las lineas han sido cambiadas de formato y limpiadas para adaptarse a tu deco ;).')
                else:
                    msgBox.setWindowTitle('Error')
                    msgBox.setText('Necesitas poner un decodificador al cual pasar el archivo.')
            else:
                msgBox.setWindowTitle('Error')
                msgBox.setText('No has seleccionado ningun archivo, seleccionalos porfavor.')

            msgBox.exec_()

        except Exception as e:
            msgbox = QMessageBox()
            msgbox.setWindowTitle('Ha ocurrido un error con tu lista.')
            text = 'De momento nuestro programa no soporta tu lista de iptv para limpiarla,pero puedes mandarnos un correo a nextpcreloaded@hotmail.com y crearemos esa funcionalidad(tambien mandanos la lista), por tu comprension gracias ;).'
            msgbox.setText(text)
            msgbox.exec_()
            self.cleanFields()

        finally:
            self.cleanFields()

    def cleanFields(self):
        self.input_file = None
        self.output_file = None
        self.patterns = []
        self.decoderType.setCurrentIndex(-1)


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

        # Headers
        
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

        # User 

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

        # Password
        
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

        # Buttons

        loginButton = QPushButton("Iniciar sesión", self)
        loginButton.setFixedWidth(135)
        loginButton.setFixedHeight(28)
        loginButton.move(60, 286)

        cancelButton = QPushButton("Cerrar", self)
        cancelButton.setFixedWidth(135)
        cancelButton.setFixedHeight(28)
        cancelButton.move(205, 286)

        # Information

        infoLink = 'https://localhost:63342/index.html'

        informationLabel = QLabel(f"<a href='{infoLink}'>Comprar</a>.", self)
        informationLabel.setOpenExternalLinks(True)
        informationLabel.setToolTip("Create una cuenta y compra el programa")
        informationLabel.move(15, 344)

        # Buttons Signals

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
        self.parsing_cleaning_window.show()


if __name__ == '__main__':

    application = QApplication(sys.argv)
    font = QFont()
    font.setPointSize(10)
    font.setFamily("Bahnschrift Light")

    application.setFont(font)
    
    window = WindowLogin()
    window.show()

sys.exit(application.exec_())
