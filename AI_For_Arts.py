import sys
import cv2
import requests
from io import BytesIO
from PyQt6.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout, QWidget,
    QLineEdit, QTextEdit, QStackedWidget, QHBoxLayout, QFrame
)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt, QThread, pyqtSignal
from deepface import DeepFace
import ollama
import openai

# OpenAI API Key (Replace with your own)
OPENAI_API_KEY = "Your API Key"

class OllamaThread(QThread):
    """Thread to handle AI Q&A chat responses"""
    response_ready = pyqtSignal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        response = ollama.chat(model="deepseek-r1", messages=[{"role": "user", "content": self.prompt}])
        self.response_ready.emit(response["message"]["content"].strip())

class MoodAnalysisApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.cap = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.frame_count = 0
        self.dominant_emotion = "Analyzing..."
        self.user_name = ""
        self.user_age = ""

    def initUI(self):
        """Initialize UI with multiple pages"""
        self.setWindowTitle("AI Mood & Personality Analyzer")
        self.setGeometry(200, 100, 900, 700)

        # Stacked Widget (Switch between pages)
        self.stacked_widget = QStackedWidget()
        self.init_home_screen()
        self.init_analysis_screen()
        self.init_character_analysis_screen()

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)
        self.stacked_widget.setCurrentIndex(0)

    def init_home_screen(self):
        """Home Screen - Name & Age Input"""
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter your name")

        self.age_input = QLineEdit(self)
        self.age_input.setPlaceholderText("Enter your age")

        self.start_btn = QPushButton("Start Analysis", self)
        self.start_btn.clicked.connect(self.start_mood_detection)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("AI Mood & Personality Analyzer", self, alignment=Qt.AlignmentFlag.AlignCenter))
        layout.addWidget(self.name_input)
        layout.addWidget(self.age_input)
        layout.addWidget(self.start_btn)

        home_widget = QWidget()
        home_widget.setLayout(layout)
        self.stacked_widget.addWidget(home_widget)

    def init_analysis_screen(self):
        """Mood Detection Screen"""
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("Detecting mood...", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.chat_box = QTextEdit(self)
        self.chat_box.setReadOnly(True)

        self.image_label = QLabel("Your AI-generated mood image will appear here.", self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.next_btn = QPushButton("Next", self)
        self.next_btn.setDisabled(True)
        self.next_btn.clicked.connect(self.show_character_analysis)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.chat_box)
        layout.addWidget(self.image_label)
        layout.addWidget(self.next_btn)

        analysis_widget = QWidget()
        analysis_widget.setLayout(layout)
        self.stacked_widget.addWidget(analysis_widget)

    def init_character_analysis_screen(self):
        """Character Analysis Q&A Screen"""
        self.qa_box = QTextEdit(self)
        self.qa_box.setReadOnly(True)

        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("Type your response...")
        self.input_box.returnPressed.connect(self.ask_ai_character_analysis)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("AI Character Analysis", self, alignment=Qt.AlignmentFlag.AlignCenter))
        layout.addWidget(self.qa_box)
        layout.addWidget(self.input_box)

        qa_widget = QWidget()
        qa_widget.setLayout(layout)
        self.stacked_widget.addWidget(qa_widget)

    def start_mood_detection(self):
        """Start Mood Detection"""
        self.user_name = self.name_input.text().strip()
        self.user_age = self.age_input.text().strip()
        if not self.user_name or not self.user_age:
            self.status_label.setText("Please enter both name and age.")
            return

        self.stacked_widget.setCurrentIndex(1)
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)
        self.start_btn.setDisabled(True)

    def update_frame(self):
        """Update video feed and detect mood"""
        ret, frame = self.cap.read()
        if not ret:
            return

        self.frame_count += 1
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray_frame, 1.1, 5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_roi = frame[y:y+h, x:x+w]

            if self.frame_count % 10 == 0:
                try:
                    analysis = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
                    self.dominant_emotion = analysis[0]['dominant_emotion'] if analysis else "Unknown"
                except:
                    self.dominant_emotion = "Error"

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = image.shape
        bytes_per_line = ch * w
        q_img = QImage(image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(q_img))

        if self.frame_count >= 100:
            self.timer.stop()
            self.cap.release()
            self.video_label.clear()
            self.status_label.setText(f"Mood Detected: {self.dominant_emotion}")
            self.chat_box.append(f"AI: Detected Mood - {self.dominant_emotion}")
            self.generate_ai_image()

    def generate_ai_image(self):
        """Generate an AI image based on detected mood"""
        prompt = f"An artistic representation of someone feeling {self.dominant_emotion}."

        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")

            image_url = response.data[0].url
            img_data = requests.get(image_url).content
            pixmap = QPixmap()
            pixmap.loadFromData(BytesIO(img_data).read())

            self.image_label.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))
            self.next_btn.setDisabled(False)
        except Exception as e:
            self.image_label.setText(f"Error generating image: {e}")

    def show_character_analysis(self):
        """Switch to Character Analysis Q&A"""
        self.stacked_widget.setCurrentIndex(2)
        self.qa_box.append(f"AI: Hi {self.user_name}, let's explore your personality!")

    def ask_ai_character_analysis(self):
        """Send user response to AI for analysis"""
        user_input = self.input_box.text().strip()
        if user_input:
            self.qa_box.append(f"You: {user_input}")
            self.input_box.clear()

            thread = OllamaThread(f"Analyze this person's character based on their response: {user_input}")
            thread.response_ready.connect(lambda response: self.qa_box.append(f"AI: {response}"))
            thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MoodAnalysisApp()
    window.show()
    sys.exit(app.exec())
