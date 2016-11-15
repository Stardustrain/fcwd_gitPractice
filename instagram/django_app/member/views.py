from django.shortcuts import render, reverse, HttpResponse, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View, FormView, TemplateView
from django.contrib.auth import login, logout, authenticate
from django import forms
from django.conf import settings
from member.models import MyUser


# class MemberLoginForm(forms.ModelForm):
#     class Meta:
#         model = MyUser
#         fields = ("username", "password",)
#         widgets = {"password": forms.PasswordInput()}


class MemberLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class MemberLogin(FormView):
    form_class = MemberLoginForm
    template_name = "member/login.html"
    success_url = reverse_lazy("photo:photo_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username,
                            password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return redirect("member:login")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("member:login")



# def login_fbv(request):
#     if request.method == "GET":
#         form = MemberLoginForm()
#         ret = {"form": form}
#         return render(request, "member/login.html", ret)
#
#     elif request.method == "POST":
#         form = MemberLoginForm(data=request.POST)
#
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password"]
#             user = authenticate(username=username,
#                                 password=password)
#             if user is not None:
#                 login(request, user)
#             return redirect("photo:photo_list")
#         else:
#             return HttpResponse("FUCK")