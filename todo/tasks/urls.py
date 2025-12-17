from django.urls import path , reverse_lazy
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', CustomLoginView.as_view() , name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')) , name='logout'),
    path('register/', views.register , name = 'register'),
    path('' , views.index, name="list"),
    path('update_task/<str:pk>/' , views.updateTask, name="update_task"),
    path('delete/<str:pk>/' , views.deleteTask, name="delete"),
]
