from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QTextCharFormat, QTextDocument

from window.highlight.base_highlighter import BaseHighlighter


class MessageHighlighter(BaseHighlighter):
    def __init__(self, parent: QTextDocument):
        super().__init__(parent)

        command_format = QTextCharFormat()
        command_format.setForeground(Qt.darkYellow)

        commands_generic = ["uptime", "game_name", "user_name", "users_count_total", "users_count_auth", "users_count_anon", "random_user"]
        commands_functions = ["random_number"]

        command_regex = QRegularExpression(rf"\${{({'|'.join(commands_generic)})}}")

        # noinspection RegExpUnnecessaryNonCapturingGroup
        self._function_regex = QRegularExpression(rf"(\${{(?:{'|'.join(commands_functions)})\()([^)]*)(\)}})")

        self._set_formats([
            (command_regex, command_format),
        ])

    def highlightBlock(self, text):
        super().highlightBlock(text)

        matches = self._function_regex.globalMatch(text)

        while matches.hasNext():
            match = matches.next()

            self.setFormat(match.capturedStart(1), match.capturedLength(1), Qt.darkYellow)
            self.setFormat(match.capturedStart(3), match.capturedLength(3), Qt.darkYellow)

            sub_matches = QRegularExpression(r"[^,]+").globalMatch(match.captured(2))

            while sub_matches.hasNext():
                sub_match = sub_matches.next()

                self.setFormat(match.capturedStart(2) + sub_match.capturedStart(), sub_match.capturedLength(), Qt.darkCyan)
