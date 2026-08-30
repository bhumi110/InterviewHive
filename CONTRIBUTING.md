# 🤝 Contributing to InterviewHive

Thank you for your interest in contributing to **InterviewHive**! 🐝

InterviewHive is an AI-powered adaptive technical interview platform that uses specialized AI agents to simulate an interactive interview experience.

Contributions are welcome across the entire project, from AI agents and prompts to backend improvements, frontend experiences, testing, documentation, and UI/UX.



## 🌟 Ways You Can Contribute

There are many ways to contribute to InterviewHive:

* 🤖 Improve existing AI agents
* 🧠 Create new interview agents
* ✍️ Improve prompts and evaluation criteria
* 🎯 Improve adaptive question selection
* 📈 Improve answer evaluation
* 🔍 Improve semantic question similarity
* 📄 Improve resume parsing
* ⚡ Improve backend performance
* 🎨 Improve the React/PixiJS interface
* 🧪 Add tests
* 🐛 Fix bugs
* 📚 Improve documentation
* 💡 Suggest new features


## 🏗️ Project Structure

InterviewHive is divided into three main areas:

```text
InterviewHive/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── pixi/
│   │   ├── services/
│   │   └── App.jsx
│   │
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── models/
│   │   ├── prompts/
│   │   ├── services/
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── notebooks/
├── tests/
├── README.md
└── CONTRIBUTING.md
```

### Backend

The backend contains the interview logic, API routes, resume processing, AI agents, question generation, evaluation, and final reporting.

### Frontend

The frontend contains the user interface, interview screens, report visualization, API communication, and PixiJS-based interview-room experience.

### Notebooks

The notebooks contain experimentation and development work related to areas such as role analysis, question generation, and answer evaluation.

## 🤖 AI Agent Architecture

InterviewHive uses multiple specialized agents rather than relying on a single LLM call.

```text
                    Candidate
                        │
                        ▼
                 Resume Analysis
                        │
                        ▼
                 Interview Manager
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        Question Generator     Interviewer
              │                   │
              └─────────┬─────────┘
                        ▼
                  Candidate Answer
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
           Evaluator           Skeptic
              │                   │
              └─────────┬─────────┘
                        ▼
                 Manager Decision
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        Follow-up/Challenge    New Question
                        │
                        ▼
                  Interview Loop
                        │
                        ▼
                       Judge
                        │
                        ▼
                 Final Interview Report
```

Current agents include:

| Agent           | Responsibility                                                     |
| --------------- | ------------------------------------------------------------------ |
| **Manager**     | Controls interview flow and decides what happens next              |
| **Interviewer** | Presents questions naturally to the candidate                      |
| **Evaluator**   | Evaluates technical and communication aspects of answers           |
| **Skeptic**     | Identifies weak areas and determines whether a challenge is needed |
| **Judge**       | Generates the final interview report                               |

When contributing to an agent, try to keep each agent focused on its specific responsibility.


## 🚀 Getting Started

### 1. Fork the Repository

Fork the InterviewHive repository to your GitHub account.

Then clone your fork:

```bash
git clone https://github.com/bhumi110/InterviewHive.git
cd InterviewHive
```

## ⚙️ Backend Setup

Move into the backend directory:

```bash
cd backend
```

Create a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

Never commit your `.env` file or API keys.

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available locally at:

```text
http://localhost:8000
```


## 🎨 Frontend Setup

Open another terminal and move into the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

Make sure the frontend API configuration points to the backend you are running.

## 🌿 Creating a Contribution

Create a separate branch for your work.

For a new feature:

```bash
git checkout -b feature/feature-name
```

For a bug fix:

```bash
git checkout -b fix/bug-name
```

For documentation:

```bash
git checkout -b docs/update-name
```

Avoid making changes directly on the `main` branch.


## 🧠 Contributing to AI Agents

If you want to improve an existing agent:

```text
backend/
└── app/
    └── agents/
        ├── manager.py
        ├── interviewer.py
        ├── evaluator.py
        ├── skeptic.py
        └── judge.py
```

Before modifying an agent, understand:

1. What information the agent receives.
2. What decision or output it is responsible for.
3. Which part of the interview engine consumes its output.
4. Whether its output is validated by a Pydantic model.
5. Whether the change affects other agents.

Try to avoid putting unrelated responsibilities into an existing agent.

## ✍️ Contributing to Prompts

Prompts are stored in:

```text
backend/app/prompts/
```

Current prompts include:

```text
interviewer.txt
evaluator.txt
skeptic.txt
judge.txt
```

When improving a prompt:

* Keep the output format explicit.
* Avoid ambiguous instructions.
* Tell the model exactly what information it should evaluate.
* Prevent hallucination where factual information is required.
* Keep structured outputs compatible with the corresponding Pydantic model.
* Test the prompt with different candidate answers.

