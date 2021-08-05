from django.urls import path
from .views import ProcessHookView

hook_patterns = ([
    path('hook/', ProcessHookView.as_view(), name="hom"),
],"hook")
