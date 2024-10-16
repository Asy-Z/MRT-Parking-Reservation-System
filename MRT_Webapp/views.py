from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as authLogin, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.utils import timezone
from urllib.parse import quote 
from datetime import datetime
from .models import User, Commuter, Administrator, Payment, Parking, Reservation

def index(request):
    return render(request, 'index.html')

def sign_up(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')

        # Check for password match
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('sign_up')

        # Check for existing email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('sign_up')

        # Create User with hashed password
        user = User.objects.create(
            name=name,
            email=email,
            password=password1, 
            role=role
        )

        # Create the corresponding user type
        if role == 'Commuter':
            Commuter.objects.create(CommName=user.name, CommEmail=user.email, CommPass=user.password)
        elif role == 'Administrator':
            Administrator.objects.create(AdminName=user.name, AdminEmail=user.email, AdminPass=user.password)

        messages.success(request, 'User created successfully!')

        # Redirect to login page
        return redirect('login')

    return render(request, 'sign_up.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the user is a Commuter
        commuter = Commuter.objects.filter(CommEmail=email, CommPass=password).first()
        if commuter:
            request.session['user_id'] = commuter.CommID  # Store Commuter ID in session
            request.session['role'] = 'Commuter'
            request.session['name'] = commuter.CommName
            return redirect('dashboard')

        # Check if the user is an Administrator
        administrator = Administrator.objects.filter(AdminEmail=email, AdminPass=password).first()
        if administrator:  # Check hashed password
            request.session['user_id'] = administrator.AdminID  # Store Admin ID in session
            request.session['role'] = 'Administrator'
            request.session['name'] = administrator.AdminName
            return redirect('dashboard')

        # If no user matches, show an error message
        messages.error(request, 'Invalid email or password.')
        return redirect('login')

    return render(request, 'login.html')

def logingOut(request):
    logout(request)
    return redirect('index')

def dashboard(request):
    return render(request, "dashboard.html")

def parking_manager(request):
    if request.method == 'POST':
        station = request.POST.get('station')
        level = request.POST.get('level')
        box_no = request.POST.get('box_no')
        status = request.POST.get('status')

        park_id = f"{station}-{level}-{f'Box {box_no}'}"
        
        try:
            selected_parking = Parking.objects.get(ParkID=park_id)
            
            if selected_parking.Status == 'Reserved':
                messages.error(request, 'This spot has already been reserved. Try Again')
                return redirect('parking_manager')
            else:
                selected_parking.Status = status
                selected_parking.save()
                messages.success(request, 'The parking spot status has been successfully updated.')
                return redirect('parking_manager')  
        except Parking.DoesNotExist:
            messages.error(request, 'The selected parking spot does not exist.')
            return redirect('parking_manager')

    context = {
        'parking_spots': Parking.MRT,  
        'ParkBox': Parking.ParkBox,  
        'kondisi_choices': Parking.kondisi,  
    }

    return render(request, "parking_manager.html", context) 

def reservation_creation(request):
    if request.method == 'POST':
        # Get the form data
        station = request.POST.get('station')
        level = request.POST.get('level')
        box_no = request.POST.get('box_no')
        date_time_start = request.POST.get('date_time_start')
        date_time_end = request.POST.get('date_time_end')
        plate_no = request.POST.get('plate_no')

        # Generate park_id
        park_id = f"{station}-{level}-{f'Box {box_no}'}"

        try:
            selected_parking = Parking.objects.get(ParkID=park_id)

            if selected_parking.Status in ['Reserved', 'Under Maintenance']:
                messages.error(request, 'This spot has already been reserved. Try again.')
                return redirect('reservation_creation')
            else:
                # Use the session data to retrieve the Commuter
                commuter_id = request.session.get('user_id')
                commuter = Commuter.objects.filter(CommID=commuter_id).first()  # Fetch commuter by ID

                if not commuter:
                    messages.error(request, 'You must be logged in to make a reservation.')
                    return redirect('login')  # Redirect to login if commuter is not found

                # Calculate total days and amount
                start_date = datetime.strptime(date_time_start, "%Y-%m-%dT%H:%M")
                end_date = datetime.strptime(date_time_end, "%Y-%m-%dT%H:%M")
                total_days = (end_date - start_date).days + 1
                amount = total_days * 4.50

                # Store reservation data in the session
                request.session['reservation_data'] = {
                    'CommID': commuter.CommID,
                    'ParkID': park_id,
                    'PlateNo': plate_no,
                    'DateTimeStart': date_time_start,
                    'DateTimeEnd': date_time_end,
                    'Amount': amount
                }

                return redirect('payment_proceed')  # Redirect to payment proceed view

        except Parking.DoesNotExist:
            messages.error(request, 'The selected parking spot does not exist.')
            return redirect('reservation_creation')

    context = {
        'spot_park': Parking.MRT,
        'BoxPark': Parking.ParkBox,
    }

    return render(request, "reservation_creation.html", context)


def payment_proceed(request):
    if request.method == 'POST':
        # Retrieve each field directly from the session
        reservation_data = request.session.get('reservation_data')

        if not reservation_data:
            messages.error(request, 'No reservation data found. Please make a reservation first.')
            return redirect('reservation_creation')

        park_id = reservation_data['ParkID']
        plate_no = reservation_data['PlateNo']
        datetime_start = reservation_data['DateTimeStart']
        datetime_end = reservation_data['DateTimeEnd']
        amount = reservation_data['Amount']
        comm_id = reservation_data['CommID']  # Retrieved from session (this is the Commuter ID)
        payment_method = request.POST.get('method')  # Payment method chosen by the user

        try:
            # Retrieve the actual Commuter instance
            commuter = Commuter.objects.get(CommID=comm_id)

            # Retrieve the actual Parking instance using the park_id
            parking = Parking.objects.get(ParkID=park_id)

            # Create a new Payment entry, using the commuter instance
            payment = Payment(
                CommID=commuter,  # Pass the Commuter instance, not the ID
                Method=payment_method,
                Amount=amount
            )
            payment.save()

            # Finalize the reservation
            reservation = Reservation(
                CommID=commuter,  # Pass the Commuter instance here too
                ParkID=parking,   # Pass the Parking instance, not just the park_id string
                PlateNo=plate_no,
                DateTimeStart=datetime_start,
                DateTimeEnd=datetime_end,
                PayID=payment  # Save payment instance
            )
            reservation.save()

            # Update parking status to 'Reserved'
            parking.Status = 'Reserved'
            parking.save()
            
            request.session['reservation_data'] = {
                    'CommID': commuter.CommID,
                    'ParkID': park_id,
                    'PlateNo': plate_no,
                    'DateTimeStart': reservation.DateTimeStart,
                    'DateTimeEnd': reservation.DateTimeEnd,
                    'Amount': amount,
                    'PayID' : payment.PayID
                }

            messages.success(request, 'Reservation and payment successful!')
            return redirect('paid')  
        except Commuter.DoesNotExist:
            messages.error(request, 'Commuter not found. Please log in again.')
            return redirect('login')
        except Parking.DoesNotExist:
            messages.error(request, 'Parking spot not found. Please try again.')
            return redirect('reservation_creation')
        except Exception as e:
            messages.error(request, f'An error occurred during payment processing: {str(e)}')
            return redirect('reservation_creation')

    else:
        return render(request, 'payment_proceed.html')

def paid(request):
    reservation_data = request.session.get('reservation_data')
    transaction_id = reservation_data['PayID']  # Example: Set this when payment is processed
    amount = reservation_data['Amount']  # Example: Amount paid
    date = timezone.now().strftime("%Y-%m-%d %H:%M:%S")  # Current date/time or fetch from the payment record

    context = {
        'transaction_id': transaction_id,
        'amount': amount,
        'date': date,
    }

    return render(request, "paid.html", context)

def reservation_view(request):
    commuter_id = request.session.get('user_id')
    if not commuter_id:
        messages.error(request, 'You must be logged in to view your reservations.')
        return redirect('login') 

    reservations = Reservation.objects.filter(CommID=commuter_id)

    return render(request, 'reservation_view.html', {'reservations': reservations})

def reservation_cancelled(request, reservation_id):
    try:
        cancelled = Reservation.objects.get(ReserveID=reservation_id)
        
        parking_update = Parking.objects.get(ParkID=cancelled.ParkID.ParkID)
        parking_update.Status = 'Available'
        parking_update.save()
        
        payment_refund = Payment.objects.get(PayID=cancelled.PayID.PayID)
        payment_refund.delete()

        cancelled.delete()

        messages.success(request, 'Reservation cancelled and payment refunded successfully.')
        return redirect('reservation_cancelled')

    except Reservation.DoesNotExist:
        messages.error(request, 'The reservation does not exist.')
        return redirect('reservation_view')

    except Parking.DoesNotExist:
        messages.error(request, 'Associated parking spot not found.')
        return redirect('reservation_view')

    except Payment.DoesNotExist:
        messages.error(request, 'Associated payment not found.')
        return redirect('reservation_view')

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('reservation_view')

def reservation_report(request):
    if not request.session.get('role') in ['Administrator']:
        return render(request, 'login.html', {'error': 'Unauthorized access'})
    
    reservations = Reservation.objects.all()
    return render(request, "reservation_report.html", {'reservations':reservations})

def transaction(request):
    if not request.session.get('role') in ['Administrator']:
        return render(request, 'login.html', {'error': 'Unauthorized access'})

    transactions = Payment.objects.all() 

    context = {
        'transactions': transactions,
    }
    return render(request, 'transaction.html', context)

