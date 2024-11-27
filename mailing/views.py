
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy, reverse
from mailing.models import Client, Message, Settings


class ClientCreateView(CreateView):
    model = Client
    fields = ('email', 'name', 'comment')
    success_url = reverse_lazy('mailing:list_client')

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save()
            new_client.save()
            return super().form_valid(form)
class ClientListView(ListView):
    model = Client

class ClientDetailView(DetailView):
    model = Client

class ClientUpdateView(UpdateView):
    model = Client
    fields = ('email', 'name', 'comment')
    def form_valid(self, form):
        if form.is_valid():
            client = form.save()
            client.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:detail_client', args=[self.kwargs.get('pk')])

class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:list_client')


class MessageCreateView(CreateView):
    model = Message
    fields = ('topic', 'body')
    success_url = reverse_lazy('mailing:list_message')

    def form_valid(self, form):
        if form.is_valid():
            new_message = form.save()
            new_message.save()
            return super().form_valid(form)

class MessageListView(ListView):
    model = Message

class MessageDetailView(DetailView):
    model = Message

class MessageUpdateView(UpdateView):
    model = Message
    fields = ('topic', 'body')
    def form_valid(self, form):
        if form.is_valid():
            message = form.save()
            message.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:detail_message', args=[self.kwargs.get('pk')])

class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:list_message')



# CRUD для модели Mailing Mailing

class MailingCreateView(CreateView):
    model = Settings
    fields = ('description', 'status', 'date_start', 'frequency', 'clients', 'message')
    success_url = reverse_lazy('mailing:list_mailing')

    def form_valid(self, form):
        if form.is_valid():
            new_mailing = form.save()
            new_mailing.save()
            return super().form_valid(form)
class MailingListView(ListView):
    model = Settings

class MailingDetailView(DetailView):
    model = Settings
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        clients = self.object.clients.all()
        context_data['clients'] = clients
        return context_data

class MailingUpdateView(UpdateView):
    model = Settings
    fields = ('description', 'status', 'date_start', 'frequency', 'clients', 'message')
    def form_valid(self, form):
        if form.is_valid():
            mailing = form.save()
            mailing.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:detail_mailing', args=[self.kwargs.get('pk')])

class MailingDeleteView(DeleteView):
    model = Settings
    success_url = reverse_lazy('mailing:list_mailing')
