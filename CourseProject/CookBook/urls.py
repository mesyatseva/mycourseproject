from django.conf.urls import url
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from CookBook import views

"""Вызов функций из .views"""
from .views import index, loginSuccessfull, profile, other_page, search, profile_liked
from .views import deleteRecipe, changeRecipe
from .views import all_kitchen, kitchen_slug, dish_slug, detail, addRecipe
from .views import add_liked_recipe_to_profile, delete_liked_recipe_from_profile

"""Вызов классов из .views"""
from .views import CBLoginView, CBLogoutView, ChangeUserInfoView
from .views import CBPasswordResetView, CBPasswordResetDoneView
from .views import RegisterUserView, RegisterDoneView, CBPasswordChangeDoneView, CBPasswordChangeView

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

app_name = 'CookBook'

# Ссылки на уровне приложения
urlpatterns = [


    path('search/', search, name='search'),
    # url('<int:fav_rec>/favourite_recipes/', views.favorite_recipes, name='profile_liked'),
    # url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    # url(r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    # url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),

    path('accounts/profile/change_recipe/<int:pk>', changeRecipe, name='change_recipe'),
    path('accounts/profile/delete_recipe/<int:pk>', deleteRecipe, name='delete_recipe'),

    # Обработчики восстановления пароля.
    url('accounts/profile/password_reset/', auth_views.PasswordResetView.as_view(
        template_name='CookBook/registration/password_reset_form.html',
        email_template_name='CookBook/registration/password_reset_email.txt',
        success_url = reverse_lazy('CookBook:password_reset_done'),
    ), name='password_reset'),
    url('accounts/profile/password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='CookBook/registration/password_reset_done.html',), name='password_reset_done'),
    url('accounts/profile/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        auth_views.PasswordResetConfirmView.as_view(template_name='CookBook/registration/password_reset_confirm.html',
                                                    success_url=reverse_lazy('CookBook:password_reset_complete')),
        name='password_reset_confirm'),
    url('accounts/profile/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='CookBook/registration/password_reset_complete.html'), name='password_reset_complete'),



    path('create_recipe/', addRecipe, name='create_recipe'),


    # path('kitchens/<str:slug>/<int:pk>/', detail, name='detail'),
    path('recipe/<int:pk>/', detail, name='detail'), # ТУТ ИЗМЕНИЛА 21:05
    path('kitchens/<str:slug>/', kitchen_slug, name='kitchens'),
    path('kitchens/', all_kitchen, name='all_kitchens'),
    path('dishes/<str:slug>/', dish_slug, name='dishes'),

    # url('password_reset/$', views.PasswordResetView.as_view(template_name='CookBook/registration/password_reset_form.html',
    #                                                               email_template_name='password_reset_email.html',
    #                                                               subject_template_name='password_reset_subject.txt',
    #                                                               success_url='/accounts/password_reset_done/',
    #                                                               from_email='support@yoursite.ma'), name='password_reset'),
    # url('password_reset_done/', views.PasswordResetDoneView.as_view(template_name='CookBook/registration/password_reset_done.html'), name='password_reset_done'),

    # Операции с УЗ
    # url('accounts/password_reset/',
    #     CBPasswordResetView.as_view(template_name='CookBook/registration/uhjkl/password_reset_form.html',
    #                                 email_template_name='password_reset_email.html',
    #                                 subject_template_name='password_reset_subject.txt',
    #                                 success_url='/accounts/password_reset_done/',
    #                                 from_email='support@yoursite.ma'), name='password_reset'),  # Сброс пароля
    # url('accounts/password_reset_done/',
    #     CBPasswordResetDoneView.as_view(template_name='CookBook/registration/uhjkl/password_reset_done.html'),
    #     name='password_reset_done'),

    # Ссылки - urls
    # url('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # url('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('accounts/profile/password_change/done', CBPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/profile/password_change', CBPasswordChangeView.as_view(), name='password_change'),

    path('accounts/profile/change', ChangeUserInfoView.as_view(), name='profile_change'),

    path('recipe/<int:pk>', delete_liked_recipe_from_profile, name='delete_liked_recipe_from_profile'),
    path('accounts/profile/liked_recipes/<int:pk>', add_liked_recipe_to_profile, name='add_liked_recipe_to_profile'),
    path('accounts/profile/profile_liked/', profile_liked, name='profile_liked'),

    path('accounts/profile/', profile, name='profile'),

    path('register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('logout/', CBLogoutView.as_view(), name='logout'),
    path('login/', CBLoginView.as_view(), name='login'),

    path('<str:page>/', other_page, name='other'),
    path('', index, name='index')
]

# url(r'password_reset/$',auth_views.PasswordResetView.as_view(template_name='password_reset.html',,subject_template_name='password_reset_subject.txt',success_url='/accounts/password_reset_done/',from_email='support@yoursite.ma')),
