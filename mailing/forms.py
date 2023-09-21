from django import forms

from mailing.models import MailingSettings, Client, MailingMessage


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):

    clients = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(user=user)

    class Meta:
        model = MailingSettings
        exclude = ('user', )


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        exclude = ('user', )


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MailingMessage
        fields = '__all__'


class UserMailingSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = ['status', ]