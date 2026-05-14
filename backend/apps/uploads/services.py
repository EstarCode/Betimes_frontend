"""
Business logic for chunked upload system
Handles file chunking, resumption, and integrity validation
"""
import hashlib
import os
from pathlib import Path
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils import timezone
from .models import UploadSession, UploadChunk


class ChunkedUploadService:
    """Service for handling chunked file uploads"""
    
    TEMP_UPLOAD_DIR = 'temp_uploads'
    MAX_FILE_SIZE = 10 * 1024 * 1024 * 1024  # 10GB
    DEFAULT_CHUNK_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_RETRY_ATTEMPTS = 3
    
    @classmethod
    def initiate_upload(cls, user, filename, file_size, chunk_size=None, checksum=None):
        """
        Initialize a new chunked upload session
        
        Args:
            user: User initiating the upload
            filename: Original filename
            file_size: Total file size in bytes
            chunk_size: Size of each chunk (default 10MB)
            checksum: Optional SHA-256 checksum of complete file
        
        Returns:
            UploadSession instance
        
        Raises:
            ValueError: If file size exceeds maximum or is invalid
        """
        if file_size > cls.MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds maximum allowed size of {cls.MAX_FILE_SIZE} bytes")
        
        if file_size <= 0:
            raise ValueError("File size must be greater than 0")
        
        chunk_size = chunk_size or cls.DEFAULT_CHUNK_SIZE
        total_chunks = (file_size + chunk_size - 1) // chunk_size  # Ceiling division
        
        # Create temp directory for this upload
        temp_path = os.path.join(cls.TEMP_UPLOAD_DIR, str(user.id))
        os.makedirs(os.path.join(settings.MEDIA_ROOT, temp_path), exist_ok=True)
        
        upload_session = UploadSession.objects.create(
            user=user,
            filename=filename,
            file_size=file_size,
            chunk_size=chunk_size,
            total_chunks=total_chunks,
            checksum_sha256=checksum or '',
            storage_temp_path=temp_path
        )
        
        return upload_session
    
    @classmethod
    def upload_chunk(cls, upload_session, chunk_number, chunk_file, checksum):
        """
        Upload a single chunk
        
        Args:
            upload_session: UploadSession instance
            chunk_number: Chunk number (0-indexed)
            chunk_file: File object containing chunk data
            checksum: SHA-256 checksum of the chunk
        
        Returns:
            UploadChunk instance
        
        Raises:
            ValueError: If chunk validation fails
        """
        if upload_session.status != 'in_progress':
            raise ValueError(f"Upload session is {upload_session.status}, cannot upload chunks")
        
        if chunk_number >= upload_session.total_chunks:
            raise ValueError(f"Invalid chunk number {chunk_number}, total chunks: {upload_session.total_chunks}")
        
        # Check if chunk already exists
        existing_chunk = UploadChunk.objects.filter(
            upload_session=upload_session,
            chunk_number=chunk_number
        ).first()
        
        if existing_chunk:
            # Chunk already uploaded, return existing
            return existing_chunk
        
        # Validate chunk checksum
        chunk_data = chunk_file.read()
        calculated_checksum = hashlib.sha256(chunk_data).hexdigest()
        
        if calculated_checksum != checksum:
            upload_session.retry_count += 1
            upload_session.save()
            raise ValueError("Chunk checksum mismatch")
        
        # Save chunk to temporary storage
        chunk_filename = f"chunk_{chunk_number}"
        chunk_path = os.path.join(
            upload_session.storage_temp_path,
            str(upload_session.id),
            chunk_filename
        )
        
        # Ensure directory exists
        full_path = os.path.join(settings.MEDIA_ROOT, chunk_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write chunk to disk
        with open(full_path, 'wb') as f:
            f.write(chunk_data)
        
        # Create chunk record
        chunk = UploadChunk.objects.create(
            upload_session=upload_session,
            chunk_number=chunk_number,
            chunk_size=len(chunk_data),
            checksum_sha256=checksum,
            storage_path=chunk_path
        )
        
        # Update session
        upload_session.uploaded_chunks += 1
        upload_session.updated_at = timezone.now()
        upload_session.save()
        
        return chunk
    
    @classmethod
    def complete_upload(cls, upload_session, final_checksum=None):
        """
        Complete the upload by merging all chunks
        
        Args:
            upload_session: UploadSession instance
            final_checksum: Optional SHA-256 checksum of complete file
        
        Returns:
            Path to the completed file
        
        Raises:
            ValueError: If upload is incomplete or checksum mismatch
        """
        if not upload_session.is_complete:
            raise ValueError(
                f"Upload incomplete: {upload_session.uploaded_chunks}/{upload_session.total_chunks} chunks uploaded"
            )
        
        # Get all chunks in order
        chunks = upload_session.chunks.order_by('chunk_number')
        
        # Merge chunks into final file
        final_filename = f"{upload_session.id}_{upload_session.filename}"
        final_path = os.path.join('uploads', str(upload_session.user.id), final_filename)
        full_final_path = os.path.join(settings.MEDIA_ROOT, final_path)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(full_final_path), exist_ok=True)
        
        # Merge chunks and calculate checksum
        hasher = hashlib.sha256()
        
        with open(full_final_path, 'wb') as final_file:
            for chunk in chunks:
                chunk_full_path = os.path.join(settings.MEDIA_ROOT, chunk.storage_path)
                with open(chunk_full_path, 'rb') as chunk_file:
                    chunk_data = chunk_file.read()
                    final_file.write(chunk_data)
                    hasher.update(chunk_data)
        
        calculated_checksum = hasher.hexdigest()
        
        # Validate final checksum if provided
        if final_checksum and calculated_checksum != final_checksum:
            # Clean up merged file
            os.remove(full_final_path)
            upload_session.status = 'failed'
            upload_session.save()
            raise ValueError("Final file checksum mismatch")
        
        # Update session
        upload_session.checksum_sha256 = calculated_checksum
        upload_session.status = 'completed'
        upload_session.completed_at = timezone.now()
        upload_session.save()
        
        # Clean up temporary chunks
        cls._cleanup_chunks(upload_session)
        
        return final_path
    
    @classmethod
    def _cleanup_chunks(cls, upload_session):
        """Remove temporary chunk files"""
        temp_dir = os.path.join(
            settings.MEDIA_ROOT,
            upload_session.storage_temp_path,
            str(upload_session.id)
        )
        
        if os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)
    
    @classmethod
    def cancel_upload(cls, upload_session):
        """Cancel an upload session and clean up"""
        upload_session.status = 'cancelled'
        upload_session.save()
        cls._cleanup_chunks(upload_session)
    
    @classmethod
    def get_upload_progress(cls, upload_session):
        """Get detailed upload progress information"""
        return {
            'session_id': str(upload_session.id),
            'filename': upload_session.filename,
            'file_size': upload_session.file_size,
            'total_chunks': upload_session.total_chunks,
            'uploaded_chunks': upload_session.uploaded_chunks,
            'progress_percentage': upload_session.progress_percentage,
            'status': upload_session.status,
            'created_at': upload_session.created_at,
            'updated_at': upload_session.updated_at,
        }
