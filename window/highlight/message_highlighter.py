from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat


class MessageHighlighter(QSyntaxHighlighter):
    def __init__(self, parent: QSyntaxHighlighter):
        super().__init__(parent)

        uptime_format = QTextCharFormat()
        uptime_format.setForeground(Qt.darkCyan)

        game_name_format = QTextCharFormat()
        game_name_format.setForeground(Qt.darkGreen)

        user_name_format = QTextCharFormat()
        user_name_format.setForeground(Qt.darkBlue)

        self._formats = [
            (QRegularExpression(r'(\W|^)\$uptime(\W|$)'), uptime_format),
            (QRegularExpression(r'(\W|^)\$game_name(\W|$)'), game_name_format),
            (QRegularExpression(r'(\W|^)\$user_name(\W|$)'), user_name_format),
        ]

    def highlightBlock(self, text):
        for pattern, char_format in self._formats:
            match_it = pattern.globalMatch(text)

            while match_it.hasNext():
                match = match_it.next()

                self.setFormat(match.capturedStart(), match.capturedLength(), char_format)
