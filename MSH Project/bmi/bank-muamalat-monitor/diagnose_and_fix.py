#!/usr/bin/env python3
"""
Diagnose and Fix UI Modules
Show actual content and fix function naming issues
"""

import os
from pathlib import Path
import re

def show_file_details(filename, expected_function):
    """Show detailed analysis of a file"""
    project_root = Path.cwd()
    file_path = project_root / "ui" / "pages" / filename
    
    print(f"\n" + "="*60)
    print(f"📄 ANALYZING: {filename}")
    print(f"🎯 EXPECTED: {expected_function}()")
    print("="*60)
    
    if not file_path.exists():
        print("❌ FILE NOT FOUND")
        return None
    
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        print(f"📊 File Info:")
        print(f"   Size: {len(content)} characters")
        print(f"   Lines: {len(lines)}")
        
        # Find all functions
        functions = []
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('def ') and not stripped.startswith('def _'):
                func_name = stripped.split('(')[0].replace('def ', '')
                functions.append((func_name, i+1, stripped))
        
        print(f"\n🔍 Functions Found ({len(functions)}):")
        if functions:
            for func_name, line_no, full_def in functions:
                marker = "✅" if func_name == expected_function else "📝"
                print(f"   {marker} {func_name} (line {line_no})")
                print(f"      {full_def}")
        else:
            print("   ❌ No functions found")
        
        # Check for main execution
        main_patterns = [
            "if __name__",
            "streamlit.run",
            "st.title",
            "st.markdown",
            "st.write"
        ]
        
        main_code_lines = []
        for i, line in enumerate(lines):
            if any(pattern in line for pattern in main_patterns):
                main_code_lines.append((i+1, line.strip()))
        
        if main_code_lines:
            print(f"\n🎯 Main Code Found ({len(main_code_lines)} lines):")
            for line_no, line in main_code_lines[:5]:  # Show first 5
                print(f"   {line_no:3d}: {line[:70]}")
            if len(main_code_lines) > 5:
                print(f"   ... and {len(main_code_lines)-5} more lines")
        
        # Show file content preview
        print(f"\n📄 Full File Content:")
        print("-" * 50)
        for i, line in enumerate(lines, 1):
            print(f"{i:3d}: {line}")
        print("-" * 50)
        
        return {
            'content': content,
            'lines': lines,
            'functions': functions,
            'main_code_lines': main_code_lines
        }
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

