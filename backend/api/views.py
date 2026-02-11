import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Dataset
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.http import FileResponse


@api_view(["POST"])
@permission_classes([AllowAny])
def upload_csv(request):
    if "file" not in request.FILES:
        return Response({"error": "No file uploaded"}, status=400)

    file = request.FILES["file"]

    # Read CSV using pandas
    df = pd.read_csv(file)

    summary = {
        "total_equipment": int(len(df)),
        "avg_flowrate": float(df["Flowrate"].mean()),
        "avg_pressure": float(df["Pressure"].mean()),
        "avg_temperature": float(df["Temperature"].mean()),
        "type_distribution": df["Type"].value_counts().to_dict(),
    }

    # Save dataset summary
    Dataset.objects.create(
        name=file.name,
        file=file,
        summary=summary
    )

    # Keep only last 5 datasets
    if Dataset.objects.count() > 5:
        Dataset.objects.order_by("uploaded_at").first().delete()

    return Response(summary)

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .models import Dataset

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dataset_history(request):
    datasets = Dataset.objects.order_by("-uploaded_at")[:5]
    data = []
    for d in datasets:
        data.append({
        "id": d.id,
        "name": d.name,
        "uploaded_at": d.uploaded_at,
        "summary": d.summary
        })

    return Response(data)

    datasets = Dataset.objects.order_by("-uploaded_at")[:5]

    data = []
    for d in datasets:
        data.append({
            "name": d.name,
            "uploaded_at": d.uploaded_at,
            "summary": d.summary
        })

    return Response(data)




@api_view(["GET"])
@permission_classes([AllowAny])
def dataset_pdf(request, dataset_id):
    import pandas as pd
    from reportlab.platypus import PageBreak

    dataset = Dataset.objects.get(id=dataset_id)
    df = pd.read_csv(dataset.file.path)
    summary = dataset.summary

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    # ===== TITLE =====
    story.append(Paragraph("Chemical Equipment Dataset Report", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"<b>Dataset Name:</b> {dataset.name}", styles["Normal"]))
    story.append(Paragraph(f"<b>Uploaded At:</b> {dataset.uploaded_at}", styles["Normal"]))
    story.append(Spacer(1, 20))

    # ===== SUMMARY =====
    story.append(Paragraph("Summary Statistics", styles["Heading2"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph(f"Total Equipment: {summary['total_equipment']}", styles["Normal"]))
    story.append(Paragraph(f"Average Flowrate: {summary['avg_flowrate']:.2f}", styles["Normal"]))
    story.append(Paragraph(f"Average Pressure: {summary['avg_pressure']:.2f}", styles["Normal"]))
    story.append(Paragraph(f"Average Temperature: {summary['avg_temperature']:.2f}", styles["Normal"]))
    story.append(Spacer(1, 20))

    # ===== CHART 1: TYPE DISTRIBUTION =====
    type_dist = summary["type_distribution"]

    plt.figure(figsize=(5, 3))
    plt.bar(type_dist.keys(), type_dist.values())
    plt.title("Equipment Type Distribution")
    plt.xticks(rotation=30)

    img1 = BytesIO()
    plt.tight_layout()
    plt.savefig(img1, format="png")
    plt.close()
    img1.seek(0)

    story.append(Paragraph("Equipment Type Distribution", styles["Heading3"]))
    story.append(Spacer(1, 8))
    story.append(Image(img1, width=360, height=220))

    # ===== FORCE NEW PAGE =====
    story.append(PageBreak())

    # ===== CHART 2: AVG FLOWRATE =====
    flowrates = {
        eq: df[df["Type"] == eq]["Flowrate"].mean()
        for eq in type_dist.keys()
    }

    plt.figure(figsize=(5, 3))
    plt.bar(flowrates.keys(), flowrates.values())
    plt.title("Average Flowrate by Equipment Type")
    plt.xticks(rotation=30)

    img2 = BytesIO()
    plt.tight_layout()
    plt.savefig(img2, format="png")
    plt.close()
    img2.seek(0)

    story.append(Paragraph("Average Flowrate by Equipment Type", styles["Heading3"]))
    story.append(Spacer(1, 8))
    story.append(Image(img2, width=360, height=220))
    story.append(Spacer(1, 20))

    # ===== CHART 3: PRESSURE VS TEMPERATURE =====
    plt.figure(figsize=(5, 3))
    plt.scatter(df["Pressure"], df["Temperature"])
    plt.xlabel("Pressure")
    plt.ylabel("Temperature")
    plt.title("Pressure vs Temperature")

    img3 = BytesIO()
    plt.tight_layout()
    plt.savefig(img3, format="png")
    plt.close()
    img3.seek(0)

    story.append(Paragraph("Pressure vs Temperature", styles["Heading3"]))
    story.append(Spacer(1, 8))
    story.append(Image(img3, width=360, height=220))

    # ===== BUILD PDF =====
    doc.build(story)
    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename=f"report_{dataset.id}.pdf",
    )
