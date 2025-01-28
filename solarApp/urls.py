

from django.urls import path
from solarApp import views


urlpatterns = [
    # path('',views.product_list,name='main_home'),
    path('',views.product_list,name='home'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('about/',views.about_page,name='about'),
    path('register/',views.register_user,name='register'),
    path('update_user/',views.update_user,name='update_user'),
    path('update_info/',views.update_info,name='update_info'),
    path('update_password/',views.update_password,name='update_password'),
    path('product/<int:pk>',views.product,name='product'),
    path('search/',views.search,name='search'),







    path('create/',views.ShopCreateView.as_view()),
    path('detail/<int:pk>',views.ShopDetailView.as_view()),
    path('update/<int:pk>',views.ShopUpdateView.as_view())
]
