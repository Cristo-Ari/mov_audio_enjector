import sys
import os
import ffmpeg
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QMessageBox, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout, QGroupBox

class AudioExtractorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Audio Extractor')

        self.layout = QVBoxLayout()

        self.ffmpeg_status_label = QLabel("FFmpeg Status: Not Found")
        self.layout.addWidget(self.ffmpeg_status_label)

        self.find_ffmpeg_button = QPushButton('Find FFmpeg')
        self.find_ffmpeg_button.clicked.connect(self.ask_user_for_ffmpeg_path)
        self.layout.addWidget(self.find_ffmpeg_button)

        self.video_file_layout = QHBoxLayout()
        self.video_file_label = QLabel("Select Video File:")
        self.video_file_input = QLineEdit(self)
        self.video_file_input.setEnabled(False)
        self.video_file_input.setStyleSheet("background-color: lightgray;")
        self.select_video_button = QPushButton('Browse')
        self.select_video_button.clicked.connect(self.select_video_file)
        self.video_file_layout.addWidget(self.video_file_label)
        self.video_file_layout.addWidget(self.video_file_input)
        self.video_file_layout.addWidget(self.select_video_button)
        self.layout.addLayout(self.video_file_layout)

        self.output_audio_layout = QHBoxLayout()
        self.output_audio_label = QLabel("Select Output Audio File:")
        self.output_audio_input = QLineEdit(self)
        self.output_audio_input.setEnabled(False)
        self.output_audio_input.setStyleSheet("background-color: lightgray;")
        self.select_output_button = QPushButton('Browse')
        self.select_output_button.clicked.connect(self.select_output_file)
        self.output_audio_layout.addWidget(self.output_audio_label)
        self.output_audio_layout.addWidget(self.output_audio_input)
        self.output_audio_layout.addWidget(self.select_output_button)
        self.layout.addLayout(self.output_audio_layout)

        self.extract_audio_button = QPushButton('Extract Audio')
        self.extract_audio_button.clicked.connect(self.extract_audio)
        self.extract_audio_button.setEnabled(False)
        self.layout.addWidget(self.extract_audio_button)

        self.setLayout(self.layout)
        self.check_ffmpeg_in_system()

        # Connect to text change signals to enable Extract Audio button when both fields are filled
        self.video_file_input.textChanged.connect(self.check_fields_filled)
        self.output_audio_input.textChanged.connect(self.check_fields_filled)

    def check_ffmpeg_in_system(self):
        if not self.is_ffmpeg_installed():
            self.show_ffmpeg_not_found_message()
        else:
            self.ffmpeg_status_label.setText("FFmpeg Status: Found")
            self.ffmpeg_status_label.setStyleSheet("color: green")
            self.find_ffmpeg_button.setEnabled(False)
            self.video_file_input.setEnabled(True)
            self.output_audio_input.setEnabled(True)

    def is_ffmpeg_installed(self):
        return os.system('ffmpeg -version') == 0

    def show_ffmpeg_not_found_message(self):
        self.ffmpeg_status_label.setText("FFmpeg Status: Not Found")
        self.ffmpeg_status_label.setStyleSheet("color: red")
        self.find_ffmpeg_button.setEnabled(True)

    def ask_user_for_ffmpeg_path(self):
        ffmpeg_folder = QFileDialog.getExistingDirectory(self, "Select the folder where ffmpeg.exe is located")
        
        if ffmpeg_folder:
            ffmpeg_path = os.path.join(ffmpeg_folder, 'ffmpeg.exe')
            if os.path.exists(ffmpeg_path):
                os.environ['PATH'] += os.pathsep + ffmpeg_folder
                self.ffmpeg_status_label.setText("FFmpeg Status: Found")
                self.ffmpeg_status_label.setStyleSheet("color: green")
                self.find_ffmpeg_button.setEnabled(False)
                self.video_file_input.setEnabled(True)
                self.output_audio_input.setEnabled(True)
            else:
                self.show_ffmpeg_not_found_in_folder_message()

    def show_ffmpeg_not_found_in_folder_message(self):
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Critical)
        message_box.setText("Failed to find ffmpeg.exe in the specified folder.")
        message_box.exec_()

    def select_video_file(self):
        video_file, _ = QFileDialog.getOpenFileName(self, "Select a video file", "", "Video Files (*.mp4 *.avi *.mov)")
        if video_file:
            self.video_file_input.setText(video_file)
            # Automatically set the output audio file path with .mp3 extension
            output_audio_file = os.path.splitext(video_file)[0] + ".mp3"
            self.output_audio_input.setText(output_audio_file)

    def select_output_file(self):
        output_file, _ = QFileDialog.getSaveFileName(self, "Save Audio File", "", "MP3 Files (*.mp3)")
        if output_file:
            self.output_audio_input.setText(output_file)

    def extract_audio(self):
        video_file = self.video_file_input.text()
        output_audio_file = self.output_audio_input.text()

        if video_file and output_audio_file:
            ffmpeg.input(video_file).output(output_audio_file).run()
            QMessageBox.information(self, "Success", f"Audio extraction completed.\nAudio saved at {output_audio_file}")
        else:
            QMessageBox.warning(self, "Error", "Please select both video file and output location.")

    def check_fields_filled(self):
        video_file = self.video_file_input.text()
        output_audio_file = self.output_audio_input.text()

        # Enable the Extract Audio button only if both fields are filled
        if video_file and output_audio_file:
            self.extract_audio_button.setEnabled(True)
        else:
            self.extract_audio_button.setEnabled(False)

    def run(self):
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioExtractorApp()
    window.run()
    sys.exit(app.exec_())
