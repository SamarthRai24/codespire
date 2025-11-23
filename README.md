# 🎓 AITR Helper: Gemini-Powered Student Assistant

**A Streamlit-based web application designed as an all-in-one student helper. It uses the Google Gemini API for powerful features like AI Study Notes generation, a custom Exam Study Planner, and a specialized AITR College Chatbot.**

---

## ✨ Features

This application provides three core functionalities tailored for student academic support:

1.  **✍️ AI Study Notes Generator:**
    * Generates **concise and clear study notes** from any topic or text input.
    * Includes **Voice Input** support for hands-free topic submission.
    * Allows listening to generated notes using **Text-to-Speech (TTS)** functionality.

2.  **🗓️ Custom Exam Study Planner:**
    * Creates a **balanced, detailed daily study schedule** based on the subjects and days remaining until the exam.
    * Subjects can be added via **text input or voice recognition**.

3.  **🏫 AITR College Chatbot:**
    * A **context-aware conversational chatbot** powered by the Gemini AI model.
    * Programmed to provide focused information specifically about **Acropolis Institute of Technology and Research (AITR)**, Indore.

---

## 🚀 Setup and Run Locally

Follow these steps to set up and create a live website through streamlit

### Prerequisites

* Python 3.8+ installed
* A stable internet connection (for API calls)



### 1. Clone the Repository



### 2. Install Dependencies
Install all necessary libraries:

Bash
pip install -r requirements.txt



### ☁️ Deployment Guide (deployment branch)
For the Live Website on Streamlit Cloud, the application is run from the deployment branch. This branch contains a modified version where audio libraries are disabled for server compatibility.

Requirements: Audio libraries (PyAudio, sounddevice) are commented out for smooth cloud installation.

(app.py): Commented out all the part that hold the voice and listen feature.

API Key: Streamlit Secrets are used to securely load the GEMINI_API_KEY.



## 🛠️ Tech Stack
### Frontend/Deployment: Streamlit
### AI/LLM: Google Gemini API
### Language: Python