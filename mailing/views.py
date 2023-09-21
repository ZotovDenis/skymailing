from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingSettingsForm, ClientForm, MessageForm
from mailing.models import Client, MailingMessage, MailingSettings, MailingLog


def home(request):
    """Возвращает главную страницу"""
    context = {'title': 'Главная'}
    return render(request, 'mailing/base.html', context)


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
        kwargs['user'] = self.request.user
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
        kwargs['user'] = self.request.user
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
