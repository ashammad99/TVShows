from django.urls import path
from . import views

app_name = 'shows'

urlpatterns = [
    # READ - List
    path('', views.shows_list, name='shows_list'),

    # CREATE - Form & Process
    path('new/', views.shows_new, name='shows_new'),
    path('create/', views.shows_create, name='shows_create'),

    # READ - Detail
    path('<int:pk>/', views.shows_detail, name='show_detail'),

    # UPDATE - Form & Process
    path('<int:pk>/edit/', views.shows_edit, name='shows_edit'),
    path('<int:pk>/update/', views.shows_update, name='shows_update'),

    # DELETE
    path('<int:pk>/delete/', views.shows_delete, name='shows_delete'),
]