from rest_framework.pagination import PageNumberPagination


class SmallPagesPaginator(PageNumberPagination):
    page_size = 5


