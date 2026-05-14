"""
Enterprise Setup Script
Automates the setup of all enterprise features
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model

User = get_user_model()


def setup_database():
    """Create database tables"""
    print("📦 Creating database tables...")
    call_command('makemigrations')
    call_command('migrate')
    print("✅ Database tables created")


def create_superuser():
    """Create initial superuser"""
    print("\n👤 Creating superuser...")
    if not User.objects.filter(email='admin@betimes.com').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@betimes.com',
            password='Admin@123456',
            role='Super_Admin'
        )
        print("✅ Superuser created: admin@betimes.com / Admin@123456")
    else:
        print("ℹ️  Superuser already exists")


def create_sample_roles():
    """Create sample users for each role"""
    print("\n👥 Creating sample users for each role...")
    
    roles = [
        ('admin@betimes.com', 'Admin', 'Admin'),
        ('manager@betimes.com', 'Manager', 'Manager'),
        ('reviewer@betimes.com', 'Reviewer', 'Reviewer'),
        ('processor@betimes.com', 'Processor', 'Processor'),
        ('viewer@betimes.com', 'Viewer', 'Viewer'),
    ]
    
    for email, role, username in roles:
        if not User.objects.filter(email=email).exists():
            User.objects.create_user(
                username=username.lower(),
                email=email,
                password='Password@123',
                role=role
            )
            print(f"✅ Created {role}: {email} / Password@123")
        else:
            print(f"ℹ️  {role} user already exists")


def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        'media/uploads',
        'media/temp_uploads',
        'media/documents',
        'logs',
        'staticfiles',
    ]
    
    for directory in directories:
        path = os.path.join(os.path.dirname(__file__), directory)
        os.makedirs(path, exist_ok=True)
        print(f"✅ Created {directory}")


def collect_static():
    """Collect static files"""
    print("\n📦 Collecting static files...")
    call_command('collectstatic', '--noinput')
    print("✅ Static files collected")


def main():
    """Main setup function"""
    print("🚀 Betimes Enterprise Platform Setup")
    print("=" * 50)
    
    try:
        setup_database()
        create_directories()
        create_superuser()
        create_sample_roles()
        collect_static()
        
        print("\n" + "=" * 50)
        print("✅ Setup completed successfully!")
        print("\n📝 Next steps:")
        print("1. Start Redis: redis-server")
        print("2. Start Celery worker: celery -A config worker -l info")
        print("3. Start Celery beat: celery -A config beat -l info")
        print("4. Start Django: python manage.py runserver")
        print("\n🔐 Login credentials:")
        print("   Super Admin: admin@betimes.com / Admin@123456")
        print("   Admin: admin@betimes.com / Password@123")
        print("   Manager: manager@betimes.com / Password@123")
        print("   Reviewer: reviewer@betimes.com / Password@123")
        print("   Processor: processor@betimes.com / Password@123")
        print("   Viewer: viewer@betimes.com / Password@123")
        print("\n📚 API Documentation: http://localhost:8000/swagger/")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
