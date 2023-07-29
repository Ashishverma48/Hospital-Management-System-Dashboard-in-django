from django.shortcuts import render, redirect
from .forms import *
# from .models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.views.generic import View
from django.contrib import messages

# Email
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util

from django.http import HttpResponse
# Create your views here.


def ViewHome(request):
    return render(request, 'novapp/index.html')


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def is_doctor(user):
    return user.groups.filter(name='Doctor').exists()


def is_patient(user):
    return user.groups.filter(name='Patient').exists()


def ViewLogout(request):
    login(request.user)
    return redirect('login')


def ViewLogin(request):
    if request.method == 'POST':
        name = request.POST.get('txt')
        password = request.POST.get('txtp')
        print(name, password)
        messages.warning(request, 'Invalid Crediential')
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            if is_admin(user):
                return HttpResponse('<h1>ADMIN PAGE</h1>')
            elif is_doctor(user):
                return HttpResponse('<h1>DOCTOR PAGE</h1>')
            elif is_patient(user):
                return HttpResponse('<h1>PATIENT PAGE</h1>')

    return render(request, 'novapp/login.html')


def ViewAdminRegister(request):
    form = AdminForm()
    if request.method == "POST":
        frm = AdminForm(request.POST)
        if frm.is_valid():
            user = frm.save()
            user.is_staff = True
            user.save()
            admin = Group.objects.get_or_create(name='Admin')
            admin[0].user_set.add(user)
            messages.success(request, 'Patient Register Sucessfully !')
            return redirect('login')

        return render(request, 'novapp/adminSignUp.html', {'form': frm})
    return render(request, 'novapp/adminSignUp.html', {'form': form})


def ViewDoctorRegister(request):
    doctuserform = DoctorUserForm()
    doctorform = DoctorForm()

    if request.method == 'POST':
        doctuserform = DoctorUserForm(request.POST)
        doctorform = DoctorForm(request.POST, request.FILES)
        # print(docterfrm)
        if doctorform.is_valid() and doctuserform.is_valid():
            user = doctuserform.save(commit=False)
            user.save()
            doctor = doctorform.save(commit=False)
            doctor.department_id = request.POST.get('department')
            doctor.user = user
            doctor.save()
            print('sucesss')
            doctor = Group.objects.get_or_create(name='Doctor')
            doctor[0].user_set.add(user)

            # doctor.save()
            messages.success(request, 'Patient Register Sucessfully !')
            return redirect('login')
        else:

            print('failes')
        # return render(request,'novapp/doctorSignUp.html',locals())
    return render(request, 'novapp/doctorSignUp.html', locals())


def ViewPatientRegister(request):

    patientuserform = PatientUserForm()
    patientform = PatientForm()

    if request.method == 'POST':
        patientuserform = PatientUserForm(request.POST)
        patientform = PatientForm(request.POST, request.FILES)

        if patientform.is_valid() and patientuserform.is_valid():
            user = patientuserform.save(commit=False)
            user.save()

            patient = patientform.save(commit=False)
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.user = user
            patient.save()
            print('sucesss')
            messages.success(request, 'Patient Register Sucessfully !')
            patient = Group.objects.get_or_create(name='Patient')
            patient[0].user_set.add(user)
            return redirect('login')

        # else:

        #     print('failes')
        # return render(request,'novapp/doctorSignUp.html',locals())
    return render(request, 'novapp/patientSignUp.html', locals())

# def ViewForgetPassword(request):
#     return render(request,'novapp/forgetPassword.html')


class ViewForgetPassword(View):
    def get(self, request):
        return render(request, 'novapp/forgetPassword.html')

    def post(self, request):
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        userId = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        link = "http://127.0.0.1:8000/setpass/"+userId+'/'+token
        body = 'Click following to reset your password ' + link
        data = {'email_subject': 'Reset Your Password',
                'body': body,
                'to_email': email
                }
        Util.send_email(data)
        messages.success(request, 'Email Sent Sucessfully !')
        return render(request, 'novapp/forgetPassword.html')


