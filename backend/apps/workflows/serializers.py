"""
Serializers for enterprise workflow system
"""
from rest_framework import serializers
from .models import WorkflowTemplate, WorkflowStage, WorkflowInstance, WorkflowApproval


class WorkflowStageSerializer(serializers.ModelSerializer):
    """Serializer for workflow stages"""
    approver_email = serializers.EmailField(source='approver_user.email', read_only=True)
    
    class Meta:
        model = WorkflowStage
        fields = [
            'id', 'stage_number', 'stage_name', 'approver_role',
            'approver_user', 'approver_email', 'department', 'required'
        ]


class WorkflowTemplateSerializer(serializers.ModelSerializer):
    """Serializer for workflow templates"""
    stages = WorkflowStageSerializer(many=True, read_only=True)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    
    class Meta:
        model = WorkflowTemplate
        fields = [
            'id', 'name', 'description', 'approval_type', 'max_stages',
            'escalation_hours', 'created_by', 'created_by_email',
            'is_active', 'created_at', 'updated_at', 'stages'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkflowApprovalSerializer(serializers.ModelSerializer):
    """Serializer for workflow approvals"""
    approver_email = serializers.EmailField(source='approver.email', read_only=True)
    
    class Meta:
        model = WorkflowApproval
        fields = [
            'id', 'stage_number', 'approver', 'approver_email',
            'decision', 'comments', 'decided_at'
        ]
        read_only_fields = ['id', 'decided_at']


class WorkflowInstanceSerializer(serializers.ModelSerializer):
    """Serializer for workflow instances"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    document_filename = serializers.CharField(source='document.filename', read_only=True)
    initiated_by_email = serializers.EmailField(source='initiated_by.email', read_only=True)
    approvals = WorkflowApprovalSerializer(many=True, read_only=True)
    
    class Meta:
        model = WorkflowInstance
        fields = [
            'id', 'template', 'template_name', 'document', 'document_filename',
            'status', 'current_stage', 'initiated_by', 'initiated_by_email',
            'created_at', 'updated_at', 'completed_at', 'approvals'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']


class ApprovalDecisionSerializer(serializers.Serializer):
    """Serializer for approval decisions"""
    decision = serializers.ChoiceField(choices=['approved', 'rejected', 'escalated'])
    comments = serializers.CharField(required=False, allow_blank=True)
