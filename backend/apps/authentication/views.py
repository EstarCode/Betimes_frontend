"""
Views for authentication.
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """API endpoint for user registration."""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'success': True,
            'message': 'User registered successfully',
            'data': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token view with user data."""
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response({
            'success': True,
            'message': 'Login successful',
            'data': serializer.validated_data
        }, status=status.HTTP_200_OK)



class UserProfileView(generics.RetrieveUpdateAPIView):
    """API endpoint for user profile."""
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Profile retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'success': True,
            'message': 'Profile updated successfully',
            'data': serializer.data
        })


class PasswordResetRequestView(generics.GenericAPIView):
    """API endpoint for password reset request."""
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # TODO: Implement email sending logic
        # For now, just return success
        
        return Response({
            'success': True,
            'message': 'Password reset email sent successfully'
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    """API endpoint for password reset confirmation."""
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # TODO: Implement token validation and password reset logic
        
        return Response({
            'success': True,
            'message': 'Password reset successfully'
        }, status=status.HTTP_200_OK)


# MFA Views
from .mfa_service import MFAService


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mfa_setup(request):
    """
    Setup MFA for user
    
    POST /api/v1/auth/mfa/setup/
    """
    mfa_service = MFAService()
    result = mfa_service.setup_totp(request.user)
    
    if result['success']:
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': result.get('error', 'MFA setup failed')},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mfa_verify_setup(request):
    """
    Verify MFA setup with token
    
    POST /api/v1/auth/mfa/verify-setup/
    Body: {"token": "123456"}
    """
    token = request.data.get('token')
    if not token:
        return Response(
            {'error': 'Token required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    mfa_service = MFAService()
    success = mfa_service.verify_totp_setup(request.user, token)
    
    if success:
        return Response({
            'success': True,
            'message': 'MFA enabled successfully'
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mfa_disable(request):
    """
    Disable MFA for user
    
    POST /api/v1/auth/mfa/disable/
    Body: {"password": "user_password"}
    """
    password = request.data.get('password')
    if not password or not request.user.check_password(password):
        return Response(
            {'error': 'Invalid password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    mfa_service = MFAService()
    success = mfa_service.disable_mfa(request.user)
    
    if success:
        return Response({
            'success': True,
            'message': 'MFA disabled successfully'
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Failed to disable MFA'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mfa_regenerate_backup_codes(request):
    """
    Regenerate backup codes
    
    POST /api/v1/auth/mfa/regenerate-backup-codes/
    """
    mfa_service = MFAService()
    codes = mfa_service.regenerate_backup_codes(request.user)
    
    if codes:
        return Response({
            'success': True,
            'backup_codes': codes
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Failed to regenerate backup codes'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def mfa_verify_login(request):
    """
    Verify MFA token during login
    
    POST /api/v1/auth/mfa/verify-login/
    Body: {"email": "user@example.com", "token": "123456", "use_backup": false}
    """
    email = request.data.get('email')
    token = request.data.get('token')
    use_backup = request.data.get('use_backup', False)
    
    if not email or not token:
        return Response(
            {'error': 'Email and token required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    mfa_service = MFAService()
    
    if use_backup:
        success = mfa_service.verify_backup_code(user, token)
    else:
        success = mfa_service.verify_totp(user, token)
    
    if success:
        # Generate JWT tokens
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_401_UNAUTHORIZED
        )
