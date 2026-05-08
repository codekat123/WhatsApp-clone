# WhatsApp Clone

A real-time chat application that mimics core WhatsApp features, built with Django, Django REST Framework, and WebSockets.


---
## 🌐 Live Deployment

The API is deployed on an AWS EC2 instance and accessible over HTTPS:

* **Base URL:** https://whats-clone-ahmed-gaber.duckdns.org/
* **API Docs (Swagger):** https://whats-clone-ahmed-gaber.duckdns.org/api/docs/

The application is running behind **Nginx** as a reverse proxy and served using **Gunicorn**, with HTTPS enabled via **Let's Encrypt**.

---

## 🚀 Features

- **User Authentication**: Secure signup and login with phone number verification
- **Real-time Messaging**: Instant message delivery using WebSockets
- **Group Chats**: Create and manage group conversations
- **Admin Controls**: Group admins can add/remove members and promote others to admins
- **Private Chats**: One-on-one conversations
- **Message Status**: See when messages are delivered and read

## 🛠️ Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Real-time**: Django Channels, WebSockets
- **Database**: PostgreSQL (production), SQLite (development)
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: OpenAPI/Swagger
- **Containerization**: Docker

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/whatsapp-clone.git
   cd whatsapp-clone
   ```

2. **Set up environment variables**
   ```bash
   cp src/.env.example src/.env
   # Edit the .env file with your configuration
   ```

3. **Start the application**
   ```bash
   # Using Docker (recommended)
   docker-compose up --build
   
   # Or run locally
   cd src
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

4. **Access the API**
   - API Documentation: http://localhost:8000/api/docs/
   - WebSocket endpoint: ws://localhost:8000/ws/chat/

## 📱 API Endpoints

### Authentication
- `POST /api/v1/users/send-otp/`: Send OTP to phone number
- `POST /api/v1/users/register/`: Register with OTP verification
- `POST /api/v1/users/token/`: Get JWT tokens

### Chats
- `GET /api/v1/chats/`: List all chats
- `POST /api/v1/chats/`: Start a new chat
- `GET /api/v1/chats/{chat_id}/`: Get chat details

### Groups
- `POST /api/v1/groups/`: Create a new group
- `PATCH /api/v1/groups/{group_id}/`: Update group details
- `DELETE /api/v1/groups/{group_id}/`: Delete a group
- `POST /api/v1/groups/{group_id}/members/`: Add member to group
- `POST /api/v1/groups/{group_id}/admins/`: Make member an admin




