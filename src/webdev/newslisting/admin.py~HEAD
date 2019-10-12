from django.contrib import admin

from .models import Topic, Article, Quote

# provides space for 3 articles
class ArticleInline(admin.TabularInline):
    model = Article
    extra = 3

class TopicAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['topic_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ArticleInline]
    list_display = ('topic_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['topic_text']

admin.site.register(Topic, TopicAdmin)
