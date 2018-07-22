from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
# Create your views here.
from django.http import JsonResponse
import json
import os
import uuid
import xlrd,xlwt
import django
from app01.models import User,Customer


#登陆
def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        user_obj = User.objects.filter(user=user, pwd=pwd).first()
        if user_obj:
            return redirect("/customer/")
    return render(request,"login.html")

#客户管理
def customer(request):
    customer_list = Customer.objects.all()  # queryset [obj,....]

    return render(request, "customer.html", {"customer_list": customer_list})

#上传文件，批量添加
def add_customer(request):
    if request.method == "GET":
        return render(request,'upload_file.html')

    user = request.POST.get('user')
    avatar = request.FILES.get('avatar')
    excel_path = os.path.join('static','plugins',avatar.name)
    with open(excel_path,'wb') as f:
        for line in avatar.chunks(chunk_size=1024*1024):#读取大文件用chunks（）函数，可以设置参数chunk_size=每次读取的字节数。
            f.write(line)
            # 打开excel文件
    excel_file = xlrd.open_workbook(excel_path)
    # 获取sheet内容
    sheet = excel_file.sheet_by_index(0) #行
    row = sheet.nrows                     #列
    custom_list = []
    for i in range(1, row):
        obj_list = sheet.row_values(i) #取得值,参数是（行数，起点，终点）
        custom_obj = Customer(name=obj_list[1], age=obj_list[2], email=obj_list[3], company=obj_list[4])
        custom_list.append(custom_obj)
    #批量插入
    Customer.objects.bulk_create(custom_list, batch_size=20)    #batch_size限制插入行数
    os.remove(excel_path)
    return redirect(reverse('index'))


#上传图片
def upload_img(request):
    if request.method == "GET":
        return render(request,'upload_img.html')
    user = request.POST.get('user')
    avatar = request.POST.get('avatar')
    print(user,avatar)
    return HttpResponse('上传成功')
def index(request):
    return render(request,'index.html')