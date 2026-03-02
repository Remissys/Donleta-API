from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login-view"),
    path("token/refresh/", views.RefreshTokenView.as_view(), name="refresh-token-view"),

    path('image/', views.ImageUploadView.as_view(), name='image-upload-view'),
    path('image/<str:file_id>/', views.ImageView.as_view(), name='image-view'),

    path('characters/', views.Characterview.as_view(), name='characters-view'),
    path('character/<str:id>/', views.CharacterSingleView.as_view(), name='character-single-view'),

    path('bosses/', views.Bossview.as_view(), name='bosses-view'),
    path('boss/<str:id>/', views.BossSingleView.as_view(), name='boss-single-view'),

    path('participants/', views.Participant.as_view(), name='participants-view'),
    path('participant/<str:participant_id>/', views.ParticipantSingleView.as_view(), name='participant-single-view'),

    path('times/', views.TimeView.as_view(), name='times-view'),
    path('time/<str:time_id>/', views.TimeSingleView.as_view(), name='time-single-view'),

    path('runs/', views.RunsView.as_view(), name='runs-view'),
    path('run/<str:id>/', views.RunsSingleView.as_view(), name='runs-single-view'),
    path('runs/daily/', views.DailyRunsView.as_view(), name='daily-runs-view'),
    path('runs/weekly/', views.WeeklyRunsView.as_view(), name='weekly-runs-view'),
    path('runs/monthly/', views.MonthlyRunsView.as_view(), name='monthly-runs-view'),
]