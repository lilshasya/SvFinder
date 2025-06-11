from django.conf import settings
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Pelajar,Penyelia,AdminSistem,Permohonan,Status
from datetime import date
from datetime import datetime, time, timedelta
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

from django.core.paginator import Paginator


def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method == "POST":
        role = request.POST.get("role")
        if role == "student":
            return redirect("signupstudent")
        elif role == "supervisor":
            return redirect("signupsupervisor")  
        elif role == "admin":
            return redirect("signupadmin")    
    return render(request, "signup.html")

def signupstudent(request):
    if request.method == "POST":
        id_pelajar = request.POST['id_pelajar']
        nama_pelajar = request.POST['nama_pelajar']
        email_pelajar = request.POST['email_pelajar']
        no_pelajar = request.POST['no_pelajar']
        katalaluan_pelajar = request.POST['katalaluan_pelajar']
        program_pelajar = request.POST['program_pelajar']
        gambar_pelajar = request.FILES.get('gambar_pelajar')

        # Check if student ID already exists
        if Pelajar.objects.filter(id_pelajar=id_pelajar).exists():
            context = {
                'message': 'Student ID already registered. Please login or use a different ID.',
                'message_type': 'error'
            }
            return render(request, 'signupstudent.html', context)

        # Hash the password before saving
        katalaluan_pelajar_hashed = make_password(katalaluan_pelajar)

        new_pelajar = Pelajar(
            id_pelajar=id_pelajar,
            nama_pelajar=nama_pelajar,
            email_pelajar=email_pelajar,
            no_pelajar=no_pelajar,
            katalaluan_pelajar=katalaluan_pelajar_hashed,
            program_pelajar=program_pelajar,
            gambar_pelajar=gambar_pelajar
        )
        new_pelajar.save()

        context = {
            'message': 'New student has been saved successfully.',
            'message_type': 'success'
        }
        return render(request, 'loginstudent.html', context)

    # GET request
    return render(request, 'signupstudent.html', {'message': '', 'message_type': ''})

    

def signupsupervisor(request):
    if request.method == "POST":
        id_penyelia = request.POST['id_penyelia']
        nama_penyelia = request.POST['nama_penyelia']
        email_penyelia = request.POST['email_penyelia']
        no_penyelia = request.POST['no_penyelia']
        category_penyelia = request.POST['category_penyelia']
        bilik_penyelia = request.POST.get('bilik_penyelia', '')
        bio_penyelia = request.POST.get('bio_penyelia', '')
        academic_penyelia = request.POST['academic_penyelia']
        kepakaran_penyelia = request.POST['kepakaran_penyelia']
        katalaluan_penyelia = request.POST['katalaluan_penyelia']
        gambar_penyelia = request.FILES.get('gambar_penyelia')

        # Check if supervisor ID already exists
        if Penyelia.objects.filter(id_penyelia=id_penyelia).exists():
            context = {
                'message': 'Supervisor ID already registered. Please login or use a different ID.',
                'message_type': 'error'
            }
            return render(request, 'signupsupervisor.html', context)

        # Hash the password before saving
        katalaluan_penyelia_hashed = make_password(katalaluan_penyelia)

        new_penyelia = Penyelia(
            id_penyelia=id_penyelia,
            nama_penyelia=nama_penyelia,
            email_penyelia=email_penyelia,
            no_penyelia=no_penyelia,
            category_penyelia=category_penyelia,
            bilik_penyelia=bilik_penyelia,
            bio_penyelia=bio_penyelia,
            academic_penyelia=academic_penyelia,
            kepakaran_penyelia=kepakaran_penyelia,
            katalaluan_penyelia=katalaluan_penyelia_hashed,
            gambar_penyelia=gambar_penyelia
        )
        new_penyelia.save()

        # ✅ Redirect to supervisor login page
        return redirect('loginsupervisor')  # This should match the name in your urls.py

    # GET request
    return render(request, 'signupsupervisor.html', {'message': '', 'message_type': ''})


