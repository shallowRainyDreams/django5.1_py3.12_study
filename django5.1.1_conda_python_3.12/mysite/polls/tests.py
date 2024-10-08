import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(question_text, days):
    # 使用给定的“question_text”创建一个问题，
    # 并发布与现在偏移的给定“天数”（过去发布的问题为负数，尚未发布的问题则为正数）。
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):

    """
    首先是一个快捷函数 create_question，它封装了创建投票的流程，减少了重复代码。

test_no_questions 不会创建任何问题，但会检查消息 "No polls are available."
并验证 latest_question_list 是否为空。
注意，django.test.TestCase 类提供了一些额外的断言方法。
在这些示例中，我们使用了 assertContains() 和 assertQuerySetEqual()。

在 test_past_question 方法中，我们创建了一个投票并检查它是否出现在列表中。

在 test_future_question 中，我们创建 pub_date 在未来某天的投票。数据库会在每次调用测试方法前被重置，所以第一个投票已经没了，所以主页中应该没有任何投票。

剩下的那些也都差不多。实际上，测试就是假装一些管理员的输入，然后通过用户端的表现是否符合预期来判断新加入的改变是否破坏了原有的系统状态。
    """

    def test_no_question(self):
        # 如果没有问题，将显示相应的消息。
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        # 过去有pub_date的问题显示在索引页面上。
        # 即查询这个问题是否出现在过去三十天内
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        # 过去有pub_date的问题显示在索引页面上。将来有pub_date的问题不会显示在该页面
        create_question(question_text="Future question.", days=30)  # 创建一个未来发布的问题
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        # 只能让过去存在的问题存在
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],
            [question],)

    def test_two_past_questions(self):
        # 可以查询到多个过去的问题
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )



# 上面八个测试案例都通过了，但是运行下面这两个报错
# TypeError: fromisoformat: argument must be str
# 这个是用来测试views中的detail函数，因此去对应地方寻找，
# 发现是return Question.objects.filter(pub_date__lte=timezone.now())的.now()没写括号
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)