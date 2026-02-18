from fpdf import FPDF
import os
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'NirikshaX Digital Forensic Scan Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(scan_data, output_path="scan_report.pdf"):
    """Generates a detailed PDF report from scan results."""
    try:
        pdf = PDFReport()
        pdf.add_page()
        
        # Title Info
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Scan Target: {scan_data.get('scan_target') or 'Unknown'}", 0, 1)
        pdf.cell(0, 10, f"Timestamp: {scan_data.get('timestamp') or str(datetime.now())}", 0, 1)
        pdf.ln(5)
        
        # Statistics
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(0, 10, "Scan Statistics", 0, 1, 'L', True)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, f"Total Files Scanned: {scan_data.get('files_found', 0)}", 0, 1)
        
        suspicious_list = scan_data.get('suspicious_files', [])
        suspicious_count = len(suspicious_list)
        
        if suspicious_count > 0:
             pdf.set_text_color(255, 0, 0)
        pdf.cell(0, 10, f"Suspicious Files Detected: {suspicious_count}", 0, 1)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)
        
        # Suspicious Files Section
        if suspicious_count > 0:
            pdf.set_font("Arial", "B", 12)
            pdf.set_fill_color(255, 200, 200)
            pdf.cell(0, 10, "Suspicious Files Detected", 0, 1, 'L', True)
            pdf.set_font("Arial", size=10)
            
            for item in suspicious_list:
                pdf.ln(2)
                pdf.set_font("Arial", "B", 10)
                pdf.cell(0, 6, f"File: {os.path.basename(item['path'])}", 0, 1)
                pdf.set_font("Arial", size=9)
                pdf.cell(0, 6, f"Path: {item['path']}", 0, 1)
                pdf.set_text_color(200, 0, 0)
                pdf.cell(0, 6, f"Reason: {item.get('reason') or 'Unknown'}", 0, 1)
                pdf.set_text_color(0, 0, 0)
                pdf.ln(2)
        else:
            pdf.set_font("Arial", "I", 10)
            pdf.cell(0, 10, "No suspicious files detected.", 0, 1)
            
        pdf.ln(5)
        
        # Full File List
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, "File Inventory (First 100)", 0, 1, 'L', True)
        pdf.set_font("Arial", size=8)
        
        # Header
        pdf.cell(90, 8, "Filename", 1, 0, 'C', True)
        pdf.cell(30, 8, "Type", 1, 0, 'C', True)
        pdf.cell(70, 8, "Hash Snippet", 1, 1, 'C', True)
        
        # Limit to 100 files for brevity in the report, or paginate properly. 
        # For now, let's just do up to 200 items to avoid making the PDF huge if scanning C:\
        all_files = scan_data.get('all_files', [])
        limit = 200
        
        for i, item in enumerate(all_files):
            if i >= limit:
                pdf.cell(0, 8, f"... and {len(all_files) - limit} more files.", 0, 1, 'C')
                break
                
            filename = os.path.basename(item['path'])
            if len(filename) > 40:
                filename = filename[:37] + "..."
                
            file_type = item.get('extension_detected') or "Unknown"
            
            file_hash = item.get('hash_sha256')
            if file_hash:
                file_hash = file_hash[:12] + "..." 
            else:
                file_hash = "-"
                
            pdf.cell(90, 8, str(filename), 1)
            pdf.cell(30, 8, str(file_type), 1)
            pdf.cell(70, 8, str(file_hash), 1)
            pdf.ln()

        pdf.output(output_path)
        return True
    except Exception as e:
        print(f"Report Generation Error: {e}")
        return False
