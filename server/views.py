from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Transaction
from django.views.decorators.csrf import csrf_exempt
import csv
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import datetime


# Create your views here.

def index(request):
    return render(request, 'index.html')

def test_view(request):
    print('request received')
    return JsonResponse({'message': 'Hello from Django!'})

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        print(reader)
        for row in reader:
            Transaction.objects.create(
                amount=row['amount'],
                date=row['date']
            )
        return JsonResponse({'message': 'CSV uploaded successfully'})
    return HttpResponse(status=400)

@csrf_exempt
def get_monthly_spending(request):
    print('request received')

    monthly_spending = (
        Transaction.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total_spending=Sum('amount'))
        .order_by('month')
    )

    # Format the month to a more readable format
    formatted_spending = [
        {
            'month': datetime.strptime(str(entry['month']), '%Y-%m-%d').strftime('%B %Y'),
            'total_spending': entry['total_spending']
        }
        for entry in monthly_spending
    ]

    print(formatted_spending)
    return JsonResponse(formatted_spending, safe=False)

