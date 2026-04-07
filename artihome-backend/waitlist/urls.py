from django.urls import path
from . import views

urlpatterns = [
    path('join/<int:product_id>/', views.join_waitlist, name='join_waitlist'),
    path('leave/<int:product_id>/', views.leave_waitlist, name='leave_waitlist'),
    path('my/', views.user_waitlists, name='user_waitlists'),
    path('pledge/<int:product_id>/', views.toggle_pledge, name='toggle_pledge'),
    path('count/<int:product_id>/', views.pledge_count, name='pledge_count'),
]
