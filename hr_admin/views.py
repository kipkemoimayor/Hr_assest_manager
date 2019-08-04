from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login ,authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import accounts_activation_token
from .models import CustomUser
from django.core.mail import EmailMessage

# Create your views here.

def index(request):
    title="Admin"

    return render(request,"index.html",{"title":title})

def signup(request):
    title="Quest SignUp"

    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            to_email=form.cleaned_data['email']
            to_email=form.cleaned_data['email']
            user=form.save(commit=False)
            user.is_active=False
            user.name=name
            user.save()

            current_site=get_current_site(request)
            mail_subject="Activate your account."
            message=render_to_string('acc_active_email.html',{
                'user':user,
                "domain":current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':accounts_activation_token.make_token(user),
            })
            to_email=form.cleaned_data['email']
            email=EmailMessage(
                mail_subject,message,to=[to_email]
            )
            email.send()

            return HttpResponse("Please confirm Your email Address to complete your Registratiom")
    else:
        form=SignupForm()


    return render(request,'accounts/signup.html',{"title":title,"form":form})


def activate(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        user=CustomUser.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None

    if user is not None and accounts_activation_token.check_token(user,token):
        user.is_active=True;
        user.save()
        login(request,user)
        return HttpResponse("login To your account")

    else:
        return HttpResponse("Link invalid")
