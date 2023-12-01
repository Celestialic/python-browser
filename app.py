import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import json

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Браузер")
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Set minimum size for the window
        self.setMinimumSize(QSize(700, 500))

        self.browser.setUrl(QUrl("https://www.google.com"))

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        home_button = QAction("Домой", self)
        home_button.triggered.connect(self.go_home)
        toolbar.addAction(home_button)

        back_button = QAction("Назад", self)
        back_button.triggered.connect(self.browser.back)
        toolbar.addAction(back_button)

        forward_button = QAction("Вперёд", self)
        forward_button.triggered.connect(self.browser.forward)
        toolbar.addAction(forward_button)

        reload_button = QAction("Перезагрузить", self)
        reload_button.triggered.connect(self.browser.reload)
        toolbar.addAction(reload_button)

        # Add an address bar
        self.address_bar = QLineEdit(self)
        self.address_bar.returnPressed.connect(self.load_url)
        toolbar.addWidget(self.address_bar)

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Меню")

        author_action = QAction("Автор", self)
        author_action.triggered.connect(self.go_to_author_channel)
        file_menu.addAction(author_action)

        update_action = QAction("Обнова или дегродация браузера", self)
        update_action.triggered.connect(self.download_browser_update)
        file_menu.addAction(update_action)

        # Add Bookmarks menu option
        bookmarks_menu = file_menu.addMenu("Закладки")
        add_bookmark_action = QAction("Добавить закладку", self)
        add_bookmark_action.triggered.connect(self.add_bookmark)
        bookmarks_menu.addAction(add_bookmark_action)

        # Add Load Bookmark menu option
        load_bookmark_action = QAction("Загрузить закладку", self)
        load_bookmark_action.triggered.connect(self.load_bookmark)
        bookmarks_menu.addAction(load_bookmark_action)

        # Add Delete Bookmark menu option
        delete_bookmark_action = QAction("Удалить закладку", self)
        delete_bookmark_action.triggered.connect(self.delete_bookmark)
        bookmarks_menu.addAction(delete_bookmark_action)

        # Add History menu option
        history_menu = file_menu.addMenu("История")
        view_history_action = QAction("Просмотреть историю", self)
        view_history_action.triggered.connect(self.view_history)
        history_menu.addAction(view_history_action)

        # Add Clear History option in the History menu
        clear_history_action = QAction("Очистить историю", self)
        clear_history_action.triggered.connect(self.clear_history)
        history_menu.addAction(clear_history_action)

        # Load bookmarks and history from file
        self.bookmarks = self.load_bookmarks()
        self.history = self.load_history()

        # Set program icon
        icon = QIcon("icon.ico")
        self.setWindowIcon(icon)

        # Connect a slot to update history on page load
        self.browser.urlChanged.connect(self.update_history)

    def update_history(self, q):
        current_url = self.browser.url().toString()
        if current_url not in self.history:
            self.history.append(current_url)
            self.save_history()

    def view_history(self):
        history_text = "\n".join(self.history)
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle("История")
        history_dialog.setGeometry(100, 100, 400, 300)

        text_browser = QTextBrowser(history_dialog)
        text_browser.setGeometry(10, 10, 380, 280)
        text_browser.setPlainText(history_text)
        text_browser.setOpenExternalLinks(True)

        history_dialog.exec_()

    def go_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def go_to_author_channel(self):
        self.browser.setUrl(QUrl("https://www.youtube.com/channel/UCwq4NzfKXrvOPz5IhhHqFWw/"))

    def download_browser_update(self):
        self.browser.setUrl(QUrl("https://drive.google.com/drive/folders/1XDv0rDyJkS1uOKY1Uud1H8TlLO2kZN3N"))

    def add_bookmark(self):
        current_url = self.browser.url().toString()
        bookmark_name, ok = QInputDialog.getText(self, "Добавить закладку", "Введите имя закладки:")
        if ok and bookmark_name:
            self.bookmarks[bookmark_name] = current_url
            self.save_bookmarks()

    def delete_bookmark(self):
        bookmark_name, ok = QInputDialog.getItem(self, "Удалить закладку", "Выберите закладку:", list(self.bookmarks.keys()), editable=False)
        if ok and bookmark_name:
            del self.bookmarks[bookmark_name]
            self.save_bookmarks()

    def clear_history(self):
        self.history = []
        self.save_history()
        QMessageBox.information(self, "История очищена", "История успешно очищена.")

    def save_bookmarks(self):
        with open("bookmarks.json", "w") as f:
            json.dump(self.bookmarks, f)

    def load_bookmarks(self):
        try:
            with open("bookmarks.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_history(self):
        with open("history.json", "w") as f:
            json.dump(self.history, f)

    def load_history(self):
        try:
            with open("history.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def load_bookmark(self):
        bookmark_name, ok = QInputDialog.getItem(self, "Загрузить закладку", "Выберите закладку:", list(self.bookmarks.keys()), editable=False)
        if ok and bookmark_name:
            url = self.bookmarks.get(bookmark_name)
            if url:
                self.browser.setUrl(QUrl(url))

    def load_url(self):
        url = self.address_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    sys.exit(app.exec_())
