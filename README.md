# StudyRoom

## Description
StudyRoom is a virtual platform where students can create and join study rooms, collaborate on resources, and engage in real-time discussions. The platform enables users to upload resources, and manage study sessions efficiently.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [API Documentation](#api-documentation)
- [Contributing](#Contributing)
- [Contact](#contact)

## Installation

### Prerequisites
- Python 3.8+
- Flask
- SQLite or any preferred database engine

### Setup
1. **Clone the Repository:**
    ```bash
     git clone https://github.com/bossambani/StudyRoom
     cd StudyRoom
    ```

2. **Create a Virtual Environment:**
    - For Windows:
    ```bash
     python3 -m venv env
     source env/Scripts/activate
    ```

    - For Linux/macOS:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install Dependencies:**
    ```bash
    - pip install -r requirements.txt
    ```


4. **Run the Application:**
    ```bash
    - flask run
    ```
    This command will start the Flask development server on 'localhost:5000`.



## Usage
1. **Sign Up and Log In:**
    - Create an account by filling out the registration form.
    - Log in using your credentials.

2. **Create a Study Room:**
    - Navigate to the "Create Room" page.
    - Fill out the form to create a new study room.
    - Share the room link with other participants.

3. **Join a Study Room:**
    - Browse available rooms or use the room link to join an existing study room.

4. **Upload and Manage Resources:**
   - Upload study materials such as PDFs, videos, or notes to the room.
   - Manage and download shared resources.

5. **Participate in Chat:**
   - Use the chat feature to communicate in real-time with other participants in the study room.

## Features
- User authentication (Sign Up, Log In, Log Out)
- Create, join, and manage study rooms
- Upload and share resources (documents, videos, etc.)
- Real-time chat functionality
- Manage room participants
- Resource organization per room

## API Documentation
The StudyRoom platform also provides a REST API for developers to interact with the system programmatically.

### Endpoints:

1. **User Authentication:**
   - **POST** `/api/v1/auth/signup` – Register a new user
   - **POST** `/api/v1/auth/login` – Log in an existing user

2. **Study Room Management:**
   - **GET** `/api/v1/rooms` – Get a list of study rooms
   - **POST** `/api/v1/rooms` – Create a new study room
   - **GET** `/api/v1/rooms/<room_id>` – Get details of a specific room

3. **Resource Management:**
   - **POST** `/api/v1/rooms/<room_id>/upload` – Upload a resource to a room
   - **GET** `/api/v1/rooms/<room_id>/resources` – List resources in a room

4. **Chat:**
   - **GET** `/api/v1/rooms/<room_id>/chat` – Get chat messages for a room
   - **POST** `/api/v1/rooms/<room_id>/chat` – Post a chat message to a room

For more detailed API documentation, refer to the [API Documentation](API.md) file.

## Contributing
We welcome contributions to StudyRoom! Here's how you can contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Submit a pull request.

For major changes, please open an issue first to discuss what you would like to change.

## Contact
If you have any questions or suggestions, feel free to contact us:

- **Email:** support@studyroom.com
- **GitHub Issues:** [Issues Page](https://github.com/bossambani/StudyRoom/issues)

