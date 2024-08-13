HealthEasy - Online Healthcare System
HealthEasy is an online healthcare system designed to help patients make appointments with doctors conveniently. The system allows doctors to manage their appointments, create prescriptions, and handle patient records efficiently. Additionally, it integrates Razorpay for seamless online payments.

Features
Patient Management: Create, edit, and delete patient accounts.
Appointment Booking: Patients can book appointments online and view their appointment status.
Doctor Management: Admin can add doctors, manage their schedules, and monitor patient interactions.
Prescription Management: Doctors can create and manage prescriptions for their patients.
Billing and Invoicing: Admin can generate bills and invoices, and patients can make payments online using Razorpay.
Technologies Used
Frontend: HTML, CSS, Tailwind CSS
Backend: Python, Django Framework
Database: PostgreSQL
Payment Gateway: Razorpay
Setup and Installation
Prerequisites
Python 3.x
PostgreSQL
Django
Razorpay account for payment gateway integration
Step-by-Step Setup
Clone the Repository:

bash
Copy code
git clone https://github.com/Jissjose17/healthcare_system.git
cd healthcare_system
Install Dependencies:
Create a virtual environment and install the required packages.

bash
Copy code
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
Database Setup:
Configure your PostgreSQL database settings in the settings.py file.

Apply Migrations:

bash
Copy code
python manage.py makemigrations
python manage.py migrate
Create a Superuser:

bash
Copy code
python manage.py createsuperuser
Run the Development Server:

bash
Copy code
python manage.py runserver
Access the website at http://127.0.0.1:8000/.

Razorpay Integration
Sign Up/Log In to Razorpay:

Visit Razorpay and create an account.
Create API Keys:

Navigate to the Razorpay dashboard and generate your API keys.
Integrate Razorpay with Django:

Install Razorpay Python SDK:
bash
Copy code
pip install razorpay
Configure your Razorpay API keys in the settings.py file:
python
Copy code
RAZORPAY_KEY_ID = 'your_key_id'
RAZORPAY_KEY_SECRET = 'your_key_secret'
Add Payment Functionality:

Implement Razorpay's payment button in your payment page.
Handle payment verification and update the transaction records accordingly.
Usage
Login
Admin: Access to manage doctors, appointments, and patient records.
Doctor: Manage appointments, accept/reject requests, and create prescriptions.
Patient: Create an account, book appointments, view appointment status, and make payments.
Admin Features
Add doctors and manage their schedules.
Create bills and invoices for patients.
Access and manage all patient records.
Doctor Features
Accept or reject appointments.
View patient details and medical history.
Create and manage prescriptions for patients.
Patient Features
Create, edit, or delete your account.
Book and manage appointments.
View appointment status and receive invoices.
Make payments online using Razorpay.
Contact
LinkedIn: Jiss Jose
Email: jissjo123@gmail.com


![userpage](<Screenshot 2024-08-13 123606.png>)