import QThread as QThread


class NaverLoginThread(QThread):
    signal = pyqtSignal(str)

    def run(self):
        try:
            login_naver()
            self.signal.emit('Login successful')
        except Exception as e:
            self.signal.emit('Login failed')


class ExcelCreationThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self, blog_post_url):
        super().__init__()
        self.blog_post_url = blog_post_url

    def run(self):
        try:
            soup = get_comments(self.blog_post_url)
            comments = extract_comments(soup)
            save_to_excel(comments)
            self.signal.emit('Excel file created')
        except Exception as e:
            self.signal.emit('Excel creation failed')


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        login_button = QPushButton('네이버\n로그인')
        login_button.clicked.connect(self.naver_login)
        layout.addWidget(login_button)

        excel_button = QPushButton('엑셀\n생성')
        excel_button.clicked.connect(self.open_excel_dialog)
        layout.addWidget(excel_button)

        send_button = QPushButton('전자책\n발송')
        # Here you should add functionality for sending the ebook.
        layout.addWidget(send_button)

        self.show()

    def naver_login(self):
        self.thread = NaverLoginThread()
        self.thread.signal.connect(self.handle_signal)
        self.thread.start()

    def open_excel_dialog(self):
        self.dialog = ExcelDialog()
        self.dialog.show()

    def handle_signal(self, msg):
        # Here you should handle the signal (e.g., display a dialog or change a label text)
        pass


class ExcelDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)

        self.url_edit = QLineEdit()
        layout.addWidget(QLabel('Blog post URL:'), 0, 0)
        layout.addWidget(self.url_edit, 0, 1)

        create_button = QPushButton('엑셀 생성')
        create_button.clicked.connect(self.create_excel)
        layout.addWidget(create_button, 1, 0, 1, 2)

    def create_excel(self):
        blog_post_url = self.url_edit.text()
        self.thread = ExcelCreationThread(blog_post_url)
        self.thread.signal.connect(self.handle_signal)
        self.thread.start()

    def handle_signal(self, msg):
        # Here you should handle the signal (e.g., display a dialog or change a label text)
        pass


app = QApplication([])
window = MainWindow()
app.exec_()
