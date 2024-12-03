from secrets import token_hex
from random import shuffle
from string import ascii_letters, digits
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from user.models import User
from user.forms import UserRegisterForm, UserProfileForm


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        self.request.get_host()

        url = f'http://{host}/user/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))

def reset(request):
    context = {
        'success_message': 'Пароль успешно сброшен, '
                           'Новый пароль был отправлен '
                           'на Ваш адрес электронный почты'
    }

    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)
        chars = list(ascii_letters + digits)
        shuffle(chars)
        password = ''.join(chars[:8])
        user.set_password(password)
        user.save()
        send_mail(
            subject='Восстановление пароля',
            message=f'Здравствуйте, вы запрашивали обновление пароля. '
                    f'Ваш новый пароль: {password}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return render(request, 'users/reset.html', context)
    else:
        return render(request, 'users/reset.html')