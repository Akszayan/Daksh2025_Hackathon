from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit, QScrollArea
)
from PyQt6.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import ollama
from bs4 import BeautifulSoup
import sys

class LearningPathGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("AI Learning Path Generator")
        self.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()
        
        self.label = QLabel("Enter your strengths and weaknesses:")
        layout.addWidget(self.label)
        
        self.strength_input = QLineEdit()
        self.strength_input.setPlaceholderText("Strong at (comma-separated)")
        layout.addWidget(self.strength_input)

        self.weakness_input = QLineEdit()
        self.weakness_input.setPlaceholderText("Weak at (comma-separated)")
        layout.addWidget(self.weakness_input)
        
        self.generate_button = QPushButton("Generate Learning Path")
        self.generate_button.clicked.connect(self.generate_learning_path)
        layout.addWidget(self.generate_button)
        
        self.result_label = QLabel("Personalized Learning Plan:")
        layout.addWidget(self.result_label)
        
        self.result_area = QScrollArea()
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_area.setWidget(self.result_text)
        self.result_area.setWidgetResizable(True)
        layout.addWidget(self.result_area)
        
        self.setLayout(layout)
    
    def initialize_driver(self):
        options = Options()
        options.headless = True
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    def scrape_learning_paths(self, url, driver):
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        topics = [topic.text.strip() for topic in soup.find_all("span", class_="text-gray-700")]
        return topics
    
    def generate_learning_path(self):
        strengths = self.strength_input.text().split(',')
        weaknesses = self.weakness_input.text().split(',')
        strengths = [s.strip() for s in strengths]
        weaknesses = [w.strip() for w in weaknesses]
        
        url = "https://roadmap.sh/ai"
        driver = self.initialize_driver()
        
        try:
            topics = self.scrape_learning_paths(url, driver)
        finally:
            driver.quit()
        
        prompt = f"""
        You are an AI learning assistant. A student is following this roadmap:
        {topics}
        
        Their strengths: {strengths}
        Their weaknesses: {weaknesses}
        
        Generate a structured **personalized learning path** that:
        - Adapts to their weaknesses.
        - Suggests practical exercises.
        - Includes extra resources.
        """
        
        response = ollama.generate(model="deepseek-r1", prompt=prompt)
        self.result_text.setText(response["response"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LearningPathGUI()
    window.show()
    sys.exit(app.exec())
