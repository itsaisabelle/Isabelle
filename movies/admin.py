from django.contrib import admin
from .models import Movie, Review, Report

# Register your models here.
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Report)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id","user", "comment", "movie", "date", "reported")

    def commentCounter(self, obj):
        return obj.comment.count()

    commentCounter.short_description = 'Number of Comments'
    list_filter = ("coummentCounter",)

