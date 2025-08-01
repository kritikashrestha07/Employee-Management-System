
from datetime import datetime
from django.shortcuts import render, HttpResponse
from . models import Employee, Role, Department
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')


def index(request):
    return render(request, 'index.html')

def all(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'view.html', context)

def add(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        salary = int(request.POST['salary'])    # OK: numeric string to int
        bonus = int(request.POST['bonus'])      # OK: numeric string to int
        phone = int(request.POST['phone'])      # OK: numeric string to int

        dept_name = request.POST['dept']        # NO int() here, this is a string like 'Finance'
        role_name = request.POST['role']
        
        try:
            department_obj = Department.objects.get(name=dept_name)
        except Department.DoesNotExist:
            return HttpResponse("Department not found!")

        try:
            role_obj = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            return HttpResponse("Role not found!")

        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone=phone,
            dept=department_obj,
            role=role_obj,
            hire_date=datetime.now()
        )
        new_emp.save()
        messages.success(request, "Employee added successfully.")
        return redirect('add') 

    elif request.method == "GET":
        departments = Department.objects.all()
        roles = Role.objects.all()
        return render(request, "add.html", {"departments": departments, "roles": roles})

    else:
        return HttpResponse("An exception occurred! Employee has not been added!")




    

def remove(request, emp_id=0):
    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        try:
            emp = Employee.objects.get(id=emp_id)
            emp.delete()
            return HttpResponse("Employee removed successfully!")
        except Employee.DoesNotExist:
            return HttpResponse("Invalid Employee ID")
    em = Employee.objects.all()
    return render(request, "remove.html", {"em": em})


def filter(request):
    if request.method == "POST":
        name = request.POST.get('name')
        department = request.POST.get('department')
        role = request.POST.get('role')

        emps = Employee.objects.all()

        if name:
            emps = emps.filter(first_name__icontains=name)

        if department:
            emps = emps.filter(dept__name__icontains=department)

        if role:
            emps = emps.filter(role__name__icontains=role)

        return render(request, 'view.html', {'emps': emps})
    elif request.method == "GET":
        return render(request, "filter.html")
    else:
        return HttpResponse("Invalid request")
