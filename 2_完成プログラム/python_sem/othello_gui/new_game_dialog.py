from PyQt6.QtWidgets import QDialog, QVBoxLayout, QGroupBox, QRadioButton, QDialogButtonBox

class NewGameDialog(QDialog):
    """
    新しいゲームの設定を選択するためのダイアログ
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Game")

        layout = QVBoxLayout(self)

        # 対戦モードの選択
        mode_groupbox = QGroupBox("Game Mode")
        self.pvp_radio = QRadioButton("Human vs. Human")
        self.pvc_radio = QRadioButton("Human vs. Computer")
        self.pvp_radio.setChecked(True)
        mode_layout = QVBoxLayout()
        mode_layout.addWidget(self.pvp_radio)
        mode_layout.addWidget(self.pvc_radio)
        mode_groupbox.setLayout(mode_layout)
        layout.addWidget(mode_groupbox)

        # AIの強さの選択
        self.ai_groupbox = QGroupBox("Computer Difficulty")
        ai_layout = QVBoxLayout()
        self.ai_radios = {}

        # othello.player.strategiesから動的に読み込む
        from othello.player.strategies import STRATEGIES

        is_first = True
        for name in STRATEGIES.keys():
            radio = QRadioButton(name)
            if is_first:
                radio.setChecked(True)
                is_first = False
            ai_layout.addWidget(radio)
            self.ai_radios[name] = radio

        self.ai_groupbox.setLayout(ai_layout)
        layout.addWidget(self.ai_groupbox)

        self.ai_groupbox.setEnabled(False)
        self.pvc_radio.toggled.connect(self.ai_groupbox.setEnabled)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_settings(self):
        """
        選択された設定を返す
        """
        game_mode = "pvc" if self.pvc_radio.isChecked() else "pvp"
        ai_difficulty = ""
        for name, radio in self.ai_radios.items():
            if radio.isChecked():
                ai_difficulty = name
                break
        return game_mode, ai_difficulty
