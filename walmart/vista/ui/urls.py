from django.urls import path
from .views import UiPageView,UiCancelacionView,UiRecargaView

app_name = 'ui'
urlpatterns = [
    path('', UiPageView.as_view(), name='ui'),
    path('cancelacion/', UiCancelacionView.as_view(), name='cancelacion'),
    path('recarga/', UiRecargaView.as_view(), name='recarga'),
    
]
