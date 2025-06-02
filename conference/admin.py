from django.contrib import admin
from .models import CallRecord,Doctor_Call_serve,AgoraChannel

admin.site.register(AgoraChannel)
admin.site.register(CallRecord)
admin.site.register(Doctor_Call_serve)