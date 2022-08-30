from typing import Optional

import inject
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QListWidgetItem, QAbstractButton, QDialogButtonBox, QApplication

from model.bot import Bot
from model.settings.answer_settings import AnswerSettings
from util.ilogger import ILogger
from window.highlight.logs_highlighter import LogsHighlighter
from window.highlight.message_highlighter import MessageHighlighter
from window.main_window.ui_main_window import Ui_MainWindow
from window.main_window.utils import _item_changed, _create_item, _remove_command, _find_unique_name


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._setup_ui()

        self._setup_logs()

        self._bot = inject.instance(Bot)
        self._reload_settings()

        self._setup_listeners()

        self._activated_command: Optional[str] = None
        self._activated_answer: Optional[str] = None

        self._bot_is_running = False

    def _setup_logs(self):
        logger = inject.instance(ILogger)
        logger.register_logging_handler(self._on_logs)

        LogsHighlighter(self._ui.log_text_edit.document())

    def _setup_ui(self):
        MessageHighlighter(self._ui.answer_text_edit.document())

    # noinspection DuplicatedCode
    def _setup_listeners(self):
        self._ui.add_command_button.clicked.connect(self._add_command_clicked)
        self._ui.remove_command_button.clicked.connect(self._remove_command_clicked)

        self._ui.add_answer_button.clicked.connect(self._add_answer_clicked)
        self._ui.remove_answer_button.clicked.connect(self._remove_answer_clicked)

        self._ui.commands_list_widget.itemSelectionChanged.connect(self._command_item_selected)
        self._ui.commands_list_widget.itemChanged.connect(self._command_item_changed)

        self._ui.answers_list_widget.itemSelectionChanged.connect(self._answer_item_selected)
        self._ui.answers_list_widget.itemChanged.connect(self._answer_item_changed)

        self._ui.answer_text_edit.textChanged.connect(self._answer_text_changed)
        self._ui.ban_check_box.stateChanged.connect(self._ban_check_box_changed)
        self._ui.rate_spin_box.valueChanged.connect(self._rate_spin_box_changed)

        self._ui.apply_button_box.clicked.connect(self._apply_button_clicked)

        self._ui.start_push_button.clicked.connect(self._start_stop_bot)

        self._ui.token_line_edit.textChanged.connect(self._token_line_edit_changed)

    def _on_logs(self, message: str):
        self._ui.log_text_edit.append(message)

    def _add_command_clicked(self):
        command_name = _find_unique_name("Новая команда", self._settings.commands)

        self._settings.commands[command_name] = {}

        self._add_command(command_name)

        self._ui.apply_button_box.setEnabled(True)

    def _add_answer_clicked(self):
        answer_name = _find_unique_name("Новый ответ", self._settings.commands[self._activated_command])

        self._settings.commands[self._activated_command][answer_name] = AnswerSettings(1, "", False)

        self._add_answer(answer_name)

        self._ui.apply_button_box.setEnabled(True)

    def _add_command(self, command_name: str):
        _create_item(command_name, self._ui.commands_list_widget, self._ui.remove_command_button)

        self._activated_command = command_name

        self._reload_answers(command_name)

    def _add_answer(self, answer_name: str):
        _create_item(answer_name, self._ui.answers_list_widget, self._ui.remove_answer_button)

        self._activated_answer = answer_name

        current_command_item = self._ui.commands_list_widget.selectedItems()[0]
        self._reload_answer_settings(current_command_item.text(), answer_name)

    def _remove_command_clicked(self):
        if _remove_command(self._ui.commands_list_widget, self._settings.commands, self._ui.remove_command_button):
            current_item = self._ui.commands_list_widget.currentItem()
            self._reload_answers(current_item.text() if current_item else None)

        self._ui.apply_button_box.setEnabled(True)

    def _remove_answer_clicked(self):
        if _remove_command(self._ui.answers_list_widget, self._settings.commands[self._activated_command], self._ui.remove_answer_button):
            current_command_item = self._ui.commands_list_widget.selectedItems()[0]
            current_item = self._ui.answers_list_widget.currentItem()
            self._reload_answer_settings(current_command_item.text(), current_item.text() if current_item else None)

        self._ui.apply_button_box.setEnabled(True)

    def _reload_settings(self):
        self._settings = self._bot.get_settings()

        self._ui.token_line_edit.setText(self._settings.token)
        self._ui.start_push_button.setEnabled(len(self._settings.token) != 0)

        current_command_item = self._ui.commands_list_widget.selectedItems()
        current_command_name = current_command_item[0].text() if current_command_item else None

        self._ui.commands_list_widget.clear()

        for key in self._settings.commands.keys():
            item = QListWidgetItem(key)
            item.setFlags(item.flags() | Qt.ItemIsEditable)

            self._ui.commands_list_widget.addItem(item)

        self._ui.remove_command_button.setEnabled(len(self._settings.commands) > 0)

        current_command = current_command_name if current_command_name and current_command_name in self._settings.commands else None
        if current_command:
            self._ui.commands_list_widget.findItems(current_command, Qt.MatchExactly)[0].setSelected(True)

        self._reload_answers(current_command)

        self._ui.apply_button_box.setEnabled(False)

    def _reload_answers(self, current_command: Optional[str]):
        current_answer_item = self._ui.answers_list_widget.selectedItems()
        current_answer_name = current_answer_item[0].text() if current_answer_item else None

        self._ui.answers_list_widget.clear()

        current_answer = None

        if current_command and current_command in self._settings.commands:
            for key in self._settings.commands[current_command].keys():
                item = QListWidgetItem(key)
                item.setFlags(item.flags() | Qt.ItemIsEditable)

                self._ui.answers_list_widget.addItem(item)

            if current_answer_name and current_answer_name in self._settings.commands[current_command]:
                current_answer = current_answer_name

        if current_answer:
            item = self._ui.answers_list_widget.findItems(current_answer, Qt.MatchExactly)
            if item:
                item[0].setSelected(True)

        self._ui.add_answer_button.setEnabled(self._ui.commands_list_widget.count() > 0)
        self._ui.remove_answer_button.setEnabled(self._ui.answers_list_widget.count() > 0)

        self._ui.answers_list_widget.setEnabled(self._ui.commands_list_widget.count() > 0)

        self._reload_answer_settings(current_command, current_answer)

    def _reload_answer_settings(self, current_command: Optional[str], current_answer: Optional[str]):
        is_enabled = current_command is not None and current_answer is not None

        if is_enabled and current_command in self._settings.commands and current_answer in self._settings.commands[current_command]:
            answer_settings = self._settings.commands[current_command][current_answer]
        else:
            answer_settings = AnswerSettings(1, "", False)

        self._ui.answer_text_edit.setEnabled(is_enabled)
        self._ui.ban_check_box.setEnabled(is_enabled)
        self._ui.rate_spin_box.setEnabled(is_enabled)

        self._ui.answer_text_edit.blockSignals(True)
        self._ui.ban_check_box.blockSignals(True)
        self._ui.rate_spin_box.blockSignals(True)

        self._ui.answer_text_edit.setPlainText(answer_settings.template)
        self._ui.ban_check_box.setChecked(answer_settings.ban)
        self._ui.rate_spin_box.setValue(answer_settings.rate)

        self._ui.answer_text_edit.blockSignals(False)
        self._ui.ban_check_box.blockSignals(False)
        self._ui.rate_spin_box.blockSignals(False)

    def _command_item_selected(self):
        item = self._ui.commands_list_widget.selectedItems()
        if not item:
            return

        self._activated_command = item[0].text()

        self._reload_answers(item[0].text())

    def _answer_item_selected(self):
        item = self._ui.answers_list_widget.selectedItems()
        if not item:
            return

        self._activated_answer = item[0].text()

        self._reload_answer_settings(self._ui.commands_list_widget.selectedItems()[0].text(), item[0].text())

    def _command_item_changed(self, item: QListWidgetItem):
        self._activated_command = _item_changed(item, self._activated_command, self._settings.commands)

        self._reload_answers(self._activated_command)

        self._ui.apply_button_box.setEnabled(True)

    def _answer_item_changed(self, item: QListWidgetItem):
        self._answer_command = _item_changed(
            item,
            self._activated_answer,
            self._settings.commands[self._ui.commands_list_widget.selectedItems()[0].text()]
        )

        self._reload_answer_settings(self._activated_command, self._answer_command)

        self._ui.apply_button_box.setEnabled(True)

    def _answer_text_changed(self):
        if self._ui.answer_text_edit.isEnabled():
            self._get_current_answer_settings().template = self._ui.answer_text_edit.toPlainText()

            self._ui.apply_button_box.setEnabled(True)

    def _ban_check_box_changed(self, state: int):
        if self._ui.ban_check_box.isEnabled():
            self._get_current_answer_settings().ban = state == Qt.Checked

            self._ui.apply_button_box.setEnabled(True)

    def _rate_spin_box_changed(self, value: int):
        if self._ui.rate_spin_box.isEnabled():
            self._get_current_answer_settings().rate = value

            self._ui.apply_button_box.setEnabled(True)

    def _apply_button_clicked(self, button: QAbstractButton):
        if button == self._ui.apply_button_box.button(QDialogButtonBox.Save):
            self._bot.set_settings(self._settings)

        self._reload_settings()

        self._ui.apply_button_box.setEnabled(False)

    def _get_current_answer_settings(self) -> AnswerSettings:
        command_name = self._ui.commands_list_widget.selectedItems()[0].text()
        answer_name = self._ui.answers_list_widget.selectedItems()[0].text()

        if command_name in self._settings.commands and answer_name in self._settings.commands[command_name]:
            return self._settings.commands[command_name][answer_name]

        return AnswerSettings(1, "", False)

    def _start_stop_bot(self):
        if self._bot_is_running:
            self._bot.stop_bot()
        else:
            self._ui.apply_button_box.button(QDialogButtonBox.Save).click()

            self._bot.start_bot()

        self._bot_is_running = not self._bot_is_running

        self._ui.token_line_edit.setEnabled(not self._bot_is_running)

        self._ui.start_push_button.setText("Стоп" if self._bot_is_running else "Сохранить и запустить")

    def _token_line_edit_changed(self, text: str):
        self._settings.token = text

        self._ui.start_push_button.setEnabled(len(text) > 0)

        self._ui.apply_button_box.setEnabled(True)