def signupadmin(request):
    if request.method == "POST":
        id_admin = request.POST['id_admin']
        nama_admin = request.POST['nama_admin']
        email_admin = request.POST['email_admin']
        no_admin = request.POST['no_admin']
        katalaluan_admin = request.POST['katalaluan_admin']

        # ✅ Check if Admin ID already exists
        if AdminSistem.objects.filter(id_admin=id_admin).exists():
            context = {
                'message': 'Admin ID already registered. Please login or use a different ID.',
                'message_type': 'error'
            }
            return render(request, 'signupadmin.html', context)

        # ✅ Optional: Hash the password before saving
        # katalaluan_admin = make_password(katalaluan_admin)

        # ✅ Save new admin
        new_admin = AdminSistem(
            id_admin=id_admin,
            nama_admin=nama_admin,
            email_admin=email_admin,
            no_admin=no_admin,
            katalaluan_admin=katalaluan_admin
        )
        new_admin.save()

        return render(request, 'signupadmin.html', {
            'message': 'NEW ADMIN HAS BEEN SAVED',
            'message_type': 'success'
        })

    # GET request
    return render(request, 'signupadmin.html', {'message': '', 'message_type': ''})

def login(request):
    if request.method == "POST":
        role = request.POST.get("role")
        if role == "student":
            return redirect("loginstudent")
        elif role == "supervisor":
            return redirect("loginsupervisor")
        elif role == "admin":
            return redirect("loginadmin")
    return render(request, "login.html")

def loginstudent(request):
    if request.method == "POST":
        id_pelajar = request.POST.get('id_pelajar')
        katalaluan_pelajar = request.POST.get('katalaluan_pelajar')

        try:
            student = Pelajar.objects.get(id_pelajar=id_pelajar)

            if check_password(katalaluan_pelajar, student.katalaluan_pelajar):
                request.session['student'] = student.id_pelajar
                return redirect('mainstudent')
            else:
                messages.error(request, "Incorrect password.")
        except Pelajar.DoesNotExist:
            messages.error(request, "Student ID not found.")

    return render(request, 'loginstudent.html')

def forgot_password(request):
    id_pelajar = request.GET.get('id')

    if request.method == "POST":
        if 'find_id' in request.POST:
            id_input = request.POST.get('id_pelajar')
            try:
                Pelajar.objects.get(id_pelajar=id_input)
                return redirect(f"{request.path}?id={id_input}")
            except Pelajar.DoesNotExist:
                messages.error(request, "Student ID not found.")

        elif 'reset_password' in request.POST:
            id_pelajar = request.POST.get('id_pelajar')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
            else:
                try:
                    student = Pelajar.objects.get(id_pelajar=id_pelajar)
                    student.katalaluan_pelajar = make_password(new_password)  # 🔐 Securely hash password
                    student.save()
                    messages.success(request, "Password reset successfully.")
                    return redirect('loginstudent')
                except Pelajar.DoesNotExist:
                    messages.error(request, "Student not found.")

    return render(request, 'forgot_password.html', {'id_pelajar': id_pelajar})

def loginsupervisor(request):
    if request.method == "POST":
        id_penyelia = request.POST.get('id_penyelia')
        katalaluan_penyelia = request.POST.get('katalaluan_penyelia')

        try:
            penyelia = Penyelia.objects.get(id_penyelia=id_penyelia)

            if check_password(katalaluan_penyelia, penyelia.katalaluan_penyelia):
                request.session['supervisor'] = penyelia.id_penyelia
                return redirect('mainsupervisor')

            else:
                messages.error(request, "Invalid password. Please try again.")

        except Penyelia.DoesNotExist:
            messages.error(request, "Supervisor ID not found. Please check your credentials.")

    return render(request, 'loginsupervisor.html')


def forgot_password_sv(request):
    if request.method == 'POST':
        if 'find_id' in request.POST:
            id_penyelia = request.POST.get('id_penyelia', '').strip()
            try:
                penyelia = Penyelia.objects.get(id_penyelia=id_penyelia)
                return render(request, 'forgot_passwordsv.html', {'id_penyelia': penyelia.id_penyelia})
            except Penyelia.DoesNotExist:
                messages.error(request, f'No supervisor found with ID "{id_penyelia}". Please try again.')
                return render(request, 'forgot_passwordsv.html')

        elif 'reset_password' in request.POST:
            id_penyelia = request.POST.get('id_penyelia', '').strip()
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')

            if not new_password or not confirm_password:
                messages.error(request, 'Please fill in both password fields.')
                return render(request, 'forgot_passwordsv.html', {'id_penyelia': id_penyelia})

            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'forgot_passwordsv.html', {'id_penyelia': id_penyelia})

            try:
                penyelia = Penyelia.objects.get(id_penyelia=id_penyelia)
                penyelia.katalaluan_penyelia = make_password(new_password)  # Make sure this is the correct field name
                penyelia.save()
                messages.success(request, 'Password reset successfully! You can now log in with your new password.')
                return redirect('loginsupervisor')  # Redirect to supervisor login

            except Penyelia.DoesNotExist:
                messages.error(request, 'Supervisor not found. Please try again.')
                return render(request, 'forgot_passwordsv.html')

    return render(request, 'forgot_passwordsv.html')

