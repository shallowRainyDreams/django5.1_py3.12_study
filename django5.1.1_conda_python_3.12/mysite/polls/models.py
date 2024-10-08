

# Create your models here.

import datetime

from django.db import models
from django.utils import timezone

from django.contrib import admin


# model层是为了数据库服务的，在下面的这些代码中，一个类就相当于一个表

# 改变模型需要这三步：
#
# 编辑 models.py 文件，改变模型。
# 运行 python manage.py makemigrations 为模型的改变生成迁移文件。
# 运行 python manage.py migrate 来应用数据库迁移。

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    # display装饰器，用来修饰后续的函数
    @admin.display(
        boolean=True,  # 是否是布尔值
        ordering="pub_date",  # 根据对应字段排序
        description="Published recently?",  # 标题描述
    )
    def was_published_recently(self):
        now = timezone.now()
        return now-datetime.timedelta(days=1)<=self.pub_date<=now



class Choice(models.Model):
    # 每个choice都能与一个question相连，因此能够通过question.choice_set.all()获取choice信息
    # 一个question可以有多个choice_text
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text