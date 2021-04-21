from django.shortcuts import render
from rest_framework import pagination, status, mixins, viewsets, filters
from core import serializers as core_serializers
from core import models as core_models

# Create your views here.
class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 12
    page_size_query_param = 'per_page'
    max_page_size = 1000

class ListVideoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = LargeResultsSetPagination
    serializer_class = core_serializers.VideoSerializer
    paginate_by = 12
    search_fields = ['title', 'description']
    filter_backends = (filters.SearchFilter,)
    queryset = core_models.Video.objects.all().order_by('-published_at')

    def list(self, request):
        # Order: ASC: Ascending Order / DESC: Descinding Order
        sort_order_req = request.GET.get('order')
        if sort_order_req is None or sort_order_req is "" or (sort_order_req != "DESC" and sort_order_req != "ASC"):
            sort_order = '-published_at'
        elif sort_order_req == "DESC":
            sort_order = '-published_at'
        else:
            sort_order = 'published_at'

        queryset = self.filter_queryset(core_models.Video.objects.all().order_by(sort_order))

        page = request.GET.get('page')
        
        try:
            page = self.paginate_queryset(queryset)
        except Exception as e:
            page = []
            data = page
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": 'No more record.',
                "data": data
            })

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            return self.get_paginated_response(data)

        return Response({
            "status": status.HTTP_200_OK,
            "message": 'Screening Records.',
            "data": data
        })