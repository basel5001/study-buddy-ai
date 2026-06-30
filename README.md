![Security](https://github.com/basel5001/study-buddy-ai/actions/workflows/security.yml/badge.svg)
![CI](https://github.com/basel5001/study-buddy-ai/actions/workflows/ci.yml/badge.svg)

# Study Buddy AI

React-based quiz generation frontend for turning study material into multiple-choice quizzes using an external AI backend.

[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![Amazon Bedrock](https://img.shields.io/badge/Amazon-Bedrock-FF9900?logo=amazonaws&logoColor=white)](https://aws.amazon.com/bedrock/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

## What This Repo Is

This repository contains the frontend application for Study Buddy. Users can paste study notes, choose quiz settings, submit content to an API, and answer generated multiple-choice questions in the browser.

The AI generation backend is not included in this repository.

## Features

- paste study material directly into the app
- choose quiz difficulty and number of questions
- submit content to a quiz-generation API
- answer questions interactively in the browser
- review score and explanations after submission
- build and serve the frontend with Docker and Nginx

## Architecture

```text
Browser UI -> React frontend -> quiz generation API -> AI model provider
```

## Tech Stack

- React
- Create React App
- Fetch API
- Docker
- Nginx
- Amazon Bedrock test script in `test_bedrock.py`

## Project Structure

```text
.
├── public/
├── src/
│   ├── App.js
│   ├── App.css
│   ├── App.test.js
│   └── utils/
├── Dockerfile
├── nginx.conf
├── test_bedrock.py
└── package.json
```

## Prerequisites

- Node.js 18+
- npm
- a running backend API that exposes `POST /generate-quiz`

## Local Development

```bash
git clone https://github.com/basel5001/study-buddy-ai.git
cd study-buddy-ai
npm install
cp .env.example .env
npm start
```

Open `http://localhost:3000` in your browser.

## Environment Variables

| Variable | Description |
| :--- | :--- |
| `REACT_APP_API_URL` | Base URL for the quiz-generation backend API |

Example:

```env
REACT_APP_API_URL=http://localhost:8000
```

## Expected Backend Contract

The frontend sends:

```json
{
  "text": "study material",
  "numQuestions": 5,
  "difficulty": "medium",
  "type": "multiple-choice"
}
```

The frontend expects a response shaped like:

```json
{
  "questions": [
    {
      "question": "...",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "correctAnswer": "A",
      "explanation": "..."
    }
  ]
}
```

## Docker

Build and run the production image:

```bash
docker build -t study-buddy-ai .
docker run -p 80:80 study-buddy-ai
```

## Bedrock Test Script

`test_bedrock.py` is a standalone script for verifying Amazon Bedrock access from Python. It is not part of the frontend runtime.

Run it separately only if you have AWS credentials and Bedrock model access configured.

## Known Limitations

- file upload UI exists, but this repository does not include file parsing logic or backend ingestion
- the backend implementation is not included here
- there are no screenshots or demo assets yet

## Recommended Next Improvements

- add screenshots or a short demo GIF
- publish or link the backend API repository if it exists
- add basic API error state improvements in the UI

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE).