class Viewsetpassword(View):
    def get(self, request, userId, token):

        try:
            user_id = smart_str(urlsafe_base64_decode(userId))
            user = User.objects.get(pk=user_id)
            print(user)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.warning(request, 'Token is not valid !')
                return render(request, 'novapp/forgetPassword.html')

        except DjangoUnicodeDecodeError as Identifier:
            pass

        return render(request, 'novapp/setNewPassword.html')

    def post(self, request, userId, token):

        password = request.POST.get('Password')
        confirmPassword = request.POST.get('confirmPassword')

        if password != confirmPassword:
            messages.warning(request, 'Password Not Match')
            return render(request, 'novapp/setNewPassword.html')
        try:
            user_id = smart_str(urlsafe_base64_decode(userId))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.warning(request, 'Token is not valid !')

            user.set_password(password)
            user.save()
            messages.success(request, 'Password Reset Sucessflly ')
            return redirect('login')
        except:

            messages.warning(request, 'Something Went Wrong ')
            return render(request, 'novapp/setNewPassword.html')


#
# <<<<<<<<<<<<<        ADMIN DASHBOARD     >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def viewAdminDashboardMain(request):
    doctorCount = Doctor.objects.all().count()
    patientCount = Patient.objects.all().count()
    attendyNum = Appointment.objects.all().filter(status=True).count()
    pendingAppointmentNum = Appointment.objects.all().filter(status=False).count()
    doctors = Doctor.objects.all()[:5]

    appointment = Appointment.objects.all().filter(
        status=False).order_by('-id')[:5]

    patients = Patient.objects.all()[:5]
    print(doctorCount)
    return render(request, 'novapp/admin/index.html', locals())


# <<<<<<<<<<<<<        ADMIN DOCTOR DASHBOARD     >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def viewAdminDoctorDashboard(request):
    doctors = Doctor.objects.all()

    return render(request, 'novapp/admin/doctors.html', locals())

 # DOCTOR PROFILE
 
def viewDoctorProfile(request, id):
    user = Doctor.objects.get(id=id)

    return render(request, 'novapp/admin/profile.html', {'user': user})

# ADD DOCTOR

def viewAdminAddDoctor(request):
    userform = DoctorUserForm()
    doctorform = DoctorForm()
    if request.method == "POST":

        userform = DoctorUserForm(request.POST)
        doctorform = DoctorForm(request.POST, request.FILES)

        if doctorform.is_valid() and userform.is_valid():
            user = userform.save()
            user.save()
            doctor = doctorform.save(commit=False)
            doctor.department_id = request.POST.get('department')
            doctor.user = user
            doctor.save()
            return redirect('adminDoctor')

        return render(request, 'novapp/admin/addDoctor.html', locals())
    return render(request, 'novapp/admin/addDoctor.html', locals())

# UPDATE DOCTOR

def viewAdminUpdateDoctor(request, id):
    doctorid = Doctor.objects.get(id=id)
    user = User.objects.get(id=doctorid.user_id)

    userform = DoctorUserForm(instance=user)
    doctorform = DoctorForm(instance=doctorid)

    if request.method == "POST":
        userform = DoctorUserForm(request.POST, instance=user)
        doctorform = DoctorForm(request.POST, request.FILES, instance=doctorid)
        if doctorform.is_valid() and userform.is_valid():
            user = userform.save()
            user.save()
            doctor = doctorform.save(commit=False)
            doctor.department_id = request.POST.get('department')
            doctor.user = user
            doctor.save()
            return redirect('adminDoctor')

        return render(request, 'novapp/admin/addDoctor.html', locals())
    return render(request, 'novapp/admin/addDoctor.html', locals())

# Delete Doctor
def viewAdminDeleteDoctor(request, id):
    doctor = Doctor.objects.get(user_id=id)
    user = User.objects.get(id=id)
    doctor.delete()
    user.delete()

    return redirect('adminDoctor')


# <<<<<<<<<<<<<        Patient     >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def viewAdminPatientDashboard(request):
    patients = Patient.objects.all().order_by('-id')
    return render(request, 'novapp/admin/patients.html',{'patients':patients})

 # PATIENT PROFILE
