# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Room, Booking, Contact
# from django.contrib import messages

# def home(request):
#     rooms = Room.objects.filter(is_available=True)[:3]
#     return render(request, 'main/home.html', {'rooms': rooms})

#     room = get_object_or_404(Room, pk=pk)
#     return render(request, 'main/rooms_details.html', {'room': room})

# def book_room(request, pk):
#     room = get_object_or_404(Room, pk=pk)
#     if request.method == 'POST':
#         Booking.objects.create(
#             room=room,
#             guest_name=request.POST['guest_name'],
#             guest_email=request.POST['guest_email'],
#             guest_phone=request.POST['guest_phone'],
#             check_in=request.POST['check_in'],
#             check_out=request.POST['check_out'],
#         )
#         messages.success(request, 'Room booked successfully!')
#         return redirect('home')
#     return render(request, 'main/book_room.html', {'room': room})

# def contact(request):
#     if request.method == 'POST':
#         Contact.objects.create(
#             name=request.POST['name'],
#             email=request.POST['email'],
#             message=request.POST['message'],
#         )
#         messages.success(request, 'Message sent successfully!')
#         return redirect('contact')
#     return render(request, 'main/contact.html')





# def rooms(request):
#     all_rooms = Room.objects.filter(is_available=True)
    
#     # Search & Filter
#     search = request.GET.get('search', '')
#     room_type = request.GET.get('room_type', '')
#     max_price = request.GET.get('max_price', '')
#     capacity = request.GET.get('capacity', '')
    
#     if search:
#         all_rooms = all_rooms.filter(name__icontains=search)
#     if room_type:
#         all_rooms = all_rooms.filter(room_type=room_type)
#     if max_price:
#         all_rooms = all_rooms.filter(price_per_night__lte=max_price)
#     if capacity:
#         all_rooms = all_rooms.filter(capacity__gte=capacity)
    
#     context = {
#         'rooms': all_rooms,
#         'search': search,
#         'room_type': room_type,
#         'max_price': max_price,
#         'capacity': capacity,
#     }
#     return render(request, 'main/rooms.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Booking, Contact, Payment
from django.contrib import messages
from django.utils import timezone
import uuid
from datetime import date








def book_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        booking = Booking.objects.create(
            room=room,
            guest_name=request.POST['guest_name'],
            guest_email=request.POST['guest_email'],
            guest_phone=request.POST['guest_phone'],
            check_in=request.POST['check_in'],
            check_out=request.POST['check_out'],
        )
        # Calculate total amount
        check_in = date.fromisoformat(request.POST['check_in'])
        check_out = date.fromisoformat(request.POST['check_out'])
        nights = (check_out - check_in).days
        total = nights * room.price_per_night

        Payment.objects.create(booking=booking, amount=total)
        return redirect('payment', booking_id=booking.id)

    return render(request, 'main/room_detail.html', {'room': room})


def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment = get_object_or_404(Payment, booking=booking)
    nights = (booking.check_out - booking.check_in).days
    return render(request, 'main/payment.html', {
        'booking': booking,
        'payment': payment,
        'nights': nights,
    })


def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment_obj = get_object_or_404(Payment, booking=booking)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        # Simulate payment success
        payment_obj.status = 'paid'
        payment_obj.transaction_id = str(uuid.uuid4())[:12].upper()
        payment_obj.paid_at = timezone.now()
        payment_obj.save()
        messages.success(request, f'✅ Payment successful! Transaction ID: {payment_obj.transaction_id}')
        return redirect('booking_success', booking_id=booking.id)
    return redirect('payment', booking_id=booking_id)


def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment_obj = get_object_or_404(Payment, booking=booking)
    return render(request, 'main/booking_success.html', {
        'booking': booking,
        'payment': payment_obj,
    })


def home(request):
    rooms = Room.objects.filter(is_available=True)[:3]
    return render(request, 'main/home.html', {'rooms': rooms})


def rooms(request):
    all_rooms = Room.objects.filter(is_available=True)

    search = request.GET.get('search', '')
    room_type = request.GET.get('room_type', '')
    max_price = request.GET.get('max_price', '')
    capacity = request.GET.get('capacity', '')

    if search:
        all_rooms = all_rooms.filter(name__icontains=search)
    if room_type:
        all_rooms = all_rooms.filter(room_type=room_type)
    if max_price:
        all_rooms = all_rooms.filter(price_per_night__lte=max_price)
    if capacity:
        all_rooms = all_rooms.filter(capacity__gte=capacity)

    context = {
        'rooms': all_rooms,
        'search': search,
        'room_type': room_type,
        'max_price': max_price,
        'capacity': capacity,
    }
    return render(request, 'main/rooms.html', context)


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'main/room_detail.html', {'room': room})


def book_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        booking = Booking.objects.create(
            room=room,
            guest_name=request.POST['guest_name'],
            guest_email=request.POST['guest_email'],
            guest_phone=request.POST['guest_phone'],
            check_in=request.POST['check_in'],
            check_out=request.POST['check_out'],
        )
        check_in = date.fromisoformat(request.POST['check_in'])
        check_out = date.fromisoformat(request.POST['check_out'])
        nights = (check_out - check_in).days
        total = nights * room.price_per_night

        Payment.objects.create(booking=booking, amount=total)
        return redirect('payment', booking_id=booking.id)

    return render(request, 'main/room_detail.html', {'room': room})


def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment_obj = get_object_or_404(Payment, booking=booking)
    nights = (booking.check_out - booking.check_in).days
    return render(request, 'main/payment.html', {
        'booking': booking,
        'payment': payment_obj,
        'nights': nights,
    })


def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment_obj = get_object_or_404(Payment, booking=booking)
    if request.method == 'POST':
        payment_obj.status = 'paid'
        payment_obj.transaction_id = str(uuid.uuid4())[:12].upper()
        payment_obj.paid_at = timezone.now()
        payment_obj.save()
        messages.success(request, f'✅ Payment successful! Transaction ID: {payment_obj.transaction_id}')
        return redirect('booking_success', booking_id=booking.id)
    return redirect('payment', booking_id=booking_id)


def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment_obj = get_object_or_404(Payment, booking=booking)
    return render(request, 'main/booking_success.html', {
        'booking': booking,
        'payment': payment_obj,
    })


def contact(request):
    if request.method == 'POST':
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            message=request.POST['message'],
        )
        messages.success(request, 'Message sent successfully!')
        return redirect('contact')  
    return render(request, 'main/contact.html')