"""
Views for enterprise workflow system
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import WorkflowTemplate, WorkflowInstance, WorkflowApproval
from .serializers import (
    WorkflowTemplateSerializer, WorkflowInstanceSerializer,
    WorkflowApprovalSerializer, ApprovalDecisionSerializer
)


class WorkflowTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for workflow templates
    """
    serializer_class = WorkflowTemplateSerializer
    permission_classes = [IsAuthenticated]
    queryset = WorkflowTemplate.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class WorkflowInstanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for workflow instances
    """
    serializer_class = WorkflowInstanceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return workflows for current user"""
        user = self.request.user
        if user.role in ['Super_Admin', 'Admin']:
            return WorkflowInstance.objects.all()
        return WorkflowInstance.objects.filter(initiated_by=user)
    
    def perform_create(self, serializer):
        serializer.save(initiated_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Approve current workflow stage
        
        POST /api/v1/workflows/instances/{id}/approve/
        Body: {"comments": "Approved"}
        """
        workflow = self.get_object()
        
        if workflow.status not in ['pending', 'in_review']:
            return Response(
                {'error': 'Workflow is not in a state that can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ApprovalDecisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create approval record
        approval = WorkflowApproval.objects.create(
            workflow_instance=workflow,
            stage_number=workflow.current_stage,
            approver=request.user,
            decision='approved',
            comments=serializer.validated_data.get('comments', '')
        )
        
        # Check if there are more stages
        template = workflow.template
        if workflow.current_stage < template.max_stages:
            # Move to next stage
            workflow.current_stage += 1
            workflow.status = 'in_review'
        else:
            # Workflow complete
            workflow.status = 'approved'
            workflow.completed_at = timezone.now()
        
        workflow.save()
        
        return Response({
            'message': 'Stage approved successfully',
            'workflow': WorkflowInstanceSerializer(workflow).data,
            'approval': WorkflowApprovalSerializer(approval).data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Reject workflow
        
        POST /api/v1/workflows/instances/{id}/reject/
        Body: {"comments": "Requires revision"}
        """
        workflow = self.get_object()
        
        if workflow.status not in ['pending', 'in_review']:
            return Response(
                {'error': 'Workflow is not in a state that can be rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ApprovalDecisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create approval record
        approval = WorkflowApproval.objects.create(
            workflow_instance=workflow,
            stage_number=workflow.current_stage,
            approver=request.user,
            decision='rejected',
            comments=serializer.validated_data.get('comments', '')
        )
        
        # Update workflow status
        workflow.status = 'rejected'
        workflow.completed_at = timezone.now()
        workflow.save()
        
        return Response({
            'message': 'Workflow rejected',
            'workflow': WorkflowInstanceSerializer(workflow).data,
            'approval': WorkflowApprovalSerializer(approval).data
        }, status=status.HTTP_200_OK)
