# @Author: Javed Ahamad
# @Date:   2017-07-13
# @Email:  javedahamad4@gmail.com
# @Filename: admin_views.py


from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from core.models import *
from django.db.models import Q
from greenDecor.settings import BASE_DIR
from django.core import serializers
import json
from django.contrib.admin.views.decorators import staff_member_required

def product_report(request, **kwargs):
    """
    Renders the product wise report
    """
    if request.method=='POST':
        from django.db.models import Sum
        import xlsxwriter
        start_date = request.POST.get('start_date',None)
        end_date = request.POST.get('end_date',None)
        workbook = xlsxwriter.Workbook(BASE_DIR+'/media/reports.xlsx')
        worksheet = workbook.add_worksheet()
        product_report = OrderDetails.objects.filter(order__placed_on__gte=start_date,order__placed_on__lt=end_date).values('plant__name','plant__selling_price','plant__actual_price').annotate(Sum('quantity'))
        bold = workbook.add_format({'bold': 1})
        worksheet.write('A1', 'Plant Name', bold)
        worksheet.write('B1', 'Quantity', bold)
        worksheet.write('C1', 'Unit Selling Price', bold)
        worksheet.write('D1', 'Unit Cost Price', bold)
        worksheet.write('E1', 'Total Selling Price', bold)
        worksheet.write('F1', 'Total Cost Price', bold)
        row = 1
        col = 0
        for pr in product_report:
            worksheet.write_string  (row, col,pr['plant__name'])
            worksheet.write_number(row, col + 1, pr['quantity__sum'] )
            worksheet.write_number  (row, col + 2, pr['plant__selling_price'])
            worksheet.write_number  (row, col + 3, pr['plant__actual_price'])
            worksheet.write_number  (row, col + 4, pr['plant__selling_price'] * pr['quantity__sum'])
            worksheet.write_number  (row, col + 5, pr['plant__actual_price'] * pr['quantity__sum'])
            row += 1
        # worksheet.write(row, 0, 'Total', bold)
        # worksheet.write(row, 2, '=SUM(C2:C5)', money_format)
        workbook.close()
        return render(request, "admin/product_report.html.j2", {'product_report':product_report,'start_date':start_date,'end_date':end_date})
    else:
        return render(request, "admin/product_report.html.j2", {})

def getPlants(request, **kwargs):
    id = request.GET.get('id','')
    category = Category.objects.get(id=id)
    result = Plants.objects.filter(Q(category=category) | Q(category=category.parent_category),active=True).distinct()
    data = serializers.serialize('json', result)
    return HttpResponse(data, content_type="application/json")
getSpecificationName = staff_member_required(getPlants)
