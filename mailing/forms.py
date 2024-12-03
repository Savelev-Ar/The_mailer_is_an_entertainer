from django import forms
from mailing.models import Settings, Message, Client


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleMixin, forms.ModelForm):

    class Meta:
        model = Settings
        fields = '__all__'


class MessageForm(StyleMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = '__all__'


class ClientForm(StyleMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'