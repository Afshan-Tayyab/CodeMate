# 💻 CodeMate – Code Learning & Analysis Platform

**CodeMate** is a code learning and analysis platform designed to help beginners understand their code, analyze its structure, and learn what each part does. It provides code analysis, syntax checking for Python, basic analysis for other supported languages, explanations, and analysis history through a simple web interface.

## 🚀 Features

* **Multi-language Support:** Python, JavaScript, Java, C++, and C.
* **Code Analysis:** Counts lines, functions, loops, and variables.
* **Syntax Status:** Detects Python syntax errors and provides basic analysis status for other supported languages.
* **Code Explanation:** Explains code statements and provides an overall program explanation.
* **Error Detection:** Displays detected errors for supported analysis.
* **Analysis History:** Stores previous analyses using SQLite.
* **Delete History:** Allows saved analysis entries to be deleted.
* **Interactive Web Interface:** Simple frontend to enter, analyze, and understand code.
* **REST API:** FastAPI backend for processing code analysis requests.

## 🛠️ Tech Stack

| Technology   | Purpose                                 |
| ------------ | --------------------------------------- |
| HTML5        | Web page structure                      |
| CSS3         | Styling and responsive design           |
| JavaScript   | Frontend interaction and API requests   |
| Python       | Backend logic and code analysis         |
| FastAPI      | REST API and frontend serving           |
| SQLite       | Storing analysis history                |
| Git & GitHub | Version control and source-code hosting |

## 📂 Project Structure

```text
CodeMate/
│
├── README.md
│
└── backend/
    ├── frontend/
    │   ├── index.html
    │   ├── style.css
    │   └── script.js
    │
    ├── main.py
    ├── database.py
    ├── requirements.txt
    ├── .gitignore
    └── codemate.db
```

> `codemate.db` is generated locally when the application runs and is not intended to be committed to GitHub.

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Afshan-Tayyab/CodeMate.git
```

### 2. Navigate to the Project

```bash
cd CodeMate
cd backend
```

### 3. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python -m uvicorn main:app --reload
```

## 🌐 Access CodeMate

Once the server is running, open these URLs in your browser:

* **CodeMate Website:** http://127.0.0.1:8000/
* **API Documentation:** http://127.0.0.1:8000/docs

## 🔍 API Endpoints

| Method | Endpoint                | Description                  |
| ------ | ----------------------- | ---------------------------- |
| POST   | `/analyze`              | Analyzes submitted code      |
| GET    | `/history`              | Retrieves analysis history   |
| DELETE | `/history/{history_id}` | Deletes a history entry      |
| GET    | `/`                     | Serves the CodeMate frontend |

### Example API Request

**POST `/analyze`**

```json
{
  "language": "python",
  "code": "x = 10\nfor i in range(5):\n    print(i)"
}
```

The API returns analysis details such as line count, functions, loops, variables, syntax status, detected errors, and code explanations.

## 🖥️ How to Use

1. Start the FastAPI server.
2. Open CodeMate in your browser.
3. Select a programming language.
4. Enter or paste your code into the editor.
5. Click **Analyze Code**.
6. Review the code statistics, syntax status, explanation, and errors.
7. View previous analyses in the Analysis History section.

## 🎯 Project Objective

The objective of CodeMate is to make programming easier for beginners by helping them understand code structure and program behavior. It brings basic code analysis and learning support into one accessible platform.

## 🔮 Future Improvements

* Add support for HTML and CSS analysis.
* Improve syntax and error detection for additional languages.
* Provide more detailed, line-by-line explanations.
* Add code formatting and syntax highlighting.
* Improve the analysis interface and learning experience.
* Explore AI-powered explanations as a future enhancement.

## 👩‍💻 Developer

**Afshan Tayyab**
B.Tech – Computer Science and Engineering
Interests: Python, Web Development, Backend Development, and Software Projects.

## 📜 License

This project is intended for educational and learning purposes. A license can be added to the repository if the project is distributed for reuse.

