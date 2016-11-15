from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, View, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeleteView
from .models import Photo, PhotoComment, PhotoLike



def photo_list(request):
    photos = Photo.objects.all()
    context = {
        'photos': photos,
    }
    return render(request, 'photo_list.html', context)


class PhotoList(ListView):
    model = Photo
    context_object_name = "photos" # 설정하지 않으면 object_list로 template에서 받게 된다
    paginate_by = 3
    ordering = "pk"


@method_decorator(login_required, name="dispatch")
class PhotoAdd(CreateView):
    model = Photo
    fields = ["image", "content"]
    # 아래 url을 지정하지 않으면 model쪽에 get_absolute_url 지정
    success_url = reverse_lazy("photo:photo_list")

    def form_valid(self, form):
        form.instance.author = MyUser.objects.get(pk=1)
        return super(PhotoAdd, self).form_valid(form)


class PhotoCommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class PhotoDisplayView(DetailView):
    model = Photo

    def get_context_data(self, **kwargs):
        context = super(PhotoDisplayView, self).get_context_data(**kwargs)
        context["form"] = PhotoCommentForm()
        return context


class PhotoCommentFormView(SingleObjectMixin, FormView):
    form_class = PhotoCommentForm
    template_name = "photo/photo_detail.html"
    model = Photo

    def form_valid(self, form):
        self.object = self.get_object()
        content = form.cleaned_data["content"]
        PhotoComment.objects.create(
            photo=self.object,
            author=self.request.user,
            content=content
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("photo:photo_detail", kwargs={"pk": self.object.pk})


class PhotoDetail(View):
    def get(self, request, *args, **kwargs):
        ret = PhotoDisplayView.as_view()
        return ret(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ret = PhotoCommentFormView.as_view()
        return ret(request, *args, **kwargs)


class PhotoLikeView(SingleObjectMixin):
    model = PhotoLike

class Delete(DeleteView):
    model = AuthorDelete
    success_url = reverse_lazy('photo_list')