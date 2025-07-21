#!/usr/bin/env python3
"""
Quick Fix for UI Modules
Simple script to check and fix existing modules
"""

import os
from pathlib import Path

def check_file_content(filename):
    """Check what's in the file"""
    project_root = Path.cwd()
    file_path = project_root / "ui" / "pages" / filename
    
    print(f"\n📄 Checking {filename}:")
    print(f"   Path: {file_path}")
    
    if not file_path.exists():
        print("   ❌ File does not exist")
        return
    
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        print(f"   📊 File size: {len(content)} characters, {len(lines)} lines")
        
        # Find all function definitions
        functions = []
        for i, line in enumerate(lines):
            if line.strip().startswith('def '):
                func_name = line.strip().split('(')[0].replace('def ', '')
                functions.append((func_name, i+1))
        
        print(f"   🔍 Functions found ({len(functions)}):")
        for func_name, line_no in functions:
            print(f"      - {func_name} (line {line_no})")
        
        # Check for template content
        if "This page is under development" in content:
            print("   ⚠️ Contains template/placeholder content")
        
        # Show last 20 lines (where debug script adds functions)
        print(f"   📄 Last 10 lines:")
        for i, line in enumerate(lines[-10:], len(lines)-9):
            print(f"      {i:3d}: {line[:80]}")
        
        return content, lines, functions
        
    except Exception as e:
        print(f"   ❌ Error reading file: {e}")
        return None, None, None

def remove_template_functions(filename, expected_function):
    """Remove auto-generated template functions"""
    project_root = Path.cwd()
    file_path = project_root / "ui" / "pages" / filename
    
    if not file_path.exists():
        return False
    
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Look for the auto-generated function
        template_markers = [
            "Auto-generated function - please customize this",
            "This page is under development. Please add your content here.",
            f"def {expected_function}():"
        ]
        
        # Find lines to remove
        lines_to_remove = []
        in_template_function = False
        template_start = None
        
        for i, line in enumerate(lines):
            # Check if this line starts an auto-generated function
            if any(marker in line for marker in template_markers):
                if f"def {expected_function}():" in line:
                    template_start = i
                    in_template_function = True
                elif "Auto-generated function" in line:
                    in_template_function = True
                    if template_start is None:
                        # Find the function definition above this comment
                        for j in range(i-1, -1, -1):
                            if lines[j].strip().startswith('def '):
                                template_start = j
                                break
            
            if in_template_function:
                lines_to_remove.append(i)
                
                # Check if we've reached the end of the function
                if line.strip() and not line.startswith(' ') and not line.startswith('\t') and i > template_start:
                    if not line.strip().startswith('def ') and not line.strip().startswith('"""') and not line.strip().startswith('"""'):
                        # This line is not part of the function
                        lines_to_remove.pop()  # Don't remove this line
                        in_template_function = False
        
        if lines_to_remove:
            print(f"   🗑️ Removing template function from lines {min(lines_to_remove)}-{max(lines_to_remove)}")
            
            # Create backup
            backup_path = file_path.with_suffix('.py.backup')
            backup_path.write_text(content, encoding='utf-8')
            print(f"   💾 Created backup: {backup_path}")
            
            # Remove the lines
            new_lines = [line for i, line in enumerate(lines) if i not in lines_to_remove]
            new_content = '\n'.join(new_lines)
            
            # Clean up multiple empty lines at the end
            new_content = new_content.rstrip() + '\n'
            
            file_path.write_text(new_content, encoding='utf-8')
            print(f"   ✅ Removed template function")
            return True
        else:
            print(f"   ℹ️ No template function found to remove")
            return False
            
    except Exception as e:
        print(f"   ❌ Error processing file: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Quick Fix for UI Modules")
    print("=" * 40)
    print("This script will help you fix modules that show template content")
    print("instead of your actual code.\n")
    
    files_to_check = {
        "strategic_analysis.py": "show_strategic_analysis",
        "decision_support.py": "show_decision_support",
        "risk_assessment.py": "show_risk_assessment",
        "compliance_monitoring.py": "show_compliance_monitoring",
        "overview.py": "show_overview",
        "financial_health.py": "show_financial_health",
    }
    
    print("🔍 Step 1: Analyzing current files...")
    
    for filename, expected_func in files_to_check.items():
        content, lines, functions = check_file_content(filename)
        
        if content and "This page is under development" in content:
            print(f"\n🔧 Step 2: Fixing {filename}...")
            remove_template_functions(filename, expected_func)
    
    print(f"\n" + "="*40)
    print("🎉 Quick fix completed!")
    print("\n📝 What to do next:")
    print("1. Check your files in ui/pages/ to see if original content is restored")
    print("2. If your original files don't have the expected function names:")
    print("   - Rename your main function to match the expected name")
    print("   - Or add an alias function like this:")
    print("   def show_strategic_analysis():")
    print("       return your_original_function()")
    print("3. Run: streamlit run app/main.py")
    print("4. Check Debug Info in sidebar to verify all modules load")
    
    print(f"\n🎯 Expected function names:")
    for filename, expected_func in files_to_check.items():
        print(f"   - {filename} → {expected_func}()")

if __name__ == "__main__":
    main()