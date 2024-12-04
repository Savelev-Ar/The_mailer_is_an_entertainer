from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy, reverse
from mailing.models import Client, Message, Settings, Attempt
from mailing.forms import MailingForm, MessageForm, ClientForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mailing import add_job_to_scheduler


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    login_url = '/user/login'
    success_url = reverse_lazy('mailing:list_client')

    def form_valid(self, form):
        user = self.request.user
        client = form.save()
        client.user = user
        client.save()
        return super().form_valid(form)
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    login_url = '/user/login/'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        clients = user.clients.all()
        context_data['object_list'] = clients
        return context_data

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    login_url = '/user/login/'

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    login_url = '/user/login/'
    success_url = reverse_lazy('mailing:list_client')

    def get_success_url(self):
        return reverse('mailing:detail_client', args=[self.kwargs.get('pk')])

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    login_url = '/user/login/'
    success_url = reverse_lazy('mailing:list_client')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    login_url = '/user/login/'
    success_url = reverse_lazy('mailing:list_message')

    def form_valid(self, form):
        user = self.request.user
        message = form.save()
        message.user = user
        message.save()
        return super().form_valid(form)

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    login_url = '/user/login/'

class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    login_url = '/user/login/'

class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    login_url = '/user/login/'
    success_url = reverse_lazy('mailing:list_message')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    login_url = '/user/login/'
    success_url = reverse_lazy('mailing:list_message')


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Settings
    form_class = MailingForm
    login_url = '/user/login/'
    success_url = reverse_lazy('mailing:list_mailing')

    def form_valid(self, form):
        user = self.request.user
        mailing = form.save()
        mailing.user = user
        mailing.save()
        if mailing.status != Settings.COMPLETED:
            add_job_to_scheduler(mailing)
        return super().form_valid(form)

class MailingListView(LoginRequiredMixin, ListView):
    model = Settings
    login_url = '/user/login/'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        block = context_data['view'].request.GET.get("block")
        unblock = context_data['view'].request.GET.get("unblock")
        if block:
            pk = context_data['view'].request.GET.get("block")
            mailing_to_block = Settings.objects.get(pk=pk)
            mailing_to_block.status = 'completed'
            mailing_to_block.save()
        elif unblock:
            pk = context_data['view'].request.GET.get("unblock")
            mailing_to_unblock = Settings.objects.get(pk=pk)
            mailing_to_unblock.status = 'launched'
            mailing_to_unblock.save()
        return context_data

class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Settings
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        clients = self.object.clients.all()
        context_data['clients'] = clients
        return context_data

class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Settings
    form_class = MailingForm

    login_url = '/user/login/'
    success_url = reverse_lazy('mailing:list_mailing')

    def form_valid(self, form):
        mailing = form.save()
        if mailing.status != Settings.COMPLETED:
            add_job_to_scheduler(mailing)
        return super().form_valid(form)

class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Settings
    login_url = '/user/login/'
    success_url = reverse_lazy('mailing:list_mailing')

@method_decorator(cache_page(60 * 1), name='dispatch')
class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        work_status = ['created', 'launched']
        context_data['count_of_newsletter'] = Settings.objects.all().count()
        context_data['count_of_active'] = Settings.objects.filter(status__in=work_status).count()
        context_data['count_of_unique_clients'] = len(set(Client.objects.all()))

        return context_data

class ReportView(LoginRequiredMixin, TemplateView):

    template_name = 'mailing/report.html'
    login_url = '/user/login/'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        setting = Settings.objects.filter(owner=user)
        queryset = Attempt.objects.filter(settings__in=setting).order_by('last_datetime')
        if (context_data['view'].request.GET.get('start_date') and
                context_data['view'].request.GET.get('end_date')):
            start_date = context_data['view'].request.GET['start_date']
            end_date = context_data['view'].request.GET['end_date']
            context_data['object_list'] = queryset.filter(last_datetime__gte=start_date).filter(last_datetime__lte=end_date).order_by('last_datetime')
            context_data['start_date'] = start_date
            context_data['end_date'] = end_date
        else:
            context_data['object_list'] = queryset
        return context_data
