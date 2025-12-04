import uuid

from PyPDF2 import PdfReader
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.global_constants import SuccessMessage, ErrorMessage
from app.goal.rag_store import add_document
from app.utils import get_response_schema
from permissions import IsUser


class DocumentIngestApiView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]

    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'document',
                openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description='Upload a PDF file',
                required=True
            ),
        ]
    )
    def post(self, request):

        if 'document' not in request.FILES:
            return Response(
                {"error": ErrorMessage.BAD_REQUEST.value},
                status=status.HTTP_400_BAD_REQUEST
            )

        pdf_file = request.FILES['document']

        try:
            # ---- Read PDF content ----
            reader = PdfReader(pdf_file)
            text_content = ""

            for page in reader.pages:
                text_content += page.extract_text() or ""

            if len(text_content.strip()) == 0:
                return Response(
                    {"error": "No readable text found in PDF"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ---- Store into ChromaDB ----
            doc_id = str(uuid.uuid4())  # unique ID for this doc
            add_document(doc_id, text_content)

            return get_response_schema({}, SuccessMessage.RECORD_CREATED.value, status.HTTP_201_CREATED)
        except Exception as e:

            return get_response_schema(
                {settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: [str(e)]},
                ErrorMessage.SOMETHING_WENT_WRONG.value,
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
