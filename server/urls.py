from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'server'

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')), 
    path('api/upload_csv/', views.upload_csv, name='upload_csv'),
    path('api/monthly_spending/', views.get_monthly_spending, name='monthly_spending'),
    # Add other endpoints as needed
]