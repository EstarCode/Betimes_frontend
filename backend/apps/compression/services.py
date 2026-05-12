"""
PDF compression service using Ghostscript.
"""

import os
import subprocess
import logging
from django.conf import settings
from config.exceptions import CompressionError

logger = logging.getLogger(__name__)


class PDFCompressionService:
    """Service class for PDF compression operations."""
    
    def __init__(self):
        self.ghostscript_path = settings.GHOSTSCRIPT_PATH
        self.compression_profiles = settings.COMPRESSION_PROFILES
    
    def compress_pdf(self, input_path, output_path, compression_level='medium'):
        """
        Compress a PDF file using Ghostscript.
        
        Args:
            input_path: Path to the input PDF file
            output_path: Path to save the compressed PDF
            compression_level: Compression level (low, medium, high)
        
        Returns:
            dict: Compression results with file sizes and ratio
        
        Raises:
            CompressionError: If compression fails
        """
        try:
            # Get compression profile
            profile = self.compression_profiles.get(compression_level, self.compression_profiles['medium'])
            
            # Build Ghostscript command with aggressive compression
            gs_command = [
                self.ghostscript_path,
                '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.4',
                f'-dPDFSETTINGS={profile["setting"]}',
                '-dNOPAUSE',
                '-dQUIET',
                '-dBATCH',
                f'-r{profile["dpi"]}',
                '-dCompressFonts=true',
                '-dSubsetFonts=true',
                '-dEmbedAllFonts=false',  # Don't embed fonts for smaller size
                '-dDetectDuplicateImages=true',  # Remove duplicate images
                '-dCompressPages=true',  # Compress page content
                '-dColorImageDownsampleType=/Bicubic',
                '-dColorImageResolution={}'.format(profile["dpi"]),
                '-dGrayImageDownsampleType=/Bicubic',
                '-dGrayImageResolution={}'.format(profile["dpi"]),
                '-dMonoImageDownsampleType=/Bicubic',
                '-dMonoImageResolution={}'.format(profile["dpi"]),
                '-dColorImageDownsampleThreshold=1.0',
                '-dGrayImageDownsampleThreshold=1.0',
                '-dMonoImageDownsampleThreshold=1.0',
                '-dAutoFilterColorImages=true',
                '-dAutoFilterGrayImages=true',
                '-dOptimize=true',  # Optimize PDF structure
                '-dPrinted=false',  # Remove print-specific data
                f'-sOutputFile={output_path}',
                input_path
            ]

            
            # Execute Ghostscript
            logger.info(f"Starting PDF compression: {input_path} -> {output_path}")
            result = subprocess.run(
                gs_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=1800  # 30 minutes timeout
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.decode('utf-8')
                logger.error(f"Ghostscript error: {error_msg}")
                raise CompressionError(f"Compression failed: {error_msg}")
            
            # Verify output file exists
            if not os.path.exists(output_path):
                raise CompressionError("Compressed file was not created")
            
            # Get file sizes
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            
            # Calculate compression ratio
            if original_size > 0:
                compression_ratio = ((original_size - compressed_size) / original_size) * 100
            else:
                compression_ratio = 0
            
            logger.info(
                f"Compression completed: {original_size} -> {compressed_size} bytes "
                f"({compression_ratio:.2f}% reduction)"
            )
            
            return {
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': round(compression_ratio, 2),
                'size_reduction': original_size - compressed_size
            }
            
        except subprocess.TimeoutExpired:
            logger.error("Compression timeout exceeded")
            raise CompressionError("Compression took too long and was cancelled")
        except Exception as e:
            logger.exception(f"Compression error: {str(e)}")
            raise CompressionError(f"Compression failed: {str(e)}")
    
    def validate_pdf(self, file_path):
        """
        Validate if a file is a valid PDF.
        
        Args:
            file_path: Path to the file to validate
        
        Returns:
            bool: True if valid PDF, False otherwise
        """
        try:
            with open(file_path, 'rb') as f:
                header = f.read(5)
                return header == b'%PDF-'
        except Exception as e:
            logger.error(f"PDF validation error: {str(e)}")
            return False
