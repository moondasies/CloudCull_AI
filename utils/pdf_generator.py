from fpdf import FPDF
import io

class CloudCullPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(14, 165, 233)  # #0EA5E9
        self.cell(0, 10, 'CloudCull AI - TechVista Solutions Executive Report', border=False, align='C')
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(169, 169, 169)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf_report(df):
    pdf = CloudCullPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    
    # Title
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(200, 10, txt="Monthly SaaS Spend Optimization Summary", ln=True, align='L')
    pdf.ln(5)
    
    # Key Stats
    pdf.set_font("helvetica", "B", 12)
    total_spend = df["Monthly Cost (\u20b9)"].sum()
    savings = df["Potential Savings (\u20b9)"].sum()
    pdf.cell(0, 10, txt=f"Total Monthly SaaS Spend: INR {total_spend:,.0f}", ln=True)
    pdf.set_text_color(239, 68, 68)  # #EF4444
    pdf.cell(0, 10, txt=f"Potential Savings Identified: INR {savings:,.0f}", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    
    # Table Header
    pdf.set_font("helvetica", "B", 10)
    pdf.set_fill_color(243, 244, 246)
    pdf.cell(60, 10, "Tool Name", border=1, fill=True)
    pdf.cell(40, 10, "Dept", border=1, fill=True)
    pdf.cell(40, 10, "Cost (INR)", border=1, fill=True)
    pdf.cell(50, 10, "Inactive Seats", border=1, fill=True)
    pdf.ln()
    
    # Table Rows
    pdf.set_font("helvetica", size=10)
    for _, row in df.head(15).iterrows():
        pdf.cell(60, 8, str(row["Tool Name"]), border=1)
        pdf.cell(40, 8, str(row["Department"]), border=1)
        pdf.cell(40, 8, f"{row['Monthly Cost (\u20b9)']:,.0f}", border=1)
        pdf.cell(50, 8, f"{row['Inactive Seats']}", border=1)
        pdf.ln()
        
    pdf.ln(15)
    pdf.set_font("helvetica", "I", 10)
    pdf.cell(0, 10, txt="Report generated automatically by CloudCull AI Engine.", ln=True, align='C')
    
    # Output to bytes
    pdf_output = pdf.output(dest='S')
    return pdf_output
