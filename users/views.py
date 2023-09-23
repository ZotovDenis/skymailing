from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView


from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserProfileForm, PasswordResetForm, UserLoginForm
from users.models import User
from users.services import send_verification_email, send_password


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def form_invalid(self, form):
        if not form.user_cache or not form.user_cache.is_active:
            messages.error(self.request, 'Вы заблокированы!')
            return redirect(reverse_lazy('users:user_blocked'))

        return super().form_invalid(form)


class UserBlockedView(TemplateView):
    template_name = 'users/user_blocked.html'


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        verification_token = get_random_string(length=15)
        form.instance.verification_token = verification_token
        send_verification_email(form.instance.email, verification_token)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:verify_email')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('mailing:home')

    def get_object(self, queryset=None):
        return self.request.user


class VerifyView(View):
    template_name = 'users/verify_email.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        verification_code = request.POST.get('verification_code')
        User = get_user_model()
        try:
            user = User.objects.get(verification_token=verification_code)
            if not user.is_verificated:
                user.is_verificated = True
                user.save()
                return redirect('users:success_verification')
        except User.DoesNotExist:
            pass
        return redirect('users:error_verification')


class SuccessVerificationView(TemplateView):
    template_name = 'users/success_verification.html'


class ErrorVerificationView(TemplateView):
    template_name = 'users/error_verification.html'


class ConfirmEmailView(View):

    def get(self, request, verification_token):

        User = get_user_model()

        try:
            user = User.objects.get(verification_token=verification_token)
            if not user.is_verificated:
                user.is_verificated = True
                user.save()
                return render(request, 'success_verification.html')

        except User.DoesNotExist:
            return render(request, 'error_verification.html')


class GenerateAndSendPasswordView(View):
    form = PasswordResetForm()

    def get(self, request):
        return render(request, 'users/password_recovery.html', {'form': self.form})

    def post(self, request):
        self.form = PasswordResetForm(request.POST)
        if self.form.is_valid():
            email = self.form.cleaned_data['email']
            if send_password(email):
                return render(request, 'users/password_reset_success.html', {'email': email})
        return render(request, 'users/password_reset_error.html')
