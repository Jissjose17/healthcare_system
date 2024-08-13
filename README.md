<h1>HealthEasy - Online Healthcare System</h1>
<hr><p>HealthEasy is an online healthcare system designed to help patients make appointments with doctors conveniently. The system allows doctors to manage their appointments, create prescriptions, and handle patient records efficiently. Additionally, it integrates Razorpay for seamless online payments.</p><h2>Technologies Used</h2>
<hr><ul>
<li>HTML</li>
</ul><ul>
<li>CSS</li>
</ul><ul>
<li>Django</li>
</ul><ul>
<li>python</li>
</ul><ul>
<li>tailwindcss</li>
</ul><ul>
<li>postgresql</li>
</ul><h2>Features</h2>
<hr><ul>
<li>Patient Management: Create, edit, and delete patient accounts.</li>
</ul><ul>
<li>Appointment Booking: Patients can book appointments online and view their appointment status.</li>
</ul><ul>
<li>Doctor Management: Admin can add doctors, manage their schedules, and monitor patient interactions.</li>
</ul><ul>
<li>Prescription Management: Doctors can create and manage prescriptions for their patients.</li>
</ul><ul>
<li>Billing and Invoicing: Admin can generate bills and invoices, and patients can make payments online using Razorpay.</li>
</ul><h5>Steps</h5><ul>
<li>Install Dependencies: Create a virtual environment and install the required packages.  bash Copy code python -m venv venv source venv/bin/activate   # On Windows use <code>venv\Scripts\activate</code> pip install -r requirements.txt</li>
</ul><ul>
<li>Install Dependencies: Create a virtual environment and install the required packages.  bash Copy code python -m venv venv source venv/bin/activate   # On Windows use <code>venv\Scripts\activate</code> pip install -r requirements.txt</li>
</ul><ul>
<li>Database Setup: Configure your PostgreSQL database settings in the settings.py file.</li>
</ul><ul>
<li>Apply Migrations:  bash Copy code python manage.py makemigrations python manage.py migrate</li>
</ul><ul>
<li>Create a Superuser:  bash Copy code python manage.py createsuperuser</li>
</ul><ul>
<li>Integrate Razorpay with Django:  Install Razorpay Python SDK: bash Copy code pip install razorpay</li>
</ul><ul>
<li>Configure your Razorpay API keys in the settings.py file: python Copy code RAZORPAY_KEY_ID = 'your_key_id' RAZORPAY_KEY_SECRET = 'your_key_secret'</li>
</ul><ul>
<li>Run the Development Server:  bash Copy code python manage.py runserver</li>
</ul><ul>
<li>Access the website at http://127.0.0.1:8000/.</li>
</ul><h2>Contact</h2>
<hr><p><span style="margin-right: 30px;"></span><a href="www.linkedin.com/in/jissjose17"><img target="_blank" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" style="width: 10%;"></a><span style="margin-right: 30px;"></span><a href="javascript:void(0)"><img target="_blank" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" style="width: 10%;"></a></p>











