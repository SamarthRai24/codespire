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

Follow these steps to set up and run the project on your local machine.

### Prerequisites

* Python 3.8+ installed
* A stable internet connection (for API calls)



### 1. Clone the Repository

Bash
git clone [https://github.com/SamarthRai24/codespire.git](https://github.com/SamarthRai24/codespire.git)
cd codespire



### 2. Install Dependencies
Install all necessary libraries:

Bash
pip install -r requirements.txt
(Note: If you do not have a requirements.txt file, manually install the key libraries: pip install streamlit google-genai sounddevice wavio gtts speechrecognition streamlit-lottie requests)



### 3. Configure API Key (Crucial)
Open the app.py file and replace the placeholder with your actual new and secure Google Gemini API Key.

Python
GEMINI_API_KEY = "API KEY" 



### 4. Run the Application
Execute the following command in your terminal:

Bash
streamlit run app.py
The application will launch in your default web browser (usually at http://localhost:8501).



## 🛠️ Tech Stack
### Frontend/Deployment: Streamlit
### AI/LLM: Google Gemini API
### Language: Python
### Key Libraries: gTTS, sounddevice, speechrecognition, streamlit_lottie