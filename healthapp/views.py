from multiprocessing import context
from urllib import request
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse
from .models import Doctor, Patient, Appointment, Prescription, Receipt
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from healthapp.models import CustomUser
from django.contrib.auth import update_session_auth_hash
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .models import Payment
# Create your views here.?

@login_required(login_url='loginpage')
def homepage(request):
    try:
        patient = Patient.objects.get(user=request.user)
        return render(request, 'patient/home.html', {'patient_data': patient})
    except Patient.DoesNotExist:
        messages.error(request, "Patient data not found")
        return redirect('loginpage')
    
def contactpage(request):
    return render(request,'patient/contact.html')

def servicepage(request):
    return render(request,'patient/service.html')



def signup_patient(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        name = request.POST['name']
        gender = request.POST['gender']
        mobile = request.POST['mobile']
        address = request.POST['address']
        image = request.FILES.get('image')

        if password != cpassword:
            messages.error(request, "Passwords do not match")
            return redirect('signuppage')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signuppage')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('signuppage')

        user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=3)
        patient = Patient(user=user, name=name, gender=gender, mobile=mobile, address=address, image=image)
        patient.save()

        login(request, user)
        return redirect('loginpage')  # Redirect to patient dashboard 

    return render(request, 'login.html')


def signuppage(request):
    return render(request,'signup.html')


def login_function(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.user_type == 2:
                return redirect('dochomepage')
            elif user.is_superuser:
                return redirect('adminpage')
            elif user.user_type == 3:
                return redirect('homepage')  
            else:
                return redirect('adminpage')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('loginpage')
    return render(request, 'login.html')





def loginpage(request):
    return render(request, 'login.html')



def logout(request):
    auth.logout(request)
    return redirect('loginpage')

def view_patients(request):
    patients = Patient.objects.all()
    return render(request, 'admin/viewpatients.html', {'patients': patients})


def adminpage(request):
    return render(request,'admin/admin.html')

def add_doctor(request):
    return render(request,'admin/adddoc.html')




def register_doctor(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        name = request.POST['name']
        mobile = request.POST['mobile']
        special = request.POST['special']
        about = request.POST['about']
        image = request.FILES.get('image')

        if password != cpassword:
            messages.error(request, "Passwords do not match")
            return redirect('add_doctor')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('add_doctor')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('add_doctor')

        user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=2)
        doctor = Doctor(user=user, name=name, mobile=mobile, special=special,about=about, image=image)
        doctor.save()

        login(request, user)
        return redirect('view_doctors')  # Redirect to doctor dashboard 

    return render(request, 'register_doctor.html')


def view_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'admin/viewdoctor.html', {'doctors': doctors})

def logoutadmin(request):
    auth.logout(request)
    return redirect('loginpage')

def dochomepage(request):
    return render(request,'doctor/dochome.html')



def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        name = request.POST['name']
        mobile = request.POST['mobile']
        special = request.POST['special']
        about = request.POST['about']
        image = request.FILES.get('image')

        user = doctor.user
        user.username = username
        user.email = email
        user.save()

        doctor.name = name
        doctor.mobile = mobile
        doctor.special = special
        doctor.about = about
        if image:
            doctor.image = image
        doctor.save()

        messages.success(request, 'Doctor updated successfully')
        return redirect('view_doctors')  # Redirect to the list of doctors page


    
   
def editdocpage(request, doctor_id): 
    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'admin/edit_doctor.html', {'doctor': doctor})


