from django.conf.urls import url
from member import views


urlpatterns = [
    url(r'login/$', views.MemberLogin.as_view(), name="login"),
    url(r'logout/$', views.logout, name="logout"),
    url(r'signup/$', views.MemberSignup.as_view(), name="signup"),
    # url(r'login/$', views.login_fbv, name="login"),
]