For JSON-producing agents, make sure the generated output remains valid and matches the expected schema.


## 🎯 Contributing to Question Generation

Question generation and similarity checking are handled in the backend services.

Relevant areas include:

```text
backend/app/services/
├── question_generator.py
├── interview_logic.py
└── similarity.py
```

Potential improvements include:

* Better question diversity
* Better difficulty adaptation
* Improved topic coverage
* Better duplicate detection
* More context-aware follow-up questions
* Improved semantic similarity thresholds
* Better handling of project-specific questions

When modifying question generation, test both:

```text
Normal question generation
        +
Duplicate/repetitive question prevention
```


## 📄 Contributing to Resume Parsing

Resume processing is handled by the backend resume parsing services.

Potential improvements include:

* Better PDF text extraction
* Better section detection
* Improved project extraction
* Improved education extraction
* Better handling of different resume formats
* More robust structured output validation

Do not introduce information that is not actually present in the candidate's resume.


## 🎨 Contributing to the Frontend

The frontend is built using React, with PixiJS used for the interactive interview-room experience.

Relevant areas include:

```text
frontend/src/
├── components/
├── pages/
├── pixi/
├── services/
└── styles/
```

You can contribute:

* New UI components
* Better responsive layouts
* Accessibility improvements
* Interview experience improvements
* Report visualization
* PixiJS animations
* Better loading/error states
* Micro-interactions
* Visual improvements

Keep the existing design language consistent when adding new components.


## 🧪 Testing

Before opening a Pull Request, test your changes locally.

At minimum, verify:

### Backend

```bash
uvicorn app.main:app --reload
```

Check that:

* The API starts successfully.
* Resume upload works.
* Interview sessions can be created.
* Questions are generated correctly.
* Answers are evaluated.
* Challenge questions work.
* Interviews can be completed.
* Final reports are generated.

### Frontend

```bash
npm run dev
```

Check that:

* Pages load correctly.
* API requests work.
* Interview flow works from beginning to end.
* Loading states work.
* Errors are handled gracefully.
* The UI remains responsive.



## 🐛 Reporting Bugs

Found a bug?

Please open a GitHub Issue with:

### Description

Clearly explain what went wrong.

### Steps to Reproduce

```text
1. Open...
2. Select...
3. Upload...
4. Submit...
5. Observe...
```

### Expected Behavior

Explain what should have happened.

### Actual Behavior

Explain what happened instead.

### Additional Information

Include relevant:

* Error messages
* Console logs
* Screenshots
* API responses
* Browser information

**Never include API keys or other secrets in an issue.**


## 💡 Suggesting Features

Have an idea for InterviewHive?

Open an Issue and describe:

### Problem

What problem does the feature solve?

### Proposed Solution

What would you like InterviewHive to do?

### Why It Helps

Explain how it improves the interview experience.

### Optional Implementation Idea

If you have an idea about how it could be implemented, include it.



## 📋 Pull Request Guidelines

Before opening a Pull Request:

* Make sure your branch is up to date.
* Test your changes locally.
* Keep the Pull Request focused.
* Avoid unrelated changes.
* Update documentation when necessary.
* Add screenshots for significant UI changes.
* Do not commit secrets or `.env` files.

A good Pull Request should explain:

```text
What changed?
Why was it changed?
How was it tested?
```

## 📝 Commit Messages

Use clear and descriptive commit messages.

Examples:

```text
feat: add project-based interview questions
```

```text
fix: handle malformed evaluator JSON
```

```text
feat: improve adaptive difficulty logic
```

```text
fix: prevent duplicate interview questions
```

```text
ui: improve interview report layout
```

```text
docs: update setup instructions
```


## 🔐 Security

Never commit:

```text
.env
API keys
Access tokens
Private credentials
```

Use environment variables instead:

```env
GROQ_API_KEY=your_api_key
```

If you accidentally expose a secret, revoke or rotate it immediately.


## 🌱 Development Philosophy

InterviewHive is designed around the idea that an interview should feel **adaptive rather than scripted**.

When contributing, prefer solutions that improve:

* Personalization
* Adaptability
* Question quality
* Evaluation quality
* Interview realism
* Explainability
* User experience

Avoid adding complexity unless it provides a meaningful improvement.

---

## 🙌 Contributors

Every contribution matters.

Whether you:

* Fix a typo
* Improve a prompt
* Add a test
* Improve the UI
* Build a new agent
* Improve the interview engine
* Fix a bug
* Suggest an idea

—you are helping make InterviewHive better.

Thank you for contributing! 🐝

## ⭐ Support the Project

If you find InterviewHive useful or interesting, consider giving the repository a ⭐ on GitHub.

Your support helps the project reach more developers and contributors.

Happy building! 🚀
