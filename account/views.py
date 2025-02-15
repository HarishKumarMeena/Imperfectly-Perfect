from email import message
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy, reverse
from account.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from account.models import Company, Customer, User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
# from account.forms import AddCustomerForm
from home import views 
# Create your views here.

def admin_home(request):
    return render(request, 'users/admin/admin_home.html')

def customer_home(request):
    return render(request,'users/customer/customer_home.html')
    
def company_home(request):
    return render(request,'users/company/company_home.html')

def company_details(request,pk):
    company_details=Company.objects.filter(id=pk)
    context={
        'company_details':company_details,
    }
    return render(request,'users/company/company_details.html',context)

#.............................................registration..............................................#

def register(request):
    return render(request,'register/register.html')


def handelSingup(request):
    if request.method =='POST':

        #Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        user_type=request.POST.get('user_type')
        #check for errorneous input
        print(user_type)

        if pass1 != pass2 :
            messages.error(request, "Password do not match.")
            return redirect('handelSingup')    

        #Create User
        try:
            myuser = User.objects.create_user(username=username, password=pass1, email=email, first_name=fname, last_name=lname, user_type=user_type)

            myuser.save()
            messages.success(request, "Account Created Successfully!")
            return redirect(views.homeView)

        except:
            messages.error(request, "Failed to SignUp!")
            return redirect('home')
    else:
        return HttpResponse("404 - Not Found")


def handleLogin(request):
    if request.method !='POST':
        return HttpResponse('Submission outside this window is not allowed 😎')
    else:
        #Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user =EmailBackEnd.authenticate(request, username=loginusername, password=loginpassword)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfuly logged in 🥰")
            user_type = user.user_type
            print(user_type)
            #print("username : "+ request.POST.get("loginusername")+ "Password: " +request.POST.get("loginpassword"))
                
            if user_type == "1":
                # return HttpResponse("Student Login")
                return redirect('admin_home')

            elif user_type == '2':
                customer_exist = Customer.objects.filter(user=user).exists()
                if customer_exist:
                    messages.success(request,"Customer home !")
                    return redirect('customer_home')

                return redirect('add_customer')

            elif user_type == '3':
                company_exist = Company.objects.filter(user=user).exists()
                if company_exist:
                    messages.success(request,"Company Login Successful !")
                    return redirect('company_home')
                return redirect('add_company')
        else:
            messages.error(request, "Invalid credentialsl, Please try again 😎")
            return redirect(views.homeView)

def add_customer(request):
    user=request.user
    customer_exist = Customer.objects.filter(user=user).exists()
    if customer_exist:
        messages.error(request,"Customer Already Registered !")
        return redirect('customer_home')
    # customer_form=AddCustomerForm
    if request.method=='POST':
        gender=request.POST['gender']
        dob=request.POST['dob']
        phone=request.POST['phone']
        address=request.POST['address']
        pin=request.POST['pin']
        profile_pic=request.POST['profile_pic']
        print(user)
        try:
            customer=Customer()
            customer.user=user
            customer.gender=gender
            customer.dob=dob
            customer.phone=phone
            customer.address=address
            customer.pin=pin
            customer.profile_pic=profile_pic
            customer.save()
            messages.success(request,"Successfuly register as a Customer")
            return redirect('customer_home')
        except Exception as e:
            print(e)
            messages.error(request,e)
            return redirect('add_customer')

    return render(request, 'users/customer/customer.html')

def add_company(request):
    user=request.user
    company_exist = Company.objects.filter(user=user).exists()
    if company_exist:
        messages.error(request,"Customer Already Registered !")
        return redirect('customer_home')
    # customer_form=AddCustomerForm
    if request.method=='POST':
        company_name=request.POST['company_name']
        cin=request.POST['cin']
        since=request.POST['since']
        phone=request.POST['phone']
        address=request.POST['address']
        pin=request.POST['pin']
        company_desc=request.POST['company_desc']
        # profile_pic=request.POST['profile_pic']
        profile_pic = request.FILES['profile_pic']
        print(user)
        try:
            company=Company()
            company.user=user
            company.company_name=company_name
            company.cin=cin
            company.since=since
            company.phone=phone
            company.address=address
            company.pin=pin
            company.company_desc=company_desc
            company.profile_pic=profile_pic
            company.save()
            messages.success(request,"Successfuly register as a Company")
            return redirect('company_home')
        except Exception as e:
            print(e)
            messages.error(request,e)
            return redirect('add_company')
    return render(request, 'users/company/company.html')


def handleLogout(request):
    if request.method=='POST':
        value=request.POST['value']
        logout(request)
        messages.success(request, "Successfuly logged out 🥰")
        
        return redirect(views.homeView)
    else:
        return HttpResponse('Sorry No Users Logged in 😎') 

#...............................profile details customer..........................#
def add_customer_profile_details(request,id):
    pass

def view_all_customer_profile(request):
    pass

def view_customer_profile(request,id):
    pass

def update_customer_password(request,id):
    pass

def update_customer_profile(request,id):
    pass

def delete_customer_profile(request,id):
    pass


# .....................profile details company.........................# 
def add_company_profile_details(request):
    pass

def view_all_company_profile(request):
    pass

def view_company_profile(request,id):
    pass


def update_company_password(request,id):
    pass

def update_company_profile(request,id):
    pass

def delete_company_profile(request,id):
    pass

# ........................my win product list for company.................#

def my_win_products(request):
    return render(request, 'users/company/my_win_product.html')