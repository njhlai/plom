from django.contrib.auth.models import User, Group
# to be taken out below
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic import View

# pip install django-braces
from braces.views import GroupRequiredMixin

from django.contrib.auth.forms import SetPasswordForm

from .signupForm import CreateUserForm
from .tokens import activation_token
from .models import Profile


# Create your views here.
# Set User Password
class SetPassword(View):
    template_name = 'Authentication/set_password.html'
    reset_invalid = 'Authentication/activation_invalid.html'
    set_password_complete = 'Authentication/set_password_complete.html'
    group_required = [u"manager", u"scanner", u"marker"]
    help_text = ["Your password can’t be too similar to your other personal information.",
                 "Your password must contain at least 8 characters.",
                 "Your password can’t be a commonly used password.",
                 "Your password can’t be entirely numeric."]

    def get(self, request, uidb64, token):
        try:
            uid = force_str((urlsafe_base64_decode(uidb64)))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        reset_form = SetPasswordForm(user)
        if user is not None and activation_token.check_token(user, token):
            user.is_active = True
            user.profile.signup_confirmation = False
            user.save()
            context = {'form': reset_form, 'help_text': SetPassword.help_text}
            return render(request, self.template_name, context)
        else:
            return render(request, self.reset_invalid)

    def post(self, request, uidb64, token):
        try:
            uid = force_str((urlsafe_base64_decode(uidb64)))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and activation_token.check_token(user, token):
            reset_form = SetPasswordForm(user, request.POST)
            error_text = ""
            for error in reset_form.error_messages.values():
                error_text = error
            if reset_form.is_valid():
                user = reset_form.save()
                user.is_active = True
                user.profile.signup_confirmation = True
                user.save()
                return render(request, self.set_password_complete)
            else:
                context = {'form': reset_form, 'help_text': SetPassword.help_text, 'errors': error_text}
                return render(request, self.template_name, context)
        else:
            return render(request, 'Authentication/activation_invalid.html')


# When users their password successfully
class SetPasswordComplete(LoginRequiredMixin, View):
    template_name = 'Authentication/set_password_complete.html'

    def get(self, request):
        return render(request, self.template_name)


# login_required make sure user is log in
class Home(LoginRequiredMixin, View):
    login_url = 'login/'
    redirect_field_name = 'login'
    home_page = 'Authentication/home.html'
    navbar_colour = {'admin': '#808080',
                     'manager': '#AD9CFF',
                     'marker': '#FF434B',
                     'scanner': '#0F984F'}

    def get(self, request):
        user = request.user.groups.all()[0].name
        if user in Home.navbar_colour:
            colour = Home.navbar_colour[user]
        context = {'navbar_colour': colour, 'user_group': user}
        return render(request, self.home_page, context)


class LoginView(View):
    template_name = 'Authentication/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(
                request,
                username=username,
                password=password
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect!')
            return render(request, self.template_name)


# Logout User
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


# Signup Manager
class SignupManager(GroupRequiredMixin, View):
    template_name = 'Authentication/manager_signup.html'
    activation_link = 'Authentication/manager_activation_link.html'
    home = 'Authentication/home.html'
    form = CreateUserForm()
    group_required = [u"admin"]
    navbar_colour = '#808080'

    def get(self, request):
        context = {'form': SignupManager.form, 'user_group': SignupManager.group_required[0],
                   'navbar_colour': SignupManager.navbar_colour}
        return render(request, self.template_name, context)

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.email = form.cleaned_data.get('email')
            group = Group.objects.get(name='manager')
            user.groups.add(group)
            # user can't log in until the link is confirmed
            user.is_active = False
            user.save()
            context = {
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': activation_token.make_token(user),
                'user_group': SignupManager.group_required[0],
                'navbar_colour': SignupManager.navbar_colour,
            }
            return render(request, self.activation_link, context)
        else:
            context = {'form': SignupManager.form, 'error': form.errors, 'user_group': SignupManager.group_required[0],
                       'navbar_colour': SignupManager.navbar_colour}
            return render(request, self.template_name, context)


class RegenerateLinks(GroupRequiredMixin, View):
    template_name = 'Authentication/regenerative_links.html'
    activation_link = 'Authentication/manager_activation_link.html'
    group_required = [u'admin']
    navbar_colour = '#808080'
    raise_exception = True

    def get(self, request):
        users = User.objects.all().filter(groups__name='manager')
        # users_profile = Profile.objects.all().values()
        context = {'users': users.values(), 'user_group': RegenerateLinks.group_required[0],
                   'navbar_colour': RegenerateLinks.navbar_colour}
        return render(request, self.template_name, context)

    def post(self, request):
        username = request.POST.get('new_link')
        user = User.objects.get(username=username)

        current_site = get_current_site(request)
        context = {
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': activation_token.make_token(user),
            'user_group': RegenerateLinks.group_required[0],
            'navbar_colour': RegenerateLinks.navbar_colour,
        }
        return render(request, self.activation_link, context)
