# 🎓 HomeworkClass

[![Polish](https://img.shields.io/badge/Język-Polski-red)](#pl)
[![English](https://img.shields.io/badge/Language-English-blue)](#en)

---
<a id="pl"></a>
## 🔴 Wersja Polska 🔴
Aplikacja webowa symulująca relację nauczyciel–uczeń. 
Pozwala ona zarówno na tworzenie klas, jak i zadań dla uczniów, które uczniowie muszą odesłać, a nauczyciel je ocenia.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092e20.svg?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Cloudinary](https://img.shields.io/badge/Cloudinary-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)

### 🤖 Użycie AI i Tutoriali
Podczas tworzenia projektu używałem sztucznej inteligencji (Gemini).  
Asystowała mi przy tworzeniu projektu - w tym hostingu.

### ⚙️ Działanie i funkcje
1. System Kont: Rejestracja i logowanie z wykorzystaniem wbudowanego systemu Django.
2. CRUD dla Klas i Zadań: Nauczyciele mogą tworzyć i edytować zarówno klasy, jak i zadania - mogą też oceniać wysłane zadania.
3. Wysyłanie Plików: Uczniowie oddają swoje zadania jako plik - ten następnie trafia do chmury (Cloudinary).

**Spróbuj sam:**
[Homework class](https://homeworkclass.up.railway.app/)
Przykładowe Konto Nauczyciela:
login: Prof
hasło: ToJestNauczyciel

**Jak to Działa:**
<img width="952" height="678" alt="image" src="https://github.com/user-attachments/assets/44cbc7fa-81ed-41a9-bca7-3ae7e81dbea8" />

### 🚀 Project Roadmap
- [x] Backend (Klasy Bazy Danych, Podstawowa Logika, CRUD)
- [x] Tailwind CSS i UI
  - [x] Strona Główna
  - [x] Strona Klas
  - [x] Strona Zadań
  - [x] Strona Wysyłania Zadań i Edycji
- [x] Ostatnie Szlify (Leprze UI, Zmiany w HTMX)
- [x] Chmura na Rozwiązania Uczniów (Cloudinary)
- [x] Upublicznienie - Railway 🚂
- [ ] Polskie Znaki
- [ ] Wyjątki
- [ ] Pop-upy

### 🏭 Struktura Projektu
```text
📦 Katalog główny projektu
├── application/                   # Folder Aplikacji
│   ├── utils/                     # Skrypt Pomocnicze (gpa, code generator)
│   ├── templates/                 # Frontend
│   ├── modles.py                  # Klasy dla SQL
│   └── views.py                   # Logika Aplikacji
│  
├── homeworkclass/                 # Konfiguracja Projektu
├── static                         # Pliki Statyczne
├── manage.py                      # Skrypt Startu
├── requirements.txt               # Zależności Projektu
├── Procfile                       # Konfiguracja Dla Hostingu
└── README.md                      # O Projekcie
```

---

<a id="en"></a>
## 🔵 English Version 🔵
Web application that simulates a student-teacher relationship.
Teachers can create classes and assignments for students to upload, which are then graded accordingly.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092e20.svg?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Cloudinary](https://img.shields.io/badge/Cloudinary-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)

### 🤖 AI Usage and Tutorials
I used AI (Gemini) during the creation of this project.  
It assisted me during the creation of this project - hosting included.

### ⚙️ Functions
1. Account System: Account registration and login with basic Django auth system.
2. Class and Assignment CRUD: Teachers can create and edit both classes and assignments, they also can grade the assignments. 
3. File Upload: Students can upload their answers via file - which then goes to the cloud (Cloudinary).

**Try for yourself:** 
[Homework class](https://homeworkclass.up.railway.app/)
Sample Teacher's Account:
login: Prof
password: ToJestNauczyciel

**How it Works:**
<img width="952" height="678" alt="image" src="https://github.com/user-attachments/assets/d681c883-f554-41c7-9958-3a79defc3120" />

### 🚀 Project Roadmap
- [x] Backend Logic (Db Classes, Basic Logic and CRUD)
- [x] Tailwind CSS and UI
  - [x] Main Page
  - [x] Classes Page
  - [x] Homeworks Page
  - [x] Homework Upload and Edit Page
- [x] Final Changes (Better UI, HTMX Changes)
- [x] Cloud for Student Uploads (Cloudinary)
- [x] Public launch - Railway 🚂
- [ ] Polish Chars
- [ ] Exceptions
- [ ] Pop-ups

### 🏭 Project structure
```text
📦 Project Main Directory
├── application/                   # App folder
│   ├── utils/                     # Additional scripts (gpa, code generator)
│   ├── templates/                 # Frontend code
│   ├── modles.py                  # Classes for SQL
│   └── views.py                   # Logic of the app
│  
├── homeworkclass/                 # Project config
├── static                         # Static Files
├── manage.py                      # Main starting script
├── requirements.txt               # Project requirements
├── Procfile                       # host config
└── README.md                      # About the project
```
