import tempfile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .run_scan import run_scan
from .models import Scan, PackageRisk
from rest_framework.decorators import api_view


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

    # Count risks
    license_risks = sum(1 for p in result["packages"] if "LICENSE_RISK" in p["risks"])
    abandoned = sum(1 for p in result["packages"] if "ABANDONED_PACKAGE" in p["risks"])

    scan = Scan.objects.create(
        total_packages=result["total_packages"],
        license_risks=license_risks,
        abandoned_packages=abandoned
    )

    for pkg in result["packages"]:
        PackageRisk.objects.create(
            scan=scan,
            name=pkg["name"],
            license=pkg["license"],
            last_updated=pkg["last_updated"],
            risks=pkg["risks"]
        )

    return Response({
        "scan_id": scan.id,
        "total_packages": result["total_packages"],
        "license_risks": license_risks,
        "abandoned_packages": abandoned
    })

@api_view(['GET'])
def list_scans(request):
    scans = Scan.objects.all().order_by('-created_at')

    data = [
        {
            "id": s.id,
            "created_at": s.created_at,
            "total_packages": s.total_packages,
            "license_risks": s.license_risks,
            "abandoned_packages": s.abandoned_packages
        }
        for s in scans
    ]

    return Response(data)

@api_view(['GET'])
def scan_details(request, scan_id):
    packages = PackageRisk.objects.filter(scan_id=scan_id)

    data = [
        {
            "name": p.name,
            "license": p.license,
            "last_updated": p.last_updated,
            "risks": p.risks
        }
        for p in packages
    ]

    return Response(data)