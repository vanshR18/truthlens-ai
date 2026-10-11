# 🔎 TruthLens AI — News Summarization & Fact-Checking System

TruthLens AI is a Python-based web application that helps users understand current news more quickly by retrieving news articles, generating concise summaries, and searching existing fact-checks related to a topic.

Built with Streamlit, the application provides a simple interactive dashboard where users can search for topics such as Chandrayaan, ISRO, and India space mission, read article summaries, access original news sources, and investigate whether claims have previously been reviewed by fact-checking organizations.

* **Project type:** Academic Mini-Project
* **Domain:** Artificial Intelligence, Natural Language Processing (NLP), and Information Retrieval
* **Interface:** Streamlit
* **Language:** Python

---

## 📌 Table of Contents

1. [Overview](#-overview)
2. [Problem Statement](#-problem-statement)
3. [Objectives](#-objectives)
4. [Features](#-features)
5. [Technology Stack](#-technology-stack)
6. [System Architecture](#-system-architecture)
7. [Project Structure](#-project-structure)
8. [Prerequisites](#-prerequisites)
9. [Installation and Setup](#-installation-and-setup)
10. [API Configuration](#-api-configuration)
11. [Running the Application](#-running-the-application)
12. [How to Use](#-how-to-use)
13. [How the System Works](#-how-the-system-works)
14. [Error Handling and Troubleshooting](#-error-handling-and-troubleshooting)
15. [Limitations](#-limitations)
16. [Future Enhancements](#-future-enhancements)
17. [Security Considerations](#-security-considerations)
18. [Conclusion](#-conclusion)
19. [References](#-references)

---

## 🌟 Overview

In today's digital environment, people encounter large amounts of news and online information. Reading several lengthy articles and manually checking claims can be time-consuming.

TruthLens AI aims to simplify this process by combining news retrieval, text summarization, and fact-check search in one interface.

Users enter a topic, and the application retrieves relevant news articles through the GNews API. For each article, it uses an extractive text-processing technique to select important sentences from the available article text. Users can also search Google Fact Check Tools for previously reviewed claims related to their topic.

> **Important:** TruthLens AI does not independently prove whether an article is true or fake. Its fact-checking feature retrieves existing reviews, while its news search and summarization features help users investigate information more efficiently.

---

## ❗ Problem Statement

The rapid growth of online news makes it difficult for readers to efficiently understand and assess information. Common challenges include:

* Lengthy news articles that take time to read.
* Information spread across multiple publishers.
* Misleading or inaccurate claims circulating online.
* Difficulty finding existing fact-checks for a particular topic.
* The need to visit multiple websites to understand a developing news story.

---

## 🎯 Objectives

* To retrieve relevant news articles using a news API.
* To generate concise summaries from available article text.
* To display article headlines, publishers, publication dates, and original links.
* To search existing fact-check reviews for a user-provided topic.
* To present information through an accessible web interface.
* To demonstrate the practical application of Python, REST APIs, and natural language processing.

---

## ✨ Features

1. **News Search:** Accepts search topics, queries GNews API, and displays titles, publishers, and publication timestamps.
2. **Automatic News Summarization:** Selects key sentences using a lightweight extractive summarization algorithm based on word frequencies.
3. **Existing Fact-Check Search:** Integrates with Google Fact Check Tools API to find claims, reviewers, ratings, and links.
4. **Interactive Streamlit Dashboard:** Features organized tabs for News & Summaries, Fact Checks, and Insights/About info.

---

## 🛠️ Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Python** | Main programming language |
| **Streamlit** | Interactive web interface |
| **Requests** | HTTP requests to external APIs |
| **GNews API** | News article retrieval |
| **Google Fact Check Tools API** | Search existing fact-check reviews |
| **Python `re` module** | Sentence splitting and text cleaning |
| **Python `collections.Counter`** | Word-frequency calculations |
| **`python-dotenv`** | Loading API keys from environment configuration |

---

## 🏗️ System Architecture

```text
[User] ---> [Streamlit Interface]
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
   [GNews API]     [Google Fact Check API]
        │                   │
        ▼                   ▼
[Extractive Summary]   [Claim Reviews & Ratings]
        └─────────┬─────────┘
                  ▼
         [User Investigation]
```

---

## 📂 Project Structure

```text
truthlens-ai/
│
├── app.py              # Main Streamlit application script
├── requirements.txt    # Python dependencies
├── .env                # API keys (private configuration)
└── README.md           # Project documentation
```

---

## 💻 Prerequisites

* Python 3.10 or newer.
* pip package manager.
* A valid **GNews API Key** ([gnews.io](https://gnews.io/)).
* A valid **Google Fact Check Tools API Key** via Google Cloud Console.

---

## ⚙️ Installation and Setup

1. **Clone or Download the Project:**
   ```bash
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   cd truthlens-ai
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the Environment:**
   * *Windows (PowerShell):* `.venv\Scripts\Activate.ps1`
   * *macOS/Linux:* `source .venv/bin/activate`

4. **Install Dependencies:**
   Create a `requirements.txt` file containing:
   ```text
   streamlit
   requests
   python-dotenv
   ```
   Then install them:
   ```bash
   python -m pip install -r requirements.txt
   ```

5. **Configure Environment Variables:**
   Create a `.env` file in the root directory:
   ```env
   GNEWS_API_KEY=your_gnews_api_key_here
   GOOGLE_FACTCHECK_API_KEY=your_google_factcheck_api_key_here
   ```

6. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

---

## ⚠️ Limitations

* **Not a definitive fake-news classifier:** It does not independently verify the universal truth of statements.
* **Extractive Summarization:** Selects existing sentences rather than generating fully rewritten abstractive summaries.
* **API Dependency:** Functionality relies on uptime and quotas of external APIs.

---

## 🎓 Conclusion

TruthLens AI demonstrates how news retrieval, extractive summarization, and existing fact-check search can be combined in a single Python web application to aid users in navigating information overload.

---

## 📚 References

* Streamlit Documentation: [docs.streamlit.io](https://docs.streamlit.io/)
* GNews API: [gnews.io](https://gnews.io/)
* Google Fact Check Tools API: [Google Developers Reference](https://developers.google.com/fact-check/tools/api)