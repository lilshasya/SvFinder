from django.urls import path

from . import views  # Make sure this import is correct

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("signupstudent/", views.signupstudent, name="signupstudent"),
    path("signupsupervisor/", views.signupsupervisor, name="signupsupervisor"),
    path("signupadmin/", views.signupadmin, name="signupadmin"),
    path('login/', views.login, name='login'),
    path('loginstudent/', views.loginstudent, name='loginstudent'),
    path('loginsupervisor/', views.loginsupervisor, name='loginsupervisor'),
    path('loginadmin/', views.loginadmin, name='loginadmin'),
    path('mainstudent/', views.mainstudent, name='mainstudent'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('mainsupervisor/', views.mainsupervisor, name='mainsupervisor'),
    path('profilesupervisor/', views.profilesupervisor, name='profilesupervisor'),
    path('supervisor/update/', views.update_profile, name='update_profile'),
    path('mainadmin', views.mainadmin, name='mainadmin'),
    path('adminstatic', views.adminstatic, name='adminstatic'),
    path('studentlist', views.studentlist, name='studentlist'),
    path('delete-studentlist/<str:id_pelajar>/', views.delete_studentlist, name='delete_studentlist'),
    path('supervisorlist', views.supervisorlist, name='supervisorlist'),
    path('profilestudent', views.profilestudent, name='profilestudent'),
    path('delete-supervisorlist/<str:id_penyelia>/', views.delete_supervisorlist, name='delete_supervisorlist'),
    path('update-supervisorlist/<str:id_penyelia>/', views.update_supervisorlist, name='update_supervisorlist'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-profilesupervisor/', views.update_profilesupervisor, name='update_profilesupervisor'),
    path('informationsv/<str:id>/', views.informationsv, name='informationsv'),  # Ensure this matches
    path('requestform/<str:id_penyelia>/', views.requestform, name='requestform'),
    path('status/', views.status, name='status'),
    path('statuspermohonan/', views.statuspermohonan, name='statuspermohonan'),
    path('student/<str:id>/', views.student_detail, name='studentdetail'),
    path('result/<str:id_permohonan>/', views.result_view, name='result'),
    path('result-success/', views.result_success, name='result_success'),
    path('list/', views.list, name='list'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('forgot-password-sv/', views.forgot_password_sv, name='forgot_password_sv'),
    
    path('view-permohonan/', views.view_permohonan, name='viewpermohonan'),






]


