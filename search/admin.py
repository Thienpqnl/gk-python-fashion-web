from django.contrib import admin
from .models import SearchQuery, SearchResult


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'query_text', 'results_count', 'created_at')
    search_fields = ('query_text',)
    list_filter = ('created_at',)


@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'search_query', 'product_id', 'relevance_score')
    search_fields = ('search_query__id', 'product_id')
