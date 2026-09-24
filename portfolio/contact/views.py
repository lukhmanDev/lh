from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

from contact.models import ContactMessage
from contact.serializers import ContactMessageSerializer



class ContactMessageListCreateView(ListCreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer


# Alias for backward compatibility
ContactMessageCreateView = ContactMessageListCreateView


class ContactMessageDetailView(RetrieveAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