def loginadmin(request):
    if request.method == 'POST':
        admin_id = request.POST.get('id_admin')
        password = request.POST.get('katalaluan_admin')

        try:
            admin = AdminSistem.objects.get(id_admin=admin_id)
            if admin.katalaluan_admin == password:  # Replace with hashed check in real apps
                request.session['admin_id'] = admin_id  # Optional: store session info
                return redirect('mainadmin')  # ✅ Redirect to admin dashboard
            else:
                messages.error(request, 'Incorrect password.')
        except AdminSistem.DoesNotExist:
            messages.error(request, 'Admin ID not found.')

    return render(request, 'loginadmin.html')  # 



def logoutstudent(request):
    request.session.flush()  # Clears all session data
    return redirect('index')

def mainstudent(request):
    
    id_pelajar = request.session.get('student', None)
    
    nama_pelajar = None
    if id_pelajar:
        try:
            pelajar = Pelajar.objects.get(id_pelajar=id_pelajar)
            nama_pelajar = pelajar.nama_pelajar
            welcome_message = f"HELLO, {nama_pelajar}"
        except Pelajar.DoesNotExist:
            welcome_message = "HELLO, Unknown Student"
    else:
        welcome_message = "HELLO, Guest"

    
    signupervisor = Penyelia.objects.all()

  
    return render(request, 'mainstudent.html', {
        'id_pelajar': id_pelajar,
        'nama_pelajar': nama_pelajar,
        'welcome_message': welcome_message,
        'signupervisor': signupervisor,
    })

def profilestudent(request):
    if 'student' not in request.session:
        return redirect('loginstudent')

    student_id = request.session['student']
    pelajar = get_object_or_404(Pelajar, id_pelajar=student_id)

    return render(request, 'profilestudent.html', {'pelajar': pelajar})

def update_profile(request):
    if 'student' not in request.session:
        return redirect('loginstudent')

    student_id = request.session['student']
    pelajar = get_object_or_404(Pelajar, id_pelajar=student_id)

    if request.method == "POST":
        no_pelajar = request.POST.get('no_pelajar')
        katalaluan_pelajar = request.POST.get('katalaluan_pelajar')
        gambar_pelajar = request.FILES.get('gambar_pelajar')

        if no_pelajar:
            pelajar.no_pelajar = no_pelajar

        if katalaluan_pelajar:
            pelajar.katalaluan_pelajar = make_password(katalaluan_pelajar)  # Hash password before saving

        if gambar_pelajar:
            pelajar.gambar_pelajar = gambar_pelajar

        pelajar.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profilestudent')

    return render(request, 'profilestudent.html', {'pelajar': pelajar})

    
def mainsupervisor(request):
    id_penyelia = request.session.get('supervisor', None)

    if id_penyelia:
        penyelia = get_object_or_404(Penyelia, id_penyelia=id_penyelia)
        welcome_message = f"Welcome, {penyelia.nama_penyelia}"
        # Optimized with select_related
        permohonan_list = Permohonan.objects.select_related('id_pelajar').filter(id_penyelia=penyelia)
    else:
        penyelia = None
        permohonan_list = []
        welcome_message = "Welcome, Guest"

    # Add information if status is already set for each permohonan
    for permohonan in permohonan_list:
        permohonan.has_status = Status.objects.filter(id_permohonan=permohonan).exists()

    return render(request, 'mainsupervisor.html', {
        'id_penyelia': id_penyelia,
        'welcome_message': welcome_message,
        'students': permohonan_list,
        'penyelia': penyelia,
    })


def profilesupervisor(request):
    if 'supervisor' not in request.session:
        return redirect('loginsupervisor')  # Redirect to the login page if the supervisor is not logged in

    supervisor_id = request.session['supervisor']  # Use supervisor session key
    penyelia = get_object_or_404(Penyelia, id_penyelia=supervisor_id)  # Fetch the supervisor data

    return render(request, 'profilesupervisor.html', {'penyelia': penyelia})


