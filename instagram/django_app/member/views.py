from django.shortcuts import render, reverse, HttpResponse, redirect
from django.urls import reverse_lazy
from django.views.generic import View, FormView, TemplateView
from django.contrib.auth import login, logout, authenticate
from django import forms
from member.models import MyUser


# class MemberLoginForm(forms.ModelForm):
#     class Meta:
#         model = MyUser
#         fields = ("username", "password",)
#         widgets = {"password": forms.PasswordInput()}


class MemberLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class MemberSignupForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ("username", "password", "first_name", "last_name","email",)
        widgets = {"password": forms.PasswordInput()}


class MemberSignup(FormView):
    form_class = MemberSignupForm
    template_name = "member/signup.html"
    success_url = reverse_lazy("photo:photo_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

    def form_valid(self, form):
        myuser = MyUser.objects.create_user(username=form.cleaned_data["username"],
                                          password=form.cleaned_data["password"],
                                          email=form.cleaned_data["email"],
                                          first_name=form.cleaned_data["first_name"],
                                          last_name=form.cleaned_data["last_name"])
        user = authenticate(username=form.cleaned_data["username"],
                            password=form.cleaned_data["password"])

        # next_url = self.request.GET.get("next")

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)


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


def member_logout(request):
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