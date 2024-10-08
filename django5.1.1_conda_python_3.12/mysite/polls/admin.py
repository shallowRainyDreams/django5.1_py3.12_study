from django.contrib import admin

# Register your models here.

from .models import Question, Choice

# TabularInline， 关联对象以一种表格的方式展示
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # 关联选项槽，即主键与该类关联，在管理页面时，会出现三个这个类


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question Text', {"fields": ["question_text"]}),
        # Date information， 标题
        #  "classes": ["collapse"]， 是一个css类，默认情况下是堆叠的，需要点击才能展示具体信息
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]  # 与其他表有关

    # 继承的list_display字段，在这个类的管理界面显示对应的字段
    list_display = ["question_text", "pub_date", "was_published_recently"]

    list_filter = ["pub_date"]  # 根据pub_date的过滤器，能够手动选择时间

    search_fields = ["question_text"]  # 列表顶部的搜索窗


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)