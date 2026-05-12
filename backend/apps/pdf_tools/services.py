"""
Betimes - Enterprise PDF Processing Services
Complete PDF manipulation toolkit with international standards
"""

import os
import io
import logging
from typing import List, Dict, Tuple, Optional
from pathlib import Path

import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PIL import Image
import pdfplumber

from config.exceptions import PDFProcessingError

logger = logging.getLogger(__name__)


class PDFToolsService:
    """Enterprise-grade PDF processing service with all operations"""
    
    # ==================== PDF MERGING ====================
    
    def merge_pdfs(self, input_paths: List[str], output_path: str) -> Dict:
        """
        Merge multiple PDF files into one
        
        Args:
            input_paths: List of PDF file paths to merge
            output_path: Path for the merged PDF
            
        Returns:
            dict: Merge statistics
        """
        try:
            logger.info(f"Merging {len(input_paths)} PDF files")
            
            merger = PdfMerger()
            total_pages = 0
            
            for pdf_path in input_paths:
                if not os.path.exists(pdf_path):
                    raise PDFProcessingError(f"File not found: {pdf_path}")
                
                reader = PdfReader(pdf_path)
                total_pages += len(reader.pages)
                merger.append(pdf_path)
            
            merger.write(output_path)
            merger.close()
            
            logger.info(f"Successfully merged {len(input_paths)} files into {output_path}")
            
            return {
                'files_merged': len(input_paths),
                'total_pages': total_pages,
                'output_size': os.path.getsize(output_path)
            }
            
        except Exception as e:
            logger.exception(f"PDF merge failed: {str(e)}")
            raise PDFProcessingError(f"Failed to merge PDFs: {str(e)}")
    
    # ==================== PDF SPLITTING ====================
    
    def split_pdf_by_pages(self, input_path: str, output_dir: str, 
                          page_ranges: Optional[List[Tuple[int, int]]] = None) -> Dict:
        """
        Split PDF by page ranges
        
        Args:
            input_path: Input PDF path
            output_dir: Directory to save split PDFs
            page_ranges: List of (start, end) tuples. If None, splits into individual pages
            
        Returns:
            dict: Split statistics
        """
        try:
            logger.info(f"Splitting PDF: {input_path}")
            
            reader = PdfReader(input_path)
            total_pages = len(reader.pages)
            
            os.makedirs(output_dir, exist_ok=True)
            
            if page_ranges is None:
                # Split into individual pages
                page_ranges = [(i, i) for i in range(total_pages)]
            
            output_files = []
            
            for idx, (start, end) in enumerate(page_ranges, 1):
                writer = PdfWriter()
                
                for page_num in range(start, min(end + 1, total_pages)):
                    writer.add_page(reader.pages[page_num])
                
                output_file = os.path.join(output_dir, f"split_{idx}.pdf")
                with open(output_file, 'wb') as f:
                    writer.write(f)
                
                output_files.append(output_file)
            
            logger.info(f"Split PDF into {len(output_files)} files")
            
            return {
                'total_pages': total_pages,
                'files_created': len(output_files),
                'output_files': output_files
            }
            
        except Exception as e:
            logger.exception(f"PDF split failed: {str(e)}")
            raise PDFProcessingError(f"Failed to split PDF: {str(e)}")
    
    def split_pdf_by_bookmarks(self, input_path: str, output_dir: str) -> Dict:
        """Split PDF by bookmarks/table of contents"""
        try:
            logger.info(f"Splitting PDF by bookmarks: {input_path}")
            
            doc = fitz.open(input_path)
            toc = doc.get_toc()
            
            if not toc:
                raise PDFProcessingError("No bookmarks found in PDF")
            
            os.makedirs(output_dir, exist_ok=True)
            output_files = []
            
            for i, (level, title, page_num) in enumerate(toc):
                # Determine end page
                if i + 1 < len(toc):
                    end_page = toc[i + 1][2] - 1
                else:
                    end_page = len(doc) - 1
                
                # Create new PDF for this section
                new_doc = fitz.open()
                new_doc.insert_pdf(doc, from_page=page_num - 1, to_page=end_page)
                
                # Sanitize title for filename
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
                output_file = os.path.join(output_dir, f"{i+1}_{safe_title}.pdf")
                
                new_doc.save(output_file)
                new_doc.close()
                output_files.append(output_file)
            
            doc.close()
            
            logger.info(f"Split PDF into {len(output_files)} sections by bookmarks")
            
            return {
                'sections_created': len(output_files),
                'output_files': output_files
            }
            
        except Exception as e:
            logger.exception(f"PDF bookmark split failed: {str(e)}")
            raise PDFProcessingError(f"Failed to split by bookmarks: {str(e)}")
    
    # ==================== PAGE MANIPULATION ====================
    
    def rotate_pages(self, input_path: str, output_path: str, 
                    rotation: int, pages: Optional[List[int]] = None) -> Dict:
        """
        Rotate PDF pages
        
        Args:
            input_path: Input PDF path
            output_path: Output PDF path
            rotation: Rotation angle (90, 180, 270)
            pages: List of page numbers to rotate. If None, rotates all pages
        """
        try:
            logger.info(f"Rotating pages in PDF: {input_path}")
            
            reader = PdfReader(input_path)
            writer = PdfWriter()
            
            total_pages = len(reader.pages)
            pages_to_rotate = pages if pages else list(range(total_pages))
            
            for i in range(total_pages):
                page = reader.pages[i]
                if i in pages_to_rotate:
                    page.rotate(rotation)
                writer.add_page(page)
            
            with open(output_path, 'wb') as f:
                writer.write(f)
            
            logger.info(f"Rotated {len(pages_to_rotate)} pages")
            
            return {
                'total_pages': total_pages,
                'pages_rotated': len(pages_to_rotate),
                'rotation_angle': rotation
            }
            
        except Exception as e:
            logger.exception(f"Page rotation failed: {str(e)}")
            raise PDFProcessingError(f"Failed to rotate pages: {str(e)}")
    
    def delete_pages(self, input_path: str, output_path: str, 
                    pages_to_delete: List[int]) -> Dict:
        """Delete specific pages from PDF"""
        try:
            logger.info(f"Deleting pages from PDF: {input_path}")
            
            reader = PdfReader(input_path)
            writer = PdfWriter()
            
            total_pages = len(reader.pages)
            
            for i in range(total_pages):
                if i not in pages_to_delete:
                    writer.add_page(reader.pages[i])
            
            with open(output_path, 'wb') as f:
                writer.write(f)
            
            logger.info(f"Deleted {len(pages_to_delete)} pages")
            
            return {
                'original_pages': total_pages,
                'pages_deleted': len(pages_to_delete),
                'remaining_pages': total_pages - len(pages_to_delete)
            }
            
        except Exception as e:
            logger.exception(f"Page deletion failed: {str(e)}")
            raise PDFProcessingError(f"Failed to delete pages: {str(e)}")
    
    def reorder_pages(self, input_path: str, output_path: str, 
                     new_order: List[int]) -> Dict:
        """Reorder PDF pages"""
        try:
            logger.info(f"Reordering pages in PDF: {input_path}")
            
            reader = PdfReader(input_path)
            writer = PdfWriter()
            
            for page_num in new_order:
                if 0 <= page_num < len(reader.pages):
                    writer.add_page(reader.pages[page_num])
            
            with open(output_path, 'wb') as f:
                writer.write(f)
            
            logger.info(f"Reordered {len(new_order)} pages")
            
            return {
                'total_pages': len(new_order),
                'reordered': True
            }
            
        except Exception as e:
            logger.exception(f"Page reordering failed: {str(e)}")
            raise PDFProcessingError(f"Failed to reorder pages: {str(e)}")
    
    # ==================== WATERMARKS & SECURITY ====================
    
    def add_watermark(self, input_path: str, output_path: str, 
                     watermark_text: str, opacity: float = 0.3) -> Dict:
        """Add text watermark to PDF using PyMuPDF"""
        try:
            logger.info(f"Adding watermark to PDF: {input_path}")
            
            doc = fitz.open(input_path)
            
            for page in doc:
                # Get page dimensions
                rect = page.rect
                
                # Add watermark text diagonally
                page.insert_text(
                    (rect.width / 2, rect.height / 2),
                    watermark_text,
                    fontsize=50,
                    color=(0.5, 0.5, 0.5),
                    rotate=45,
                    overlay=True
                )
            
            doc.save(output_path)
            doc.close()
            
            logger.info(f"Watermark added successfully")
            
            return {
                'watermark_added': True,
                'pages_watermarked': len(doc)
            }
            
        except Exception as e:
            logger.exception(f"Watermark addition failed: {str(e)}")
            raise PDFProcessingError(f"Failed to add watermark: {str(e)}")
    
    def add_password(self, input_path: str, output_path: str, 
                    user_password: str, owner_password: Optional[str] = None) -> Dict:
        """Add password protection to PDF using PyMuPDF"""
        try:
            logger.info(f"Adding password protection to PDF: {input_path}")
            
            doc = fitz.open(input_path)
            
            # Set encryption
            perm = int(
                fitz.PDF_PERM_ACCESSIBILITY |  # always use this
                fitz.PDF_PERM_PRINT |  # permit printing
                fitz.PDF_PERM_COPY |  # permit copying
                fitz.PDF_PERM_ANNOTATE  # permit annotations
            )
            
            owner_pwd = owner_password or user_password
            
            doc.save(
                output_path,
                encryption=fitz.PDF_ENCRYPT_AES_256,
                owner_pw=owner_pwd,
                user_pw=user_password,
                permissions=perm
            )
            doc.close()
            
            logger.info(f"Password protection added successfully")
            
            return {
                'password_protected': True,
                'encryption_level': 'AES-256'
            }
            
        except Exception as e:
            logger.exception(f"Password protection failed: {str(e)}")
            raise PDFProcessingError(f"Failed to add password: {str(e)}")
    
    def remove_password(self, input_path: str, output_path: str, password: str) -> Dict:
        """Remove password protection from PDF"""
        try:
            logger.info(f"Removing password from PDF: {input_path}")
            
            doc = fitz.open(input_path)
            
            if doc.is_encrypted:
                if not doc.authenticate(password):
                    raise PDFProcessingError("Invalid password")
            
            doc.save(output_path, encryption=fitz.PDF_ENCRYPT_NONE)
            doc.close()
            
            logger.info(f"Password removed successfully")
            
            return {
                'password_removed': True
            }
            
        except Exception as e:
            logger.exception(f"Password removal failed: {str(e)}")
            raise PDFProcessingError(f"Failed to remove password: {str(e)}")
    
    # ==================== EXTRACTION ====================
    
    def extract_text(self, input_path: str) -> Dict:
        """Extract all text from PDF with international character support"""
        try:
            logger.info(f"Extracting text from PDF: {input_path}")
            
            text_content = []
            
            with pdfplumber.open(input_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        text_content.append({
                            'page': page_num,
                            'text': text
                        })
            
            logger.info(f"Extracted text from {len(text_content)} pages")
            
            return {
                'pages_processed': len(text_content),
                'content': text_content,
                'total_characters': sum(len(p['text']) for p in text_content)
            }
            
        except Exception as e:
            logger.exception(f"Text extraction failed: {str(e)}")
            raise PDFProcessingError(f"Failed to extract text: {str(e)}")
    
    def extract_images(self, input_path: str, output_dir: str) -> Dict:
        """Extract all images from PDF"""
        try:
            logger.info(f"Extracting images from PDF: {input_path}")
            
            os.makedirs(output_dir, exist_ok=True)
            
            doc = fitz.open(input_path)
            image_count = 0
            extracted_images = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    image_filename = f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
                    image_path = os.path.join(output_dir, image_filename)
                    
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)
                    
                    extracted_images.append(image_path)
                    image_count += 1
            
            doc.close()
            
            logger.info(f"Extracted {image_count} images")
            
            return {
                'images_extracted': image_count,
                'output_files': extracted_images
            }
            
        except Exception as e:
            logger.exception(f"Image extraction failed: {str(e)}")
            raise PDFProcessingError(f"Failed to extract images: {str(e)}")
    
    def extract_tables(self, input_path: str) -> Dict:
        """Extract tables from PDF with international standards"""
        try:
            logger.info(f"Extracting tables from PDF: {input_path}")
            
            tables_data = []
            
            with pdfplumber.open(input_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    tables = page.extract_tables()
                    for table_index, table in enumerate(tables):
                        tables_data.append({
                            'page': page_num,
                            'table_index': table_index + 1,
                            'data': table
                        })
            
            logger.info(f"Extracted {len(tables_data)} tables")
            
            return {
                'tables_extracted': len(tables_data),
                'tables': tables_data
            }
            
        except Exception as e:
            logger.exception(f"Table extraction failed: {str(e)}")
            raise PDFProcessingError(f"Failed to extract tables: {str(e)}")
    
    def extract_metadata(self, input_path: str) -> Dict:
        """Extract PDF metadata with international standards"""
        try:
            logger.info(f"Extracting metadata from PDF: {input_path}")
            
            doc = fitz.open(input_path)
            metadata = doc.metadata
            
            # Additional info
            info = {
                'page_count': len(doc),
                'file_size': os.path.getsize(input_path),
                'metadata': metadata,
                'is_encrypted': doc.is_encrypted,
                'is_pdf': doc.is_pdf,
                'pdf_version': doc.pdf_version() if hasattr(doc, 'pdf_version') else 'Unknown'
            }
            
            doc.close()
            
            logger.info(f"Metadata extracted successfully")
            
            return info
            
        except Exception as e:
            logger.exception(f"Metadata extraction failed: {str(e)}")
            raise PDFProcessingError(f"Failed to extract metadata: {str(e)}")
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def get_page_count(self, input_path: str) -> int:
        """Get number of pages in PDF"""
        try:
            reader = PdfReader(input_path)
            return len(reader.pages)
        except Exception as e:
            logger.exception(f"Failed to get page count: {str(e)}")
            raise PDFProcessingError(f"Failed to get page count: {str(e)}")
    
    def validate_pdf(self, file_path: str) -> bool:
        """Validate if file is a valid PDF"""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(5)
                return header == b'%PDF-'
        except Exception:
            return False
    
    def optimize_pdf(self, input_path: str, output_path: str) -> Dict:
        """Optimize PDF for web viewing"""
        try:
            logger.info(f"Optimizing PDF: {input_path}")
            
            doc = fitz.open(input_path)
            doc.save(
                output_path,
                garbage=4,  # Maximum garbage collection
                deflate=True,  # Compress streams
                clean=True  # Clean up
            )
            doc.close()
            
            original_size = os.path.getsize(input_path)
            optimized_size = os.path.getsize(output_path)
            reduction = ((original_size - optimized_size) / original_size) * 100
            
            logger.info(f"PDF optimized: {reduction:.2f}% reduction")
            
            return {
                'original_size': original_size,
                'optimized_size': optimized_size,
                'reduction_percentage': round(reduction, 2)
            }
            
        except Exception as e:
            logger.exception(f"PDF optimization failed: {str(e)}")
            raise PDFProcessingError(f"Failed to optimize PDF: {str(e)}")

    
    # ==================== PDF MERGING ====================
    
    def merge_pdfs(self, input_paths: List[str], output_path: str) -> Dict:
        """
        Merge multiple PDF files into one
        
        Args:
            input_paths: List of PDF file paths to merge
            output_path: Path for the merged PDF
            
        Returns:
            dict: Merge statistics
        """
        try:
            logger.info(f"Merging {len(input_paths)} PDF files")
            
            merger = PdfMerger()
            total_pages = 0
            
            for pdf_path in input_paths:
                if not os.path.exists(pdf_path):
                    raise PDFProcessingError(f"File not found: {pdf_path}")
                
                reader = PdfReader(pdf_path)
                total_pages += len(reader.pages)
                merger.append(pdf_path)
            
            merger.write(output_path)
            merger.close()
            
            logger.info(f"Successfully merged {len(input_paths)} files into {output_path}")
            
            return {
                'files_merged': len(input_paths),
                'total_pages': total_pages,
                'output_size': os.path.getsize(output_path)
            }
            
        except Exception as e:
            logger.exception(f"PDF merge failed: {str(e)}")
            raise PDFProcessingError(f"Failed to merge PDFs: {str(e)}")
    
    # ==================== PDF SPLITTING ====================
    
    def split_pdf_by_pages(self, input_path: str, output_dir: str, 
                          page_ranges: Optional[List[Tuple[int, int]]] = None) -> Dict:
        """
        Split PDF by page ranges
        
        Args:
            input_path: Input PDF path
            output_dir: Directory to save split PDFs
            page_ranges: List of (start, end) tuples. If None, splits into individual pages
            
        Returns:
            dict: Split statistics
        """
        try:
            logger.info(f"Splitting PDF: {input_path}")
            
            reader = PdfReader(input_path)
            total_pages = len(reader.pages)
            
            os.makedirs(output_dir, exist_ok=True)
            
            if page_ranges is None:
                # Split into individual pages
                page_ranges = [(i, i) for i in range(total_pages)]
            
            output_files = []
            
            for idx, (start, end) in enumerate(page_ranges, 1):
                writer = PdfWriter()
                
                for page_num in range(start, min(end + 1, total_pages)):
                    writer.add_page(reader.pages[page_num])
                
                output_file = os.path.join(output_dir, f"split_{idx}.pdf")
                with open(output_file, 'wb') as f:
                    writer.write(f)
                
                output_files.append(output_file)
            
            logger.info(f"Split PDF into {len(output_files)} files")
            
            return {
                'total_pages': total_pages,
                'files_created': len(output_files),
                'output_files': output_files
            }
            
        except Exception as e:
            logger.exception(f"PDF split failed: {str(e)}")
            raise PDFProcessingError(f"Failed to split PDF: {str(e)}")
    
    def split_pdf_by_bookmarks(self, input_path: str, output_dir: str) -> Dict:
        """Split PDF by bookmarks/table of contents"""
        try:
            logger.info(f"Splitting PDF by bookmarks: {input_path}")
            
            doc = fitz.open(input_path)
            toc = doc.get_toc()
            
            if not toc:
                raise PDFProcessingError("No bookmarks found in PDF")
            
            os.makedirs(output_dir, exist_ok=True)
            output_files = []
            
            for i, (level, title, page_num) in enumerate(toc):
                # Determine end page
                if i + 1 < len(toc):
                    end_page = toc[i + 1][2] - 1
                else:
                    end_page = len(doc) - 1
                
                # Create new PDF for this section
                new_doc = fitz.open()
                new_doc.insert_pdf(doc, from_page=page_num - 1, to_page=end_page)
                
                # Sanitize title for filename
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
                output_file = os.path.join(output_dir, f"{i+1}_{safe_title}.pdf")
                
                new_doc.save(output_file)
                new_doc.close()
                output_files.append(output_file)
            
            doc.close()
            
            logger.info(f"Split PDF into {len(output_files)} sections by bookmarks")
            
            return {
                'sections_created': len(output_files),
                'output_files': output_files
            }
            
        except Exception as e:
            logger.exception(f"PDF bookmark split failed: {str(e)}")
            raise PDFProcessingError(f"Failed to split by bookmarks: {str(e)}")
    
    # ==================== PAGE MANIPULATION ====================
    
    def rotate_pages(self, input_path: str, output_path: str, 
                    rotation: int, pages: Optional[List[int]] = None) -> Dict:
        """
        Rotate PDF pages
        
        Args:
            input_path: Input PDF path
            output_path: Output PDF path
            rotation: Rotation angle (90, 180, 270)
            pages: List of page numbers to rotate. If None, rotates all pages
        """
        try:
            logger.info(f"Rotating pages in PDF: {input_path}")
            
            reader = PdfReader(input_path)
            writer = PdfWriter()
            
            total_pages = len(reader.pages)
            pages_to_rotate = pages if pages else list(range(total_pages))
            
            for i in range(total_pages):
                page = reader.pages[i]
                if i in pages_to_rotate:
                    page.rotate(rotation)
                writer.add_page(page)
            
            with open(output_path, 'wb') as f:
                writer.write(f)
            
            logger.info(f"Rotated {len(pages_to_rotate)} pages")
            
            return {
                'total_pages': total_pages,
                'pages_rotated': len(pages_to_rotate),
                'rotation_angle': rotation
            }
            
        except Exception as e:
            logger.exception(f"Page rotation failed: {str(e)}")
            raise PDFProcessingError(f"Failed to rotate pages: {str(e)}")
    
    def delete_pages(self, input_path: str, output_path: str, 
                    pages_to_delete: List[int]) -> Dict:
        """Delete specific pages from PDF"""
        try:
            logger.info(f"Deleting pages from PDF: {input_path}")
            
            reader = PdfReader(input_path)
            writer = PdfWriter()
            
            total_pages = len(reader.pages)
            
            for i in range(total_pages):
                if i not in pages_to_delete:
                    writer.add_page(reader.pages[i])
            
            with open(output_path, 'wb') as f:
                writer.write(f)
            
            logger.info(f"Deleted {len(pages_to_delete)} pages")
            
            return {
                'original_pages': total_pages,
                'pages_deleted': len(pages_to_delete),
                'remaining_pages': total_pages - len(pages_to_delete)
            }
            
        except Exception as e:
            logger.exception(f"Page deletion failed: {str(e)}")
            raise PDFProcessingError(f"Failed to delete pages: {str(e)}")
    
    def reorder_pages(self, input_path: str, output_path: str, 
                     new_order: List[int]) -> Dict:
        """Reorder PDF pages"""
        try:
            logger.info(f"Reordering pages in PDF: {input_path}")
            
            reader = PdfReader(input_path)
            writer = PdfWriter()
            
            for page_num in new_order:
                if 0 <= page_num < len(reader.pages):
                    writer.add_page(reader.pages[page_num])
            
            with open(output_path, 'wb') as f:
                writer.write(f)
            
            logger.info(f"Reordered {len(new_order)} pages")
            
            return {
                'total_pages': len(new_order),
                'reordered': True
            }
            
        except Exception as e:
            logger.exception(f"Page reordering failed: {str(e)}")
            raise PDFProcessingError(f"Failed to reorder pages: {str(e)}")
    
    # ==================== WATERMARKS & SECURITY ====================
    
    def add_watermark(self, input_path: str, output_path: str, 
                     watermark_text: str, opacity: float = 0.3) -> Dict:
        """Add text watermark to PDF"""
        try:
            logger.info(f"Adding watermark to PDF: {input_path}")
            
            doc = fitz.open(input_path)
            
            for page in doc:
                # Get page dimensions
                rect = page.rect
                
                # Add watermark text
                text_rect = fitz.Rect(0, 0, rect.width, rect.height)
                page.insert_textbox(
                    text_rect,
                    watermark_text,
                    fontsize=50,
                    color=(0.5, 0.5, 0.5),
                    align=fitz.TEXT_ALIGN_CENTER,
                    rotate=45,
                    overlay=True
                )
            
            doc.save(output_path)
            doc.close()
            
            logger.info(f"Watermark added successfully")
            
            return {
                'watermark_added': True,
                'pages_watermarked': len(doc)
            }
            
        except Exception as e:
            logger.exception(f"Watermark addition failed: {str(e)}")
            raise PDFProcessingError(f"Failed to add watermark: {str(e)}")
    
    def add_password(self, input_path: str, output_path: str, 
                    user_password: str, owner_password: Optional[str] = None) -> Dict:
        """Add password protection to PDF"""
        try:
            logger.info(f"Adding password protection to PDF: {input_path}")
            
            with Pdf.open(input_path) as pdf:
                pdf.save(
                    output_path,
                    encryption=Encryption(
                        user=user_password,
                        owner=owner_password or user_password,
                        R=6  # AES-256 encryption
                    )
                )
            
            logger.info(f"Password protection added successfully")
            
            return {
                'password_protected': True,
                'encryption_level': 'AES-256'
            }
            
        except Exception as e:
            logger.exception(f"Password protection failed: {str(e)}")
            raise PDFProcessingError(f"Failed to add password: {str(e)}")
    
    def remove_password(self, input_path: str, output_path: str, password: str) -> Dict:
        """Remove password protection from PDF"""
        try:
            logger.info(f"Removing password from PDF: {input_path}")
            
            with Pdf.open(input_path, password=password) as pdf:
                pdf.save(output_path)
            
            logger.info(f"Password removed successfully")
            
            return {
                'password_removed': True
            }
            
        except Exception as e:
            logger.exception(f"Password removal failed: {str(e)}")
            raise PDFProcessingError(f"Failed to remove password: {str(e)}")
    
    # ==================== EXTRACTION ====================
    
    def extract_text(self, input_path: str) -> Dict:
        """Extract all text from PDF"""
        try:
            logger.info(f"Extracting text from PDF: {input_path}")
            
            text_content = []
            
            with pdfplumber.open(input_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        text_content.append({
                            'page': page_num,
                            'text': text
                        })
            
            logger.info(f"Extracted text from {len(text_content)} pages")
            
            return {
                'pages_processed': len(text_content),
                'content': text_content,
                'total_characters': sum(len(p['text']) for p in text_content)
            }
            
        except Exception as e:
            logger.exception(f"Text extraction failed: {str(e)}")
            raise PDFProcessingError(f"Failed to extract text: {str(e)}")
    
    def extract_images(self, input_path: str, output_dir: str) -> Dict:
        """Extract all images from PDF"""
        try:
            logger.info(f"Extracting images from PDF: {input_path}")
            
            os.makedirs(output_dir, exist_ok=True)
            
            doc = fitz.open(input_path)
            image_count = 0
            extracted_images = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    image_filename = f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
                    image_path = os.path.join(output_dir, image_filename)
                    
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)
                    
                    extracted_images.append(image_path)
                    image_count += 1
            
            doc.close()
            
            logger.info(f"Extracted {image_count} images")
            
            return {
                'images_extracted': image_count,
                'output_files': extracted_images
            }
            
        except Exception as e:
            logger.exception(f"Image extraction failed: {str(e)}")
            raise PDFProcessingError(f"Failed to extract images: {str(e)}")
    
    def extract_metadata(self, input_path: str) -> Dict:
        """Extract PDF metadata"""
        try:
            logger.info(f"Extracting metadata from PDF: {input_path}")
            
            doc = fitz.open(input_path)
            metadata = doc.metadata
            
            # Additional info
            info = {
                'page_count': len(doc),
                'file_size': os.path.getsize(input_path),
                'metadata': metadata,
                'is_encrypted': doc.is_encrypted,
                'is_pdf': doc.is_pdf
            }
            
            doc.close()
            
            logger.info(f"Metadata extracted successfully")
            
            return info
            
        except Exception as e:
            logger.exception(f"Metadata extraction failed: {str(e)}")
            raise PDFProcessingError(f"Failed to extract metadata: {str(e)}")
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def get_page_count(self, input_path: str) -> int:
        """Get number of pages in PDF"""
        try:
            reader = PdfReader(input_path)
            return len(reader.pages)
        except Exception as e:
            logger.exception(f"Failed to get page count: {str(e)}")
            raise PDFProcessingError(f"Failed to get page count: {str(e)}")
    
    def validate_pdf(self, file_path: str) -> bool:
        """Validate if file is a valid PDF"""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(5)
                return header == b'%PDF-'
        except Exception:
            return False