# Update profile view for supervisor
def update_profilesupervisor(request):
    if request.method == "POST":
        # Get the supervisor ID from session
        supervisor_id = request.session.get('supervisor')
        
        # Fetch the supervisor object from the database
        try:
            penyelia = Penyelia.objects.get(id_penyelia=supervisor_id)
        except Penyelia.DoesNotExist:
            messages.error(request, "Supervisor not found.")
            return redirect('profilesupervisor')  # Redirect back if supervisor not found

        # Update profile picture if a new image is uploaded
        if request.FILES.get('gambar_penyelia'):
            penyelia.gambar_penyelia = request.FILES['gambar_penyelia']
            penyelia.bilik_penyelia = request.POST.get('bilik_penyelia', penyelia.bilik_penyelia)
        
        penyelia.bilik_penyelia = request.POST.get('bilik_penyelia', penyelia.bilik_penyelia)# Update phone number
        penyelia.bio_penyelia = request.POST.get('bio_penyelia', penyelia.bio_penyelia)

        penyelia.no_penyelia = request.POST['no_penyelia']
        
        # Handle password update (if any)
        if request.POST.get('katalaluan_penyelia'):
            # You may hash and update password here if provided
            # e.g., using Django's set_password() for password fields
            pass
        
        # Save the updated supervisor object
        penyelia.save()

        # Add a success message
        messages.success(request, "Profile updated successfully.")

        # Redirect to supervisor's profile page
        return redirect('profilesupervisor')  # This should be the URL name for profilesupervisor.html

    # In case of GET request, redirect to profile page
    return redirect('profilesupervisor') 

def mainadmin(request):
    return render(request, 'mainadmin.html')

def studentlist(request):
    search_id = request.GET.get('search_id')
    program_filter = request.GET.get('program_pelajar')

    students = Pelajar.objects.all()

    if search_id:
        students = students.filter(id_pelajar__icontains=search_id)

    if program_filter:
        students = students.filter(program_pelajar=program_filter)

    paginator = Paginator(students, 8)  # Show 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'studentlist.html', {
        'students': page_obj.object_list,
        'page_obj': page_obj
    })
def delete_studentlist(request, id_pelajar):
    student = get_object_or_404(Pelajar, id_pelajar=id_pelajar)
    if request.method == 'POST':
        student.delete()
        return render(request, 'delete_studentlist.html')
    return render(request, 'studentlist.html')

def supervisorlist(request):
    search_id = request.GET.get('search_id')
    if search_id:
        supervisors = Penyelia.objects.filter(id_penyelia__icontains=search_id)
    else:
        supervisors = Penyelia.objects.all()
    
    return render(request, 'supervisorlist.html', {'supervisors': supervisors})


def delete_supervisorlist(request, id_penyelia):
    supervisor = get_object_or_404(Penyelia, id_penyelia=id_penyelia)
    if request.method == 'POST':
        supervisor.delete()
        return render(request, 'delete_supervisorlist.html')
    
def update_supervisorlist(request, id_penyelia):
    supervisor = get_object_or_404(Penyelia, id_penyelia=id_penyelia)
    if request.method == 'POST':
        supervisor.delete()
        return render(request, 'update_supervisorlist.html')


def update_supervisor(request, id):
    if request.method == 'POST':
        supervisor = Penyelia.objects.get(id_penyelia=id)
        supervisor.nama_penyelia = request.POST['nama_penyelia']
        supervisor.email_penyelia = request.POST['email_penyelia']
        supervisor.no_penyelia = request.POST['no_penyelia']
        supervisor.kepakaran_penyelia = request.POST['kepakaran_penyelia']
        supervisor.category_penyelia = request.POST['category_penyelia']
        supervisor.save()
        return redirect('supervisorlist')


