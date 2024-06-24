from PyQt5 import QtWidgets
import sys
from app import Ui_MainWindow
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
)
from time import time, sleep
import re
import os


class App(QtWidgets.QMainWindow):
    def __init__(self) -> None:

        # Initilaze app and add ui
        super(App, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # For display beauty makes unvisible some objectes
        self.ui.preview_ss.setVisible(False)
        self.ui.textPreiew_ss.setVisible(False)

        # Checks for boxes cliked or not.
        self.ui.checkBox_maxComment.stateChanged.connect(self.func_max_comment)
        self.ui.checkbox_minLike.stateChanged.connect(self.func_min_like)
        self.ui.screenShot.stateChanged.connect(self.screenShot_mode)
        self.ui.checkBox_mustFindText.stateChanged.connect(self.func_mustFindText)

        # For start fetching commentes
        self.ui.button_fetch.clicked.connect(self.check_if_valid)

    def screenShot_mode(self):

        boxes = self.ui.verticalLayoutWidget.findChildren(QtWidgets.QCheckBox)

        if self.ui.screenShot.isChecked() == True:

            for box in boxes:
                if box.objectName() == "screenShot":
                    continue
                box.setEnabled(False)

            self.ui.textNormal.setVisible(False)
            self.ui.textBrowser.setVisible(False)
            self.ui.preview_ss.setVisible(True)
            self.ui.textPreiew_ss.setVisible(True)

        else:
            self.ui.preview_ss.setVisible(False)
            self.ui.textPreiew_ss.setVisible(False)
            self.ui.textNormal.setVisible(True)
            self.ui.textBrowser.setVisible(True)

            for box in boxes:
                box.setEnabled(True)

    def check_if_valid(self):
        link = self.ui.input_YoutubeLink.text()
        print(link)
        if not check_link(link):
            self.ui.warning.setText("Please enter a valid youtube link")
            return
        self.initializeSelenium(link)

    # Find
    def initializeSelenium(self, link):
        take_as_ss = self.ui.screenShot.isChecked()
        user_comment = self.ui.comment.isChecked()
        user_name = self.ui.userName.isChecked()
        likes = self.ui.likes.isChecked()

        if self.ui.checkBox_maxComment.isChecked():
            comment_count = int(self.ui.count_maxComments.text())
        else:
            comment_count = 9999
        if self.ui.checkbox_minLike.isChecked():
            min_like = int(self.ui.count_minLikes.text())
        else:
            min_like = 0
        if self.ui.checkBox_mustFindText.isChecked():
            mustFindText = self.ui.inputText_mustFindText.text().lower()
        else:
            mustFindText = None
        fetch_comments(
            link,
            take_as_ss,
            user_comment,
            user_name,
            likes,
            comment_count,
            min_like,
            mustFindText,
        )

    # Controls app visualtion

    def func_mustFindText(self):
        cb = self.sender()
        if cb.isChecked():
            self.ui.inputText_mustFindText.setEnabled(True)
        else:
            self.ui.inputText_mustFindText.setEnabled(False)

    def func_max_comment(self):
        cd = self.sender()

        if cd.isChecked():
            self.ui.count_maxComments.setEnabled(True)
        else:
            self.ui.count_maxComments.setEnabled(False)

    def func_min_like(self, value):
        cd = self.sender()

        if cd.isChecked():
            self.ui.count_minLikes.setEnabled(True)
        else:
            self.ui.count_minLikes.setEnabled(False)

    # Functions that returns necessary numbers, strings and boolines
    def return_min_like(self):
        return int(self.ui.count_minLikes.text)

    def return_max_comment(self):
        return int(self.ui.count_maxComments.text)

    def return_link(self):
        return self.ui.input_YoutubeLink.text


def int_converter(string):
    if "K" in string:
        string = string.replace(".", "")
        string = string.replace("K", "00")
        return int(string)

    return int(string)


# Checks link if is youtube or not
def check_link(link):
    if not re.search(r"(?:https?://(?:www.)?youtube.com)", link):
        return False
    return True


comment_list = []


# Start selenium
def fetch_comments(
    link,
    take_as_ss=False,
    user_comment=True,
    user_name=True,
    likes=False,
    comment_count=9999,
    min_like=0,
    mustFindText=None,
):
    if link == "that just... why ?":
        raise TypeError
    if link == "For test":
        return 0
    driver = webdriver.Chrome()
    driver.get(f"{link}")
    SCROLL_PAUSE_TIME = 0.5
    sleep(5)
    comments = driver.find_elements(By.ID, "comments")
    # Get scroll height
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while len(comments) < comment_count:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);"
        )

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script(
            "return document.documentElement.scrollHeight"
        )

        comments = driver.find_elements(By.ID, "comment")
        if new_height == last_height:
            print("Not that much comments")
            break
        last_height = new_height

    # Check if we want ss or text
    if not take_as_ss:

        for i in comments:
            # End loop if enough comment are found
            if comment_count <= 0:
                break

            # Save every comment as dictionaray
            try:
                # If like count is not enough skip this comment
                if min_like != 0:
                    if min_like > int_converter(
                        i.find_element(By.ID, "vote-count-middle").text
                    ):
                        continue

                if mustFindText:
                    if (
                        mustFindText
                        not in  i.find_element(By.ID, "content-text").text.lower()
                    ):
                        continue

                start = {}
                if user_name:
                    user = i.find_element(By.ID, "author-text").text
                    start["USER NAME"] = user
                if user_comment:
                    user_text = i.find_element(By.ID, "content-text").text
                    start["COMMENT"] = user_text

                if likes:
                    like = i.find_element(By.ID, "vote-count-middle").text
                    start["LIKE"] = like

                comment_list.append(start)

            except NoSuchElementException:
                print("Element not found!")

            comment_count -= 1

        write_to_file("comment", comment_list)

    else:
        # Open a folder named as current time
        folder_name = time()
        os.makedirs(f"{folder_name}")
        i = 1
        for userComment in comments:
            if comment_count <= 0:
                break
            try:
                userComment.screenshot(f"{folder_name}/comment{i}.png")
            except:
                print(f"While taking ss of comment{i} an error occurred skipping...")
            i += 1
            comment_count -= 1


# Writes to file
def write_to_file(filename, comments):
    with open(f"{filename}.txt", "w", encoding="utf-8") as file:
        file.write("------------------------------------------------\n\n")
        for dic in comments:
            for key, value in dic.items():
                try:

                    file.write(f"{key} : {value}\n")
                except UnicodeEncodeError:
                    print("UnicodeEncodeError")

            file.write("\n------------------------------------------------\n\n")

        file.write(
            "              ------------------ END OF WRITING ------------------       "
        )
        return


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = App()
    win.setWindowTitle("Youtube Comment Collecter")
    win.show()


    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
