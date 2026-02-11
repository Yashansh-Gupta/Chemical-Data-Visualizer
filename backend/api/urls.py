from django.urls import path
from .views import upload_csv, dataset_history, dataset_pdf
from . import views

urlpatterns = [
    path("upload/", upload_csv),
    path("history/", dataset_history),
    path("report/<int:dataset_id>/", dataset_pdf),
    path("report/<int:dataset_id>/", views.dataset_pdf),

]