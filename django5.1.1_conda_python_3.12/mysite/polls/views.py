
from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)


# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExit:
#     #     raise Http404("Question does not exist")  # 抛出异常，raise用于异常处理，表示错误或异常情况，会中断程序流程
#     #
#     # return render(request, 'polls/detail.html', {"question": question})
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {"question": question})
#
#
# def result(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {"question":question})


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # return Question.objects.order_by("-pub_date")[:5]  # 指定模板中使用的变量名

        # Question.objects.filter(pub_date__lte=timezone.now())
        # 返回一个包含 Question 的 pub_date 小于或等于（即，早于或等于） timezone.now 的时间查询集。
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        # 不返回未发布的问题
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # pk=request.POST['choice'], 从请求的post表单中获取key为choice的val
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render('polls/detail.html', {
                "question": question,
                "error_message": "You didn't select a choice.",
            }, )
    else:
        selected_choice.votes = F('votes') + 1  # 指示数据库 将投票数增加 1
        selected_choice.save()
        #  HttpResponseRedirect 只接收一个参数：用户将要被重定向的 URL
        # 作用是将用户请求重定向到另一个 URL
        # 关于HttpResponseRedirect和HttpResponse的区别
        # 重定向是根据当前用户请求，返回一个新的url给用户
        # 而HttpResponse就是根据当前请求返回给同一个url传递新值
        # 以下是gpt4o给出的解决
        # 重定向：当使用 HttpResponseRedirect 时，服务器会告诉浏览器去访问另一个 URL。这意味着用户在浏览器中看到的地址会改变，通常用于引导用户到另一个页面或处理某个操作后的反馈（比如提交表单后重定向到感谢页面）。
        # HttpResponse：使用 HttpResponse 时，服务器会直接返回内容给用户，通常是在同一个页面上显示一些数据或结果。用户的浏览器地址不会改变，页面的内容可能会更新，但地址栏中的 URL 仍然是当前页面。

        # reverse()函数的作用是避免在views中硬编码url， 而是像前端那样作为一个模板，
        # 'polls:results' 指向polls下的result的url，并且传入指定参数
        return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))