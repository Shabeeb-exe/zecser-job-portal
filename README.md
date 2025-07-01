# Django Job Portal 🚀

A RESTful job portal application built with Django and Django REST Framework, featuring multi-type user authentication (Job Seeker/Employer), profile management, and file uploads.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2-brightgreen.svg)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/Django_REST_Framework-3.14-red.svg)](https://www.django-rest-framework.org)

## Features

- **Custom User Model** with role-based authentication (Job Seeker/Employer)
- **Profile Management**:
  - Job Seeker profiles with resume uploads
  - Employer profiles with company details
- **Secure Authentication** using Django REST Framework
- **File Uploads** for resumes and company logos
- **Modern API Design** ready for frontend integration

## Setup Instructions 🛠️

1.**Clone the repository**
   ```bash
   git clone https://github.com/yourusername/django-job-portal.git
   cd django-job-portal
   ```

2.**Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3.**Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4.**Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5.**Run migrations**
   ```bash
   python manage.py migrate
   ```

6.**Create superuser**
  ```bash
  python manage.py createsuperuser
  ```

7.**Run development server**
  ```bash
  python manage.py runserver
  ```
## API Endpoints 🌐


| Endpoint               | Method | Description          |
|------------------------|--------|----------------------|
| `/api/auth/register/`  | POST   | User registration   |
| `/api/auth/login/`     | POST   | User login          |
| `/api/jobseekers/`     | GET    | List job seekers    |
| `/api/employers/`      | GET    | List employers      |

## Technologies Used 💻


**Backend**  
![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django)  
![DRF](https://img.shields.io/badge/Django_REST_Framework-3.15-800000?logo=django)

**Database**  
![SQLite](https://img.shields.io/badge/SQLite-Development-003B57?logo=sqlite)  
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Production-4169E1?logo=postgresql)

**Authentication**  
🔜 Custom user model with JWT (Coming soon)

**File Storage**  
📁 Local storage (Development)  
![AWS S3](https://img.shields.io/badge/AWS_S3-Production-569A31?logo=amazons3)(Coming soon)

## Contributing 🤝  
✨ **We welcome contributions from everyone!** Follow these steps to get started:  

1.**Fork** the repository �  
2.**Create** your feature branch  
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3.**Commit** your changes
  ```bash
  git commit -m 'Add some AmazingFeature'
  ```
4.**Push** to the branch
  ```bash
  git push origin feature/AmazingFeature
  ```

## License 📄
🔓 **Open Source, Open Hearts**  

This project is licensed under the **[MIT License](https://opensource.org/licenses/MIT)** - see the [LICENSE](LICENSE) file for full details.  

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](https://opensource.org/licenses/MIT)  
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)  

💡 *Permissive, free, and community-friendly.* 


##

[![LinkedIn](https://img.shields.io/badge/-LinkedIn-black?style=for-the-badge&logo=linkedin&colorB=2867B2)](https://www.linkedin.com/in/muhammed-shabeeb-kt-38901921a)

[![Portfolio](https://img.shields.io/badge/Portfolio-%23000000?style=for-the-badge&logo=firefox&logoColor=#FF7139)](https://shabeeb-exe.github.io/Portfolio/)

*Made with ❤️ and Django*
  
