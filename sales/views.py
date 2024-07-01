from django.shortcuts import render, HttpResponse, redirect
from .models import Salesperson, SalesRecord
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pandas as pd
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from .models import Salesperson, SalesRecord
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import calendar
# Create your views here.

def index(request):
    return render(request, 'sales/sales_performance.html')

def sales_performance(request):
    salespersons = Salesperson.objects.all()

    for person in salespersons:
        sales_data = SalesRecord.objects.filter(salesperson=person).annotate(
            sales_month_truncated=TruncMonth('sales_month')
        ).values('sales_month_truncated').annotate(total_sales=Sum('sales_amount'))

        person.months = [calendar.month_name[sales['sales_month_truncated'].month] for sales in sales_data]
        person.sales_amounts = [sales['total_sales'] for sales in sales_data]

    return render(request, 'sales/sales_performance.html', {'salespersons': salespersons})


def file_upload(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')
        dd = request.FILES
        
        print('file', uploaded_files)
        option = request.POST.get('option')
        fs = FileSystemStorage()

        # Debugging: Print the list of uploaded files
        print("Uploaded files:", uploaded_files)
        if not uploaded_files:
            return HttpResponseBadRequest(f"No files uploaded")

        dfs = []
        for uploaded_file in uploaded_files:
            print(uploaded_file.name)
            file_path = fs.save(uploaded_file.name, uploaded_file)
            full_file_path = fs.path(file_path)  # Get the full path of the saved file

            # Debugging: Print the file path
            print("Saved file path:", full_file_path)
            try:
                df = pd.read_excel(full_file_path)
                dfs.append(df)
            except Exception as e:
                print(f"Error reading Excel file {full_file_path}: {e}")
                return HttpResponseBadRequest(f"Error reading Excel file {uploaded_file.name}")

        if option == 'common':
            if len(dfs) < 2:
                return HttpResponseBadRequest("At least two files are required for finding common employees.")
            common_df = dfs[0]
            for df in dfs[1:]:
                common_df = pd.merge(common_df, df, how='inner')

            common_file_path = 'common.xlsx'
            common_df.to_excel(common_file_path, index=False)
            with open(common_file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="common.xlsx"'
                return response

        elif option == 'unique':
            all_df = pd.concat(dfs)
            unique_df = all_df.drop_duplicates(keep=False)

            unique_file_path = 'unique.xlsx'
            unique_df.to_excel(unique_file_path, index=False)
            with open(unique_file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="unique.xlsx"'
                return response

    return render(request, 'sales/file_upload.html')