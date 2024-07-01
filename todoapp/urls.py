# todoapp/urls.py

from django.urls import path, include
from . import views

app_name = 'todoapp'

urlpatterns = [
    path('user/', include([
        path('login/', views.user_login, name='user_login'),
        path('register/', views.user_register, name='user_register'),
        path('account/', views.user_account, name='user_account'),
        path('logout/', views.logout),
        path('alltodolist/', views.all_todolist, name='all_todolist'),
        path('createtodo/', views.create_todo, name='create_todo'),
        path('edittodo/<id>', views.update_todo, name='update_todo'),
        path('deletetodo/<id>', views.delete_todo, name='delete_todo'),
    ])),
    path('admin_login/', include([
			path('account/',views.login_admin, name='adminlogin'),
	]))
]
