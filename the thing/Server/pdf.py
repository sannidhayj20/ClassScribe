from fpdf import FPDF

def generate_pdf(output):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size = 15)
    
    pdf.cell(200, 10, txt = "StudyBuddy.ai",
            ln = 1, align = 'C')
    
    pdf.cell(200, 10, txt = "Generated Summary.",
            ln = 2, align = 'C')
    
    pdf.cell(200, 10, txt = str(output),
            ln = 4, align = 'L')
    
    pdf.output("model\outputs\summary.pdf")  
