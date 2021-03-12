from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('adda/', views.adda, name='adda'),
    path('user/', views.log_in, name='login'),
    path('aboutuser/', views.aboutuser, name='aboutuser'),
    path('log_out/', views.log_out, name='logout'),
    path('register/', views.register, name='register'),
    path('<int:pk>', views.NewDeteilView.as_view(), name="menu_detail"),
    path('<int:pk>/update', views.NewUpdateView.as_view(), name="menu_update"),

]
