# ☂️ Umbrella Onboarding Assistant – RAG + Voice-Enabled Chatbot

## A **RAG-based (Retrieval-Augmented Generation)** assistant designed for **Umbrella Corporation** to streamline **employee onboarding**. It guides new hires through company policies, role-specific details, and procedures — supporting both **text and voice-based** interaction

## 🚀 Overview

The assistant integrates **LangChain + Groq Llama** for contextual conversation and combines **speech recognition (Whisper)** and **text-to-speech (gTTS + pyttsx3)** for a fully interactive onboarding experience.

It uses **PostgreSQL + SQLAlchemy** for structured employee/auth data, and **ChromaDB** for RAG retrieval from internal documents such as the `umbrella_corp_policies.pdf`.

---

## 🎯 Problem Statement

New employees joining large organizations face several challenges during onboarding:

- **Information Overload:** Lengthy employee handbooks and policy documents are overwhelming

- **Delayed Responses:** HR teams can't provide instant answers to common questions 24/7

- **Generic Experience:** One-size-fits-all onboarding doesn't account for department-specific needs

- **Accessibility:** Important information is scattered across multiple documents and portals

- **Language Barriers:** Reading complex documents is time-consuming; voice interaction is more natural

The Challenge: How do we create an intelligent, personalized, and accessible onboarding experience that provides instant, accurate answers while reducing the burden on HR teams?

---

## 💡 Solution Overview

The Umbrella Corporation AI Onboarding Assistant is an intelligent chatbot that:

- Provides instant answers to employee questions about company policies, benefits, and procedures

- Personalizes responses based on employee role, department, and profile information

- Supports voice interaction for hands-free, natural communication

- Uses RAG (Retrieval-Augmented Generation) to ensure accurate, policy-based responses

- Maintains conversation context for multi-turn dialogues

- Authenticates users to provide secure, personalized information

---

## How It Works?

- Employee logs in with their credentials

- Assistant retrieves employee profile (name, role, department, supervisor)

- Employee asks a question via text or voice input

- RAG system searches relevant company policies from the vector database

- LLM generates a personalized response based on retrieved context + employee info

- Response is delivered as text and optionally as audio (auto-plays for voice queries)

---

## ✨ Key Features

### 🤖 Intelligent Conversational AI

RAG-based responses using company policy documents
Context-aware answers personalized to employee role and department
Multi-turn conversations with maintained history
Streaming responses for real-time feedback

### 🎤 Voice Interaction

Speech-to-Text: Record questions using your microphone (Groq Whisper API)
Text-to-Speech: Hear responses with natural voice synthesis (gTTS/pyttsx3)
Smart Audio Control:

Text queries: Audio available, manual playback
Voice queries: Audio auto-plays for natural conversation flow

### 🔐 Authentication & Personalization

Secure login/signup with password hashing (bcrypt)
PostgreSQL database for user and employee data
Role-based responses tailored to department and position
Session management for secure, persistent sessions

### 🎨 Professional UI/UX

Modern Streamlit interface with dark theme
Fixed voice input bar always accessible at the bottom
Smooth animations and responsive design
Real-time status indicators for processing feedback
Chat history with user and AI message distinction

### 🗂️ Document Processing

PDF ingestion of company policies
Vector storage using Chroma DB for fast retrieval
Semantic search to find most relevant policy sections

---

## 🏗️ Architecture

### 1) High-Level Architecture

![High-Level Architecture](assets/diagrams/High_Level_Architecture.png)

The system consists of four main layers:

- Presentation Layer: Streamlit UI with voice input capabilities
- Application Layer: Business logic, authentication, session management
- Data Layer: PostgreSQL for structured data, Vector DB for document embeddings
- External Services: Groq API (LLM + STT), gTTS (TTS)

### 2) Assistant Orchestration Flow

![Assistant Orchestration Flow](assets/diagrams/Assistant_Orchestration.png)

Detailed Flow:

- User Input: Text typed or voice recorded
- Speech-to-Text (if voice): Audio → Groq Whisper → Text
- Context Building: Combine system prompt + employee info + user query
- RAG Retrieval: Search vector DB for relevant policy chunks
- LLM Generation: ChatGroq (Llama 3.3) generates response with retrieved context
- Text-to-Speech: Response text → gTTS/pyttsx3 → Audio bytes
- UI Rendering: Display text + audio player with conditional autoplay

### 3) Data Model

![Data Model](assets/diagrams/Data_Model.png)

Tables:

- users: Authentication (email, password_hash, created_at)
- employees: Profile information (name, role, department, supervisor, skills, etc.)
- Relationship: 1-to-1 mapping via email

---

## 🛠️ Technology Stack

### Core Technologies

