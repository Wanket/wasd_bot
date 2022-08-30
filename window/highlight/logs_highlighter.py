from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont


class LogsHighlighter(QSyntaxHighlighter):
    def __init__(self, parent: QSyntaxHighlighter):
        super().__init__(parent)

        time_format = QTextCharFormat()
        time_format.setForeground(Qt.darkCyan)

        info_format = QTextCharFormat()
        info_format.setFontWeight(QFont.Bold)
        info_format.setForeground(Qt.darkGreen)

        debug_format = QTextCharFormat()
        debug_format.setFontWeight(QFont.Bold)
        debug_format.setForeground(Qt.darkBlue)

        warning_format = QTextCharFormat()
        warning_format.setFontWeight(QFont.Bold)
        warning_format.setForeground(Qt.darkYellow)

        error_format = QTextCharFormat()
        error_format.setFontWeight(QFont.Bold)
        error_format.setForeground(Qt.darkRed)

        critical_format = QTextCharFormat()
        critical_format.setFontWeight(QFont.Bold)
        critical_format.setForeground(Qt.darkMagenta)

        exception_format = QTextCharFormat()
        exception_format.setFontWeight(QFont.Bold)
        exception_format.setForeground(Qt.darkMagenta)

        self._formats = [
            (QRegularExpression(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}'), time_format),
            (QRegularExpression(r'INFO:'), info_format),
            (QRegularExpression(r'DEBUG:'), debug_format),
            (QRegularExpression(r'WARNING:'), warning_format),
            (QRegularExpression(r'ERROR:'), error_format),
            (QRegularExpression(r'CRITICAL:'), critical_format),
            (QRegularExpression(r'EXCEPTION:'), exception_format),
        ]

    def highlightBlock(self, text):
        for pattern, char_format in self._formats:
            match_it = pattern.globalMatch(text)

            while match_it.hasNext():

                match = match_it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), char_format)
