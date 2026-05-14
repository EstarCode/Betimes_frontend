"""
Enterprise Workflow System Models
Supports multi-step approval chains with routing and escalation
"""
from django.db import models
from django.contrib.auth import get_user_model
from apps.versions.models import Document
import uuid

User = get_user_model()


class WorkflowTemplate(models.Model):
    """
    Reusable workflow template
    """
    APPROVAL_TYPES = [
        ('sequential', 'Sequential'),
        ('parallel', 'Parallel'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    approval_type = models.CharField(max_length=50, choices=APPROVAL_TYPES)
    max_stages = models.IntegerField(default=10)
    escalation_hours = models.IntegerField(default=48)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'workflow_templates'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class WorkflowStage(models.Model):
    """
    Individual stage in a workflow template
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(WorkflowTemplate, on_delete=models.CASCADE, related_name='stages')
    stage_number = models.IntegerField()
    stage_name = models.CharField(max_length=255)
    approver_role = models.CharField(max_length=50, blank=True)
    approver_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.CharField(max_length=100, blank=True)
    required = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'workflow_stages'
        unique_together = [['template', 'stage_number']]
        ordering = ['stage_number']
    
    def __str__(self):
        return f"{self.template.name} - Stage {self.stage_number}"


class WorkflowInstance(models.Model):
    """
    Active workflow instance for a document
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('escalated', 'Escalated'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(WorkflowTemplate, on_delete=models.SET_NULL, null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='workflows')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')
    current_stage = models.IntegerField(default=1)
    initiated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'workflow_instances'
        indexes = [
            models.Index(fields=['document']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Workflow for {self.document.filename} - {self.status}"


class WorkflowApproval(models.Model):
    """
    Individual approval decision in a workflow
    """
    DECISION_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('escalated', 'Escalated'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow_instance = models.ForeignKey(WorkflowInstance, on_delete=models.CASCADE, related_name='approvals')
    stage_number = models.IntegerField()
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    decision = models.CharField(max_length=50, choices=DECISION_CHOICES)
    comments = models.TextField(blank=True)
    decided_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'workflow_approvals'
        indexes = [
            models.Index(fields=['workflow_instance']),
            models.Index(fields=['decided_at']),
        ]
        ordering = ['-decided_at']
    
    def __str__(self):
        return f"{self.approver} - {self.decision}"
