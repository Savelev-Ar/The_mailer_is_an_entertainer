from django.urls import path

from mailing.views import (ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, ClientCreateView,
                           MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView, MessageCreateView,
                           MailingListView, MailingDetailView, MailingUpdateView, MailingDeleteView, MailingCreateView)


app_name = 'mailing'

urlpatterns = [
    #path('', MailingListView.as_view(), name='mailing_list'),
    #path('', ClientListView.as_view(), name='list_client'),
    path('client/create/', ClientCreateView.as_view(), name='create_client'),
    path('client/detail/<int:pk>', ClientDetailView.as_view(), name='detail_client'),
    path('client/update/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
    path('client/', ClientListView.as_view(), name='list_client'),
    path('message/create/', MessageCreateView.as_view(), name='create_message'),
    path('message/detail/<int:pk>', MessageDetailView.as_view(), name='detail_message'),
    path('message/update/<int:pk>', MessageUpdateView.as_view(), name='update_message'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),
    path('message/', MessageListView.as_view(), name='list_message'),
    path('mailing/create/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailing/detail/<int:pk>', MailingDetailView.as_view(), name='detail_mailing'),
    path('mailing/update/<int:pk>', MailingUpdateView.as_view(), name='update_mailing'),
    path('mailing/delete/<int:pk>', MailingDeleteView.as_view(), name='delete_mailing'),
    path('mailing/', MailingListView.as_view(), name='list_mailing'),

]
