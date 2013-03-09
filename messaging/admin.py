# coding=utf-8
from django.contrib import admin
from messaging.models import Mailbox, Message

admin.site.register(Message)
admin.site.register(Mailbox)