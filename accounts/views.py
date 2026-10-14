from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView, View
from .forms import CustomerSignUpForm, ControllerSignUpForm, IssueForm
from .models import CustomUser, Issue
from django.urls import reverse_lazy
import base64
from django.core.files.base import ContentFile
import uuid
from django.urls import reverse_lazy

class SignupSelectionView(TemplateView):
    template_name = 'accounts/signup_selection.html'

class CustomerSignUpView(CreateView):
    model = CustomUser
    form_class = CustomerSignUpForm
    template_name = 'accounts/customer_signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class ControllerSignUpView(CreateView):
    model = CustomUser
    form_class = ControllerSignUpForm
    template_name = 'accounts/controller_signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if self.request.user.role == CustomUser.Role.CONTROLLER:
                context['customers'] = CustomUser.objects.filter(role=CustomUser.Role.CUSTOMER).prefetch_related('issues')
            elif self.request.user.role == CustomUser.Role.CUSTOMER:
                context['issue_form'] = IssueForm()
                context['my_issues'] = self.request.user.issues.all().order_by('-created_at')
        return context

class SubmitIssueView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.user.role == CustomUser.Role.CUSTOMER:
            form = IssueForm(request.POST)
            if form.is_valid():
                issue = form.save(commit=False)
                issue.customer = request.user
                issue.save()
        return redirect('home')

class ResolveIssueView(LoginRequiredMixin, View):
    def post(self, request, issue_id, *args, **kwargs):
        if request.user.role == CustomUser.Role.CUSTOMER:
            issue = get_object_or_404(Issue, id=issue_id, customer=request.user)
            issue.is_resolved = True
            issue.save()
        return redirect('home')
