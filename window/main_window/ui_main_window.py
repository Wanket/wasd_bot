# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialogButtonBox,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QSplitter,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.start_tab = QWidget()
        self.start_tab.setObjectName(u"start_tab")
        self.verticalLayout_6 = QVBoxLayout(self.start_tab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.token_line_edit = QLineEdit(self.start_tab)
        self.token_line_edit.setObjectName(u"token_line_edit")
        self.token_line_edit.setEchoMode(QLineEdit.Password)

        self.horizontalLayout.addWidget(self.token_line_edit)

        self.channel_line_edit = QLineEdit(self.start_tab)
        self.channel_line_edit.setObjectName(u"channel_line_edit")
        self.channel_line_edit.setMaximumSize(QSize(130, 16777215))

        self.horizontalLayout.addWidget(self.channel_line_edit)

        self.start_push_button = QPushButton(self.start_tab)
        self.start_push_button.setObjectName(u"start_push_button")

        self.horizontalLayout.addWidget(self.start_push_button)


        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.splitter = QSplitter(self.start_tab)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.commands_list_widget = QListWidget(self.layoutWidget)
        self.commands_list_widget.setObjectName(u"commands_list_widget")
        self.commands_list_widget.setSortingEnabled(True)

        self.verticalLayout_2.addWidget(self.commands_list_widget)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.add_command_button = QPushButton(self.layoutWidget)
        self.add_command_button.setObjectName(u"add_command_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.add_command_button.sizePolicy().hasHeightForWidth())
        self.add_command_button.setSizePolicy(sizePolicy1)
        self.add_command_button.setMaximumSize(QSize(26, 16777215))

        self.horizontalLayout_4.addWidget(self.add_command_button)

        self.remove_command_button = QPushButton(self.layoutWidget)
        self.remove_command_button.setObjectName(u"remove_command_button")
        sizePolicy1.setHeightForWidth(self.remove_command_button.sizePolicy().hasHeightForWidth())
        self.remove_command_button.setSizePolicy(sizePolicy1)
        self.remove_command_button.setMaximumSize(QSize(26, 16777215))

        self.horizontalLayout_4.addWidget(self.remove_command_button)

        self.horizontalSpacer_3 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.verticalLayout_5 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_5.addWidget(self.label_2)

        self.answers_list_widget = QListWidget(self.layoutWidget1)
        self.answers_list_widget.setObjectName(u"answers_list_widget")
        self.answers_list_widget.setSortingEnabled(True)

        self.verticalLayout_5.addWidget(self.answers_list_widget)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_6 = QLabel(self.layoutWidget1)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_5.addWidget(self.label_6)

        self.horizontalSpacer_4 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.timeout_spin_box = QSpinBox(self.layoutWidget1)
        self.timeout_spin_box.setObjectName(u"timeout_spin_box")
        self.timeout_spin_box.setMaximum(999)

        self.horizontalLayout_5.addWidget(self.timeout_spin_box)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.add_answer_button = QPushButton(self.layoutWidget1)
        self.add_answer_button.setObjectName(u"add_answer_button")
        sizePolicy1.setHeightForWidth(self.add_answer_button.sizePolicy().hasHeightForWidth())
        self.add_answer_button.setSizePolicy(sizePolicy1)
        self.add_answer_button.setMaximumSize(QSize(26, 16777215))

        self.horizontalLayout_6.addWidget(self.add_answer_button)

        self.remove_answer_button = QPushButton(self.layoutWidget1)
        self.remove_answer_button.setObjectName(u"remove_answer_button")
        sizePolicy1.setHeightForWidth(self.remove_answer_button.sizePolicy().hasHeightForWidth())
        self.remove_answer_button.setSizePolicy(sizePolicy1)
        self.remove_answer_button.setMaximumSize(QSize(26, 16777215))

        self.horizontalLayout_6.addWidget(self.remove_answer_button)

        self.horizontalSpacer_5 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.splitter.addWidget(self.layoutWidget1)
        self.layoutWidget2 = QWidget(self.splitter)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.layoutWidget2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_4.addWidget(self.label_3)

        self.answer_text_edit = QPlainTextEdit(self.layoutWidget2)
        self.answer_text_edit.setObjectName(u"answer_text_edit")

        self.verticalLayout_4.addWidget(self.answer_text_edit)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.layoutWidget2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.horizontalSpacer_2 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.rate_spin_box = QSpinBox(self.layoutWidget2)
        self.rate_spin_box.setObjectName(u"rate_spin_box")
        self.rate_spin_box.setMinimum(1)

        self.horizontalLayout_3.addWidget(self.rate_spin_box)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.ban_check_box = QCheckBox(self.layoutWidget2)
        self.ban_check_box.setObjectName(u"ban_check_box")

        self.verticalLayout_4.addWidget(self.ban_check_box)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(self.layoutWidget2)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)

        self.sticker_line_edit = QLineEdit(self.layoutWidget2)
        self.sticker_line_edit.setObjectName(u"sticker_line_edit")

        self.horizontalLayout_7.addWidget(self.sticker_line_edit)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.apply_button_box = QDialogButtonBox(self.layoutWidget2)
        self.apply_button_box.setObjectName(u"apply_button_box")
        sizePolicy1.setHeightForWidth(self.apply_button_box.sizePolicy().hasHeightForWidth())
        self.apply_button_box.setSizePolicy(sizePolicy1)
        self.apply_button_box.setStandardButtons(QDialogButtonBox.Reset|QDialogButtonBox.Save)

        self.horizontalLayout_2.addWidget(self.apply_button_box)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.splitter.addWidget(self.layoutWidget2)

        self.verticalLayout_6.addWidget(self.splitter)

        self.tabWidget.addTab(self.start_tab, "")
        self.help_tab = QWidget()
        self.help_tab.setObjectName(u"help_tab")
        self.verticalLayout_7 = QVBoxLayout(self.help_tab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_5 = QLabel(self.help_tab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_5.setWordWrap(True)
        self.label_5.setOpenExternalLinks(True)

        self.verticalLayout_7.addWidget(self.label_5)

        self.tabWidget.addTab(self.help_tab, "")
        self.logs_tab = QWidget()
        self.logs_tab.setObjectName(u"logs_tab")
        self.verticalLayout_3 = QVBoxLayout(self.logs_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.log_text_edit = QTextEdit(self.logs_tab)
        self.log_text_edit.setObjectName(u"log_text_edit")

        self.verticalLayout_3.addWidget(self.log_text_edit)

        self.tabWidget.addTab(self.logs_tab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"wasd.tv bot", None))
        self.token_line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0422\u043e\u043a\u0435\u043d wasd.tv", None))
        self.channel_line_edit.setInputMask("")
        self.channel_line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u044f \u043a\u0430\u043d\u0430\u043b\u0430", None))
        self.start_push_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0438 \u0437\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043c\u0430\u043d\u0434\u0430", None))
        self.add_command_button.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.remove_command_button.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0432\u0435\u0442\u044b", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0430\u0439\u043c\u0430\u0443\u0442 \u043a\u043e\u043c\u0430\u043d\u0434\u044b", None))
        self.timeout_spin_box.setSuffix(QCoreApplication.translate("MainWindow", u" \u0441\u0435\u043a", None))
        self.add_answer_button.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.remove_answer_button.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u043a\u0441\u0442 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0435\u0440\u043e\u044f\u0442\u043d\u043e\u0441\u0442\u043d\u043e\u0435 \u0441\u043e\u043e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u0435", None))
        self.ban_check_box.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c \u0432 \u0431\u0430\u043d", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u044f \u0441\u0442\u0438\u043a\u0435\u0440\u0430", None))
        self.sticker_line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u043d\u0430\u043b-\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.start_tab), QCoreApplication.translate("MainWindow", u"\u0411\u043e\u0442", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt;\">\u0413\u0434\u0435 \u0432\u0437\u044f\u0442\u044c \u0442\u043e\u043a\u0435\u043d?</span></p><p>\u041f\u0435\u0440\u0435\u0439\u0442\u0438 \u043f\u043e <a href=\"https://wasd.tv/general-settings/API\"><span style=\" text-decoration: underline; color:#007af4;\">\u0441\u0441\u044b\u043b\u043a\u0435</span></a>, \u043d\u0430\u0436\u0430\u0442\u044c &quot;\u0421\u0433\u0435\u043d\u0435\u043d\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043d\u043e\u0432\u044b\u0439 \u0442\u043e\u043a\u0435\u043d&quot;, \u0437\u0430\u0442\u0435\u043c \u043a\u043d\u043e\u043f\u043a\u0443 \u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u0442\u043e\u043a\u0435\u043d\u0430.</p><p><span style=\" font-size:12pt;\">\u041a\u0430\u043a\u0438\u0435 \u043f\u043b\u0435\u0439\u0441\u0445\u043e\u043b\u0434\u0435\u043d\u044b \u043f\u043e\u0434\u0434\u0435\u0436\u0438\u0432\u0430\u044e\u0442\u0441\u044f \u0432 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f\u0445?</span>"
                        "<br/><span style=\" color:#808000;\">${uptime}</span> \u2014 \u0441\u0443\u043c\u043c\u0430\u0440\u043d\u043e\u0435 \u0432\u0440\u0435\u043c \u0441\u0442\u0440\u0438\u043c\u0430;</p><p><span style=\" color:#808000;\">${game_name}</span> \u2014 \u0438\u043c\u044f \u0442\u0435\u043a\u0443\u0449\u0435\u0439 \u0438\u0433\u0440\u044b;</p><p><span style=\" color:#808000;\">${user_name}</span> \u2014 \u0438\u043c\u044f \u043d\u0430\u043f\u0438\u0441\u0430\u0432\u0448\u0435\u0433\u043e \u043a\u043e\u043c\u0430\u043d\u0434\u0443 \u0431\u043e\u0442\u0430;</p><p><span style=\" color:#808000;\">${users_count_total}</span> \u2014 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u0435 \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439;</p><p><span style=\" color:#808000;\">${users_count_auth}</span> \u2014 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u0435 \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0430\u0432\u0442\u043e\u0440"
                        "\u0438\u0437\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0445 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439;</p><p><span style=\" color:#808000;\">${users_count_anon}</span> \u2014 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u0435 \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0430\u043d\u043e\u043d\u0438\u043c\u043d\u044b\u0445 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439;</p><p><span style=\" color:#808000;\">${random_user}</span> \u2014 \u0441\u043b\u0443\u0447\u0430\u0439\u043d\u044b\u0439 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c \u0438\u0437 \u0447\u0430\u0442\u0430;</p><p><span style=\" color:#808000;\">${random_number(</span><span style=\" color:#008080;\">x</span>, <span style=\" color:#008080;\">y</span><span style=\" color:#808000;\">)}</span> \u2014 \u0441\u043b\u0443\u0447\u0430\u0439\u043d\u043e\u0435 \u0446\u0435\u043b\u043e\u0435 \u0447\u0438\u0441\u043b\u043e \u0432 \u0434\u0438"
                        "\u0430\u043f\u0430\u0437\u043e\u043d\u0435 \u043e\u0442 <span style=\" color:#008080;\">x</span> \u0434\u043e <span style=\" color:#008080;\">y</span> \u043d\u0435\u0432\u043a\u043b\u044e\u0447\u0438\u0442\u0435\u043b\u044c\u043d\u043e;</p><p><span style=\" color:#808000;\">${users_tagged}</span> \u2014 \u0441\u043f\u0438\u0441\u043e\u043a \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439, \u043a\u043e\u0442\u043e\u0440\u044b\u0445 \u0443\u043a\u0430\u0437\u0430\u043b \u0432 \u043a\u043e\u043c\u0430\u043d\u0434\u0435 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c (\u0432\u043a\u043b\u044e\u0447\u0430\u044f \u0441\u0438\u043c\u0432\u043e\u043b @).</p><p>\u041f\u0440\u0438\u043c\u0435\u0440: \u043c\u043e\u0436\u043d\u043e \u0441\u043e\u0437\u0434\u0430\u0442\u044c \u043a\u043e\u043c\u0430\u043d\u0434\u0443 &quot;!\u0432\u0440\u0435\u043c\u044f&quot; \u0441 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435\u043c &quot;\u0421\u0442\u0440\u0438\u043c \u0438"
                        "\u0434\u0435\u0442 <span style=\" color:#808000;\">${uptime}</span>&quot;. \u0411\u043e\u0442 \u043f\u043e \u044d\u0442\u043e\u043c\u0443 \u0448\u0430\u0431\u043b\u043e\u043d\u0443 \u043d\u0430\u043f\u0438\u0448\u0435\u0442 \u0432 \u0447\u0430\u0442 &quot;\u0421\u0442\u0440\u0438\u043c \u0438\u0434\u0435\u0442 5 \u043c\u0438\u043d\u0443\u0442 26 \u0441\u0435\u043a\u0443\u043d\u0434&quot;.</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.help_tab), QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043c\u043e\u0449\u044c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.logs_tab), QCoreApplication.translate("MainWindow", u"\u041b\u043e\u0433\u0438", None))
    # retranslateUi