def viewPatientProfile(request, id):
    user = Patient.objects.get(id=id)
    doctorid = user.assignedDoctorId
    doctor = Doctor.objects.get(id=doctorid)
    return render(request, 'novapp/admin/profile.html', {'user': user, 'doctor': doctor})

# ADD NEW PATIENT
def viewAdminAddPatient(request):
    userform = PatientUserForm()
    patientform = PatientForm()
    if request.method == 'POST':
        userform = PatientUserForm(request.POST)
        patientform = PatientForm(request.POST, request.FILES)
        if userform.is_valid() and patientform.is_valid():
            user = userform.save()
            user.save()
            patient = patientform.save(commit=False)
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.user = user
            patient.save()
            return redirect('adminPatient')
        return render(request, 'novapp/admin/addPatient.html', locals())
    return render(request, 'novapp/admin/addPatient.html', locals())

#UPDATE PATIENT 
def viewAdminUpdatePatient(request, id):
    patient = Patient.objects.get(id=id)
    user = User.objects.get(id=patient.user_id)
    userform = PatientUserForm(instance=user)
    patientform = PatientForm(instance=patient)
    if request.method == 'POST':
        userform = PatientUserForm(request.POST, instance=user)
        patientform = PatientForm(
            request.POST, request.FILES, instance=patient)
        if userform.is_valid() and patientform.is_valid():
            userfrm = userform.save()
            userfrm.save()
            patientfrm = patientform.save(commit=False)
            patientfrm.assignedDoctorId = request.POST.get('assignedDoctorId')
            patientfrm.user = userfrm
            patientfrm.save()
            return redirect('adminPatient')
        return render(request, 'novapp/admin/addPatient.html', locals())

    return render(request, 'novapp/admin/addPatient.html', locals())

# DELETE PATIENT
def viewAdminDeletePatient(request, id):
    patient = Patient.objects.get(id=id)
    user = User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('adminPatient')


# <<<<<<<<<<<<<        APPOINTMENT     >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# APOINT
def viewAdminAppointmentDashboard(request):
    appointments = Appointment.objects.all()
    return render(request, 'novapp/admin/appointments.html', locals())

# VARIFY && TAKE APPOINTMENT
def viewTakeAppointment(request, id):
    app = Appointment.objects.get(id=id)
    app.status = True
    app.save()
    return redirect('adminAppointment')

# ADD APPOINTMENT
def viewAddAppointment(request):
    app = AppointmentForm()
    if request.method == 'POST':
        app = AppointmentForm(request.POST)
        if app.is_valid():
            appointment = app.save(commit=False)
            appointment.doctorName = app.cleaned_data['doctorName']
            appointment.department = app.cleaned_data['department']
            appointment.save()
            return redirect('adminAppointment')
        return render(request, 'novapp/admin/addAppointment.html', {'app': app})

    return render(request, 'novapp/admin/addAppointment.html', {'app': app})

#  UPDATE APPOINTMENT
def viewUpdateAppointment(request, id):
    patient = Appointment.objects.get(id=id)
    app = AppointmentForm(instance=patient)
    if request.method == 'POST':
        app = AppointmentForm(request.POST,instance=patient)
        if app.is_valid():
            appointment = app.save(commit=False)
            appointment.doctorName = app.cleaned_data['doctorName']
            appointment.department = app.cleaned_data['department']
            appointment.save()
            return redirect('adminAppointment')
        return render(request, 'novapp/admin/addAppointment.html', {'app': app})

    return render(request, 'novapp/admin/addAppointment.html', {'app': app})

# DELETE APPOINTMENT
def viewDeleteAppointment(request,id):
    app = Appointment.objects.get(id=id)
    app.delete()
    return redirect('adminAppointment')



# <<<<<<<<<<<<<        DEPARTMENT     >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def viewDepartment(request):
    department = Department.objects.all()
    return render(request,'novapp/admin/departments.html',{'department':department})