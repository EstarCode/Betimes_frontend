"""
Enterprise OCR Service
Extracts text from scanned documents and images
Requirement 8: OCR Text Extraction with 95% accuracy
Supports 7 languages: English, Spanish, French, German, Chinese, Japanese, Arabic
"""

import os
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from pdf2image import convert_from_path

try:
    from config.exceptions import OCRError
except ImportError:
    class OCRError(Exception):
        pass

logger = logging.getLogger(__name__)


class OCRService:
    """
    Enterprise-grade OCR service with multi-language support
    Performance target: 10-page document in < 90 seconds
    Accuracy target: 95% for clear documents
    """
    
    # Language codes for Tesseract
    SUPPORTED_LANGUAGES = {
        'english': 'eng',
        'spanish': 'spa',
        'french': 'fra',
        'german': 'deu',
        'chinese': 'chi_sim',
        'japanese': 'jpn',
        'arabic': 'ara',
    }
    
    # Performance tracking
    MAX_PROCESSING_TIME_PER_PAGE = 9  # seconds (90s for 10 pages)
    
    def __init__(self, tesseract_cmd=None):
        """
        Initialize OCR service
        
        Args:
            tesseract_cmd: Path to tesseract executable (optional)
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        
        # Verify Tesseract is installed
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            logger.error(f"Tesseract not found: {str(e)}")
            raise OCRError("Tesseract OCR is not installed or not in PATH")
    
    def extract_text_from_image(self, image_path: str, language: str = 'english',
                               config: Optional[str] = None) -> Dict:
        """
        Extract text from a single image
        
        Args:
            image_path: Path to image file (JPG, PNG, TIFF)
            language: Language of the document
            config: Custom Tesseract configuration
        
        Returns:
            dict: Extracted text and metadata
        """
        start_time = time.time()
        
        try:
            logger.info(f"Extracting text from image: {image_path}")
            
            # Validate language
            lang_code = self.SUPPORTED_LANGUAGES.get(language.lower())
            if not lang_code:
                raise OCRError(f"Unsupported language: {language}")
            
            # Open and preprocess image
            image = Image.open(image_path)
            image = self._preprocess_image(image)
            
            # Default config for better accuracy
            if config is None:
                config = '--oem 3 --psm 3'  # LSTM OCR Engine, Automatic page segmentation
            
            # Extract text
            text = pytesseract.image_to_string(image, lang=lang_code, config=config)
            
            # Get confidence scores
            data = pytesseract.image_to_data(image, lang=lang_code, output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in data['conf'] if conf != '-1']
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            elapsed = time.time() - start_time
            
            logger.info(f"Text extraction completed in {elapsed:.2f}s with {avg_confidence:.1f}% confidence")
            
            return {
                'success': True,
                'text': text.strip(),
                'language': language,
                'confidence': round(avg_confidence, 2),
                'word_count': len(text.split()),
                'character_count': len(text),
                'processing_time': elapsed
            }
            
        except Exception as e:
            logger.exception(f"OCR failed for image: {str(e)}")
            raise OCRError(f"Failed to extract text from image: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_path: str, language: str = 'english',
                             output_pdf_path: Optional[str] = None) -> Dict:
        """
        Extract text from scanned PDF and optionally create searchable PDF
        
        Args:
            pdf_path: Path to PDF file
            language: Language of the document
            output_pdf_path: Path to save searchable PDF (optional)
        
        Returns:
            dict: Extracted text and metadata
        """
        start_time = time.time()
        
        try:
            logger.info(f"Extracting text from PDF: {pdf_path}")
            
            # Validate language
            lang_code = self.SUPPORTED_LANGUAGES.get(language.lower())
            if not lang_code:
                raise OCRError(f"Unsupported language: {language}")
            
            # Convert PDF pages to images
            images = convert_from_path(pdf_path, dpi=300)
            
            page_texts = []
            total_confidence = 0
            
            for page_num, image in enumerate(images, 1):
                logger.info(f"Processing page {page_num}/{len(images)}")
                
                # Preprocess image
                image = self._preprocess_image(image)
                
                # Extract text
                text = pytesseract.image_to_string(image, lang=lang_code, config='--oem 3 --psm 3')
                
                # Get confidence
                data = pytesseract.image_to_data(image, lang=lang_code, output_type=pytesseract.Output.DICT)
                confidences = [int(conf) for conf in data['conf'] if conf != '-1']
                page_confidence = sum(confidences) / len(confidences) if confidences else 0
                
                page_texts.append({
                    'page': page_num,
                    'text': text.strip(),
                    'confidence': round(page_confidence, 2)
                })
                
                total_confidence += page_confidence
            
            # Combine all text
            full_text = '\n\n'.join([p['text'] for p in page_texts])
            avg_confidence = total_confidence / len(images) if images else 0
            
            # Create searchable PDF if requested
            if output_pdf_path:
                self._create_searchable_pdf(pdf_path, images, page_texts, output_pdf_path, lang_code)
            
            elapsed = time.time() - start_time
            
            logger.info(f"PDF OCR completed in {elapsed:.2f}s with {avg_confidence:.1f}% confidence")
            
            return {
                'success': True,
                'text': full_text,
                'pages': page_texts,
                'page_count': len(images),
                'language': language,
                'average_confidence': round(avg_confidence, 2),
                'word_count': len(full_text.split()),
                'character_count': len(full_text),
                'processing_time': elapsed,
                'searchable_pdf_created': output_pdf_path is not None
            }
            
        except Exception as e:
            logger.exception(f"OCR failed for PDF: {str(e)}")
            raise OCRError(f"Failed to extract text from PDF: {str(e)}")
    
    def batch_ocr(self, file_paths: List[str], language: str = 'english',
                  output_dir: Optional[str] = None) -> Dict:
        """
        Perform OCR on multiple files
        
        Args:
            file_paths: List of file paths
            language: Language of the documents
            output_dir: Directory to save searchable PDFs (optional)
        
        Returns:
            dict: Batch processing results
        """
        start_time = time.time()
        
        try:
            logger.info(f"Starting batch OCR for {len(file_paths)} files")
            
            results = []
            successful = 0
            failed = 0
            
            for file_path in file_paths:
                try:
                    file_ext = Path(file_path).suffix.lower()
                    
                    if file_ext == '.pdf':
                        output_pdf = None
                        if output_dir:
                            output_pdf = os.path.join(output_dir, 
                                                     Path(file_path).stem + '_searchable.pdf')
                        result = self.extract_text_from_pdf(file_path, language, output_pdf)
                    else:
                        result = self.extract_text_from_image(file_path, language)
                    
                    results.append({
                        'file': file_path,
                        'status': 'success',
                        'result': result
                    })
                    successful += 1
                    
                except Exception as e:
                    logger.error(f"Failed to process {file_path}: {str(e)}")
                    results.append({
                        'file': file_path,
                        'status': 'failed',
                        'error': str(e)
                    })
                    failed += 1
            
            elapsed = time.time() - start_time
            
            logger.info(f"Batch OCR completed in {elapsed:.2f}s: {successful} successful, {failed} failed")
            
            return {
                'total_files': len(file_paths),
                'successful': successful,
                'failed': failed,
                'results': results,
                'total_processing_time': elapsed
            }
            
        except Exception as e:
            logger.exception(f"Batch OCR failed: {str(e)}")
            raise OCRError(f"Batch OCR failed: {str(e)}")
    
    # Helper methods
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR accuracy
        
        Args:
            image: PIL Image object
        
        Returns:
            Preprocessed image
        """
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Increase contrast
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Increase sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)
        
        return image
    
    def _create_searchable_pdf(self, original_pdf_path: str, images: List[Image.Image],
                              page_texts: List[Dict], output_path: str, lang_code: str):
        """
        Create searchable PDF with text layer overlay
        
        Args:
            original_pdf_path: Path to original PDF
            images: List of page images
            page_texts: List of extracted text per page
            output_path: Path to save searchable PDF
            lang_code: Tesseract language code
        """
        try:
            logger.info(f"Creating searchable PDF: {output_path}")
            
            # Create new PDF with text layer
            doc = fitz.open()
            
            for i, (image, page_data) in enumerate(zip(images, page_texts)):
                # Convert PIL image to bytes
                import io
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                
                # Create new page
                page = doc.new_page(width=image.width, height=image.height)
                
                # Insert image
                page.insert_image(page.rect, stream=img_byte_arr)
                
                # Add invisible text layer
                text = page_data['text']
                if text:
                    # Add text as invisible overlay
                    page.insert_text((0, 0), text, fontsize=1, color=(1, 1, 1), overlay=False)
            
            # Save searchable PDF
            doc.save(output_path)
            doc.close()
            
            logger.info(f"Searchable PDF created: {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to create searchable PDF: {str(e)}")
            # Don't raise exception, just log the error
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return list(self.SUPPORTED_LANGUAGES.keys())
    
    def validate_language(self, language: str) -> bool:
        """Check if language is supported"""
        return language.lower() in self.SUPPORTED_LANGUAGES