def delete_doctor(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    doctor.delete()
    messages.success(request, 'Doctor deleted successfully')
    return redirect('view_doctors')

@login_required(login_url='loginpage')
def book_appointmentpage(request):
    doctors = Doctor.objects.all()
    return render(request, 'patient/bookappointment.html', {'doctors': doctors})


def create_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST['doctor']
        patient= request.POST['patient_name']
        symptoms = request.POST['symptoms']
        date = request.POST['appointment_date']
        time = request.POST['appointment_time']
        doctor = get_object_or_404(Doctor, id=doctor_id)
        
        appointment = Appointment(doctor=doctor, patient_name=patient, symptoms=symptoms, date=date, time=time)
        appointment.save()
        
        return redirect('appointment_success')

    return render(request, 'patient/bookappointment.html')

def create_appointmentpage(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctors = Doctor.objects.all()

    context = {
        'doctor': doctor,
        'doctors': doctors
    }
    return render(request, 'patient/create_appointment.html', context)



def delete_appointments(request):
    appointment_ids = request.POST.getlist('appointment_ids')
    if appointment_ids:
        Appointment.objects.filter(id__in=appointment_ids).delete()
    return redirect('doctor_appointments')

def adminview_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'admin/viewappointments.html', {'appointments': appointments})


def delete_patients(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        ids = data.get('ids', [])
        if ids:
            Patient.objects.filter(id__in=ids).delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'No IDs provided'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})






def about(request):
    return render(request, 'patient/about.html')


def create_prescription(request):
    if request.method == 'POST':
        appointment_id = request.POST['appointment']
        symptoms = request.POST['symptoms']
        prescription_text = request.POST['prescription']

        appointment = Appointment.objects.get(id=appointment_id)

        prescription = Prescription(
            symptoms=appointment,
            prescription=prescription_text,
            patient_name=appointment
        )
        prescription.save()

        messages.success(request, 'Prescription created successfully')
        return redirect('view_prescriptions')  # Redirect to view prescriptions page

    appointments = Appointment.objects.all()
    return render(request, 'doctor/create_prescription.html', {'appointments': appointments})


def doctor_appointments(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor)
    return render(request, 'doctor/viewappointments.html', {'appointments': appointments})



def update_appointment_status(request, appointment_id,status):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = status
    appointment.save()
    messages.success(request, f"Appointment status updated to {status}.")
    return redirect('doctor_appointments')




def delete_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    prescription.delete()
    return redirect('view_prescriptions')

def prescriptionpage(request):
    doctors =get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctors)
    return render(request, 'doctor/create_prescription.html', {'appointments': appointments} )


def view_prescriptions(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    prescriptions = Prescription.objects.filter(doctor=doctor)
    return render(request, 'doctor/view_prescriptions.html', {'prescriptions': prescriptions})


def patient_appointments(request):
    patient = get_object_or_404(Patient, user=request.user)
    appointments = Appointment.objects.filter(patient_name=patient)
    return render(request, 'patient/patient_appointments.html', {'appointments': appointments})


    

def appointment_success(request):
    return render(request, 'patient/appointment_success.html')



def profile(request):
    patient = Patient.objects.get(user=request.user)
    return render(request, 'patient/profile.html', {'patient_data': patient})

def edit_profilepage(request):
    patient = Patient.objects.get(user=request.user)
    return render(request, 'patient/edit_profile.html', {'patient_data': patient})

def edit_profile(request):
    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        mobile = request.POST['mobile']
        address = request.POST['address']
        image = request.FILES.get('image')

        patient = Patient.objects.get(user=request.user)
        patient.name = name
        patient.gender = gender
        patient.mobile = mobile
        patient.address = address
        if image:
            patient.image = image
        patient.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('profile')  # Redirect to the profile page

    return render(request, 'patient/edit_profile.html')



@login_required
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        name = request.POST['name']
        gender = request.POST['gender']
        mobile = request.POST['mobile']
        address = request.POST['address']
        image = request.FILES.get('image')

        patient = Patient.objects.get(user=request.user)
        user = request.user

        if password and password != cpassword:
            messages.error(request, "Passwords do not match")
            return redirect('edit_profile')

        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)

        user.username = username
        user.email = email
        user.save()

        patient.name = name
        patient.gender = gender
        patient.mobile = mobile
        patient.address = address
        if image:
            patient.image = image
        patient.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('profile')  

    return render(request, 'patient/edit_profile.html', {'patient': request.user.patient, 'user': request.user})


def delete_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    patient.delete()    
    return redirect('loginpage')




