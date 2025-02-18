# main project's urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface URL
    path('api/', include('events.urls')),  # Include API URLs from the events app
    path('api/accounts/', include('accounts.urls')),
    path('api/bets/', include('bets.urls')),
    path('api/transactions/', include('transactions.urls')),
]