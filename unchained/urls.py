"""unchained URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static
from . import settings
from . import views
from django.conf.urls import include
from django.views.static import serve
from django.contrib.auth import views as auth_views


#from django.contrib.auth.models import User #password reset
#u = User.objects.get(username='unchained')
#u.set_password('aaron')
#u.save()
#from django.contrib.auth import get_user_model #List users
#User = get_user_model()
#users = User.objects.all()
#print(users)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.query),
    path('update',views.update),
    path('accounts/login/', auth_views.LoginView.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#http://192.168.0.36:8000/admin/login/?next=/admin/