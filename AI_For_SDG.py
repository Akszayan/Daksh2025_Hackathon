import openai
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit, QScrollArea
)
from PyQt6.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import sys

# OpenAI API Key (Replace with your actual key)
OPENAI_API_KEY = "Your Api Key"

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
You are an AI learning mentor who creates **fun and engaging** personalized learning paths. 
Your goal is to **make learning enjoyable and easy to understand** for the student. 
Avoid recommending books, research papers, or thesis-based learning.

The student is following this roadmap:
{topics}

### **Student's Profile**
- **Strengths:** {strengths}
- **Weaknesses:** {weaknesses}

### **Your Task**
1. **Compare their strengths and weaknesses**  
   - Show how their strong concepts can help in understanding weaker ones.  
   - Use relatable analogies or real-world examples.  

2. **Interactive & Fun Learning Roadmap**  
   - Suggest **YouTube videos, online courses, and interactive platforms** (like Coursera, Udemy, freeCodeCamp, Kaggle, etc.).  
   - Recommend **hands-on coding exercises, projects, and quizzes** instead of dry theory.  

3. **Step-by-Step Guide to Overcome Weaknesses**  
   - Break down the **complex topics** into simple, bite-sized lessons.  
   - Provide **fun challenges and mini-projects** to practice each concept.  
   - Suggest **real-world applications** for each topic to make it practical.  

4. **Gamified Learning Suggestions**  
   - Recommend **web-based tools, coding games, and interactive exercises** (like Codewars, LeetCode, or MIT Scratch).  
   - Include **community-driven platforms** (like Discord, Stack Overflow, and GitHub discussions) for motivation.  

Keep it concise, engaging, and tailored to their level. No books, theses, or heavy theoretical concepts. Focus on joyful and practical learning.
"""


        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an expert AI learning assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=1000
        )

        self.result_text.setText(response.choices[0].message.content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LearningPathGUI()
    window.show()
    sys.exit(app.exec())