def create_function_fix(filename, expected_function, analysis):
    """Create the missing function based on analysis"""
    project_root = Path.cwd()
    file_path = project_root / "ui" / "pages" / filename
    
    if not analysis:
        return False
    
    content = analysis['content']
    functions = analysis['functions']
    
    # Check if function already exists
    existing_func = None
    for func_name, line_no, full_def in functions:
        if func_name == expected_function:
            print(f"   ✅ Function {expected_function} already exists!")
            return True
    
    print(f"\n🔧 Creating function {expected_function} for {filename}")
    
    # Strategy 1: If there's an existing main-like function, create alias
    main_like_functions = []
    for func_name, line_no, full_def in functions:
        if any(keyword in func_name.lower() for keyword in ['main', 'run', 'start', 'display', 'show']):
            main_like_functions.append(func_name)
    
    if main_like_functions:
        existing_func = main_like_functions[0]
        print(f"   🔗 Creating alias to existing function: {existing_func}")
        
        alias_code = f'''

def {expected_function}():
    """Main function for {filename.replace('.py', '').replace('_', ' ').title()} module"""
    return {existing_func}()
'''
    
    # Strategy 2: If there's a main block, wrap it in function
    elif analysis['main_code_lines']:
        print(f"   🎁 Wrapping main code in function")
        
        # Find the main block
        main_start = None
        for line_no, line in analysis['main_code_lines']:
            if 'if __name__' in line:
                main_start = line_no - 1  # Convert to 0-based index
                break
        
        if main_start is not None:
            lines = analysis['lines']
            
            # Extract code from main block
            main_code = []
            in_main = False
            
            for i in range(main_start + 1, len(lines)):
                line = lines[i]
                if not line.strip():
                    if in_main:
                        main_code.append("")
                    continue
                
                indent = len(line) - len(line.lstrip())
                if indent > 0 and not in_main:
                    in_main = True
                    main_code.append(line[4:])  # Remove 4 spaces of indent
                elif in_main:
                    if indent >= 4:
                        main_code.append(line[4:])
                    else:
                        break
            
            if main_code:
                alias_code = f'''

def {expected_function}():
    """Main function for {filename.replace('.py', '').replace('_', ' ').title()} module"""
    # Wrapped main code
'''
                for code_line in main_code:
                    alias_code += f"    {code_line}\n"
            else:
                alias_code = f'''

def {expected_function}():
    """Main function for {filename.replace('.py', '').replace('_', ' ').title()} module"""
    import streamlit as st
    st.error("Could not auto-wrap main code. Please implement this function manually.")
'''
        else:
            alias_code = f'''

def {expected_function}():
    """Main function for {filename.replace('.py', '').replace('_', ' ').title()} module"""
    import streamlit as st
    st.error("Could not find main code. Please implement this function manually.")
'''
    
    # Strategy 3: Create placeholder
    else:
        print(f"   📝 Creating placeholder function")
        alias_code = f'''

def {expected_function}():
    """Main function for {filename.replace('.py', '').replace('_', ' ').title()} module"""
    import streamlit as st
    st.error("This module needs manual implementation. Please add your code to this function.")
    st.info("Available functions in this module: {[f[0] for f in functions]}")
'''
    
    # Add the function to the file
    new_content = content + alias_code
    
    # Create backup
    backup_path = file_path.with_suffix('.py.backup')
    backup_path.write_text(content, encoding='utf-8')
    print(f"   💾 Backup created: {backup_path}")
    
    # Write new content
    file_path.write_text(new_content, encoding='utf-8')
    print(f"   ✅ Added function {expected_function}")
    
    return True

def main():
    """Main diagnostic function"""
    print("🔍 DIAGNOSE AND FIX UI MODULES")
    print("="*60)
    print("This script will show you exactly what's in each file")
    print("and fix the function naming issues.")
    print("\n⚠️ Files will be backed up before modification.")
    
    files_to_fix = {
        "overview.py": "show_overview",
        "decision_support.py": "show_decision_support", 
        "risk_assessment.py": "show_risk_assessment",
        "compliance_monitoring.py": "show_compliance_monitoring",
        "strategic_analysis.py": "show_strategic_analysis",
        "financial_health.py": "show_financial_health",
    }
    
    print(f"\n🔍 STEP 1: DETAILED ANALYSIS")
    print("="*60)
    
    # First, show all file contents
    analyses = {}
    for filename, expected_func in files_to_fix.items():
        analyses[filename] = show_file_details(filename, expected_func)
    
    print(f"\n" + "="*60)
    print(f"🔧 STEP 2: APPLYING FIXES")
    print("="*60)
    
    fixed_count = 0
    for filename, expected_func in files_to_fix.items():
        if analyses[filename]:
            print(f"\n🛠️ Fixing {filename}:")
            if create_function_fix(filename, expected_func, analyses[filename]):
                fixed_count += 1
        else:
            print(f"\n❌ Skipping {filename} (could not analyze)")
    
    print(f"\n" + "="*60)
    print(f"🎉 SUMMARY")
    print("="*60)
    print(f"✅ Fixed {fixed_count}/{len(files_to_fix)} files")
    print(f"💾 Backups created for all modified files")
    
    print(f"\n📋 NEXT STEPS:")
    print(f"1. Review the fixes in your files")
    print(f"2. Customize the auto-generated functions if needed")
    print(f"3. Run: streamlit run app/main.py")
    print(f"4. Check Debug Info to verify all modules load")
    
    print(f"\n🎯 If you see errors, check the function implementations")
    print(f"   and make sure they call your actual code correctly.")

if __name__ == "__main__":
    main()