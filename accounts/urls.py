from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.SignupSelectionView.as_view(), name='signup'),
    path('signup/customer/', views.CustomerSignUpView.as_view(), name='customer_signup'),
    path('signup/controller/', views.ControllerSignUpView.as_view(), name='controller_signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('submit-issue/', views.SubmitIssueView.as_view(), name='submit_issue'),
    path('resolve-issue/<int:issue_id>/', views.ResolveIssueView.as_view(), name='resolve_issue'),
    path('', views.HomeView.as_view(), name='home'),
]
