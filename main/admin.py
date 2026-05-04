from django.contrib import admin
from .models import Room, Booking, Contact, RoomImage


from .models import Room, Booking, Contact, RoomImage, Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'status', 'transaction_id', 'paid_at']
    list_filter = ['status']





class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 3

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type', 'price_per_night', 'capacity', 'is_available']
    list_filter = ['room_type', 'is_available']
    inlines = [RoomImageInline]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['guest_name', 'room', 'check_in', 'check_out', 'guest_email']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'sent_at']

@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ['room', 'caption']