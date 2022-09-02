from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QTextCharFormat, QTextDocument

from window.highlight.base_highlighter import BaseHighlighter


class MessageHighlighter(BaseHighlighter):
    def __init__(self, parent: QTextDocument):
        super().__init__(parent)

        uptime_format = QTextCharFormat()
        uptime_format.setForeground(Qt.darkCyan)

        game_name_format = QTextCharFormat()
        game_name_format.setForeground(Qt.darkGreen)

        user_name_format = QTextCharFormat()
        user_name_format.setForeground(Qt.darkBlue)

        users_count_total_format = QTextCharFormat()
        users_count_total_format.setForeground(Qt.darkRed)

        users_count_auth_format = QTextCharFormat()
        users_count_auth_format.setForeground(Qt.darkYellow)

        users_count_anon_format = QTextCharFormat()
        users_count_anon_format.setForeground(Qt.darkMagenta)

        self._set_formats([
            (QRegularExpression(r'(\W|^)\$uptime(\W|$)'), uptime_format),
            (QRegularExpression(r'(\W|^)\$game_name(\W|$)'), game_name_format),
            (QRegularExpression(r'(\W|^)\$user_name(\W|$)'), user_name_format),
            (QRegularExpression(r'(\W|^)\$users_count_total(\W|$)'), users_count_total_format),
            (QRegularExpression(r'(\W|^)\$users_count_auth(\W|$)'), users_count_auth_format),
            (QRegularExpression(r'(\W|^)\$users_count_anon(\W|$)'), users_count_anon_format),
        ])
