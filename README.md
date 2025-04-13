Python Online Shop Project

Project Description
This project is an online shop system developed in Python. It enables product management, shopping cart functionality, payment processing, and order placement for users. The goal is to provide a simple and extensible platform for small businesses looking to set up an online store.

Features
- Product management (add, edit, delete products)
- Shopping cart with add/remove item capabilities
- Simulated online payment system (using a test gateway)
- Admin panel for sellers
- User registration and login
- Product search by category and name

Prerequisites
To run this project, ensure you have the following installed:
- Python 3.8 or higher
- Python libraries: Django
- SQLite database (used by default)
- Git for cloning the repository

Installation
1. Clone the project repository from GitHub:
   git clone https://github.com/your-username/online-shop-python.git
2. Navigate to the project directory:
   cd shop
3. Create a virtual environment:
   python -m venv venv
4. Activate the virtual environment:
   - On Windows: venv\Scripts\activate
   - On Linux/Mac: source venv/bin/activate
5. Install required Python libraries:
   pip install django

Usage
1. Start the project server:
   python manage.py runserver 5000
2. Open your browser and go to:
   http://localhost:5000
3. To access the admin panel:
   - Username: admin
   - Password: 1234
4. Add products, manage your cart, and place orders.

Configuration
- To change the database, edit config.py.
- To use a real payment gateway, update settings in payment.py.
- Set environment variables (e.g., SECRET_KEY) in a .env file.

Contributing
We welcome contributions! To collaborate:
1. Fork the repository:
   https://github.com/MEHRSHAD-OSG/store.git
2. Create a new branch:
   git checkout -b feature/your-feature
3. Commit your changes:
   git commit -m "Add new feature"
4. Push your changes:
   git push origin feature/your-feature
5. Open a Pull Request on GitHub.

Support
- To report issues, create an Issue on GitHub:
  https://github.com/MEHRSHAD-OSG/store/issues
- Include error details, Python version, and operating system.
- For questions, mehrshadoshaghi54@gmail.com.

License
This project is licensed under the MIT License. See the LICENSE file in the repository for details.

Developer
- Name: Mehrshad
- Email: mehrshadoshaghi54@gmail.com
- GitHub: https://github.com/MEHRSHAD-OSG
