# 🐝 Contributing to InterviewHive

Thanks for your interest in contributing to **InterviewHive**!

InterviewHive is an AI-powered adaptive technical interview platform. Contributions are welcome across the **frontend, backend, AI agents, UI/UX, testing, and documentation**.

## 🚀 Getting Started

### 1. Fork & Clone

```bash
git clone https://github.com/bhumi110/InterviewHive.git
cd InterviewHive
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## 🌿 Branches

Create a branch for your contribution:

```bash
git checkout -b feature/your-feature
```

Examples:

```text
feature/improve-report-ui
feature/better-question-generation
fix/resume-parser
docs/update-readme
```

## 💡 What You Can Contribute

* 🧠 Improve AI agents and interview logic
* 🎨 Improve UI/UX and PixiJS experience
* 🐛 Fix bugs
* 📄 Improve resume parsing
* 📊 Improve interview reports
* 🧪 Add tests
* 📚 Improve documentation

## 🔀 Pull Requests

Before submitting a PR:

* Test your changes locally
* Keep the PR focused
* Explain what you changed and why
* Add screenshots for UI changes
* Make sure no API keys or secrets are committed

Use clear commit messages:

```text
feat: improve adaptive interview logic
fix: handle invalid evaluator response
docs: update setup instructions
```

## 🔐 Important

**Never commit your `.env` file or API keys.**

## 🤝 Code of Conduct

Please be respectful, constructive, and welcoming to other contributors.


⭐ Thanks for helping improve **InterviewHive**!
