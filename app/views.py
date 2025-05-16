from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Profile
from .forms import SignupForm
# Create your views here.
def index(req):
    return render(req,'base.html')
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
def main(req):
    return render(req,'main_dashboard.html')
# def signup_1(req):
#     if req.method == "POST":
#         fname = req.POST.get("fname")
#         lname = req.POST.get("lname")
#         uname = req.POST.get("uname")  # This is the email
#         username1 = req.POST.get("username1")
#         upass = req.POST.get("upass")
#         ucpass = req.POST.get("ucpass")
#         address_line1 = req.POST.get("address_line1")
#         city = req.POST.get("city")
#         pincode = req.POST.get("pincode")
#         context = {}

#         # Basic validation
#         if not all([fname, lname, uname, username1, upass, ucpass, address_line1, city, pincode]):
#             context["errmsg"] = "All fields are required."
#             return render(req, "signup_1.html", context)

#         if upass != ucpass:
#             context["errmsg"] = "Password and Confirm Password do not match."
#             return render(req, "signup_1.html", context)

#         try:
#             # Create user
#             userdata = User.objects.create_user(username=username1, email=uname, password=upass,
#                                                 first_name=fname, last_name=lname)
#             # Save extended profile (if using a Profile model)
#             # Example only if you have a related Profile model
#             # Profile.objects.create(user=userdata, address_line1=address_line1, city=city, pincode=pincode)

#             # You can store address in session or print/log for now if no profile model
#             userdata.set_password(upass)
#             userdata.save()
#             req.session['address_line1'] = address_line1
#             req.session['city'] = city
#             req.session['pincode'] = pincode
            

#             return redirect("/signin_1")
#         except Exception as e:
#             print("Signup error:", e)
#             context["errmsg"] = "User already exists or error occurred."
#             return render(req, "signup_1.html", context)

#     return render(req, "signup_1.html", {"errmsg": ""})

# chatgpt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Profile

# ---------------------- PATIENT SIGNUP ----------------------
def signup_1(request):
    if request.method == "POST":
        return handle_signup(request, user_type="patient")
    return render(request, "signup_1.html", {"errmsg": ""})


# ---------------------- DOCTOR SIGNUP ----------------------
def signup_2(request):
    if request.method == "POST":
        return handle_signup(request, user_type="doctor")
    return render(request, "signup_2.html", {"errmsg": ""})


# ---------------------- SIGNUP HANDLER ----------------------
from django.contrib.auth.models import User

def handle_signup(request, user_type):
    context = {}
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if not form.is_valid():
            context["errmsg"] = form.errors.as_text()
            return render(request, f"signup_{'1' if user_type == 'patient' else '2'}.html", context)

        fname = form.cleaned_data["fname"]
        lname = form.cleaned_data["lname"]
        email = form.cleaned_data["uname"]
        username = form.cleaned_data["username1"]
        password = form.cleaned_data["upass"]
        confirm_password = form.cleaned_data["ucpass"]
        address_line1 = form.cleaned_data["address_line1"]
        city = form.cleaned_data["city"]
        pincode = form.cleaned_data["pincode"]
        photo = form.cleaned_data["photo"]

        # Check for username duplication
        if User.objects.filter(username=username).exists():
            context["errmsg"] = "Username already exists. Please choose another."
            return render(request, f"signup_{'1' if user_type == 'patient' else '2'}.html", context)

        # Check for email duplication (optional but good practice)
        if User.objects.filter(email=email).exists():
            context["errmsg"] = "Email already registered. Try logging in."
            return render(request, f"signup_{'1' if user_type == 'patient' else '2'}.html", context)

        # Check if passwords match
        if password != confirm_password:
            context["errmsg"] = "Passwords do not match."
            return render(request, f"signup_{'1' if user_type == 'patient' else '2'}.html", context)

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=fname,
                last_name=lname
            )

            profile, created = Profile.objects.get_or_create(user=user)
            profile.user_type = user_type
            profile.address_line1 = address_line1
            profile.city = city
            profile.pincode = pincode
            profile.photo = photo
            profile.save()

            return redirect(f"/signin_{'1' if user_type == 'patient' else '2'}")

        except Exception as e:
            print("Signup error:", e)
            context["errmsg"] = "Unexpected error occurred. Try again later."
            return render(request, f"signup_{'1' if user_type == 'patient' else '2'}.html", context)

    # If GET request, show blank form
    form = SignupForm()
    context["form"] = form
    return render(request, f"signup_{'1' if user_type == 'patient' else '2'}.html", context)



