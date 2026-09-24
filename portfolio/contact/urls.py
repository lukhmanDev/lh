from django.urls import path

from contact.views import ContactMessageDetailView, ContactMessageListCreateView


urlpatterns = [
    path('messages/', ContactMessageListCreateView.as_view(), name='contact-message-create'),
    path('messages/<int:pk>/', ContactMessageDetailView.as_view(), name='contact-message-detail'),
]

