from django.urls import path

from .views import MatrixTraversalView

urlpatterns = [
    path('traverse/', MatrixTraversalView.as_view(), name='traverse'),
]
