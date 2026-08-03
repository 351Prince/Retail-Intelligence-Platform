import os
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from src.utils.database import get_data

st.set_page_config(page_title="Export Report", layout="wide")

st.title("📄 Export Executive Report")

df = get_data()

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
profit_margin = (total_profit / total_sales) * 100

best_product = df.groupby("Product")["Sales"].sum().idxmax()
best_region = df.groupby("Region")["Sales"].sum().idxmax()
best_category = df.groupby("Category")["Profit"].sum().idxmax()

st.metric("Revenue", f"${total_sales:,.0f}")
st.metric("Profit", f"${total_profit:,.0f}")
st.metric("Profit Margin", f"{profit_margin:.2f}%")

st.write("### Report Preview")

st.markdown(f"""
- **Total Revenue:** ${total_sales:,.2f}
- **Total Profit:** ${total_profit:,.2f}
- **Profit Margin:** {profit_margin:.2f}%
- **Best Product:** {best_product}
- **Best Region:** {best_region}
- **Best Category:** {best_category}
""")

def build_pdf():
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(tmp.name)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Retail Intelligence Platform</b>", styles["Title"]))
    story.append(Paragraph("Executive Business Report", styles["Heading2"]))

    story.append(Paragraph(f"Total Revenue: ${total_sales:,.2f}", styles["BodyText"]))
    story.append(Paragraph(f"Total Profit: ${total_profit:,.2f}", styles["BodyText"]))
    story.append(Paragraph(f"Profit Margin: {profit_margin:.2f}%", styles["BodyText"]))
    story.append(Paragraph(f"Best Product: {best_product}", styles["BodyText"]))
    story.append(Paragraph(f"Best Region: {best_region}", styles["BodyText"]))
    story.append(Paragraph(f"Best Category: {best_category}", styles["BodyText"]))

    story.append(Paragraph("<br/><b>AI Recommendations</b>", styles["Heading2"]))
    story.append(Paragraph("• Increase inventory for best-selling products.", styles["BodyText"]))
    story.append(Paragraph("• Improve sales in low-performing regions.", styles["BodyText"]))
    story.append(Paragraph("• Focus marketing on high-profit categories.", styles["BodyText"]))
    story.append(Paragraph("• Monitor monthly sales trend regularly.", styles["BodyText"]))

    doc.build(story)

    return tmp.name

if st.button("📥 Generate PDF Report"):
    pdf_path = build_pdf()

    with open(pdf_path, "rb") as f:
        st.download_button(
            "⬇ Download PDF",
            data=f,
            file_name="Retail_Executive_Report.pdf",
            mime="application/pdf"
        )
