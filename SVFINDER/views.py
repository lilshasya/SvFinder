from django.conf import settings
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Pelajar,Penyelia,AdminSistem,Permohonan,Status
from datetime import date
from datetime import datetime, time, timedelta
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef


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

        # Exclude permohonan that already has a status
        permohonan_with_status = Status.objects.filter(id_permohonan=OuterRef('pk'))
        permohonan_list = (
            Permohonan.objects.select_related('id_pelajar')
            .filter(id_penyelia=penyelia)
            .annotate(has_status=Exists(permohonan_with_status))
            .filter(has_status=False)
        )
    else:
        penyelia = None
        permohonan_list = []
        welcome_message = "Welcome, Guest"

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
    student_count = Pelajar.objects.count()
    supervisor_count = Penyelia.objects.count()
    report_count = Permohonan.objects.count()

    range_type = request.GET.get('range', 'week')  # default to 'week'
    today = timezone.now().date()

    labels = []
    data = []

    if range_type == 'day':
        labels = [today.strftime('%d-%b-%Y')]
        count = Permohonan.objects.filter(tarikh_permohonan=today).count()
        data = [count]

    elif range_type == 'month':
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month.replace(month=start_of_month.month % 12 + 1, day=1) - timedelta(days=1))

        monthly_data = (
            Permohonan.objects
            .filter(tarikh_permohonan__range=[start_of_month, end_of_month])
            .values('tarikh_permohonan')
            .annotate(count=Count('id_permohonan'))
        )

        # Create a dictionary for fast lookup
        count_map = {item['tarikh_permohonan']: item['count'] for item in monthly_data}

        for i in range(1, end_of_month.day + 1):
            day = start_of_month.replace(day=i)
            labels.append(day.strftime('%d %b'))
            data.append(count_map.get(day, 0))

    else:  # week
        start_date = today - timedelta(days=6)
        weekly_data = (
            Permohonan.objects
            .filter(tarikh_permohonan__range=[start_date, today])
            .values('tarikh_permohonan')
            .annotate(count=Count('id_permohonan'))
        )
        count_map = {item['tarikh_permohonan']: item['count'] for item in weekly_data}

        for i in range(7):
            day = start_date + timedelta(days=i)
            labels.append(day.strftime('%a'))  # e.g., Mon
            data.append(count_map.get(day, 0))

    context = {
        'student_count': student_count,
        'supervisor_count': supervisor_count,
        'report_count': report_count,
        'chart_labels': labels,
        'chart_data': data,
        'selected_range': range_type,
    }

    return render(request, 'mainadmin.html', context)

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

    tarikh_permohonan = date.today()
    id_permohonan = f"P{id_pelajar_id}_{now().strftime('%Y%m%d%H%M%S')}"
    error_message = None

    # ✅ Check if already accepted
    accepted_exists = Status.objects.filter(
        id_permohonan__id_pelajar=pelajar,
        status='Accepted'
    ).exists()

    if accepted_exists:
        error_message = "You already have a supervisor assigned. You cannot make any more requests."
    else:
        last_request = Permohonan.objects.filter(id_pelajar=pelajar).order_by('-tarikh_permohonan').first()

        if last_request:
            last_status = Status.objects.filter(id_permohonan=last_request).order_by('-tarikh_kemaskini_status').first()
            days_since_last = (tarikh_permohonan - last_request.tarikh_permohonan).days

            if not last_status:
                if days_since_last >= 3:
                    Status.objects.create(
                        id_status=f"S{last_request.id_pelajar.id}",
                        id_permohonan=last_request,
                        status='Rejected',
                        ulasan='Auto-rejected due to no response after 3 days.',
                        tarikh_kemaskini_status=tarikh_permohonan
                    )
                else:
                    next_allowed = last_request.tarikh_permohonan + timedelta(days=3)
                    error_message = f"You must wait until {next_allowed.strftime('%d %B %Y')} to reapply."
            elif last_status.status != 'Rejected' and days_since_last < 3:
                next_allowed = last_request.tarikh_permohonan + timedelta(days=3)
                error_message = f"You must wait until {next_allowed.strftime('%d %B %Y')} to reapply."

    if request.method == 'POST' and not error_message:
        sinopsis = request.FILES.get('fail_permohonan')

        Permohonan.objects.create(
            id_permohonan=id_permohonan,
            id_pelajar=pelajar,
            id_penyelia=supervisor,
            tarikh_permohonan=tarikh_permohonan,
            sinopsis=sinopsis
        )

        return redirect('status')

    return render(request, 'requestform.html', {
        'id_pelajar': id_pelajar_id,
        'id_penyelia': id_penyelia,
        'tarikh_permohonan': tarikh_permohonan,
        'id_permohonan': id_permohonan,
        'error_message': error_message,
    })


def status(request):
    return render(request, 'status.html')


