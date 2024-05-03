from email import message
from unicodedata import category
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from config.settings import MEDIA_ROOT, MEDIA_URL
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from reservationApp.forms import UserRegistration, UpdateProfile, UpdatePasswords, SaveCategory, SaveLocation, SaveBus, SaveSchedule, SaveBooking, PayBooked
from reservationApp.models import Booking, Category, Location, Bus, Schedule
from cryptography.fernet import Fernet
from django.conf import settings
import base64
from datetime import datetime
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from .forms import TripRequestForm
from .models import Department, TripRequest
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.core import serializers
from dateutil.relativedelta import relativedelta


context = {
    'page_title' : 'File Management System',
}

def admin_check(user):
    return user.is_staff

#login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

@login_required
def home(request):
    today = timezone.now()
    tomorrow = today + timezone.timedelta(days=1)
    yesterday = today - timezone.timedelta(days=1)
    last_month = today - relativedelta(months=1)
    context['page_title'] = 'Home'
    context['buses'] = Bus.objects.count()
    context['categories'] = Category.objects.count()
    context['trip_requests'] = TripRequest.objects.count()
    context['upcoming_trip'] = Schedule.objects.filter(status=1, schedule__gt=today).count()
    context['yesterdays_trip'] = Schedule.objects.filter(schedule__date=yesterday.date()).count()
    context['todays_trip'] = Schedule.objects.filter(schedule__range=(today, tomorrow)).count()
    context['todays_trips'] = Schedule.objects.filter(schedule__date=today.date())
    context['last_month_trips'] = Schedule.objects.filter(schedule__date__range=(last_month, today)).count()
    
    if context['last_month_trips'] > 0:
        context['trip_increase_percentage'] = ((context['upcoming_trip'] - context['last_month_trips']) / context['last_month_trips']) * 100
    else:
        context['trip_increase_percentage'] = 0

    if context['yesterdays_trip'] > 0:
        context['todays_trip_increase_percentage'] = ((context['todays_trip'] - context['yesterdays_trip']) / context['yesterdays_trip']) * 100
    else:
        context['todays_trip_increase_percentage'] = 0


    return render(request, 'home.html', context)

def registerUser(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home-page')
    context = {}
    context['page_title'] = "Register User"
    if request.method == 'POST':
        data = request.POST
        form = UserRegistration(data)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            # Create a Department instance and associate it with the user
            status = data.get('status')  # get the status from the submitted form data
            Department.objects.create(user=user, status=status)

            # Generate email verification token
            token = default_token_generator.make_token(user)

            # Get current site
            current_site = get_current_site(request)

            # Send an email to the user with the token
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            send_mail(mail_subject, message, 'info@mywebsite.com', [user.email])

            messages.success(request, 'Please confirm your email address to complete the registration')
            return redirect('login')
        else:
            context['form'] = form
    else:
        form = UserRegistration()
        context['form'] = form
    return render(request, 'register.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated, you can now login.')
            return redirect('login')  # assuming you have a login view named 'login'
        else:
            messages.error(request, 'The activation link is invalid!')
            return redirect('register-user')  # assuming you have a register view named 'register'
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        messages.error(request, 'The activation link is invalid!')
        return redirect('register-user')  # assuming you have a register view named 'register'


@login_required
def update_profile(request):
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = UpdateProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile")
        else:
            context['form'] = form
            
    return render(request, 'manage_profile.html',context)


@login_required
def update_password(request):
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile")
        else:
            context['form'] = form
    else:
        form = UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)


@login_required
def profile(request):
    context['page_title'] = 'Profile'
    return render(request, 'profile.html',context)


# Category
@user_passes_test(admin_check)
def category_mgt(request):
    context['page_title'] = "Bus Categories"
    categories = Category.objects.all()
    context['categories'] = categories

    return render(request, 'category_mgt.html', context)

