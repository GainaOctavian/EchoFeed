
# EchoFeed - Personalized News Web Application

**Bachelor's Thesis by Aurelian-Octavian Găină**  
*Academy of Economic Studies, Faculty of Cybernetics, Statistics, and Economic Informatics*  
Scientific Coordinator: Lecturer Mădălina Doinea-Zurini  
Date: June 2024

## Overview

EchoFeed is an intelligent web application designed to personalize news feeds for users by leveraging artificial intelligence and modern web technologies. The project was developed as part of my bachelor's thesis to demonstrate full-stack development skills, external API integration, and the implementation of AI-driven algorithms for content personalization.

## Key Features

- **AI-Powered Personalization:** Uses OpenAI GPT-4o for keyword generation and content categorization.
- **Advanced News Search:** Integration with Google Search API for accessing diverse and relevant news sources.
- **Modern UI:** Built with NiceGUI to offer an intuitive and responsive user interface.
- **Efficient Data Management:** Elasticsearch for fast, scalable data indexing and search capabilities.
- **Secure Authentication:** Implementation of secure login mechanisms with hashed passwords.
- **Containerization:** Docker-based deployment for easy scalability and efficient resource management.

## System Architecture

The application is based on a microservices architecture, enhancing modularity, scalability, and maintainability.

- **Frontend:** Developed using NiceGUI for dynamic, responsive design.
- **Backend:** Built with FastAPI, handling API endpoints, user management, and business logic.
- **Database:** Elasticsearch for real-time data indexing and high-performance search operations.
- **External APIs:** 
  - **OpenAI API:** For AI-driven keyword generation and content recommendations.
  - **Google Search API:** For retrieving up-to-date news articles from reliable sources.

## Technologies Used

- **Backend:** FastAPI, Python
- **Frontend:** NiceGUI, HTML5, CSS3, JavaScript
- **Database:** Elasticsearch
- **AI Integration:** OpenAI GPT-4o
- **API Integration:** Google Search API
- **Containerization:** Docker

## 🚀 Quick Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GainaOctavian/EchoFeed.git
   cd EchoFeed
   ```

2. **Set up the virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```ini
   OPENAI_API_KEY=your_openai_key
   GOOGLE_SEARCH_API_KEY=your_google_key
   ELASTICSEARCH_URL=http://localhost:9200
   ```

5. **Start Elasticsearch:**
   ```bash
   docker network create echofeed
   docker run --net echofeed --name echofeed-elastic -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.11.4
   ```

6. **Run the application:**
   ```bash
   uvicorn app:app --reload
   ```

   The application will be available at `http://localhost:8000`.

## 📊 Use Cases

- **Personalized News Feed:** Delivers news articles tailored to user preferences based on reading history and interests.
- **Advanced Search Capabilities:** Allows users to perform customized searches using AI-generated keywords.
- **User Management:** Secure registration, login, and user role management for both regular users and administrators.

## 🌟 Future Development

- Enhancing recommendation algorithms for improved accuracy.
- Expanding API integrations to include more news sources.
- Implementing advanced analytics for tracking user engagement and content performance.

## 🚨 Disclaimer

This project is the result of my personal work and reflects my programming skills, analytical thinking, and expertise in integrating modern technologies. It was developed as part of my bachelor's thesis at the Academy of Economic Studies, Bucharest.

For feedback or collaboration, feel free to open an issue in the repository.
