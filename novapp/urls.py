from django.urls import path
from .views import *
urlpatterns = [
    path('',ViewHome,name='home'),
    path('login/',ViewLogin,name='login'),
    path('logout/',ViewLogout,name='logout'),
    path('admin-register/',ViewAdminRegister,name='adminRegister'),
    path('patient-register/',ViewPatientRegister,name='patientRegister'),
    path('doctor-register/',ViewDoctorRegister,name='doctorRegister'),
    path('forget-password/',ViewForgetPassword.as_view(),name='forgetPassword'),
    path('setpass/<userId>/<token>',Viewsetpassword.as_view(),name='setpass'),


    # ADMIN DASHBOARD

    path('admin-dash/',viewAdminDashboardMain,name='adminMain'),

    path('admin-doctor-dash/',viewAdminDoctorDashboard,name='adminDoctor'),
    path('doc-profile/<int:id>/',viewDoctorProfile,name='docProfile'),
    path('admin-add-doctor/',viewAdminAddDoctor,name='adminAddDoctor'),
    path('admin-update-doctor/<int:id>/',viewAdminUpdateDoctor,name='adminUpdateDoctor'),
    path('admin-delete-doctor/<int:id>/',viewAdminDeleteDoctor,name='adminDeleteDoctor'),




#     

    path('admin-patient-dash/',viewAdminPatientDashboard,name='adminPatient'),
    path('admin-add-patient/',viewAdminAddPatient,name='adminAddPatient'),
    path('admin-update-atient/<int:id>',viewAdminUpdatePatient,name='adminUpdatePatient'),
    path('patient-profile/<int:id>/',viewPatientProfile,name='patientProfile'),
    path('patient-delete/<int:id>/',viewAdminDeletePatient,name='deletePatient'),


    path('admin-appointment-dash/',viewAdminAppointmentDashboard,name='adminAppointment'),
    path('take_appointment/<int:id>/',viewTakeAppointment,name='takeAppointment'),
    

]