def submitsv(request):
    return render(request, 'submitsv.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


def informationsv(request, id):
    print("Supervisor ID:", id)  # Debugging line
    supervisor = get_object_or_404(Penyelia, id_penyelia=id)
    return render(request, 'informationsv.html', {'supervisor': supervisor})

def requestform(request, id_penyelia):
    supervisor = get_object_or_404(Penyelia, pk=id_penyelia)

    if 'student' not in request.session:
        return redirect('loginstudent')

    id_pelajar_id = request.session['student']
    pelajar = get_object_or_404(Pelajar, id_pelajar=id_pelajar_id)

    tarikh_permohonan = now().date()
    id_permohonan = f"P{id_pelajar_id}"
    error_message = None

    # Check if student already has an accepted supervisor
    accepted_exists = Permohonan.objects.filter(
        id_pelajar=pelajar,
        status='Accepted'
    ).exists()

    if accepted_exists:
        error_message = "You can't make a new request because you already have a supervisor assigned."

    else:
        # Check if student needs to wait 3 days after last request
        last_request = Permohonan.objects.filter(id_pelajar=pelajar).order_by('-tarikh_permohonan').first()
        if last_request:
            days_since_last = (tarikh_permohonan - last_request.tarikh_permohonan).days
            if days_since_last < 3:
                next_allowed = last_request.tarikh_permohonan + timedelta(days=3)
                error_message = (
                    f"You can only submit a new application after {next_allowed.strftime('%d %B %Y')}."
                )

    if request.method == 'POST':
        if accepted_exists:
            error_message = "Submission blocked: You already have a supervisor assigned."
        elif not error_message:
            sinopsis = request.FILES.get('fail_permohonan', None)
            Permohonan.objects.create(
                id_permohonan=id_permohonan,
                id_pelajar=pelajar,
                id_penyelia=supervisor,
                tarikh_permohonan=tarikh_permohonan,
                sinopsis=sinopsis,
                status='Pending'
            )
            return redirect('status')

    return render(request, 'requestform.html', {
        'id_pelajar': id_pelajar_id,
        'id_penyelia': id_penyelia,
        'tarikh_permohonan': tarikh_permohonan,
        'id_permohonan': id_permohonan,
        'error_message': error_message,
    })

def adminstatic(request):
    return render(request, 'adminstatic.html', {
        'id_laporan': 'LPR001',
        'bilangan_diluluskan': 12,
        'bilangan_ditolak': 5,
        'id_admin': 'ADM2025',
    })

def status(request):
    return render(request, 'status.html')

def statuspermohonan(request):
    if 'student' not in request.session:
        return redirect('loginstudent')

    id_pelajar_id = request.session['student']
    pelajar = get_object_or_404(Pelajar, id_pelajar=id_pelajar_id)

    permohonan_list = Permohonan.objects.filter(id_pelajar=pelajar).prefetch_related('status_set')

    for permohonan in permohonan_list:
        latest_status = permohonan.status_set.order_by('-tarikh_kemaskini_status').first()

        if latest_status:
            # Convert tarikh_permohonan (a date) to aware datetime at 00:00
            tarikh_permohonan_aware = timezone.make_aware(
                datetime.combine(permohonan.tarikh_permohonan, time.min),
                timezone.get_current_timezone()
            )
            now = timezone.now()
            age = now - tarikh_permohonan_aware

            print(f"[DEBUG] Permohonan ID: {permohonan.id_permohonan}")
            print(f"[DEBUG] Status: {latest_status.status}")
            print(f"[DEBUG] Request Date: {permohonan.tarikh_permohonan}")
            print(f"[DEBUG] Age: {age.days} days")

            if latest_status.status == "pending" and age > timedelta(days=3):
                # Update status to Rejected due to timeout
                latest_status.status = "Rejected"
                latest_status.ulasan = "Auto rejected after 3 days without response."
                latest_status.tarikh_kemaskini_status = now
                latest_status.save()
                print(f"[DEBUG] Status updated to {latest_status.status} for permohonan {permohonan.id_permohonan}")

        # Attach latest_status for template usage
        permohonan.latest_status = latest_status

    return render(request, 'statuspermohonan.html', {
        'permohonan_list': permohonan_list,
        'pelajar': pelajar
    })

def statusdetails(request, id_permohonan):
    # Get the permohonan instance using id_permohonan
    permohonan = get_object_or_404(Permohonan, id=id_permohonan)

    # Get the related status instance
    status = Status.objects.filter(id_permohonan=permohonan).first()

    return render(request, 'statusdetails.html', {
        'status': status,
        'permohonan': permohonan
    })

def student_detail(request, id):
    permohonan = get_object_or_404(Permohonan, id_permohonan=id)

    if request.method == 'POST' and request.user.groups.filter(name='Penyelia').exists():
        status = request.POST.get('status')
        if status in ['accept', 'reject']:
            permohonan.status = status
            permohonan.save()

            # Redirect to result page
            return redirect('result', id=permohonan.id_permohonan)

    return render(request, 'studentdetails.html', {'permohonan': permohonan})

def result_view(request, id_permohonan):
    permohonan = get_object_or_404(Permohonan, id_permohonan=id_permohonan)
    id_status = f"S {permohonan.id_pelajar_id}"

    # Try to get or auto-create rejected status if overdue
    status_instance = Status.objects.filter(id_status=id_status).first()

    if not status_instance:
        days_passed = (date.today() - permohonan.tarikh_permohonan).days
        if days_passed > 3:
            # Auto-reject and create status
            status_instance = Status.objects.create(
                id_status=id_status,
                id_permohonan=permohonan,
                status="Rejected",
                ulasan="Automatically rejected after 3 days without action.",
                tarikh_kemaskini_status=date.today()
            )

    if request.method == "POST":
        status_value = request.POST.get("status")
        ulasan = request.POST.get("ulasan")
        tarikh_kemaskini_status = date.today()

        if status_instance:
            # Update existing status
            status_instance.status = status_value
            status_instance.ulasan = ulasan
            status_instance.tarikh_kemaskini_status = tarikh_kemaskini_status
            status_instance.save()
        else:
            # Create a new one if not found
            Status.objects.create(
                id_status=id_status,
                id_permohonan=permohonan,
                status=status_value,
                ulasan=ulasan,
                tarikh_kemaskini_status=tarikh_kemaskini_status
            )

        return redirect('result_success')

    context = {
        "permohonan": permohonan,
        "today": date.today()
    }
    return render(request, "result.html", context)


def result_success(request):  # <- match name here
    return render(request, "result_success.html")



def list(request):
    id_penyelia = request.session.get('supervisor', None)
    
    if not id_penyelia:
        return render(request, 'list.html', {'permohonan_data': []})

    penyelia = get_object_or_404(Penyelia, id_penyelia=id_penyelia)
    permohonan_list = Permohonan.objects.filter(id_penyelia=penyelia)

    data = []
    for permohonan in permohonan_list:
        status_obj = Status.objects.filter(id_permohonan=permohonan).last()
        
        # Check if there's no status, and set the status to 'PENDING'
        if not status_obj:
            status = 'Pending'
            tarikh_kemaskini_status = 'Not updated'
        else:
            status = status_obj.status
            tarikh_kemaskini_status = status_obj.tarikh_kemaskini_status

        data.append({
            'id_permohonan': permohonan.id_permohonan,
            'nama_pelajar': permohonan.id_pelajar.nama_pelajar,  # Ensure the model has a 'nama_pelajar' field
            'status': status,  # 'PENDING' if no status is found
            'tarikh_kemaskini_status': tarikh_kemaskini_status,
        })

    context = {
        'permohonan_data': data
    }
    return render(request, 'list.html', context)

def view_permohonan(request):
    status_filter = request.GET.get('status')

    # Start with all applications
    permohonans_base = Permohonan.objects.all()

    data = []
    for permohonan in permohonans_base:
        status_obj = Status.objects.filter(id_permohonan=permohonan).last()
        status = status_obj.status if status_obj else 'Pending'

        # Apply filter if selected
        if status_filter and status != status_filter:
            continue

        # Fetch names (with error handling just in case)
        nama_pelajar = permohonan.id_pelajar.nama_pelajar if hasattr(permohonan, 'id_pelajar') else 'Unknown'
        nama_penyelia = permohonan.id_penyelia.nama_penyelia if hasattr(permohonan, 'id_penyelia') else 'Unknown'

        data.append({
            'id_permohonan': permohonan.id_permohonan,
            'id_penyelia': permohonan.id_penyelia.id_penyelia if hasattr(permohonan.id_penyelia, 'id_penyelia') else 'Unknown',
            'nama_pelajar': nama_pelajar,
            'nama_penyelia': nama_penyelia,
            'status': status,
        })

    # Count status types
    count_accepted = sum(1 for d in data if d['status'] == "Accepted")
    count_rejected = sum(1 for d in data if d['status'] == "Rejected")
    total_permohonan = len(data)

    context = {
        'permohonans': data,
        'count_accepted': count_accepted,
        'count_rejected': count_rejected,
        'total_permohonan': total_permohonan,
        'selected_status': status_filter
    }

    return render(request, 'viewpermohonan.html', context)