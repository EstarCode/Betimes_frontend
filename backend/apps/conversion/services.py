"""
File conversion services.
"""

import os
import logging
from PIL import Image
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader
from config.exceptions import ConversionError

logger = logging.getLogger(__name__)


class FileConversionService:
    """Service class for file conversion operations."""
    
    def word_to_pdf(self, input_path, output_path):
        """Convert Word document to PDF."""
        try:
            logger.info(f"Converting Word to PDF: {input_path}")
            
            # Read Word document
            doc = Document(input_path)
            
            # Create PDF
            c = canvas.Canvas(output_path, pagesize=letter)
            width, height = letter
            
            y_position = height - 50
            for para in doc.paragraphs:
                if y_position < 50:
                    c.showPage()
                    y_position = height - 50
                
                c.drawString(50, y_position, para.text[:100])
                y_position -= 20
            
            c.save()
            logger.info(f"Word to PDF conversion completed: {output_path}")
            
        except Exception as e:
            logger.exception(f"Word to PDF conversion failed: {str(e)}")
            raise ConversionError(f"Word to PDF conversion failed: {str(e)}")
    
    def image_to_pdf(self, input_path, output_path):
        """Convert image to PDF using Pillow."""
        try:
            logger.info(f"Converting image to PDF: {input_path}")
            
            # Open and convert image
            img = Image.open(input_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save as PDF
            img.save(output_path, 'PDF', resolution=100.0)
            
            logger.info(f"Image to PDF conversion completed: {output_path}")
            
        except Exception as e:
            logger.exception(f"Image to PDF conversion failed: {str(e)}")
            raise ConversionError(f"Image to PDF conversion failed: {str(e)}")

    
    def pdf_to_image(self, input_path, output_path):
        """Convert PDF to image (first page)."""
        try:
            logger.info(f"Converting PDF to image: {input_path}")
            
            # Note: Requires pdf2image library and poppler
            try:
                from pdf2image import convert_from_path
                images = convert_from_path(input_path, first_page=1, last_page=1)
                if images:
                    images[0].save(output_path, 'PNG')
            except ImportError:
                logger.warning("pdf2image not available")
                raise ConversionError("PDF to image conversion requires pdf2image library and poppler")
            
            logger.info(f"PDF to image conversion completed: {output_path}")
            
        except Exception as e:
            logger.exception(f"PDF to image conversion failed: {str(e)}")
            raise ConversionError(f"PDF to image conversion failed: {str(e)}")
    
    def pdf_to_text(self, input_path, output_path):
        """Extract text from PDF."""
        try:
            logger.info(f"Extracting text from PDF: {input_path}")
            
            reader = PdfReader(input_path)
            text_content = []
            
            for page in reader.pages:
                text_content.append(page.extract_text())
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(text_content))
            
            logger.info(f"PDF to text extraction completed: {output_path}")
            
        except Exception as e:
            logger.exception(f"PDF to text extraction failed: {str(e)}")
            raise ConversionError(f"PDF to text extraction failed: {str(e)}")
    
    def excel_to_pdf(self, input_path, output_path):
        """Convert Excel to PDF."""
        try:
            logger.info(f"Converting Excel to PDF: {input_path}")
            
            # Note: This requires LibreOffice or similar
            raise ConversionError("Excel to PDF conversion requires LibreOffice installation")
            
        except Exception as e:
            logger.exception(f"Excel to PDF conversion failed: {str(e)}")
            raise ConversionError(f"Excel to PDF conversion failed: {str(e)}")
    
    def ppt_to_pdf(self, input_path, output_path):
        """Convert PowerPoint to PDF."""
        try:
            logger.info(f"Converting PowerPoint to PDF: {input_path}")
            
            # Note: This requires LibreOffice or similar
            raise ConversionError("PowerPoint to PDF conversion requires LibreOffice installation")
            
        except Exception as e:
            logger.exception(f"PowerPoint to PDF conversion failed: {str(e)}")
            raise ConversionError(f"PowerPoint to PDF conversion failed: {str(e)}")
