"""
Role-Based Access Control (RBAC) Permissions
Defines granular permissions for each role
"""

ROLE_PERMISSIONS = {
    'Super_Admin': ['*'],  # All permissions
    
    'Admin': [
        # User management
        'users.create', 'users.read', 'users.update', 'users.delete',
        'users.assign_role', 'users.manage_permissions',
        
        # Workflow management
        'workflows.create', 'workflows.read', 'workflows.update', 'workflows.delete',
        'workflows.assign', 'workflows.manage_templates',
        
        # System management
        'system.configure', 'system.monitor', 'system.manage_settings',
        
        # Audit access
        'audit.read', 'audit.export',
        
        # Document management
        'documents.read', 'documents.create', 'documents.update', 'documents.delete',
        'documents.download', 'documents.share',
        
        # Processing
        'processing.create', 'processing.read', 'processing.cancel',
    ],
    
    'Manager': [
        # Document management
        'documents.read', 'documents.create', 'documents.update', 'documents.delete',
        'documents.download', 'documents.share',
        
        # Workflow management
        'workflows.create', 'workflows.read', 'workflows.approve', 'workflows.reject',
        
        # Team management
        'team.read', 'team.documents.read',
        
        # Processing
        'processing.create', 'processing.read',
        
        # Dashboard
        'dashboard.read', 'dashboard.team_metrics',
    ],
    
    'Reviewer': [
        # Document viewing
        'documents.read', 'documents.download',
        
        # Workflow participation
        'workflows.read', 'workflows.approve', 'workflows.reject', 'workflows.comment',
        
        # Dashboard
        'dashboard.read',
    ],
    
    'Processor': [
        # Document management
        'documents.create', 'documents.read', 'documents.update', 'documents.download',
        
        # Processing
        'processing.create', 'processing.read', 'processing.monitor',
        
        # Dashboard
        'dashboard.read',
    ],
    
    'Viewer': [
        # Document viewing only
        'documents.read',
        
        # Dashboard
        'dashboard.read',
    ],
}


def has_permission(user, permission):
    """
    Check if a user has a specific permission
    
    Args:
        user: User instance
        permission: Permission string (e.g., 'documents.create')
    
    Returns:
        bool: True if user has permission
    """
    if not user or not user.is_authenticated:
        return False
    
    user_permissions = ROLE_PERMISSIONS.get(user.role, [])
    
    # Super Admin has all permissions
    if '*' in user_permissions:
        return True
    
    return permission in user_permissions


def get_user_permissions(user):
    """
    Get all permissions for a user
    
    Args:
        user: User instance
    
    Returns:
        list: List of permission strings
    """
    if not user or not user.is_authenticated:
        return []
    
    return ROLE_PERMISSIONS.get(user.role, [])


def require_permission(permission):
    """
    Decorator to require a specific permission for a view
    
    Usage:
        @require_permission('documents.create')
        def create_document(request):
            ...
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not has_permission(request.user, permission):
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied(f"Permission denied: {permission}")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
