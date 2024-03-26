from django.contrib import admin
from .models import ContactForm,Post,Comment,PostApproved

admin.site.register(ContactForm)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostApproved)


# Register your models here.