| **Category** | **Technology** | **Purpose** |
|---------------|----------------|--------------|
| **Frontend** | Streamlit | Interactive web UI |
| **Backend** | Python 3.8+ | Application logic |
| **LLM** | ChatGroq (Llama 3.3 70B) | Conversational AI |
| **STT** | Groq Whisper Large v3 | Speech-to-text |
| **TTS** | gTTS + pyttsx3 | Text-to-speech |
| **Database** | PostgreSQL | User / employee data |
| **Vector DB** | Chroma DB | Document embeddings |
| **Auth** | bcrypt | Password hashing |
| **ORM** | SQLAlchemy | Database interactions |

---

## 📁 Project Structure

```bash
CLIENT_ONBOARDING_RAG_CHATBOT/
│
├── assets/
│   ├── diagrams/                   # Architecture diagrams
│   │   ├── Assistant_Orchestration.png
│   │   ├── Data_Model_Auth_and_Employees.png
│   │   └── High_Level_Architecture.png
│   └── ui_screens/                 # UI screenshots (add your screenshots here)
│
├── auth/
│   ├── __init__.py
│   ├── auth_utils.py               # Password hashing utilities
│   ├── login.py                    # Login page logic
│   └── signup.py                   # Signup page logic
│
├── data/
│   ├── vectorstore/                # Chroma DB vector storage
│   ├── __init__.py
│   ├── employees.py                # Employee data seeding
│   ├── questions.txt               # Sample questions
│   └── umbrella_corp_policies.pdf  # Company policy document
│
├── database/
│   ├── __init__.py
│   ├── db.py                       # Database connection & models
│   ├── seed_employees.py           # Seed employee data
│   └── test_db_conn.py             # Test DB connection
│
├── voice/
│   ├── __init__.py
│   ├── speech_to_text.py           # Groq Whisper STT
│   └── text_to_speech.py           # gTTS/pyttsx3 TTS
│
├── app.py                          # Main Streamlit application
├── assistant.py                    # LLM orchestration logic
├── gui.py                          # UI components & rendering
├── prompt.py                       # System prompts
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (not in repo)
├── .gitignore
└── README.md                       # This file

```

---

## 🚀 Installation

### Prerequisites

Python 3.8 or higher
PostgreSQL 12+ installed and running
Groq API key (Get it here)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Client-Onboarding-RAG-Chatbot.git
cd Client-Onboarding-RAG-Chatbot
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

### On Windows

venv\Scripts\activate

### On macOS/Linux

source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up PostgreSQL Database

```bash
# Create database
createdb umbrella_db

### Or using psql

psql -U postgres
CREATE DATABASE umbrella_db;
\q
```

### Step 5: Configure Environment Variables

Create a .env file in the project root:

```bash
env# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

### Database Configuration

DATABASE_URL=postgresql://username:password@localhost:5432/umbrella_db

### Optional: Specify if using different host/port

DB_HOST=localhost
DB_PORT=5432
DB_NAME=umbrella_db
DB_USER=your_db_username
DB_PASSWORD=your_db_password
```

### Step 6: Initialize Database

```bash
# Test database connection
python database/test_db_conn.py

### Seed employee data

python database/seed_employees.py
```

### Step 7: Run the Application

```bash
streamlit run app.py
The application will open in your browser at http://localhost:8501
```

---

## ⚙️ Configuration

### Environment Variables

| **Variable** | **Description** | **Required** | **Default** |
|---------------|----------------|---------------|--------------|
| `GROQ_API_KEY` | Groq API key for LLM and STT | ✅ Yes | - |
| `DATABASE_URL` | PostgreSQL connection string | ✅ Yes | - |
| `DB_HOST` | Database host | ❌ No | `localhost` |
| `DB_PORT` | Database port | ❌ No | `5432` |
| `DB_NAME` | Database name | ❌ No | `umbrella_db` |
| `DB_USER` | Database username | ❌ No | `postgres` |
| `DB_PASSWORD` | Database password | ❌ No | - |

Create a `.env` file in the project root and configure your credentials:

```bash
# .env

GROQ_API_KEY=your_groq_api_key_here

DATABASE_URL=postgresql+psycopg2://postgres:yourpassword@localhost:5432/umbrella_db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=umbrella_db
DB_USER=postgres
DB_PASSWORD=yourpassword
```

---

## 🧠 Model Configuration

To change or upgrade the LLM model, edit the model name in assistant.py:

```bash
# Default: ChatGroq with Llama 3.3 70B
llm = ChatGroq(model="llama-3.3-70b-versatile")

# Alternative models:
# llm = ChatGroq(model="llama-3.1-8b-instant")
```

💡 Tip:

Use llama-3.3-70b-versatile for high reasoning accuracy and context-rich onboarding queries.

Use llama-3.1-8b-instant for faster response times during local testing.

---

## 🧩 Database Setup

If PostgreSQL isn’t already initialized, run:

```bash
python -m database.seed_employees
```

This will create necessary tables and seed employee data used for login validation.

## ✅ Verification

Once the .env is set and DB seeded, test the connection:

```bash
python -m database.test_db_conn
```

Expected output:

✅ Database Connected Successfully

---

## 📖 Usage

### 1. Sign Up

