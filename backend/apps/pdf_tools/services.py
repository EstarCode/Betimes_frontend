"""
PDF Tools Services
Implements PDF split, merge, and manipulation operations
Requirements 5 & 6: PDF Split and Merge
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Optional
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import fitz  # PyMuPDF

try:
    from config.exceptions import PDFError
except ImportError:
    class PDFError(Exception):
        pass

logger = logging.getLogger(__name__)


class PDFToolsService:
    """
    Enterprise PDF manipulation service
    Supports split, merge, and advanced operations
    """
    
    def split_pdf_by_range(self, input_path: str, output_dir: str, 
                          page_ranges: List[Dict[str, int]]) -> Dict:
        """
        Split PDF by page ranges
        Requirement 5: PDF Split by page range
        
        Args:
            input_path: Path to input PDF
            output_dir: Directory to save split PDFs
            page_ranges: List of dicts with 'start', 'end', 'output_name'
                Example: [{'start': 1, 'end': 5, 'output_name': 'part1.pdf'}]
        
        Returns:
            dict: Split results with output files
        """
        try:
            logger.info(f"Splitting PDF by ranges: {input_path}")
            
            # Validate input
            if not os.path.exists(input_path):
                raise PDFError(f"Input file not found: {input_path}")
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Read input PDF
            reader = PdfReader(input_path)
            total_pages = len(reader.pages)
            
            output_files = []
            
            for range_spec in page_ranges:
                start_page = range_spec.get('start', 1)
                end_page = range_spec.get('end', total_pages)
                output_name = range_spec.get('output_name', f'split_{start_page}_{end_page}.pdf')
                
                # Validate page range
                if start_page < 1 or end_page > total_pages:
                    raise PDFError(
                        f"Page range {start_page}-{end_page} exceeds document length ({total_pages} pages)"
                    )
                
                if start_page > end_page:
                    raise PDFError(f"Invalid range: start ({start_page}) > end ({end_page})")
                
                # Create writer for this range
                writer = PdfWriter()
                
                # Add pages (convert to 0-indexed)
                for page_num in range(start_page - 1, end_page):
                    writer.add_page(reader.pages[page_num])
                
                # Preserve metadata
                if reader.metadata:
                    writer.add_metadata(reader.metadata)
                
                # Write output file
                output_path = os.path.join(output_dir, output_name)
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
                output_files.append({
                    'path': output_path,
                    'name': output_name,
                    'pages': f"{start_page}-{end_page}",
                    'page_count': end_page - start_page + 1,
                    'size': os.path.getsize(output_path)
                })
                
                logger.info(f"Created split file: {output_name} (pages {start_page}-{end_page})")
            
            return {
                'success': True,
                'input_file': input_path,
                'total_pages': total_pages,
                'output_files': output_files,
                'split_count': len(output_files)
            }
            
        except Exception as e:
            logger.exception(f"PDF split failed: {str(e)}")
            raise PDFError(f"Failed to split PDF: {str(e)}")
    
    def split_pdf_by_bookmarks(self, input_path: str, output_dir: str) -> Dict:
        """
        Split PDF by bookmark boundaries
        Requirement 5: PDF Split by bookmarks
        
        Args:
            input_path: Path to input PDF
            output_dir: Directory to save split PDFs
        
        Returns:
            dict: Split results with output files
        """
        try:
            logger.info(f"Splitting PDF by bookmarks: {input_path}")
            
            # Use PyMuPDF for bookmark extraction
            doc = fitz.open(input_path)
            toc = doc.get_toc()  # Table of contents (bookmarks)
            
            if not toc:
                raise PDFError("PDF has no bookmarks")
            
            os.makedirs(output_dir, exist_ok=True)
            
            # Read with PyPDF2 for splitting
            reader = PdfReader(input_path)
            total_pages = len(reader.pages)
            
            output_files = []
            
            # Process bookmarks
            for i, bookmark in enumerate(toc):
                level, title, page_num = bookmark
                
                # Only process top-level bookmarks
                if level != 1:
                    continue
                
                # Determine page range
                start_page = page_num
                
                # Find next top-level bookmark
                end_page = total_pages
                for j in range(i + 1, len(toc)):
                    if toc[j][0] == 1:  # Next top-level bookmark
                        end_page = toc[j][2] - 1
                        break
                
                # Create writer
                writer = PdfWriter()
                
                # Add pages (PyMuPDF uses 1-indexed, PyPDF2 uses 0-indexed)
                for page_idx in range(start_page - 1, end_page):
                    if page_idx < total_pages:
                        writer.add_page(reader.pages[page_idx])
                
                # Sanitize title for filename
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_title = safe_title[:50]  # Limit length
                output_name = f"{safe_title}.pdf"
                
                # Write output
                output_path = os.path.join(output_dir, output_name)
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
                output_files.append({
                    'path': output_path,
                    'name': output_name,
                    'bookmark': title,
                    'pages': f"{start_page}-{end_page}",
                    'page_count': end_page - start_page + 1,
                    'size': os.path.getsize(output_path)
                })
                
                logger.info(f"Created split file from bookmark: {title}")
            
            doc.close()
            
            return {
                'success': True,
                'input_file': input_path,
                'total_pages': total_pages,
                'output_files': output_files,
                'split_count': len(output_files)
            }
            
        except Exception as e:
            logger.exception(f"PDF bookmark split failed: {str(e)}")
            raise PDFError(f"Failed to split PDF by bookmarks: {str(e)}")
    
    def merge_pdfs(self, input_files: List[Dict], output_path: str,
                   create_toc: bool = True) -> Dict:
        """
        Merge multiple PDF files with custom ordering
        Requirement 6: PDF Merge with custom ordering and TOC
        
        Args:
            input_files: List of dicts with 'path' and optional 'title'
                Example: [{'path': 'file1.pdf', 'title': 'Chapter 1'}]
            output_path: Path to save merged PDF
            create_toc: Whether to create table of contents
        
        Returns:
            dict: Merge results
        """
        try:
            logger.info(f"Merging {len(input_files)} PDF files")
            
            if len(input_files) > 100:
                raise PDFError("Cannot merge more than 100 files")
            
            if not input_files:
                raise PDFError("No input files provided")
            
            # Validate all input files exist
            for file_spec in input_files:
                if not os.path.exists(file_spec['path']):
                    raise PDFError(f"Input file not found: {file_spec['path']}")
            
            # Use PdfMerger for better bookmark handling
            merger = PdfMerger()
            
            toc_entries = []
            current_page = 0
            
            for idx, file_spec in enumerate(input_files):
                file_path = file_spec['path']
                file_title = file_spec.get('title', Path(file_path).stem)
                
                # Get page count
                reader = PdfReader(file_path)
                page_count = len(reader.pages)
                
                # Add to merger with bookmark
                if create_toc:
                    merger.append(file_path, outline_item=file_title)
                else:
                    merger.append(file_path)
                
                toc_entries.append({
                    'title': file_title,
                    'page': current_page + 1,
                    'page_count': page_count
                })
                
                current_page += page_count
                
                logger.info(f"Added file {idx + 1}/{len(input_files)}: {file_title} ({page_count} pages)")
            
            # Write merged PDF
            merger.write(output_path)
            merger.close()
            
            # Get output file size
            output_size = os.path.getsize(output_path)
            
            logger.info(f"Merged PDF created: {output_path} ({current_page} total pages)")
            
            return {
                'success': True,
                'output_path': output_path,
                'total_pages': current_page,
                'file_count': len(input_files),
                'output_size': output_size,
                'table_of_contents': toc_entries if create_toc else None
            }
            
        except Exception as e:
            logger.exception(f"PDF merge failed: {str(e)}")
            raise PDFError(f"Failed to merge PDFs: {str(e)}")
    
    def extract_pages(self, input_path: str, output_path: str, 
                     page_numbers: List[int]) -> Dict:
        """
        Extract specific pages from PDF
        
        Args:
            input_path: Path to input PDF
            output_path: Path to save extracted pages
            page_numbers: List of page numbers to extract (1-indexed)
        
        Returns:
            dict: Extraction results
        """
        try:
            logger.info(f"Extracting {len(page_numbers)} pages from PDF")
            
            reader = PdfReader(input_path)
            total_pages = len(reader.pages)
            
            # Validate page numbers
            for page_num in page_numbers:
                if page_num < 1 or page_num > total_pages:
                    raise PDFError(f"Page {page_num} out of range (1-{total_pages})")
            
            writer = PdfWriter()
            
            # Add requested pages
            for page_num in sorted(set(page_numbers)):  # Remove duplicates and sort
                writer.add_page(reader.pages[page_num - 1])
            
            # Preserve metadata
            if reader.metadata:
                writer.add_metadata(reader.metadata)
            
            # Write output
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return {
                'success': True,
                'input_file': input_path,
                'output_file': output_path,
                'extracted_pages': len(page_numbers),
                'output_size': os.path.getsize(output_path)
            }
            
        except Exception as e:
            logger.exception(f"Page extraction failed: {str(e)}")
            raise PDFError(f"Failed to extract pages: {str(e)}")
    
    def rotate_pages(self, input_path: str, output_path: str,
                    rotation: int, pages: Optional[List[int]] = None) -> Dict:
        """
        Rotate PDF pages
        
        Args:
            input_path: Path to input PDF
            output_path: Path to save rotated PDF
            rotation: Rotation angle (90, 180, 270)
            pages: List of page numbers to rotate (None = all pages)
        
        Returns:
            dict: Rotation results
        """
        try:
            if rotation not in [90, 180, 270]:
                raise PDFError("Rotation must be 90, 180, or 270 degrees")
            
            reader = PdfReader(input_path)
            writer = PdfWriter()
            
            total_pages = len(reader.pages)
            pages_to_rotate = pages if pages else list(range(1, total_pages + 1))
            
            for page_num in range(1, total_pages + 1):
                page = reader.pages[page_num - 1]
                
                if page_num in pages_to_rotate:
                    page.rotate(rotation)
                
                writer.add_page(page)
            
            # Write output
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return {
                'success': True,
                'rotated_pages': len(pages_to_rotate),
                'rotation': rotation,
                'output_path': output_path
            }
            
        except Exception as e:
            logger.exception(f"Page rotation failed: {str(e)}")
            raise PDFError(f"Failed to rotate pages: {str(e)}")
    
    def get_pdf_info(self, file_path: str) -> Dict:
        """
        Get PDF metadata and information
        
        Args:
            file_path: Path to PDF file
        
        Returns:
            dict: PDF information
        """
        try:
            reader = PdfReader(file_path)
            
            # Get bookmarks
            bookmarks = []
            if reader.outline:
                bookmarks = self._extract_bookmarks(reader.outline)
            
            info = {
                'page_count': len(reader.pages),
                'file_size': os.path.getsize(file_path),
                'has_bookmarks': len(bookmarks) > 0,
                'bookmark_count': len(bookmarks),
                'bookmarks': bookmarks,
                'metadata': {}
            }
            
            # Extract metadata
            if reader.metadata:
                info['metadata'] = {
                    'title': reader.metadata.get('/Title', ''),
                    'author': reader.metadata.get('/Author', ''),
                    'subject': reader.metadata.get('/Subject', ''),
                    'creator': reader.metadata.get('/Creator', ''),
                    'producer': reader.metadata.get('/Producer', ''),
                }
            
            return info
            
        except Exception as e:
            logger.exception(f"Failed to get PDF info: {str(e)}")
            raise PDFError(f"Failed to get PDF info: {str(e)}")
    
    def _extract_bookmarks(self, outline, level=1):
        """Recursively extract bookmarks from PDF outline"""
        bookmarks = []
        
        for item in outline:
            if isinstance(item, list):
                bookmarks.extend(self._extract_bookmarks(item, level + 1))
            else:
                bookmarks.append({
                    'title': item.get('/Title', 'Untitled'),
                    'level': level
                })
        
        return bookmarks
