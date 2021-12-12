from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message

#アドミンページに作成したインスタンスを反映させる
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)

