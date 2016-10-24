"""
A super simple trainer that uses Qt5,7 to train your katakan and hiragana
"""

from PyQt5.QtCore import QFile, QRegExp, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QMainWindow, QMenu,
    QMessageBox, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QGroupBox
)

import random

CHARACTERS = [
    'ア', 'イ', 'ウ', 'エ', 'オ', 'カ', 'ガ', 'キ', 'ギ',
    'ク', 'グ', 'ケ', 'ゲ', 'コ', 'ゴ', 'サ', 'ザ', 'シ', 'ジ',
    'ス', 'ズ', 'セ', 'ゼ', 'ソ', 'ゾ', 'タ', 'ダ', 'チ', 'ヂ',
    'ツ', 'ヅ', 'テ', 'デ', 'ト', 'ド', 'ナ', 'ニ', 'ヌ', 'ネ',
    'ノ', 'ハ', 'バ', 'パ', 'ヒ', 'ビ', 'ピ', 'フ', 'ブ', 'プ',
    'ヘ', 'ベ', 'ペ', 'ホ', 'ボ', 'ポ', 'マ', 'ミ', 'ム', 'メ',
    'モ', 'ヤ', 'ユ', 'ヨ', 'ラ', 'リ', 'ル', 'レ', 'ロ',
    'ワ', 'ヰ', 'ヱ', 'ヲ', 'ン', 'ヴ', 'ヷ', 'ヸ', 'ヹ', 'ヺ',

    'リャ', 'リュ', 'リョ', 'ミャ', 'ミュ', 'ミョ', 'ピャ', 'ピュ',
    'ピョ', 'ビャ', 'ビュ', 'ビョ', 'ヒャ', 'ヒュ', 'ヒョ', 'ニャ',
    'ニュ', 'ニョ', 'チャ', 'チュ', 'チョ', 'ジャ', 'ジュ', 'ジョ',
    'シャ', 'シュ', 'ショ', 'ギャ', 'ギュ', 'ギョ', 'キャ', 'キュ',
    'キョ', 'フォ', 'フェ', 'フィ', 'ファ', 'ディ', 'ティ', 'ドゥ',
    'トゥ', 'チェ', 'ジェ', 'シェ', 'ウェ', 'ヴァ',

    'あ', 'い', 'う', 'え', 'お', 'か', 'が', 'き', 'ぎ', 'く',
    'ぐ', 'け', 'げ', 'こ', 'ご', 'さ', 'ざ', 'し', 'じ', 'す',
    'ず', 'せ', 'ぜ', 'そ', 'ぞ', 'た', 'だ', 'ち', 'ぢ', 'つ',
    'づ', 'て', 'で', 'と', 'ど', 'な', 'に', 'ぬ', 'ね', 'の',
    'は', 'ば', 'ぱ', 'ひ', 'び', 'ぴ', 'ふ', 'ぶ', 'ぷ', 'へ',
    'べ', 'ぺ', 'ほ', 'ぼ', 'ぽ', 'ま', 'み', 'む', 'め', 'も',
    'や', 'ゆ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ', 'わ', 'ゐ',
    'ゑ', 'を', 'ん', 'ゔ',

    'りゃ', 'りゅ', 'りょ', 'みゃ', 'みゅ', 'みょ', 'ぴゃ', 'ぴゅ',
    'ぴょ', 'びゃ', 'びゅ', 'びょ', 'ひゃ', 'ひゅ', 'ひょ', 'にゃ',
    'にゅ', 'にょ', 'ちゃ', 'ちゅ', 'ちょ', 'じゃ', 'じゅ', 'じょ',
    'しゃ', 'しゅ', 'しょ', 'ぎゃ', 'ぎゅ', 'ぎょ', 'きゃ', 'きゅ',
    'きょ'
]

