from rest_framework.pagination import PageNumberPagination

class MessagesPagination(PageNumberPagination):
    page_size = 20
    page_query_param = "page"
    page_size_query_param = "page_size"  # optional: allow clients to request smaller pages
    max_page_size = 100                   # optional: cap any requested page_size