@user_passes_test(admin_check)
def save_category(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            category = Category.objects.get(pk=request.POST['id'])
        else:
            category = None
        if category is None:
            form = SaveCategory(request.POST)
        else:
            form = SaveCategory(request.POST, instance= category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

@user_passes_test(admin_check)
def manage_category(request, pk=None):
    context['page_title'] = "Manage Category"
    if not pk is None:
        category = Category.objects.get(id = pk)
        context['category'] = category
    else:
        context['category'] = {}

    return render(request, 'manage_category.html', context)

@user_passes_test(admin_check)
def delete_category(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            category = Category.objects.get(id = request.POST['id'])
            category.delete()
            messages.success(request, 'Category has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'Category has failed to delete'
            print(err)

    else:
        resp['msg'] = 'Category has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Location
@user_passes_test(admin_check)
def location_mgt(request):
    context['page_title'] = "Locations"
    locations = Location.objects.all()
    context['locations'] = locations

    return render(request, 'location_mgt.html', context)

@user_passes_test(admin_check)
def save_location(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            location = Location.objects.get(pk=request.POST['id'])
        else:
            location = None
        if location is None:
            form = SaveLocation(request.POST)
        else:
            form = SaveLocation(request.POST, instance= location)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

@user_passes_test(admin_check)
def manage_location(request, pk=None):
    context['page_title'] = "Manage Location"
    if not pk is None:
        location = Location.objects.get(id = pk)
        context['location'] = location
    else:
        context['location'] = {}

    return render(request, 'manage_location.html', context)

@user_passes_test(admin_check)
def delete_location(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            location = Location.objects.get(id = request.POST['id'])
            location.delete()
            messages.success(request, 'Location has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'location has failed to delete'
            print(err)

    else:
        resp['msg'] = 'location has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")


# bus
@user_passes_test(admin_check)
def bus_mgt(request):
    context['page_title'] = "Buses"
    buses = Bus.objects.all()
    context['buses'] = buses

    return render(request, 'bus_mgt.html', context)

@user_passes_test(admin_check)
def save_bus(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            bus = Bus.objects.get(pk=request.POST['id'])
        else:
            bus = None
        if bus is None:
            form = SaveBus(request.POST)
        else:
            form = SaveBus(request.POST, instance= bus)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bus has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

@user_passes_test(admin_check)
def manage_bus(request, pk=None):
    context['page_title'] = "Manage Bus"
    categories = Category.objects.filter(status = 1).all()
    context['categories'] = categories
    if not pk is None:
        bus = Bus.objects.get(id = pk)
        context['bus'] = bus
    else:
        context['bus'] = {}

    return render(request, 'manage_bus.html', context)

@user_passes_test(admin_check)
def delete_bus(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            bus = Bus.objects.get(id = request.POST['id'])
            bus.delete()
            messages.success(request, 'Bus has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'bus has failed to delete'
            print(err)

    else:
        resp['msg'] = 'bus has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")    


# schedule
@user_passes_test(admin_check)
def schedule_mgt(request):
    context['page_title'] = "Trip Schedules"
    schedules = Schedule.objects.all()
    context['schedules'] = schedules

    return render(request, 'schedule_mgt.html', context)

@user_passes_test(admin_check)
def save_schedule(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            schedule = Schedule.objects.get(pk=request.POST['id'])
        else:
            schedule = None
        if schedule is None:
            form = SaveSchedule(request.POST)
        else:
            form = SaveSchedule(request.POST, instance=schedule)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.save()
            form.save_m2m()  # save the many-to-many data for the form
            messages.success(request, 'Schedule has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@user_passes_test(admin_check)
def manage_schedule(request, pk=None):
    context = {}
    context['page_title'] = "Manage Schedule"
    buses = Bus.objects.filter(status = 1).all()
    locations = Location.objects.filter(status = 1).all()
    context['buses'] = buses
    context['locations'] = locations
    context['able_to_book_choices'] = Schedule.ABLE_TO_BOOK_CHOICES

    if not pk is None:
        schedule = Schedule.objects.get(id = pk)
        context['schedule'] = schedule
    else:
        context['schedule'] = {}

    return render(request, 'manage_schedule.html', context)

@user_passes_test(admin_check)
def delete_schedule(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            schedule = Schedule.objects.get(id = request.POST['id'])
            schedule.delete()
            messages.success(request, 'Schedule has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'schedule has failed to delete'
            print(err)

    else:
        resp['msg'] = 'Schedule has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")  


@login_required
def scheduled_trips(request):
    context = {}
    try:
        # Get the department of the current user
        user_department = Department.objects.get(user=request.user).status
    except ObjectDoesNotExist:
        user_department = None

    if not request.method == 'POST':
        context['page_title'] = "Scheduled Trips"
        # Filter the schedules based on the status, schedule and able_to_book fields
        schedules = Schedule.objects.filter(status='1', schedule__gt=datetime.now(), able_to_book=user_department).all()
        context['schedules'] = schedules
        context['is_searched'] = False
        context['data'] = {}
    else:
        context['page_title'] = "Search Result | Scheduled Trips"
        context['is_searched'] = True
        date = datetime.strptime(request.POST['date'],"%Y-%m-%d").date()
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')
        depart = Location.objects.get(id=request.POST['depart'])
        destination = Location.objects.get(id=request.POST['destination'])
        # Filter the schedules based on the status, schedule, depart, destination and able_to_book fields
        schedules = Schedule.objects.filter(Q(status='1') & Q(schedule__year=year) & Q(schedule__month=month) & Q(schedule__day=day) & Q(Q(depart=depart) | Q(destination=destination)) & Q(able_to_book=user_department)).all()
        context['schedules'] = schedules
        context['data'] = {'date':date,'depart':depart, 'destination': destination}

    return render(request, 'scheduled_trips.html', context)

def api_scheduled_trips(request):
    try:
        user_department = Department.objects.get(user=request.user).status
    except ObjectDoesNotExist:
        user_department = None

    schedules = Schedule.objects.filter(status='1', schedule__gt=datetime.now(), able_to_book=user_department).all()
    schedules_json = serializers.serialize('json', schedules)

    return JsonResponse(schedules_json, safe=False)

@login_required
def manage_booking(request, schedPK=None, pk=None):
    context['page_title'] = "Manage Booking"
    context['schedPK'] = schedPK
    if not schedPK is None:
        schedule = Schedule.objects.get(id = schedPK)
        context['schedule'] = schedule
    else:
        context['schedule'] = {}
    if not pk is None:
        book = Booking.objects.get(id = pk)
        context['book'] = book
    else:
        context['book'] = {}

    return render(request, 'manage_book.html', context)

@login_required
def save_booking(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            booking = Booking.objects.get(pk=request.POST['id'])
        else:
            booking = None
        if booking is None:
            form = SaveBooking(request.POST)
        else:
            form = SaveBooking(request.POST, instance= booking)
        if form.is_valid():
            form.save()
            if booking is None:
                booking = Booking.objects.last()
                messages.success(request, f'Booking has been saved successfully. Your Booking Refderence Code is: <b>{booking.code}</b>', extra_tags = 'stay')
            else:
                messages.success(request, f'<b>{booking.code}</b> Booking has been updated successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

@user_passes_test(admin_check)
def approve_booked(request):
    resp = {'status':'failed','msg':''}
    if not request.method == 'POST':
        resp['msg'] = "Unknown Booked ID"
    else:
        booking = Booking.objects.get(id= request.POST['id'])
        form = PayBooked(request.POST, instance=booking)
        if form.is_valid():
            booking.status = '2'  # Change the status to 'Approved'
            form.save()
            messages.success(request, f"<b>{booking.code}</b> has been approved successfully", extra_tags='stay')
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    resp['msg'] += str(error + "<br>")
    
    return HttpResponse(json.dumps(resp),content_type = 'application/json')

@user_passes_test(admin_check)
def reject_booked(request):
    resp = {'status':'failed','msg':''}
    if not request.method == 'POST':
        resp['msg'] = "Unknown Booked ID"
    else:
        booking = Booking.objects.get(id= request.POST['id'])
        form = PayBooked(request.POST, instance=booking)
        if form.is_valid():
            booking.status = '3'  # Change the status to 'Rejected'
            form.save()
            messages.success(request, f"<b>{booking.code}</b> has been rejected", extra_tags='stay')
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    resp['msg'] += str(error + "<br>")
    
    return HttpResponse(json.dumps(resp),content_type = 'application/json')


@user_passes_test(admin_check)
def bookings(request):
    context['page_title'] = "Bookings"
    # Exclude bookings with status '2' (approved) and '3' (rejected)
    bookings = Booking.objects.exclude(status__in=['2', '3'])
    context['bookings'] = bookings

    return render(request, 'bookings.html', context)


@user_passes_test(admin_check)
def view_booking(request,pk=None):
    if pk is None:
        messages.error(request, "Unkown Booking ID")
        return redirect('booking-page')
    else:
        context['page_title'] = 'Vieww Booking'
        context['booking'] = Booking.objects.get(id = pk)
        return render(request, 'view_booked.html', context)


@user_passes_test(admin_check)
def delete_booking(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            booking = Booking.objects.get(id = request.POST['id'])
            code = booking.code
            booking.delete()
            messages.success(request, f'[<b>{code}</b>] Booking has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'booking has failed to delete'
            print(err)

    else:
        resp['msg'] = 'booking has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")  

@login_required
def find_trip(request):
    context['page_title'] = 'Find Trip Schedule'
    context['locations'] = Location.objects.filter(status = 1).all
    today = datetime.today().strftime("%Y-%m-%d")
    context['today'] = today
    return render(request, 'find_trip.html', context)
    
@login_required
def request_trip(request):
    if request.method == 'POST':
        form = TripRequestForm(request.POST)
        if form.is_valid():
            trip_request = form.save(commit=False)
            trip_request.user = request.user
            trip_request.save()
            messages.success(request, 'Your trip request has been sent successfully.')
            form = TripRequestForm()
    else:
        form = TripRequestForm()
    return render(request, 'request_trip.html', {'form': form})


@user_passes_test(admin_check)
def trip_request_list(request):
    trip_requests = TripRequest.objects.filter(status='active')
    return render(request, 'trip_request_list.html', {'trip_requests': trip_requests})

def handle_request(request, request_id):
    trip_request = TripRequest.objects.get(id=request_id)
    if request.POST['action'] == 'accept':
        trip_request.status = 'accepted'
        Schedule.objects.create(
            code=str(trip_request.id),  # you might want to generate a unique code here
            bus=trip_request.bus,
            depart=trip_request.depart,
            destination=trip_request.destination,
            schedule=trip_request.schedule,
            seats_available=trip_request.seats,
            status='1'  # assuming '1' means 'Active'
        )
        messages.success(request, 'Request has been added to Scheduled Trips List successfully.')
    else:
        trip_request.status = 'rejected'
        messages.success(request, 'Request has been rejected successfully.')
    trip_request.save()
    return redirect('trip_request_list')

@login_required
def request_status(request):
    trip_request = TripRequest.objects.filter(user=request.user).last()
    return render(request, 'request_status.html', {'trip_request': trip_request})