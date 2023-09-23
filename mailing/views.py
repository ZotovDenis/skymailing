import random

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from mailing.forms import MailingSettingsForm, ClientForm, MessageForm
from mailing.models import Client, MailingMessage, MailingSettings, MailingLog
from users.models import User


def home(request):
    """Возвращает главную страницу"""
    blog_list = Blog.objects.all()
    random_blog = random.sample(list(blog_list), 3)
    context = {
        'title': 'Главная',
        'settings_list': MailingSettings.objects.all(),
        'active_settings': MailingSettings.objects.filter(status='started'),
        'client_list': Client.objects.all(),
        'blog_list': random_blog,
    }
    return render(request, 'mailing/home.html', context)


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('mailing:user_list')
    permission_required = 'users.set_active'
    fields = ['is_active', ]

    # def form_valid(self, form):
    #     user = form.instance
    #     if not user.is_active:
    #         return redirect(reverse_lazy('users:blocked'))
    #     return super().form_valid(form)


def users(request):
    context = {
        'user_list': User.objects.all()
    }
    return render(request, 'mailing/user_list.html', context)


class ClientListView(ListView):
    """Возвращает страницу Клиентов"""
    model = Client
    template_name = 'mailing/client_list.html'
    extra_context = {'title': 'Список клиентов'}

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


class MessageListView(ListView):
    """Возвращает страницу Писем"""
    model = MailingMessage
    template_name = 'mailing/message_list.html'
    extra_context = {'title': 'Список писем'}


class MessageCreateView(CreateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(UpdateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:message_list')


class MailingSettingsListView(ListView):
    model = MailingSettings
    extra_context = {'title': 'Список рассылок'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        queryset = MailingSettings.objects.all()

        if not self.request.user.is_staff and not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)

        return queryset

        # return MailingSettings.objects.filter(user=self.request.user)


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.object.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm

    success_url = reverse_lazy('mailing:mailing_list')
    pk_url_kwarg = 'pk'
    permission_required = 'mailing.modify_settings_status'

    def get_object(self, queryset=None):
        return MailingSettings.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.object.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()

        ############################ Данный участок кода требует корректировки и уточнения #################################

        # Проверка, является ли пользователь сотрудником
        if self.request.user.is_staff:
            mailing_settings = self.object

            # Если пользователь является сотрудником и рассылка принадлежит другому пользователю,
            # то они могут изменять только поле статуса
            if mailing_settings.user != self.request.user:
                mailing_settings.status = form.cleaned_data['status']

        ####################################################################################################################
        self.object.save()

        return super().form_valid(form)


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_list')


class MaillingLogListView(ListView):
    """Возвращает страницу Клиентов"""
    model = MailingLog
    template_name = 'mailing/maillinglogs_list.html'
    extra_context = {'title': 'Список логов'}