def statuspermohonan(request):
    if 'student' not in request.session:
        return redirect('loginstudent')

    id_pelajar_id = request.session['student']
    pelajar = get_object_or_404(Pelajar, id_pelajar=id_pelajar_id)

    permohonan_list = Permohonan.objects.filter(id_pelajar=pelajar).prefetch_related('status_set')
    now_time = timezone.now()
    accepted_exists = False  # Flag for accepted status

    for permohonan in permohonan_list:
        status_list = permohonan.status_set.order_by('-tarikh_kemaskini_status')
        latest_status = status_list.first()

        tarikh_permohonan_aware = timezone.make_aware(
            datetime.combine(permohonan.tarikh_permohonan, time.min),
            timezone.get_current_timezone()
        )
        age = now_time - tarikh_permohonan_aware

        if latest_status:
            if latest_status.status == "Accepted":
                accepted_exists = True  # ✅ Student already has an accepted supervisor
            elif latest_status.status == "Pending" and age > timedelta(days=3):
                latest_status.status = "Rejected"
                latest_status.ulasan = "Auto rejected after 3 days without response."
                latest_status.tarikh_kemaskini_status = now_time
                latest_status.save()
        else:
            if age > timedelta(days=3):
                Status.objects.create(
                    id_status=f"S{permohonan.id_pelajar.id}",
                    id_permohonan=permohonan,
                    status='Rejected',
                    ulasan='Auto rejected due to no status after 3 days.',
                    tarikh_kemaskini_status=now_time.date()
                )

        permohonan.latest_status = Status.objects.filter(id_permohonan=permohonan).order_by('-tarikh_kemaskini_status').first()

    return render(request, 'statuspermohonan.html', {
        'permohonan_list': permohonan_list,
        'pelajar': pelajar,
        'accepted_exists': accepted_exists  # Pass to template
    })



def student_detail(request, id):
    permohonan = get_object_or_404(Permohonan, id_permohonan=id)

    if request.method == 'POST' and request.user.groups.filter(name='Penyelia').exists():
        status_choice = request.POST.get('status')
        ulasan = request.POST.get('remarks', '')

        if status_choice in ['accept', 'reject']:
            status_value = 'Accepted' if status_choice == 'accept' else 'Rejected'

            # Rejected other pending permohonan if accept is selected
            if status_value == 'Accepted':
                Status.objects.filter(
                    id_permohonan__id_pelajar=permohonan.id_pelajar,
                    status='Pending'
                ).exclude(id_permohonan=permohonan).update(
                    status='Rejected',
                    ulasan='Auto rejected after another supervisor accepted.',
                    tarikh_kemaskini_status=now()
                )

            Status.objects.create(
                id_status=f"S{permohonan.id_pelajar.id}_{now().strftime('%Y%m%d%H%M%S')}",
                id_permohonan=permohonan,
                status=status_value,
                ulasan=ulasan or ('Accepted by supervisor' if status_value == 'Accepted' else 'Rejected by supervisor'),
                tarikh_kemaskini_status=now()
            )

            return redirect('result', id=permohonan.id_permohonan)

    return render(request, 'studentdetails.html', {'permohonan': permohonan})

def result_view(request, id_permohonan):
    permohonan = get_object_or_404(Permohonan, id_permohonan=id_permohonan)

    if request.method == "POST":
        id_status = f"S-{permohonan.id_permohonan}"  # Unique per permohonan
        status_value = request.POST.get("status")
        ulasan = request.POST.get("ulasan")
        tarikh_kemaskini_status = date.today()

        Status.objects.update_or_create(
            id_status=id_status,
            defaults={
                "id_permohonan": permohonan,
                "status": status_value,
                "ulasan": ulasan,
                "tarikh_kemaskini_status": tarikh_kemaskini_status,
            }
        )

        # Tambahan: Auto-reject permohonan lain jika accepted
        if status_value == "Accepted":
            Status.objects.filter(
                id_permohonan__id_pelajar=permohonan.id_pelajar
            ).exclude(id_permohonan=permohonan).update(
                status="Rejected",
                ulasan="Auto rejected after one application was accepted.",
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
        return render(request, 'list.html', {'permohonan_data': [], 'no_data': True})

    penyelia = get_object_or_404(Penyelia, id_penyelia=id_penyelia)
    permohonan_list = Permohonan.objects.filter(id_penyelia=penyelia)

    data = []
    accepted_count = 0
    rejected_count = 0
    pending_count = 0

    for permohonan in permohonan_list:
        status_obj = Status.objects.filter(id_permohonan=permohonan).last()

        if not status_obj:
            status = 'Pending'
            tarikh_kemaskini_status = 'Not updated'
            pending_count += 1
        else:
            status = status_obj.status
            tarikh_kemaskini_status = status_obj.tarikh_kemaskini_status

            if status.lower() == 'accepted':
                accepted_count += 1
            elif status.lower() == 'rejected':
                rejected_count += 1
            elif status.lower() == 'pending':
                pending_count += 1

        data.append({
            'id_permohonan': permohonan.id_permohonan,
            'nama_pelajar': permohonan.id_pelajar.nama_pelajar,
            'status': status,
            'tarikh_kemaskini_status': tarikh_kemaskini_status,
        })

    context = {
        'permohonan_data': data,
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
        'pending_count': pending_count,
        'total_count': len(data),
        'no_data': len(data) == 0,
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