def create_receiptpage(request):
    appointment=Appointment.objects.all()
    prescription=Prescription.objects.all()
    return render(request, 'admin/create_receipt.html',{'appointments':appointment,'prescriptions':prescription})


def delete_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.delete()
    return redirect(reverse('create_receiptpage'))

def delete_prescription(request, prescription_id):
    prescription = Prescription.objects.get(id=prescription_id)
    prescription.delete()
    return redirect(reverse('create_receiptpage')) 
def create_receipt(request):
    if request.method == 'POST':
        invoice_number = request.POST.get('invoice_number')
        hospital_name = request.POST.get('hospital_name')
        hospital_phone = request.POST.get('hospital_phone')
        hospital_email = request.POST.get('hospital_email')
        patient_name = request.POST.get('patient')
        symptoms= request.POST.get('symptoms')
        doctor = request.POST.get('doctor')
        doctor_fee = request.POST.get('doctor_fee')
        prescription= request.POST.get('prescription')
        prescription_amount = request.POST.get('prescription_amount')
        total_amount = request.POST.get('total_amount')

        receipt = Receipt(
            invoice_number=invoice_number,
            hospital_name=hospital_name,
            hospital_phone=hospital_phone,
            hospital_email=hospital_email,
            patient_name=patient_name,  
            symptoms=symptoms,  
            doctor=doctor,  
            doctor_fee=doctor_fee,
            prescription=prescription,  
            prescription_amount=prescription_amount,
            total_amount=total_amount,
        )
        receipt.save()
        return redirect('view_receiptpage') 
    else:
        return redirect('create_receiptpage')




def view_receiptpage(request):
    receipts = Receipt.objects.all()
    return render(request, 'admin/view_receiptpage.html', {'receipt': receipts})


def delete_receipt(request, receipt_id):
    try:
        receipt = Receipt.objects.get(id=receipt_id)
        receipt.delete()
        return redirect('view_receiptpage')
    except Receipt.DoesNotExist:
        return HttpResponse('Receipt not found', status=404)


def patient_viewreceipt(request):
    patient = get_object_or_404(Patient, user=request.user)
    receipt = Receipt.objects.filter(patient_name=patient)
    return render(request, 'patient/receipt.html', {'receipt': receipt})



razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def paymentfunction(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        amount = int(request.POST.get('amount')) * 100  # Amount in paise (convert INR to paise)

        client = razorpay.Client(auth=("rzp_test_zH5Pb6BHyTbVje", "aMDOa1QQbdkBI2fOGDlMMciA"))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

        # Save the payment details to the database
        payment_record = Payment(
            name=name,
            email=email,
            amount=amount / 100, 
        )
        payment_record.save()

        context = {
            'name': name,
            'email': email,
            'amount': amount / 100,  # Convert to rupees for display
            'razorpay_key': settings.RAZORPAY_KEY_ID,
        }

        return redirect(reverse('payment_success'))

    return redirect('payment_page')

def payment_success(request):
    payments = Payment.objects.all()  # Retrieve all payment records
    context = {'payments': payments}
    return render(request, 'patient/payment_success.html', context)


def payment_page(request):
    return render(request, 'patient/create_payment.html')

def view_payment_page(request):
    payments = Payment.objects.all()  # Retrieve all payment records
    context = {'payments': payments}
    return render(request, 'admin/view_payment.html', context)



def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.delete()
    return redirect('view_payment_page')

def paymentpage(request):
    if request.method == 'POST':
        print("Razorpay Key ID:", settings.RAZORPAY_KEY_ID)
        print("Razorpay Key Secret:", settings.RAZORPAY_KEY_SECRET)

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            result = client.utility.verify_payment_signature(params_dict)

            if result:
                amount = 50000  # Rs 500
                try:
                    client.payment.capture(payment_id, amount)
                    return render(request, 'payment_success.html')
                except:
                    return render(request, 'payment_failed.html')
            else:
                return render(request, 'payment_failed.html')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


