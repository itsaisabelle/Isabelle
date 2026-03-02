from django.contrib import admin
from .models import Movie, Review, Report, Most

# Register your models here.
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Report)

@admin.register(Review)
class ReviewAdmin(admin.Review):
    list_display = ("id","user", "comment", "movie", "date", "reported", "commentCounter")
    list_filter = ['user','reported', 'movie', 'date', 'commentCounter']
    ordering = ['-commentCounter']

@admin.register(Most)
class MostAdmin(admin.ModelAdmin):
    list_display = ('movie', 'reviewCounter', 'amountPurchased')
    list_filter = ['amountPurchased', 'reviewCounter']

