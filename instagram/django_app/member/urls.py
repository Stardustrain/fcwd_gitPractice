from django.conf.urls import url
from member import views


urlpatterns = [
    url(r'login/$', views.MemberLogin.as_view(), name="login"),
    url(r'signup/$', views.MemberSignup.as_view(), name="signup"),
    url(r'logout/$', views.LogoutView.as_view(), name="logout"),
]
