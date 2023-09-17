from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, MailingListView, \
    MailingSettingsCreateView, MailingSettingsUpdateView, MailingSettingsDeleteView, home, MaillingLogListView

app_name = MailingConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('customer_list/', ClientListView.as_view(), name='client_list'),
    path('customer/create/', ClientCreateView.as_view(), name='client_form'),
    path('customer/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('customer/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_form'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/create/', MailingSettingsCreateView.as_view(), name='mailing_form'),
    path('mailing/update/<int:pk>/', MailingSettingsUpdateView.as_view(), name='mailing_update'),
    path('mailing/delete/<int:pk>/', MailingSettingsDeleteView.as_view(), name='mailing_delete'),

    path('logs/', MaillingLogListView.as_view(), name='log_list'),
]