Click "Sign Up" in the sidebar
Enter your email and password
Your account is created, but you need an employee profile to use the assistant

### 2. Login

Select "Login" in the sidebar
Enter your credentials
The system loads your employee profile

### 3. Ask Questions (Text)

Type your question in the chat input at the bottom
Press Enter or click the send button
The assistant responds with personalized information
Audio player appears (manual control)

### 4. Ask Questions (Voice)

Expand "🎙️ Voice input (optional)" section
Click the microphone icon
Speak your question clearly
Stop recording
Wait for transcription
The assistant responds
Audio plays automatically

### 5. Sample Questions

- What are my job responsibilities?

- What are the company benefits?

- What is the vacation policy?

- Who is my supervisor?

- What is the dress code?

- How do I request time off?

- What safety procedures should I know?

---

## 📸 UI Walkthrough (Screens)

### Below is a step-by-step visual overview of the **Umbrella Onboarding Assistant** interface

---

### 🟢 1. Application Launch — Database Connection

![App Launch](assets/ui_screens/1.png)
The application initializes with a connected PostgreSQL database status, confirming a secure backend link before interaction.

---

### 🔐 2. Employee Login Screen

![Login Screen](assets/ui_screens/2.png)
Employees can log in using their corporate email and password. Credentials are securely validated via the authentication module (`bcrypt + SQLAlchemy`).

---

### 🆕 3. Employee Registration Screen

![Sign Up Screen](assets/ui_screens/3.png)
New employees can register using their corporate email and a secure password. The form includes password confirmation with masked entry fields.

---

### ✅ 4. Successful Login

![Successful Login](assets/ui_screens/4.png)
After authentication, a success alert confirms a verified connection to the employee database and grants access to the internal assistant dashboard.

---

### 🧭 5. Onboarding Dashboard – Welcome View

![Welcome View](assets/ui_screens/5.png)
The assistant greets the logged-in employee and outlines usage instructions and corporate compliance reminders. Employee metadata is dynamically fetched and displayed in the sidebar.

---

### 🧩 6. Chat Interface – Default Mode

![Chat Interface](assets/ui_screens/6.png)
Main conversational UI with integrated chat input, optional voice capture, and real-time assistant response rendering. The design maintains contextual awareness of the employee profile.

---

### 🎙️ 7. Voice Interaction & Response

![Voice Mode](assets/ui_screens/7.png)
Voice input feature (Groq Whisper STT) allows employees to speak queries. The assistant transcribes, processes, and replies via text and optional TTS playback.

---

### 🧠 8. Contextual Policy Response

![Policy Response](assets/ui_screens/8.png)
Example of an employee query regarding sensitive or confidential data (e.g., SSN).  
The chatbot maintains strict privacy compliance — it does **not** disclose personal or secure employee information and instead politely redirects the user to contact the HR department for such inquiries.

---

### 🩺 9. Conversational Memory & Long-form Support

![Conversation Flow](assets/ui_screens/9.png)
Demonstrates the assistant’s ability to maintain long-form conversational memory — seamlessly preserving context across multiple queries (e.g., HR, SSN, wellness, and benefits).  
It provides empathetic, policy-compliant responses while ensuring privacy, along with synchronized text and audio playback for a natural, human-like support experience.

---

## 🗄️ Database Schema

```bash
Users Table
sqlCREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Employees Table
sqlCREATE TABLE employees (
    employee_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    position VARCHAR(100),
    department VARCHAR(100),
    supervisor VARCHAR(100),
    location VARCHAR(100),
    hire_date DATE,
    salary DECIMAL(10, 2),
    skills TEXT[],
    FOREIGN KEY (email) REFERENCES users(email)
);
```

### Sample Data

The system comes pre-seeded with 50 employee records across various departments:

- R&D: Research Scientists, Lab Technicians
- Security: Security Officers, Guards
- Operations: Managers, Coordinators
- IT: Software Engineers, System Admins
- HR: HR Specialists, Recruiters

---

## 🔌 API Integrations

### Groq API

### Endpoints Used

#### 1. Chat Completions (LLM)

- Model: llama-3.3-70b-versatile
- Streaming: Yes
- Purpose: Generate conversational responses

#### 2. Audio Transcriptions (STT)

- Model: whisper-large-v3
- Format: WAV audio
- Purpose: Convert voice to text

### Rate Limits

- Free tier: 30 requests/minute
- Check Groq Console for your limits

### Google Text-to-Speech (gTTS)

- Purpose: Convert response text to audio
- Language: English (en)
- Fallback: pyttsx3 (offline TTS)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

## 🧭 Future Enhancements

### 📁 Integration with SharePoint/Confluence for live document retrieval

### 🧠 Fine-tuned domain-specific LLM responses

### 🌐 Multi-language STT + TTS

### 🔊 Continuous conversation mode for voice

### 🧩 HR analytics dashboard for query insights

---

### Built with ❤️ for better employee onboarding experiences
