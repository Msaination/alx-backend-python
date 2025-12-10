from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagesPagination(PageNumberPagination):
    page_size = 20
    page_query_param = "page"
    page_size_query_param = "page_size"  # optional
    max_page_size = 100                  # optional

    def get_paginated_response(self, data):
        # Explicitly use page.paginator.count to include total item count
        return Response({
            "count": self.page.paginator.count,
            "page": self.page.number,
            "page_size": self.get_page_size(self.request),
            "num_pages": self.page.paginator.num_pages,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })
