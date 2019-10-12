from django.contrib import admin

from .models import Topic, Article

# provides space for 3 articles
class ArticleInline(admin.TabularInline):
    model = Article
    extra = 3

class TopicAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['keywords']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ArticleInline]
    list_display = ('keywords', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['keywords']

admin.site.register(Topic, TopicAdmin)
