from django.urls import path
from .views import UiPageView


ui_patterns = ([
    path('', UiPageView.as_view(), name='ui'),
],"ui")
