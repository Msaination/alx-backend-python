from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    # ✅ Default page size
    page_size = 20
    # Allow clients to override with ?page_size= query param
    page_size_query_param = 'page_size'
    # Maximum allowed page size
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Custom paginated response including count, total pages, current page, next/previous links, and results.
        """
        return Response({
            'count': self.page.paginator.count,              # ✅ total number of messages
            'total_pages': self.page.paginator.num_pages,    # ✅ total pages available
            'current_page': self.page.number,                # ✅ current page number
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })