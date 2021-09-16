from django.urls import path

from . import views




urlpatterns = [
        #Leave as empty string for base url
	path('', views.useraut, name="useraut"),
	path('train/', views.train, name="train"),
	path('userprofile/', views.userprofile, name="userprofile"),
	path('register/', views.register, name="register"),
	path('login/',views.loginpage,name="login"),
	path('logoutuser',views.logoutuser,name='logoutuser')
]



