from django.contrib import admin

from .models import Like

class LikeAdmin(admin.ModelAdmin):
    list_display = ('like_id','author', 'post')


admin.site.register(Like, LikeAdmin)