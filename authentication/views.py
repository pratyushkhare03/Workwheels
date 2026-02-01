from django.shortcuts import render, redirect
from django.contrib import messages
from .models import USER
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login , logout
from django.views.decorators.cache import never_cache

# Create your views here.
def index(request):
    return render(request, 'sitemaster.html')

@never_cache
def register(request):
      path = request.path
      initial_form = 'login' if 'login' in path else 'register'
      if request.method == "POST":
        username = request.POST['Usernm']
        email = request.POST['email']
        password = request.POST['password']
        # password2 = request.POST['password2']
        role = request.POST['role']

        # if password != password2:
        #     messages.error(request, "Passwords do not match.")
        #     return redirect('/signup/')

        if User.objects.filter(username=username, role=role).exists():
            messages.error(request, "Username already exists. Login with same credentials.")
            return redirect('/login/')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password )

        # Link to Employee
        USER.objects.create(username=user,  role=role)

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('/login/')  # Change to your login page

     #return render(request,'register.html')
      return render(request, 'register.html', {initial_form: 'register'})

# Login function

@never_cache
def  login(req):
    path = req.path
    initial_form = 'login' if 'login' in path else 'register'
    if req.method == "POST":
     usernm = req.POST['username']
     pasw = req.POST['password']
     role = req.POST['role']
     user = User.objects.filter(username=usernm)
     if not user.exists():
        messages.error(req,"User does not exist please register first")
        return redirect("/register")
     user=authenticate(username = usernm , password = pasw, role=role)
     if user is None:
        messages.error(req,"Wrong password enter a valid one")
        return redirect('/login')
     else:
        auth_login(req,user)
        messages.success(req,"Logged in successfully")    
     if role == "employee":

                 return redirect('/employee')

     else:
                 return redirect('/driver')

    return render(req, 'register.html', {initial_form: 'login'})


def logout_view(request):
    logout(request)
    request.session.flush()         # clears all session data (extra safety)
    messages.success(request, "Logged out successfully")
    return redirect('/')
