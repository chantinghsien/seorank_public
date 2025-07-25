from django.contrib import admin

from ranking.models import (UserProfileInfo,
                            Domain,
                            Keyword,
                            KeywordRankHistory)

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Domain)
admin.site.register(Keyword)
admin.site.register(KeywordRankHistory)