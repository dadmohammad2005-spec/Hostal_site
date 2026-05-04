# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('rooms/', views.rooms, name='rooms'),
#     path('room/<int:pk>/', views.room_detail, name='room_detail'),
#     path('book/<int:pk>/', views.book_room, name='book_room'),
#     path('contact/', views.contact, name='contact'),
# ]



# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('rooms/', views.rooms, name='rooms'),
#     path('room/<int:pk>/', views.room_detail, name='room_detail'),
#     path('book/<int:pk>/', views.book_room, name='book_room'),
#     path('payment/<int:booking_id>/', views.payment, name='payment'),
#     path('process-payment/<int:booking_id>/', views.process_payment, name='process_payment'),
#     path('booking-success/<int:booking_id>/', views.booking_success, name='booking_success'),
#     path('contact/', views.contact, name='contact'),
# ]



from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.rooms, name='rooms'),
    path('room/<int:pk>/', views.room_detail, name='room_detail'),
    path('book/<int:pk>/', views.book_room, name='book_room'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('process-payment/<int:booking_id>/', views.process_payment, name='process_payment'),
    path('booking-success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('contact/', views.contact, name='contact'),
]