from asgiref.sync import async_to_sync
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Matrix
from .serializers import MatrixSerializer
from .utils_library import get_matrix, start_matrix_data


class MatrixTraversalView(APIView):
    """
   This class defines the Matrix Traversal API endpoint.
   """

    def post(self, request):
        """
        Endpoint for handling POST requests.
        Processes the request data and creates a Matrix object.
        """
        # Extract the 'url' from the request data
        url = request.data.get('url')
        if not url:
            return Response({"error": "source_url is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the matrix data asynchronously
            travers_matrix = async_to_sync(get_matrix)(url)
            # Start processing the matrix data
            start_data = start_matrix_data(url)
            # Create a Matrix object with the processed data
            matrix_obj = Matrix.objects.create(start_matrix=start_data, matrix_data=travers_matrix)
            # Serialize the Matrix object
            serializer = MatrixSerializer(matrix_obj)
            return Response({'data': travers_matrix}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