PHONETICS = [
    'a', 'i', 'u', 'e', 'o', 'ka', 'ga', 'ki', 'gi',
    'ku', 'gu', 'ke', 'ge', 'ko', 'go', 'sa', 'za', 'shi', 'ji',
    'su', 'zu', 'se', 'ze', 'so', 'zo', 'ta', 'da', 'chi', 'ji',
    'tsu', 'zu', 'te', 'de', 'to', 'do', 'na', 'ni', 'nu', 'ne',
    'no', 'ha', 'ba', 'pa', 'hi', 'bi', 'pi', 'fu', 'bu', 'pu',
    'he', 'be', 'pe', 'ho', 'bo', 'po', 'ma', 'mi', 'mu', 'me',
    'mo', 'ya', 'yu', 'yo', 'ra', 'ri', 'ru', 're', 'ro',
    'wa', 'wi', 'we', 'wo', 'n', 'vu', 'va', 'vi', 've', 'vo',

    'rya', 'ryu', 'ryo', 'mya', 'myu', 'myo', 'pya', 'pyu',
    'pyo', 'bya', 'byu', 'byo', 'hya', 'hyu', 'hyo', 'nya',
    'nyu', 'nyo', 'cha', 'chu', 'cho', 'ja', 'ju', 'jo',
    'sha', 'shu', 'sho', 'gya', 'gyu', 'gyo', 'kya', 'kyu',
    'kyo', 'fo', 'fe', 'fi', 'fa', 'di', 'ti', 'du',
    'tu', 'che', 'je', 'she', 'we', 'va',

    'a', 'i', 'u', 'e', 'o', 'ka', 'ga', 'ki', 'gi', 'ku',
    'gu', 'ke', 'ge', 'ko', 'go', 'sa', 'za', 'shi', 'ji', 'su',
    'zu', 'se', 'ze', 'so', 'zo', 'ta', 'da', 'chi', 'ji', 'tsu',
    'zu', 'te', 'de', 'to', 'do', 'na', 'ni', 'nu', 'ne', 'no',
    'ha', 'ba', 'pa', 'hi', 'bi', 'pi', 'fu', 'bu', 'pu', 'he',
    'be', 'pe', 'ho', 'bo', 'po', 'ma', 'mi', 'mu', 'me', 'mo',
    'ya', 'yu', 'yo', 'ra', 'ri', 'ru', 're', 'ro', 'wa', 'wi',
    'we', 'wo', 'n', 'vu',

    'rya', 'ryu', 'ryo', 'mya', 'myu', 'myo', 'pya', 'pyu',
    'pyo', 'bya', 'byu', 'byo', 'hya', 'hyu', 'hyo', 'nya',
    'nyu', 'nyo', 'cha', 'chu', 'cho', 'ja', 'ju', 'jo',
    'sha', 'shu', 'sho', 'gya', 'gyu', 'gyo', 'kya', 'kyu',
    'kyo'
]

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.index = random.randint(0, len(CHARACTERS))

        self.character = QLabel(CHARACTERS[self.index])
        self.phonetic = QLabel(PHONETICS[self.index])

        font = QFont('Arial', 100, QFont.Normal)
        self.character.setFont(font)
        self.phonetic.setVisible(False)

        font = QFont('Aardvark Cafe', 50, QFont.Normal)
        self.phonetic.setFont(font)
        phlayout = QHBoxLayout()
        phlayout.setAlignment(Qt.AlignCenter)
        phlayout.addWidget(self.phonetic)

        self.input_field = QLineEdit()
        self.input_field.textChanged.connect(self.check_valid)
        self.input_field.returnPressed.connect(self.show_phonetic)

        char_layout = QHBoxLayout()
        char_layout.setAlignment(Qt.AlignCenter)
        char_layout.addWidget(self.character)

        main_layout = QVBoxLayout()

        main_layout.addLayout(char_layout)
        main_layout.addLayout(phlayout)
        main_layout.addWidget(self.input_field)

        main_layout.setAlignment(Qt.AlignCenter)

        hlayout = QHBoxLayout()
        hlayout.addLayout(main_layout)
        hlayout.setAlignment(Qt.AlignCenter)

        gbox = QGroupBox()
        gbox.setLayout(hlayout)

        vlayout = QVBoxLayout()
        vlayout.addWidget(gbox)

        self.setLayout(vlayout)

    def check_valid(self):
        """If the text input is correct, load a new symbol"""
        if self.input_field.text() == self.phonetic.text():
            self.change_symbol()

    def show_phonetic(self):
        self.phonetic.setVisible(True)

    def change_symbol(self):
        """Change the displayed symbol and clear the text box"""
        self.index = random.randint(0, len(CHARACTERS)-1)

        self.character.setText(CHARACTERS[self.index])
        self.phonetic.setText(PHONETICS[self.index])
        self.phonetic.setVisible(False)

        self.input_field.setText('')


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 512)
    window.show()
    sys.exit(app.exec_())
