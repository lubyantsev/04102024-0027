from django.urls import path
from .views import create_schedule, home_view, schedule_detail_view
from .views import main_page, edit_schedule

urlpatterns = [
    path('', main_page, name='main_page'),
    path('edit_schedule/', edit_schedule, name='edit_schedule'),
    path('', home_view, name='home'),
    path('create_schedule/', create_schedule, name='create_schedule'),
    path('schedule/<int:schedule_id>/', schedule_detail_view, name='schedule_detail'),
]