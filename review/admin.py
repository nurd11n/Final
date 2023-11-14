from django.contrib import admin
from .models import Like, Favourites, Rating, Comment


admin.site.register(Like)
admin.site.register(Favourites)
admin.site.register(Rating)
admin.site.register(Comment)
