import sys
import os
import ffmpeg
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QMessageBox

class AudioExtractorApp(QWidget):
    def __init__(self):
        super().__init__()

    def check_ffmpeg_in_system(self):
        if not self.is_ffmpeg_installed():
            self.show_ffmpeg_not_found_message()

    def is_ffmpeg_installed(self):
        return os.system('ffmpeg -version') == 0

    def show_ffmpeg_not_found_message(self):
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText("FFmpeg is not found in the global environment variables.")
        message_box.setInformativeText("Do you want to specify the path to the ffmpeg.exe file?")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        response = message_box.exec_()

        if response == QMessageBox.Yes:
            self.ask_user_for_ffmpeg_path()
        else:
            sys.exit()

    def ask_user_for_ffmpeg_path(self):
        ffmpeg_folder = QFileDialog.getExistingDirectory(self, "Select the folder where ffmpeg.exe is located")
        
        if ffmpeg_folder:
            ffmpeg_path = os.path.join(ffmpeg_folder, 'ffmpeg.exe')
            if os.path.exists(ffmpeg_path):
                os.environ['PATH'] += os.pathsep + ffmpeg_folder
                self.show_ffmpeg_found_message()
            else:
                self.show_ffmpeg_not_found_in_folder_message()

    def show_ffmpeg_found_message(self):
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Information)
        message_box.setText("FFmpeg has been successfully found.")
        message_box.exec_()

    def show_ffmpeg_not_found_in_folder_message(self):
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Critical)
        message_box.setText("Failed to find ffmpeg.exe in the specified folder.")
        message_box.exec_()

    def select_video_file(self):
        return QFileDialog.getOpenFileName(self, "Select a video file", "", "Video Files (*.mp4 *.avi *.mov)")[0]

    def select_output_file(self):
        return QFileDialog.getSaveFileName(self, "Save Audio File", "", "MP3 Files (*.mp3)")[0]

    def extract_audio(self, video_file, output_audio_file):
        ffmpeg.input(video_file).output(output_audio_file).run()
        print(f"Audio extraction completed. Audio saved at {output_audio_file}")

    def run(self):
        self.check_ffmpeg_in_system()
        video_file = self.select_video_file()
        output_audio_file = self.select_output_file()
        
        if video_file and output_audio_file:
            self.extract_audio(video_file, output_audio_file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioExtractorApp()
    window.run()
    sys.exit(app.exec_())
