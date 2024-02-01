from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.views.generic import FormView
from django.contrib.auth import login, logout

# Create your views here.


class MyLoginView(LoginView):
    # redirect user if authentication is succeed
    redirect_authenticated_user = True
    template_name = "registration/login.html"

    # url after success login
    def get_success_url(self):
        return reverse_lazy("core:home")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid email or password")
        return self.render_to_response(self.get_context_data(form=form))


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        user = form.save()
        if user:
            messages.success(self.request, "Welcome to PlayHub")
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)


def logout_view(request):
    logout(request)
    return redirect("core:home")
