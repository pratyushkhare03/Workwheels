from django.shortcuts import render, redirect
from django.contrib import messages
from .models import USER
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login , logout

# Create your views here.
def index(request):
    return render(request, 'sitemaster.html')

def register(request):
    path = request.path
    initial_form = 'login' if 'login' in path else 'register'

    if request.method == "POST":
        username = request.POST['Usernm']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        # ✅ Check only username (NOT role)
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Login with same credentials.")
            return redirect('/login/')

        # ✅ Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # ✅ Assign role using boolean fields
        if role == "driver":
            user.driver = True
        elif role == "employee":
            user.employee = True

        user.save()

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('/login/')

    return render(request, 'register.html', {'initial_form': initial_form})

# Login function

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

    return render(req, 'register.html', {'initial_form': initial_form})


def logout_view(request):
    logout(request)
    request.session.flush()         # clears all session data (extra safety)
    messages.success(request, "Logged out successfully")
    return redirect('/')
