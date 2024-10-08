
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # path参数包含route：响应请求时去匹配, 如https://www.example.com/myapp/ 时，它会尝试匹配 myapp/
    # 这个route是浏览器访问url的，但是定位到哪个视图，就是由前端模板的name去寻找
    # view：视图中对应的函数调用
    # kwargs：任意个关键字参数可以作为一个字典传递给目标视图函数
    # name：为你的 URL 取名能使你在 Django 的任意地方唯一地引用它，即前端调用就是通过这个name去调用

    # ex: /polls/
    path("", views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    path("<int:pk>", views.DetailView.as_view(), name='detail'),

    path("<int:pk>/results", views.ResultsView.as_view(), name='results'),

    path("<int:question_id>/vote", views.vote, name='vote'),
]