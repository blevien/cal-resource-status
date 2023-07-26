from django.urls import path, include
from . import views

urlpatterns = [
    path('display/<int:display>', views.index, name='index'),

]
