from django.db import models


class SearchQuery(models.Model):
    query_text = models.CharField(max_length=255)
    results_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'search_query'

    def __str__(self):
        return self.query_text


class SearchResult(models.Model):
    search_query = models.ForeignKey(SearchQuery, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    relevance_score = models.FloatField(default=0.0)

    class Meta:
        db_table = 'search_result'

    def __str__(self):
        return f"Result for {self.search_query.query_text}"
