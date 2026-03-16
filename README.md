# Notes Sharing API

## 📌 Project Overview

A full-stack web application for uploading and sharing notes publicly or privately.
Users can upload notes, download them, view public notes from other users, and even ask AI questions related to an uploaded note.

The project demonstrates secure backend architecture, authentication, file handling, pagination, and AI integration using a modern tech stack.

---
## 🌐 Live Demo

Frontend:
👉 https://notes-sharing-frontend-taupe.vercel.app/

Backend API:
👉 https://notes-sharing-api-9tma.onrender.com/docs

---

### 🚀 Features

## 👤 User Features

- User registration and login
- Upload notes
- Download uploaded notes
- Share notes publicly or privately
- View public notes from other users
- Ask AI questions about uploaded notes

## ⚙️ System Features

- JWT Authentication for secure access
- Protected routes for private notes
- Clean pagination for listing notes
- Search functionality in both public and private notes
- AI-powered question answering for notes
- Structured backend using FastAPI best practices

---

## Tech Stack

Backend
- Python
- FastAPI
- SQLAlchemy
- JWT
- OAuth

Frontend:
- React
- Tailwind CSS

Database:
- PostgreSQL

---

## 📦 Deployment

The project is fully deployed:
Frontend deployed on: Vercel
Backend API deployed on: Render
Database hosted on: Render PostgreSQL

---

## ⚙️ Installation (Local Setup)

If you want to run the project locally:

## 1️⃣ Clone the Repository
```bash
git clone https://github.com/Vaishnavi-020/Notes-Sharing-API.git
cd notes-sharing-api
```
---

## 2️⃣ Backend Setup
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend will run on:
http://localhost:8000

Swagger Docs:
http://localhost:8000/docs

---

## 3️⃣ Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend will run on:
http://localhost:5173

---

## 🔐 Authentication

The application uses:
- JWT access tokens
- Protected routes
- User-specific note access

---

## 🧠 AI Integration

Users can ask questions related to a particular uploaded note, and the system processes the note content to generate relevant responses.

---

## 📈 Future Improvements

- Docker containerization
- CI/CD pipeline
- Improved AI summarization

---

## 👩‍💻 Author
Vaishnavi Sinha