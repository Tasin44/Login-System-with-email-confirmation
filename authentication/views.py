
from django.core.mail import EmailMessage,send_mail
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect,render
from django.contrib.auth import authenticate,login,logout
from Loginsystem import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from base64 import urlsafe_b64encode, urlsafe_b64decode
from django.utils.encoding import force_bytes,force_str
from .tokens import generate_token

def home(request):
    return render(request,"authentication/index.html")

def signup(request):
    if request.method=="POST":
        '''
        The user's input is collected from the request.POST dictionary for the below fields 
        These are all the variable which we're going for backend'''
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another.")
            return redirect('home') 

        ''' 
        check if email already exist()
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please use a different email.")
            return redirect('home')'''

        if len(username) > 10:
            messages.error(request, "Username must be 10 characters . ")
        
        if pass1!=pass2:
            messages.error(request, "Password didn't match")
        
        if not username.isalnum():
            messages.error(request,"Username must be alphanumeric!")
            return redirect('home')

        '''
        If validation passes, the system creates a new User object using 
        Django’s built-in User.objects.create_user() method.'''
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.is_active=False 
        '''
        during signup, myuser.is_active will be False,when the user
        will click on the confirmation link & all the credentials correct
        like user id and tokens, then is_active will be true,
        means the account will be activated after email confirmation.
        '''
        myuser.save() # save the user in a database
        # here myuser is a object, User is a model .
        # User.objects.create means create a user for me 

        messages.success(request,"Your account sucessfully created. We've sent you a confirmation email")
        # messages is a inbuilt library 

        #Email functionality part

        subject="wellcome to Loginsystem"
        message = "Hello" + myuser.first_name + "Thanks for your mail,welcome to our project"
        from_email=settings.EMAIL_HOST_USER
        to_send= [myuser.email]
        send_mail(subject,message,from_email,to_send,fail_silently=True)


        current_site = get_current_site(request)
        email_subject="Confirm your email @Loginsystem"
        message2=render_to_string('email_confirmation.html',{

                'name': myuser.first_name,
                'domain':current_site.domain,
                'uid': urlsafe_b64encode(force_bytes(myuser.pk)).decode('utf-8'),
                'token':generate_token.make_token(myuser)
        })


        email=EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request,"authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username=request.POST['username']
        pass1=request.POST['pass1']
        
        user = authenticate(username=username,password=pass1)

        if user is not None:
            login(request,user)
            fname=user.first_name
            return render(request,"authentication/index.html",{'fname':fname})
            # {'fname':fname} is a dictionary,before using it,we've to mentioned it
            # like fname=user.first_name
            
        else:
            messages.error(request,"Bad Credentials!")
            return redirect('home')


    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    # It'll logout the current user which is requested 
    # through the current url 
    messages.success(request,"Logged out Successfully !")
    return redirect('home')


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_b64decode(uidb64))
        print("Decoded UID:", uid)  # Debug print
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        print(f"Error: {e}")  # Debugging
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        '''
            during signup, myuser.is_active will be False,when the user
            will click on the confirmation link & all the credentials correct
            like user id and tokens, then is_active will be true,
            means we're going to activate the account  
        '''
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        print("Token verification failed or user is None")  # Debugging
        return render(request, 'activation_failed.html')

'''
current_site = get_current_site(request):

This retrieves the current site’s domain (e.g., www.example.com) 
from the request context.
The get_current_site() function is a built-in Django utility from 
django.contrib.sites.shortcuts.
This is helpful for dynamically generating URLs in the email, 
so that even if the site’s domain changes, the email will always contain 
the correct domain.

message2 = render_to_string('email_confirmation.html', {...}):
This renders an HTML email template (email_confirmation.html) 
and passes some context to it.
The render_to_string() function takes an HTML template 
and a context dictionary to generate the final email content.

'domain': current_site.domain:
The domain of the current site is passed in, 
ensuring that the confirmation link in the email includes the correct URL.


'uid': urlsafe_b64encode(force_bytes(myuser.pk)).decode('utf-8'):
This encodes the user's primary key (ID) into a URL-safe format.
The primary key (or pk) of the user is retrieved (myuser.pk), 
converted into bytes (force_bytes()), 
and then encoded using Base64 (urlsafe_b64encode()).
This encoding ensures that the user ID can safely be included 
in the URL as part of the confirmation link, without causing any
issues in the URL format.
'''