from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

#chatgpt
# ---------------------- PATIENT SIGNIN ----------------------
def signin_1(request):
    if request.method == "POST":
        return handle_signin(request, user_type="patient")
    return render(request, "signin_1.html")


# ---------------------- DOCTOR SIGNIN ----------------------
def signin_2(request):
    if request.method == "POST":
        return handle_signin(request, user_type="doctor")
    return render(request, "signin_2.html")


# ---------------------- SIGNIN HANDLER ----------------------
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile
from django.shortcuts import render, redirect

def handle_signin(request, user_type):
    email = request.POST.get("uname")  # email entered
    password = request.POST.get("upass")
    context = {}

    if not email or not password:
        context["errmsg"] = "Fields can't be empty"
        return render(request, f"signin_{'1' if user_type == 'patient' else '2'}.html", context)

    try:
        user = User.objects.get(email=email)
        profile = Profile.objects.get(user=user)

        if profile.user_type != user_type:
            context["errmsg"] = f"This account is not registered as {user_type}."
            return render(request, f"signin_{'1' if user_type == 'patient' else '2'}.html", context)

        user = authenticate(username=user.username, password=password)
        if user:
            login(request, user)
            # Redirect based on user_type
            if user_type == "patient":
                return redirect("/patient_d")  # your patient dashboard URL
            else:
                return redirect("/doctor_d")  # Or wherever you want
        else:
            context["errmsg"] = "Invalid email or password"
    except User.DoesNotExist:
        context["errmsg"] = "User not found."
    except Profile.DoesNotExist:
        context["errmsg"] = "Profile not found."
    except Exception as e:
        print("Signin error:", e)
        context["errmsg"] = "An error occurred during signin."

    return render(request, f"signin_{'1' if user_type == 'patient' else '2'}.html", context)

###################m --------------my code
# def signin_1(req):
#     if req.method == "POST":
#         username = req.POST["username1"]
#         upass = req.POST["upass"]
#         context = {}
#         if username  == "" or upass == "":
#             context["errmsg"] = "Field can't be empty"
#             return render(req, "signin_1.html", context)
#         else:
#             userdata = authenticate(username=username , password=upass)
#             if userdata is not None:
#                 login(req, userdata)
#                 return redirect("/patient_d")
#             else:
#                 context["errmsg"] = "Invalid username and password"
#                 return render(req, "signin_1.html", context)
#     else:
#         return render(req, "signin_1.html")


def userlogout(req):
    logout(req)
   
    return redirect("/")

# def patient_d(req):
    # address_line1 = req.session.get("address_line1", "Not provided")
    # city = req.session.get("city", "Not provided")
    # pincode = req.session.get("pincode", "Not provided")

    # context = {
    #     "user": req.user,
    #     "address_line1": address_line1,
    #     "city": city,
    #     "pincode": pincode,
    # }
    # return render(req,'patient_dashbord.html',context)
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def patient_d(request):
    # Fetch all users with profile user_type = patient
    patients = Profile.objects.filter(user_type='patient').select_related('user')
    return render(request, "patient_dashbord.html", {"patients": patients})

@login_required
def doctor_d(request):
    # Fetch all users with profile user_type = doctor
    doctors = Profile.objects.filter(user_type='doctor').select_related('user')
    return render(request, "doctor_dashboard.html", {"doctors": doctors})



# def doctor_d(req):
    # address_line1 = req.session.get("address_line1", "Not provided")
    # city = req.session.get("city", "Not provided")
    # pincode = req.session.get("pincode", "Not provided")

    # context = {
    #     "user": req.user,
    #     "address_line1": address_line1,
    #     "city": city,
    #     "pincode": pincode,
    # }
    # return render(req,'patient_dashbord.html',context)
    # if not req.user.is_authenticated:
    #     return redirect("/signin_2")

    # try:
    #     profile = Profile.objects.get(user=req.user)
    # except Profile.DoesNotExist:
    #     profile = None

    # return render(req, "doctor_dashboard.html", {
    #     "user": req.user,
    #     "profile": profile
    # })