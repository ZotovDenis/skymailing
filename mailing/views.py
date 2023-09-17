from django.shortcuts import render
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


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


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


class MailingListView(ListView):
    model = MailingSettings
    extra_context = {'title': 'Список рассылок'}


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()

        context['time_field'] = form['time']
        context['period_field'] = form['period']
        context['status_field'] = form['status']
        context['message_field'] = form['message']
        context['clients'] = form['clients']
        return context


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm

    success_url = reverse_lazy('mailing:mailing_list')


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_list')


class MaillingLogListView(ListView):
    """Возвращает страницу Клиентов"""
    model = MailingLog
    template_name = 'mailing/maillinglogs_list.html'
    extra_context = {'title': 'Список логов'}
