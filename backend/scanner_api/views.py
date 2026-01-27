import tempfile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .run_scan import run_scan


@api_view(['POST'])
def scan_dependencies(request):
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        for chunk in file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    result = run_scan(tmp_path, max_depth=2)

    return Response(result)
