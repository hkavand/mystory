"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    #Auth
    path('signup/',views.signupuser, name='signupuser'),
    path('logout/',views.logoutuser, name='logoutuser'),
    path('login/',views.loginuser, name='loginuser'),
    path('verify/',views.verify, name='verify'),

    #todo
    path('privatepage/',views.privatepage, name='privatepage'),
    path('',views.home, name='home'),
    path('create/',views.createtodo, name='createtodo'),
    path('todo/<int:todo_pk>',views.viewtodo, name='viewtodo'),
    path('todo/<int:todo_pk>/complete',views.completetodo, name='completetodo'),
    path('todo/<int:todo_pk>/delete',views.deletetodo, name='deletetodo'),
    path('completed/',views.completedtodos, name='completedtodos'),

    #extra
    path('faq/',views.faq,name='faq'),
    path('contactus',views.contactus,name='contactus'),
    path('profile',views.profile,name='profile'),
    path('editprofile',views.editprofile,name='editprofile'),
    path('fullstory',views.fullstory,name='fullstory'),
    path('comment',views.savecomment,name='savecomment'),
    path('viewprofile/<str:user_username>/',views.viewprofile,name='viewprofile'),
    path('editstory/<int:post_pk>/',views.editstory,name='editstory'),
    path('deletestory',views.deletestory,name='deletestory'),

    #Global
    path('global',views.globalspace,name='global'),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)