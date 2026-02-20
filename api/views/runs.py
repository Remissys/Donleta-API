from rest_framework.views import APIView
from rest_framework import status
from ..services import RunService
from ..serializers import RunCreateSerializer, SingleRunSerializer, ScoresRunSerializer, WeeklyRunsSerializer, RunsSerializer
from django.http import JsonResponse

class RunsView(APIView):
    def post(self, request):
        try:   
            serializers = RunCreateSerializer(data=request.data)
            serializers.is_valid(raise_exception=True)

            RunService.create_run(serializers.validated_data)

            return JsonResponse({"status": True, "message": "Runs created successfully"}, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return JsonResponse({"status": False, "message": "Error creating runs"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RunsSingleView(APIView):
    def get(self, request, id: str):
        try:   
            run = RunService.get_run_by_id(id)

            serializers = SingleRunSerializer(run)

            return JsonResponse({"status": True, "message": "Runs retrieved successfully", "data": serializers.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"status": False, "message": "Error retrieving runs"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DailyRunsView(APIView):
    def get(self, request):
        try:   
            day = request.query_params.get("day")

            runs = RunService.get_daily_runs(day)

            serializers = RunsSerializer(runs)

            return JsonResponse({"status": True, "message": "Daily runs retrieved successfully", "data": serializers.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"status": False, "message": "Error retrieving daily runs"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class WeeklyRunsView(APIView):
    def get(self, request):
        try:
            edition = request.query_params.get("edition")
            week = request.query_params.get("week")

            runs = RunService.get_weekly_runs(edition, week)

            serializers = WeeklyRunsSerializer(runs, many=True)

            return JsonResponse({"status": True, "message": "Weekly runs retrieved successfully", "data": serializers.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"status": False, "message": "Error retrieving weekly runs"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class MonthlyRunsView(APIView):
    def get(self, request):
        try:
            edition = request.query_params.get("edition")

            runs = RunService.get_monthly_runs(edition)

            serializers = ScoresRunSerializer(runs, many=True)

            return JsonResponse({"status": True, "message": "Monthly runs retrieved successfully", "data": serializers.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"status": False, "message": "Error retrieving monthly runs"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)