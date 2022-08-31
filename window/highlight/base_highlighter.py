from typing import List, Tuple

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QSyntaxHighlighter, QTextDocument, QTextCharFormat


class BaseHighlighter(QSyntaxHighlighter):
    def __init__(self, parent: QTextDocument):
        super().__init__(parent)

        self.__formats: List[Tuple[QRegularExpression, QTextCharFormat]] = []

    def _set_formats(self, formats: List[Tuple[QRegularExpression, QTextCharFormat]]):
        self.__formats = formats

    def highlightBlock(self, text):
        for pattern, char_format in self.__formats:
            match_it = pattern.globalMatch(text)

            while match_it.hasNext():

                match = match_it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), char_format)
