# 🌐 AI-Powered Human-Centric Learning & Creativity Suite

> **Daksh 2025 – AI Hackathon | SASTRA Deemed University, Thanjavur**
> 🏆 **1st Place – AI for Sustainable Development Goals (SDG)**

---

## 📌 Overview

This repository presents a **general-purpose, modular AI prototype suite** developed during **Daksh 2025**, the annual technical hackathon conducted by **SASTRA Deemed University, Thanjavur**.

The project explores how **Artificial Intelligence can be applied responsibly and creatively across education, sustainability, and the arts**, with a strong focus on:

* Human-centric design
* Accessibility and engagement
* Responsible AI (local vs cloud inference)

⚠️ **Note:** This implementation represents a **basic / early-stage prototype** intended to demonstrate feasibility, architecture, and impact. It is not a production-ready system.

---

## 🏆 Hackathon Achievement

* **Event:** Daksh 2025 – AI Hackathon
* **Institution:** SASTRA Deemed University, Thanjavur
* **Category:** AI for Sustainable Development Goals (SDG)
* **Result:** 🥇 **First Place**

The project was evaluated on innovation, real-world impact, technical execution, and alignment with SDGs.

---

## 🧩 Project Structure & Modules

This repository contains **three independent but thematically connected AI modules**, each addressing a different real-world domain.

---

### 1️⃣ Assistive Learning – Cloud AI–Driven Personalized Learning

**Purpose:**
To generate **personalized, engaging AI learning paths** by adapting to a learner’s strengths and weaknesses.

**Key Features:**

* Desktop GUI using **PyQt6**
* Dynamic scraping of AI learning roadmaps
* Cloud-based LLM inference (OpenAI)
* Focus on **practical, joyful learning** (no heavy theory, books, or research papers)

**Core Technologies:**

* PyQt6
* Selenium + BeautifulSoup
* OpenAI GPT-based models

**Use Case:**
Ideal for beginners and intermediate learners seeking adaptive learning guidance.

---

### 2️⃣ AI for SDG – Sustainable, Local AI Learning Assistant

**Purpose:**
To demonstrate **privacy-aware, cost-efficient, and sustainable AI** using **local LLM inference**, aligned with SDG principles.

**Key Features:**

* Same assistive learning concept as Module 1
* Replaced cloud APIs with **local LLM inference**
* Offline-capable AI responses
* Reduced dependency on external services

**Core Technologies:**

* PyQt6
* Selenium + BeautifulSoup
* Ollama (Local LLM)
* DeepSeek-R1 model

**Why This Matters:**

* Promotes AI accessibility
* Reduces cloud dependency
* Aligns with sustainable AI practices

🏆 **This module directly contributed to securing 1st place in the AI for SDG category.**

---

### 3️⃣ AI for Arts – Emotion-Aware Creativity & Personality Analysis

**Purpose:**
To explore the intersection of **AI, emotion, creativity, and human-computer interaction**.

**Key Features:**

* Real-time webcam-based mood detection
* Facial emotion analysis using computer vision
* Emotion-driven AI-generated artwork
* Personality & character analysis via conversational AI
* Multi-screen interactive desktop experience

**Core Technologies:**

* PyQt6
* OpenCV
* DeepFace
* OpenAI (Image Generation)
* Ollama (Local LLM for personality analysis)

**Use Case:**
Demonstrates AI applications in **digital art, psychology, and creative expression**.

---

## 🏗️ High-Level Architecture

```
User Input / Camera
        ↓
   PyQt6 Desktop UI
        ↓
 Data Processing Layer
 (CV / Scraping / Context)
        ↓
 AI Inference Layer
 (Cloud LLM or Local LLM)
        ↓
 Results Rendered to UI
```

Each module follows a **clean separation of concerns**, enabling easy extension and experimentation.

---

## ⚙️ Setup & Installation (Prototype Level)

### Prerequisites

* Python 3.9+
* Google Chrome (for Selenium-based modules)
* Webcam (for AI for Arts module)

### Common Dependencies

```bash
pip install pyqt6 selenium webdriver-manager beautifulsoup4 opencv-python deepface ollama openai requests
```

⚠️ API keys (OpenAI) must be added manually where applicable. Local LLM modules require **Ollama** to be installed and running.

---

## 🚧 Limitations

* Prototype-level error handling
* Hardcoded UI flows
* Basic scraping logic (no caching or async handling)
* Not optimized for large-scale deployment
* Ethical considerations (face analysis) not production-hardened

These were accepted trade-offs given hackathon time constraints.

---

## 🔮 Future Improvements

* Modular backend service layer
* Async processing for scraping & inference
* Dataset-based personalization
* Model benchmarking & explainability
* Deployment-ready architecture (desktop → web)
* Stronger privacy & consent workflows

---

## 🎯 Key Takeaway

This project demonstrates how **AI can be designed not just to be powerful, but meaningful** — supporting education, sustainability, and creative expression.

While intentionally kept **general and minimal**, the architecture provides a strong foundation for real-world expansion.

---

## 📜 License

This project is released for **academic, research, and learning purposes**.

---

> *Built with curiosity, constraints, and conviction during Daksh 2025.*
