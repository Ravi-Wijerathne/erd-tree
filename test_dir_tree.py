#!/usr/bin/env python3
"""
Test script for Directory Tree Generator cross-platform functionality
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the current directory to Python path to import dir_tree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import dir_tree
    print("✓ Successfully imported dir_tree module")
except ImportError as e:
    print(f"✗ Failed to import dir_tree: {e}")
    sys.exit(1)

def test_os_detection():
    """Test OS detection"""
    print(f"✓ Detected OS: {dir_tree.CURRENT_OS}")
    return True

def test_tree_generation():
    """Test tree generation functionality"""
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test structure
        test_dir = Path(temp_dir) / "test_project"
        test_dir.mkdir()

        (test_dir / "README.md").write_text("# Test Project")
        (test_dir / "src").mkdir()
        (test_dir / "src" / "main.py").write_text("print('Hello World')")
        (test_dir / "src" / "utils").mkdir()
        (test_dir / "src" / "utils" / "helper.py").write_text("def helper(): pass")

        # Test tree generation
        output_file = test_dir / "tree.txt"
        success = dir_tree.generate_tree(str(test_dir), str(output_file), "text")

        if success and output_file.exists():
            print("✓ Tree generation successful")
            with open(output_file, 'r') as f:
                content = f.read()
                if "test_project" in content and "README.md" in content:
                    print("✓ Tree content looks correct")
                    return True
                else:
                    print("✗ Tree content incorrect")
                    return False
        else:
            print("✗ Tree generation failed")
            return False

def main():
    """Run all tests"""
    print("Running Directory Tree Generator Tests...")
    print("=" * 50)

    tests = [
        ("OS Detection", test_os_detection),
        ("Tree Generation", test_tree_generation),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}")

    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Cross-platform functionality is working.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())