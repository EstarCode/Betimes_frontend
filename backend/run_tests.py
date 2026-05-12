#!/usr/bin/env python
"""
Comprehensive test runner for PDF Utility SaaS Platform.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('TESTING', '1')
django.setup()

from django.core.management import call_command
from django.test.utils import get_runner
from django.conf import settings


def run_tests():
    """Run all tests with coverage."""
    print("=" * 70)
    print("PDF Utility SaaS Platform - Test Suite")
    print("=" * 70)
    print()
    
    # Run Django system checks
    print("Running system checks...")
    call_command('check')
    print("[OK] System checks passed")
    print()
    
    # Run tests
    print("Running tests...")
    print("-" * 70)
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False, keepdb=False)
    
    failures = test_runner.run_tests([
        'apps.authentication.tests',
        'apps.compression.tests',
        'apps.conversion.tests',
        'apps.pdf_tools.tests',
        'apps.analytics.tests',
    ])
    
    print("-" * 70)
    print()
    
    if failures:
        print(f"[FAIL] Tests failed: {failures} failure(s)")
        sys.exit(1)
    else:
        print("[OK] All tests passed!")
        print()
        print("=" * 70)
        print("Test Summary:")
        print("  - Authentication: [OK]")
        print("  - Compression: [OK]")
        print("  - Conversion: [OK]")
        print("  - PDF Tools: [OK]")
        print("  - Analytics: [OK]")
        print("=" * 70)
        sys.exit(0)


if __name__ == '__main__':
    run_tests()

