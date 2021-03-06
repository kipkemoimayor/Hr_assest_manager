from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,Http404
from django.contrib.auth import login ,authenticate,logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm,LoginForm,UserSignUp,NewPasswordForm,AssestForm,ProfileForm,UpdateProfile
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import accounts_activation_token
from .models import CustomUser,AssetModel,EmployeeProfile,Notifications
from django.core.mail import EmailMessage
from django.contrib import messages
import pusher

# Create your views here.
'''
Account settings
'''
channels_client = pusher.Pusher(
    app_id='841275',
    key='80de7e6b8bc917286ed8',
    secret='bfd12143823fae827fa2',
    cluster='ap2',
    ssl=True
)

def index(request):
    title="Admin"
    if request.user.is_authenticated:
        profile=EmployeeProfile.objects.filter(user=request.user)
    else:
        profile=''
    return render(request,"index.html",{"title":title,"profile":profile})

def signup(request):
    title="Quest SignUp"

    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            to_email=form.cleaned_data['email']
            user=form.save(commit=False)
            user.is_active=False
            user.name=name
            user.is_superuser="t"
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
def activate_user(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        user=CustomUser.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None

    if user is not None and accounts_activation_token.check_token(user,token):
        user.is_active=True;
        user.save()
        login(request,user)
        return HttpResponse("<p>Your account is now active please Create new password <a href='/accounts/password/'>here</a></p>")

    else:
        return HttpResponse("Link invalid")


def user_login(request):
    title="Login"
    # logout(request)
    username= password=''
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():

            username=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    '''
                    saving status and user to Notifications
                    '''

                    s='my-channel'
                    d='message'
                    mess=f'{request.user} has logged in!'
                    channels_client.trigger(s, 'my-event',{d: mess})
                    s=Notifications.objects.create(message=mess,user=request.user)
                    s.save()
                    return redirect("/")

            else:
                 messages.error(request,'username or password not correct')
                 return redirect('login')



    login_form=LoginForm()
    return render(request,'accounts/login.html',{"title":title,"form":login_form})


def user_logout(request):
    '''
    saving status and user to Notifications
    '''

    s='my-channel'
    d='message'
    mess=f'{request.user} logged  🤔 out!'

    try:
        channels_client.trigger(s, 'my-event',{d: mess})
        s=Notifications.objects.create(message=mess,user=request.user)
        s.save()
    except:
        print("Error Sending Notifications")

    logout(request)
    return redirect("/")
@login_required(login_url="/accounts/login/")
def dashboard(request):
    title=f'{request.user} dashboard'
    if request.user.is_superuser:
        users=CustomUser.objects.all().exclude(username=request.user)
        try:
            notifications=Notifications.objects.all()
        except :
            raise Http404()
        if request.method=='POST':
            form=UserSignUp(request.POST)
            if form.is_valid():
                name=form.cleaned_data['name']
                username=form.cleaned_data['username']
                to_email=form.cleaned_data['email']
                user=form.save(commit=False)
                user.is_active=False
                user.name=name
                user.is_superuser="f"
                valid_user=CustomUser.objects.filter(username=username)
                valid_email=CustomUser.objects.filter(email=to_email)
                print(valid_user,valid_email)
                print("*"*9)
                if len(username)==0 or len(valid_email) ==0 :
                    user.save()
                    current_site=get_current_site(request)
                    mail_subject=f" Hello {name} Please Activate your Account"
                    message=render_to_string('user_activate.html',{
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
                    return redirect("dashboard")

                else:
                    messages.error(request,'username or email already taken')
                    return redirect("dashboard")

        form=UserSignUp()
        user_form=AssestForm()

        return render(request,'dashboard.html',{"title":title,"form":form,'users':users,'user_form':user_form,'notifications':notifications})
    else:
        return HttpResponse("You are not authorized")


def new_password(request):
    title='Create new Password'

    if request.method=='POST':
        new_user=request.POST.get('username')
        test_user=CustomUser.objects.filter(username=new_user)
        if len(test_user)>=1:
            instance=CustomUser.objects.get(username=new_user)
            form=NewPasswordForm(request.POST,instance=instance)
            if form.is_valid():
                user=form.cleaned_data['username']
                password2=form.cleaned_data['password2']
                password1=form.cleaned_data['password1']
                username=CustomUser.objects.filter(username=user)
                if username is not None:
                    if password1 and  password2 and password1!=password2:
                        messages.error(request,"Password mismatch")
                        return redirect("password")
                    else:
                        password=form.save(commit=False)
                        password.set_password(form.cleaned_data['password2'])
                        password.save()
                        messages.success(request,"Password changed succefully please Login")
                        return redirect("login")
                else:
                    messages.error(request,"invalid Username or Password mismatch")
                    return redirect("password")
        else:
            messages.error(request,"invalid Username")
            return redirect("password")

    form=NewPasswordForm()

    return render(request,'accounts/pass_new.html',{'title':title,"form":form})


#ajax call

def asset_ajax(request):

    if request.method=="POST":
        value=request.POST.get('value','')
        instance=CustomUser.objects.get(id=value)

        form=AssestForm(request.POST)


        if form.is_valid():
            asset=form.save(commit=False)
            asset.user=instance
            asset.save()
            print("saved......")
            data={'success':"succefully asigned asset"}
            return JsonResponse(data)

def view_assests(request):
    assets=AssetModel.objects.all()
    data=dict()
    for j in assets:
        data[j.user.name]=[]
    for i in assets:
            for j in data:
                if i.user.name == j:
                    data[j].append(i.asset_name)
    return JsonResponse(data)


def employee_profile(request):
    title="Profile"
    try:
        profiles=EmployeeProfile.objects.filter(user=request.user)
    except Exception as e:
        raise Http404()
    if profiles:
        if request.method=="POST":
            id=EmployeeProfile.objects.get(user=request.user)
            id=id.id
            instance=EmployeeProfile.objects.get(pk=int(id))
            date=request.POST.get("date",'')
            update_form=UpdateProfile(request.POST,request.FILES,instance=instance)
            if update_form.is_valid():
                update=update_form.save(commit=False)
                update.save()
                '''
                saving status and user to Notifications
                '''

                s='my-channel'
                d='message'
                mess=f'{request.user} Updated Profile 🤔 🤔!'
                channels_client.trigger(s, 'my-event',{d: mess})
                s=Notifications.objects.create(message=mess,user=request.user)
                s.save()
                # messages.success(request,"Profile Updated succefully")
                return redirect('profile')

    if request.method=="POST":
        date=request.POST.get("date",'')
        form=ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile=form.save(commit=False)
            print(date)
            profile.dob=date
            profile.user=request.user
            profile.save()
            '''
            saving status and user to Notifications
            '''

            s='my-channel'
            d='message'
            mess=f'{request.user} Updated Profile!'
            channels_client.trigger(s, 'my-event',{d: mess})
            s=Notifications.objects.create(message=mess,user=request.user)
            s.save()
            return redirect("profile")


    arr=[]
    for i in profiles:
        arr.append(i.user.name)


    if arr:
        names=arr[0].split(" ")
        if len(names)>1:
            name=names[0][0]+names[1][0]
        else:
            name=names[0][0]+names[0][-1]
    else:
        name=''
        pass

    form=ProfileForm()
    update_form=UpdateProfile()
    return render(request,'profile.html',{"title":title,"form":form,'profiles':profiles,"update_form":update_form,"name":name})

    #INITIATION PUSHER''
