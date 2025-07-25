from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

import datetime

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nickname = models.CharField(max_length = 10)

    def __str__(self):
        return self.user.username
    
class Domain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="domains",
                             verbose_name="所屬使用者")
    domain_name = models.CharField(max_length=255, verbose_name="域名")

    class Meta:
        unique_together = ('user', 'domain_name',)
        verbose_name = "域名"
        verbose_name_plural = "域名"
        indexes = [
            models.Index(fields=["user", "domain_name"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.domain_name}"
    
class Keyword(models.Model):
    domain_name = models.ForeignKey(Domain, on_delete=models.CASCADE,
                               related_name="keywords",
                               verbose_name="所屬域名")
    keyword_name = models.CharField(max_length=255, verbose_name="關鍵字")

    class Meta:
        unique_together = ("domain_name", "keyword_name",)
        verbose_name = "關鍵字"
        verbose_name_plural = "關鍵字"
        indexes = [
            models.Index(fields=["domain_name", "keyword_name"]),
        ]

    def __str__(self):
        return f"{self.domain_name.user.username} - {self.domain_name.domain_name} - {self.keyword_name}"
    
class KeywordRankHistory(models.Model):
    keyword_name = models.ForeignKey(Keyword, on_delete=models.CASCADE,
                                related_name='rank_history', # 通過 keyword.rank_history.all() 訪問該關鍵字的歷史排名
                                verbose_name="所屬關鍵字")
    rank = models.IntegerField(null=True, blank=True, verbose_name="排名") # 可為空，表示尚未抓取或無排名
    # 建立日期：auto_now_add=True 會在物件首次創建時自動設置為當前時間
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立日期")

    class Meta:
        verbose_name = "關鍵字排名歷史"
        verbose_name_plural = "關鍵字排名歷史"
        # 按建立日期降序排列，方便查看最新排名
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['keyword_name', 'created_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.keyword_name.domain_name.user.username} - {self.keyword_name.domain_name.domain_name} - {self.keyword_name.keyword_name} - {self.rank if self.rank is not None else 'N/A'} @ {self.created_at.strftime('%Y-%m-%d %H:%M')}"