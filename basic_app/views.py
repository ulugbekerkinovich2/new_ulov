from django.db.models import Count, Sum, Max
from django.db.models.functions import ExtractMonth
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from basic_app.models import Mark
from . import models
from . import serializers


class PageNumberPagination(PageNumberPagination):
    page_size = 2


class DataPagination(PageNumberPagination):
    page_size = 50


class Limitoffset(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10


# Create your views here.
class ListFile(generics.ListCreateAPIView):
    queryset = models.Upload_File.objects.all().order_by('-id')
    serializer_class = serializers.UploadFileSerializer
    pagination_class = PageNumberPagination


class ListFile2(generics.ListCreateAPIView):
    queryset = models.Upload_File2.objects.all().order_by('-id')
    serializer_class = serializers.UploadFile2Serializer
    pagination_class = PageNumberPagination


# class ListMark(generics.ListAPIView):
#     queryset = models.Mark.objects.annotate(count_from_that_model=Count('models'))
#     serializer_class = serializers.MarkSerializer
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#
#         # Serialize the queryset data for each mark
#         data = [
#             {
#                 'mark_name': mark.mark_name,
#                 'count_from_that_model': mark.count_from_that_model
#             }
#             for mark in queryset
#         ]
#
#         reponse_data = {
#             'data': data,
#             'total_count': queryset.count()
#         }
#         return Response(reponse_data)

class ListMark(generics.ListAPIView):
    queryset = Mark.objects.annotate(count_from_that_model=Count('models', distinct=True))
    serializer_class = serializers.MarkSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['mark_name']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Serialize the queryset data for each mark
        data = []
        for mark in queryset:
            mark_data = {
                'mark_name': mark.mark_name,
                'model_count': queryset.count(),
                'count_from_that_model': mark.count_from_that_model,
            }
            data.append(mark_data)

        reponse_data = {
            'data': data,
            # 'total_count': queryset.count()
        }
        return Response(reponse_data)


class ListMarks22(generics.ListAPIView):
    queryset = Mark.objects.annotate(count_of_unique_models=Count('data22__model', distinct=True))
    serializer_class = serializers.Mark22Serializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # Calculate the overall count of unique models
        overall_count = sum(item['count_of_unique_models'] for item in serializer.data)

        # Create the final response data
        data = {
            'all_count': overall_count,
            'marks': serializer.data,
        }
        return Response(data)


class ListModel22(generics.ListAPIView):
    serializer_class = serializers.ModelCountSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['mark__mark_name']

    def get_queryset(self):
        queryset = models.DATA21.objects.select_related('model', 'mark')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Retrieve the mark name from the search filter if provided
        mark_name = request.query_params.get('mark__mark_name', None)

        if mark_name:
            # Filter the queryset by the provided mark name
            queryset = queryset.filter(mark__mark_name=mark_name)

        # Annotate the queryset with the count of models for each mark
        queryset = queryset.values('model__model_name').annotate(count_of_models=Count('model__model_name'))

        return Response(queryset)


class ListModel21(generics.ListAPIView):
    serializer_class = serializers.ModelCountSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['mark__mark_name']

    def get_queryset(self):
        queryset = models.DATA22.objects.select_related('model', 'mark')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Retrieve the mark name from the search filter if provided
        mark_name = request.query_params.get('mark__mark_name', None)

        if mark_name:
            # Filter the queryset by the provided mark name
            queryset = queryset.filter(mark__mark_name=mark_name)

        # Annotate the queryset with the count of models for each mark
        queryset = queryset.values('model__model_name').annotate(count_of_models=Count('model__model_name'))

        return Response(queryset)


class ListMarks21(generics.ListAPIView):
    queryset = Mark.objects.annotate(count_of_unique_models=Count('data21__model', distinct=True))
    serializer_class = serializers.Mark21Serializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Calculate the overall count of unique models
        overall_count = sum(item['count_of_unique_models'] for item in serializer.data)

        # Create the final response data
        data = {
            'all_count': overall_count,
            'marks': serializer.data,
        }
        return Response(data)


class ListModel1(generics.ListAPIView):
    queryset = models.Model1.objects.all()
    serializer_class = serializers.ModelSerializer
    # pagination_class = Limitoffset
    filter_backends = [filters.SearchFilter]
    search_fields = ['mark_id.mark_name']


class ListData21(generics.ListAPIView):
    queryset = models.DATA21.objects.all()
    serializer_class = serializers.Data21Serializer
    pagination_class = DataPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['sana']
    # pagination_class = Limitoffset


class ListData22(generics.ListAPIView):
    queryset = models.DATA22.objects.all()
    serializer_class = serializers.Data22Serializer
    pagination_class = DataPagination
    # pagination_class = Limitoffset
    filter_backends = [filters.SearchFilter]
    search_fields = ['sana', 'country', 'model__model_name', 'mark__mark_name']


class ListData21Statistics(generics.ListAPIView):
    serializer_class = serializers.Data21Serializer
    pagination_class = DataPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['mark__mark_name']

    def get_queryset(self):
        # Get the latest file_id
        latest_file_id = models.DATA21.objects.aggregate(latest_file_id=Max('file_id'))['latest_file_id']

        # Annotate the queryset to get the count of models for each mark
        queryset = models.DATA21.objects.filter(file_id_id=latest_file_id).values('model__model_name', 'mark').annotate(
            count_from_that_model=Count('model')).order_by('mark')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count_all_data = queryset.aggregate(total_count=Sum('count_from_that_model'))['total_count']

        # Create the response data in the desired format
        data = [
            {
                'model_name': item['model__model_name'],
                'mark_name': item['mark'],
                'count_from_that_model': item['count_from_that_model']
            }
            for item in queryset
        ]

        # Add the total count to the response data
        response_data = {
            'data': data,
            'total_count': count_all_data
        }
        return Response(response_data)


# class ListData22Statistics(generics.ListAPIView):
#     serializer_class = serializers.Data22Serializer
#     pagination_class = DataPagination
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['mark__mark_name']
#
#     def get_queryset(self):
#         # Annotate the queryset to get the count of models for each mark
#         queryset = models.DATA22.objects.values('model__model_name', 'mark').annotate(
#             count_from_that_model=Count('model')).order_by('mark')
#
#         return queryset
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         count_all_data = queryset.aggregate(total_count=Sum('count_from_that_model'))['total_count']
#
#         # Create the response data in the desired format
#         data = [
#             {
#                 'model_name': item['model__model_name'],
#                 'mark_name': item['mark'],
#                 'count_from_that_model': item['count_from_that_model']
#             }
#             for item in queryset
#         ]
#
#         # Add the total count to the response data
#         response_data = {
#             'data': data,
#             'total_count': count_all_data
#         }
#         return Response(response_data)

class ListData22Statistics(generics.ListAPIView):
    serializer_class = serializers.Data22Serializer
    pagination_class = DataPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['mark__mark_name']

    def get_queryset(self):
        # Get the latest file_id
        latest_file_id = models.DATA22.objects.aggregate(latest_file_id=Max('file_id'))['latest_file_id']

        # Annotate the queryset to get the count of models for each mark
        queryset = models.DATA22.objects.filter(file_id_id=latest_file_id).values('model__model_name', 'mark').annotate(
            count_from_that_model=Count('model')).order_by('mark')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count_all_data = queryset.aggregate(total_count=Sum('count_from_that_model'))['total_count']

        data = [
            {
                'model_name': item['model__model_name'],
                'mark_name': item['mark'],
                'count_from_that_model': item['count_from_that_model']
            }
            for item in queryset
        ]

        # Add the total count to the response data
        response_data = {
            'data': data,
            'total_count': count_all_data
        }
        return Response(response_data)


class DailyModel21CountView(APIView):
    def get(self, request):
        # Get the last added file_id from the DATA21 model
        last_file_id = models.DATA21.objects.aggregate(last_file_id=Max('file_id'))['last_file_id']

        # Filter DATA21 objects by the last added file_id
        data21_query = models.DATA21.objects.filter(file_id=last_file_id).annotate(month=ExtractMonth('sana'))
        data21_query = data21_query.values('month').annotate(count_of_models=Count('id'))

        # Create the response data with month and the count of models
        serializer = serializers.MonthlyModelCountSerializer(data21_query, many=True)
        return Response(serializer.data)


class DailyModel22CountView(APIView):
    def get(self, request):
        # Get the last added file_id from the DATA21 model
        last_file_id = models.DATA22.objects.aggregate(last_file_id=Max('file_id'))['last_file_id']

        # Filter DATA21 objects by the last added file_id
        data22_query = models.DATA22.objects.filter(file_id=last_file_id).annotate(month=ExtractMonth('sana'))
        data22_query = data22_query.values('month').annotate(count_of_models=Count('id'))

        # Create the response data with month and the count of models
        serializer = serializers.MonthlyModelCountSerializer(data22_query, many=True)
        return Response(serializer.data)
