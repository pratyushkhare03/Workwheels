from django.shortcuts import render,redirect
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
        # password2 = request.POST['password2']
        role = request.POST['role']

        # if password != password2:
        #     messages.error(request, "Passwords do not match.")
        #     return redirect('/signup/')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('/register')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password )

        # Link to Employee
        USER.objects.create(username=user,  role=role)

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('/')  # Change to your login page

     #return render(request,'register.html')
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
        messages.error(req,"wrong username give a currect username")
        return redirect("/register")
     user=authenticate(username = usernm , password = pasw)
     if user is None:
        messages.error(req,"wrong password enter a valid one")
        return redirect('/')
     else:
        auth_login(req,user)

   #   if hasattr(USER, 'driver'):
   #              role = 'driver'
   #   elif hasattr(USER, 'employee'):
   #              role = 'employee'
      #   role = USER.objects.filter(role)
     if role == "employee":
      # #   if User.objects.filter(username=username).exists():
                 return redirect('/employee')
      # #   elif role == "driver":
     else:
                 return redirect('/driver')
    #return render(req,'register.html')
    return render(req, 'register.html', {'initial_form': initial_form})
