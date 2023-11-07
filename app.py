import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import json

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyBrowser - от ГЕРЫЧА")
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.showMaximized()

        self.browser.setUrl(QUrl("https://www.google.com"))

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        home_button = QAction("Хата", self)
        home_button.triggered.connect(self.go_home)
        toolbar.addAction(home_button)

        back_button = QAction("Зад", self)
        back_button.triggered.connect(self.browser.back)
        toolbar.addAction(back_button)

        forward_button = QAction("Перед", self)
        forward_button.triggered.connect(self.browser.forward)
        toolbar.addAction(forward_button)

        reload_button = QAction("Шиндовс 0x0001", self)
        reload_button.triggered.connect(self.browser.reload)
        toolbar.addAction(reload_button)

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

        # Load bookmarks from file
        self.bookmarks = self.load_bookmarks()

        # Set program icon
        icon = QIcon("icon.ico")
        self.setWindowIcon(icon)

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

    def save_bookmarks(self):
        with open("bookmarks.json", "w") as f:
            json.dump(self.bookmarks, f)

    def load_bookmarks(self):
        try:
            with open("bookmarks.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def load_bookmark(self):
        bookmark_name, ok = QInputDialog.getItem(self, "Загрузить закладку", "Выберите закладку:", list(self.bookmarks.keys()), editable=False)
        if ok and bookmark_name:
            url = self.bookmarks.get(bookmark_name)
            if url:
                self.browser.setUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    sys.exit(app.exec_())
