"""
Enterprise File Conversion Services
Supports PDF, Word, Excel, PowerPoint, and image conversions
Optimized for performance with proper error handling
"""

import os
import logging
import subprocess
import tempfile
from pathlib import Path
from PIL import Image
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from PyPDF2 import PdfReader, PdfWriter
from pdf2docx import Converter
import time

try:
    from config.exceptions import ConversionError
except ImportError:
    class ConversionError(Exception):
        pass

logger = logging.getLogger(__name__)


class FileConversionService:
    """
    Enterprise-grade file conversion service
    Supports: PDF, Word, Excel, PowerPoint, Images
    Performance target: 10MB file in < 30 seconds
    """
    
    # Performance tracking
    MAX_CONVERSION_TIME = 30  # seconds for 10MB file
    
    def pdf_to_word(self, input_path, output_path):
        """
        Convert PDF to Word (DOCX) with formatting preservation
        Requirement 2: PDF to Word Conversion
        """
        start_time = time.time()
        try:
            logger.info(f"Converting PDF to Word: {input_path}")
            
            # Check if PDF is scanned (no text)
            reader = PdfReader(input_path)
            has_text = False
            for page in reader.pages:
                text = page.extract_text().strip()
                if text:
                    has_text = True
                    break
            
            if not has_text:
                raise ConversionError("PDF contains scanned images without text. OCR is required.")
            
            # Convert using pdf2docx
            cv = Converter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
            
            # Preserve metadata
            self._preserve_metadata(input_path, output_path)
            
            elapsed = time.time() - start_time
            logger.info(f"PDF to Word conversion completed in {elapsed:.2f}s: {output_path}")
            
            return {
                'success': True,
                'output_path': output_path,
                'conversion_time': elapsed,
                'file_size': os.path.getsize(output_path)
            }
            
        except Exception as e:
            logger.exception(f"PDF to Word conversion failed: {str(e)}")
            raise ConversionError(f"PDF to Word conversion failed: {str(e)}")
    
    def word_to_pdf(self, input_path, output_path):
        """
        Convert Word document to PDF with formatting preservation
        Requirement 3: Word to PDF Conversion
        Supports DOC and DOCX formats
        """
        start_time = time.time()
        try:
            logger.info(f"Converting Word to PDF: {input_path}")
            
            # Try LibreOffice first (best quality)
            if self._has_libreoffice():
                self._convert_with_libreoffice(input_path, output_path)
            else:
                # Fallback to python-docx + reportlab
                self._word_to_pdf_fallback(input_path, output_path)
            
            # Preserve metadata
            self._preserve_metadata(input_path, output_path)
            
            elapsed = time.time() - start_time
            logger.info(f"Word to PDF conversion completed in {elapsed:.2f}s: {output_path}")
            
            return {
                'success': True,
                'output_path': output_path,
                'conversion_time': elapsed,
                'file_size': os.path.getsize(output_path)
            }
            
        except Exception as e:
            logger.exception(f"Word to PDF conversion failed: {str(e)}")
            raise ConversionError(f"Word to PDF conversion failed: {str(e)}")
    
    def _word_to_pdf_fallback(self, input_path, output_path):
        """Fallback Word to PDF conversion using python-docx"""
        doc = Document(input_path)
        
        # Create PDF with proper formatting
        pdf = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        for para in doc.paragraphs:
            if para.text.strip():
                p = Paragraph(para.text, styles['Normal'])
                story.append(p)
                story.append(Spacer(1, 0.2*inch))
        
        pdf.build(story)
    
    def pdf_to_images(self, input_path, output_dir, dpi=150, format='jpg'):
        """
        Convert PDF pages to images
        Requirement 7: PDF to JPG conversion with configurable DPI
        Supports DPI: 72, 150, 300
        """
        start_time = time.time()
        try:
            logger.info(f"Converting PDF to images: {input_path} at {dpi} DPI")
            
            from pdf2image import convert_from_path
            
            # Convert all pages
            images = convert_from_path(input_path, dpi=dpi)
            
            output_files = []
            os.makedirs(output_dir, exist_ok=True)
            
            for i, image in enumerate(images, start=1):
                output_file = os.path.join(output_dir, f"page_{i}.{format}")
                
                # Convert to RGB if needed
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                image.save(output_file, format.upper(), quality=95)
                output_files.append(output_file)
            
            elapsed = time.time() - start_time
            logger.info(f"PDF to images conversion completed in {elapsed:.2f}s: {len(output_files)} pages")
            
            return {
                'success': True,
                'output_files': output_files,
                'page_count': len(output_files),
                'conversion_time': elapsed
            }
            
        except Exception as e:
            logger.exception(f"PDF to images conversion failed: {str(e)}")
            raise ConversionError(f"PDF to images conversion failed: {str(e)}")
    
    def excel_to_pdf(self, input_path, output_path):
        """
        Convert Excel (XLSX, XLS) to PDF
        Requirement 7: Excel to PDF conversion
        """
        start_time = time.time()
        try:
            logger.info(f"Converting Excel to PDF: {input_path}")
            
            if self._has_libreoffice():
                self._convert_with_libreoffice(input_path, output_path)
            else:
                raise ConversionError("Excel to PDF conversion requires LibreOffice")
            
            elapsed = time.time() - start_time
            logger.info(f"Excel to PDF conversion completed in {elapsed:.2f}s: {output_path}")
            
            return {
                'success': True,
                'output_path': output_path,
                'conversion_time': elapsed
            }
            
        except Exception as e:
            logger.exception(f"Excel to PDF conversion failed: {str(e)}")
            raise ConversionError(f"Excel to PDF conversion failed: {str(e)}")
    
    def powerpoint_to_pdf(self, input_path, output_path):
        """
        Convert PowerPoint (PPTX, PPT) to PDF
        Requirement 7: PowerPoint to PDF conversion
        """
        start_time = time.time()
        try:
            logger.info(f"Converting PowerPoint to PDF: {input_path}")
            
            if self._has_libreoffice():
                self._convert_with_libreoffice(input_path, output_path)
            else:
                raise ConversionError("PowerPoint to PDF conversion requires LibreOffice")
            
            elapsed = time.time() - start_time
            logger.info(f"PowerPoint to PDF conversion completed in {elapsed:.2f}s: {output_path}")
            
            return {
                'success': True,
                'output_path': output_path,
                'conversion_time': elapsed
            }
            
        except Exception as e:
            logger.exception(f"PowerPoint to PDF conversion failed: {str(e)}")
            raise ConversionError(f"PowerPoint to PDF conversion failed: {str(e)}")
    
    def text_to_pdf(self, input_path, output_path, font='Helvetica', font_size=12):
        """
        Convert text file to PDF
        Requirement 7: TXT to PDF with configurable font and size
        """
        start_time = time.time()
        try:
            logger.info(f"Converting text to PDF: {input_path}")
            
            with open(input_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            # Create PDF
            pdf = SimpleDocTemplate(output_path, pagesize=letter)
            styles = getSampleStyleSheet()
            style = styles['Normal']
            style.fontName = font
            style.fontSize = font_size
            
            story = []
            for line in text_content.split('\n'):
                if line.strip():
                    p = Paragraph(line, style)
                    story.append(p)
                else:
                    story.append(Spacer(1, 0.2*inch))
            
            pdf.build(story)
            
            elapsed = time.time() - start_time
            logger.info(f"Text to PDF conversion completed in {elapsed:.2f}s: {output_path}")
            
            return {
                'success': True,
                'output_path': output_path,
                'conversion_time': elapsed
            }
            
        except Exception as e:
            logger.exception(f"Text to PDF conversion failed: {str(e)}")
            raise ConversionError(f"Text to PDF conversion failed: {str(e)}")
    
    def image_to_pdf(self, input_path, output_path):
        """Convert image to PDF using Pillow."""
        start_time = time.time()
        try:
            logger.info(f"Converting image to PDF: {input_path}")
            
            # Open and convert image
            img = Image.open(input_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save as PDF
            img.save(output_path, 'PDF', resolution=100.0)
            
            elapsed = time.time() - start_time
            logger.info(f"Image to PDF conversion completed in {elapsed:.2f}s: {output_path}")
            
            return {
                'success': True,
                'output_path': output_path,
                'conversion_time': elapsed
            }
            
        except Exception as e:
            logger.exception(f"Image to PDF conversion failed: {str(e)}")
            raise ConversionError(f"Image to PDF conversion failed: {str(e)}")
    
    def pdf_to_text(self, input_path, output_path):
        """Extract text from PDF."""
        start_time = time.time()
        try:
            logger.info(f"Extracting text from PDF: {input_path}")
            
            reader = PdfReader(input_path)
            text_content = []
            
            for page in reader.pages:
                text_content.append(page.extract_text())
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(text_content))
            
            elapsed = time.time() - start_time
            logger.info(f"PDF to text extraction completed in {elapsed:.2f}s: {output_path}")
            
            return {
                'success': True,
                'output_path': output_path,
                'conversion_time': elapsed
            }
            
        except Exception as e:
            logger.exception(f"PDF to text extraction failed: {str(e)}")
            raise ConversionError(f"PDF to text extraction failed: {str(e)}")
    
    # Helper methods
    
    def _has_libreoffice(self):
        """Check if LibreOffice is installed"""
        try:
            result = subprocess.run(['libreoffice', '--version'], 
                                  capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def _convert_with_libreoffice(self, input_path, output_path):
        """Convert document using LibreOffice"""
        output_dir = os.path.dirname(output_path)
        
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        
        if result.returncode != 0:
            raise ConversionError(f"LibreOffice conversion failed: {result.stderr.decode()}")
        
        # LibreOffice creates file with same name but .pdf extension
        temp_output = os.path.join(output_dir, 
                                   Path(input_path).stem + '.pdf')
        
        if os.path.exists(temp_output) and temp_output != output_path:
            os.rename(temp_output, output_path)
    
    def _preserve_metadata(self, input_path, output_path):
        """Preserve document metadata during conversion"""
        try:
            # Extract metadata from input
            if input_path.endswith('.pdf'):
                reader = PdfReader(input_path)
                metadata = reader.metadata
                
                # Apply to output if it's also PDF
                if output_path.endswith('.pdf'):
                    writer = PdfWriter()
                    with open(output_path, 'rb') as f:
                        reader_out = PdfReader(f)
                        for page in reader_out.pages:
                            writer.add_page(page)
                    
                    if metadata:
                        writer.add_metadata(metadata)
                    
                    with open(output_path, 'wb') as f:
                        writer.write(f)
        except Exception as e:
            logger.warning(f"Could not preserve metadata: {str(e)}")
