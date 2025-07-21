#!/usr/bin/env python3
"""
Debug Setup Script for Bank Muamalat Health Monitor
Checks file structure and helps troubleshoot import issues
"""

import os
import sys
from pathlib import Path

def check_file_structure():
    """Check if all required files exist"""
    print("🔍 Checking file structure...")
    
    # Get current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check if we're in the right place
    if current_dir.name == "app":
        project_root = current_dir.parent
        app_dir = current_dir
        print("📍 Detected: Running from app/ directory")
    else:
        project_root = current_dir
        app_dir = current_dir / "app"
        print("📍 Detected: Running from project root")
    
    print(f"📁 Project root: {project_root}")
    print(f"📁 App directory: {app_dir}")
    
    # Files to check
    required_files = {
        "Authentication": app_dir / "security" / "auth.py",
        "Main Application": app_dir / "main.py",
        "UI Overview": project_root / "ui" / "pages" / "overview.py",
        "Decision Support": project_root / "ui" / "pages" / "decision_support.py",
        "Risk Assessment": project_root / "ui" / "pages" / "risk_assessment.py",
        "Compliance Monitoring": project_root / "ui" / "pages" / "compliance_monitoring.py",
        "Strategic Analysis": project_root / "ui" / "pages" / "strategic_analysis.py",
        "Financial Health": project_root / "ui" / "pages" / "financial_health.py",
    }
    
    # Check __init__.py files
    init_files = {
        "UI Package Init": project_root / "ui" / "__init__.py",
        "Pages Package Init": project_root / "ui" / "pages" / "__init__.py",
    }
    
    print("\n📋 Required Files Check:")
    all_good = True
    
    for name, filepath in required_files.items():
        if filepath.exists():
            print(f"✅ {name}: {filepath}")
        else:
            print(f"❌ {name}: {filepath} (NOT FOUND)")
            all_good = False
    
    print("\n📦 Package Init Files:")
    for name, filepath in init_files.items():
        if filepath.exists():
            print(f"✅ {name}: {filepath}")
        else:
            print(f"❌ {name}: {filepath} (NOT FOUND)")
            if not filepath.exists():
                print(f"   💡 Creating: {filepath}")
                try:
                    filepath.parent.mkdir(parents=True, exist_ok=True)
                    filepath.write_text("# Package initialization\n")
                    print(f"   ✅ Created: {filepath}")
                except Exception as e:
                    print(f"   ❌ Failed to create: {e}")
                    all_good = False
    
    return all_good, project_root

def check_function_exports():
    """Check if required functions exist in UI modules"""
    print("\n🔍 Checking function exports...")
    
    # Add project root to Python path
    _, project_root = check_file_structure()
    sys.path.insert(0, str(project_root))
    
    modules_to_check = {
        "overview": "show_overview",
        "decision_support": "show_decision_support", 
        "risk_assessment": "show_risk_assessment",
        "compliance_monitoring": "show_compliance_monitoring",
        "strategic_analysis": "show_strategic_analysis",
        "financial_health": "show_financial_health",
    }
    
    for module_short_name, function_name in modules_to_check.items():
        module_name = f"ui.pages.{module_short_name}"
        file_path = project_root / "ui" / "pages" / f"{module_short_name}.py"
        
        print(f"\n🔍 Checking {module_name}:")
        
        # First, check if file content contains the function
        if file_path.exists():
            content = file_path.read_text(encoding='utf-8')
            if f"def {function_name}" in content:
                print(f"   ✅ Function '{function_name}' found in file")
            else:
                print(f"   ❌ Function '{function_name}' NOT found in file")
                print(f"   📄 File content preview (first 10 lines):")
                lines = content.split('\n')[:10]
                for i, line in enumerate(lines, 1):
                    print(f"   {i:2d}: {line[:80]}")
                if len(lines) == 10:
                    total_lines = len(content.split('\n'))
                    if total_lines > 10:
                        print(f"   ... (truncated, total lines: {total_lines})")
                continue
        
        # Try to import the module
        try:
            module = __import__(module_name, fromlist=[function_name])
            if hasattr(module, function_name):
                print(f"   ✅ {module_name}.{function_name} - Import successful")
            else:
                print(f"   ❌ {module_name}.{function_name} - Function not found after import")
                available_funcs = [name for name in dir(module) if not name.startswith('_')]
                print(f"   📋 Available functions in module: {available_funcs}")
        except ImportError as e:
            print(f"   ❌ {module_name} - Import error: {e}")
        except SyntaxError as e:
            print(f"   ❌ {module_name} - Syntax error: {e}")
        except Exception as e:
            print(f"   ❌ {module_name} - Other error: {e}")

def analyze_individual_files():
    """Analyze each file individually to find issues"""
    print("\n🔬 Analyzing individual files...")
    
    _, project_root = check_file_structure()
    pages_dir = project_root / "ui" / "pages"
    
    files_to_check = [
        "overview.py",
        "decision_support.py", 
        "risk_assessment.py",
        "compliance_monitoring.py",
        "strategic_analysis.py",
        "financial_health.py",
    ]
    
    for filename in files_to_check:
        file_path = pages_dir / filename
        print(f"\n📄 Analyzing {filename}:")
        
        if not file_path.exists():
            print(f"   ❌ File does not exist")
            continue
            
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            print(f"   📊 File size: {len(content)} characters, {len(lines)} lines")
            
            # Check for function definitions
            functions = []
            for i, line in enumerate(lines):
                if line.strip().startswith('def '):
                    func_name = line.strip().split('(')[0].replace('def ', '')
                    functions.append(f"{func_name} (line {i+1})")
            
            if functions:
                print(f"   ✅ Functions found: {', '.join(functions)}")
            else:
                print(f"   ❌ No functions found")
            
            # Check for syntax errors
            try:
                compile(content, str(file_path), 'exec')
                print(f"   ✅ Syntax is valid")
            except SyntaxError as e:
                print(f"   ❌ Syntax error at line {e.lineno}: {e.msg}")
                if e.lineno and e.lineno <= len(lines):
                    print(f"   📍 Problematic line: {lines[e.lineno-1]}")
            
            # Check imports
            imports = [line.strip() for line in lines if line.strip().startswith(('import ', 'from '))]
            if imports:
                print(f"   📦 Imports: {len(imports)} import statements")
                for imp in imports[:3]:  # Show first 3 imports
                    print(f"      - {imp}")
                if len(imports) > 3:
                    print(f"      - ... and {len(imports)-3} more")
                    
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")

def fix_common_issues():
    """Try to fix common issues automatically"""
    print("\n🔧 Attempting to fix common issues...")
    
    _, project_root = check_file_structure()
    pages_dir = project_root / "ui" / "pages"
    
    # Check and fix __init__.py files
    print("🔧 Checking __init__.py files...")
    
    ui_init = project_root / "ui" / "__init__.py"
    if not ui_init.exists() or ui_init.stat().st_size == 0:
        print("   📝 Creating/fixing ui/__init__.py")
        ui_init.write_text('"""UI Package"""\n__version__ = "1.0.0"\n', encoding='utf-8')
    
    pages_init = project_root / "ui" / "pages" / "__init__.py"
    init_content = '''"""
Pages Package Initialization
"""
# Empty init file to avoid import issues
__version__ = "1.0.0"
'''
    print("   📝 Creating clean ui/pages/__init__.py")
    pages_init.write_text(init_content, encoding='utf-8')
    
    # Check each module file
    expected_functions = {
        "overview.py": "show_overview",
        "decision_support.py": "show_decision_support",
        "risk_assessment.py": "show_risk_assessment", 
        "compliance_monitoring.py": "show_compliance_monitoring",
        "strategic_analysis.py": "show_strategic_analysis",
        "financial_health.py": "show_financial_health",
    }
    
    for filename, expected_func in expected_functions.items():
        file_path = pages_dir / filename
        
        if file_path.exists():
            content = file_path.read_text(encoding='utf-8')
            if f"def {expected_func}" not in content:
                print(f"   ⚠️ {filename} missing function {expected_func}")
                # Add the missing function at the end
                func_title = filename.replace('.py', '').replace('_', ' ').title()
                missing_func = f'''

def {expected_func}():
    """Auto-generated function - please customize this"""
    import streamlit as st
    st.markdown("## {func_title}")
    st.info("This page is under development. Please add your content here.")
    
    # Sample content for demonstration
    st.write("Please add your custom content here.")

'''
                try:
                    file_path.write_text(content + missing_func, encoding='utf-8')
                    print(f"   ✅ Added missing function {expected_func} to {filename}")
                except Exception as e:
                    print(f"   ❌ Failed to add function to {filename}: {e}")
        else:
            print(f"   📝 Creating missing file {filename}")
            generate_missing_functions()  # This will create the missing file

def generate_missing_functions():
    """Generate template functions for missing modules"""
    print("\n🔧 Generating template functions...")
    
    _, project_root = check_file_structure()
    pages_dir = project_root / "ui" / "pages"
    
    templates = {
        "overview.py": '''import streamlit as st

def show_overview():
    """Portfolio Overview Page"""
    st.markdown("## Portfolio Overview")
    st.info("This is the overview page. Add your portfolio overview code here.")
    
    # Sample content
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Assets", "Rp 50.2B", "2.1%")
    with col2:
        st.metric("Risk Score", "3.2/5", "-0.1")
    with col3:
        st.metric("Shariah Compliance", "98.5%", "0.2%")

if __name__ == "__main__":
    show_overview()
''',
        "decision_support.py": '''import streamlit as st

def show_decision_support():
    """Decision Support System Page"""
    st.markdown("## Decision Support System")
    st.info("This is the decision support page. Add your decision support tools here.")
    
    # Sample content
    st.markdown("### Investment Recommendations")
    st.write("AI-powered investment recommendations and portfolio optimization tools.")

if __name__ == "__main__":
    show_decision_support()
''',
        "risk_assessment.py": '''import streamlit as st

def show_risk_assessment():
    """Risk Assessment Page"""
    st.markdown("## Risk Assessment")
    st.info("This is the risk assessment page. Add your risk analysis tools here.")
    
    # Sample content
    st.markdown("### Risk Analysis")
    st.write("Comprehensive risk modeling and stress testing tools.")

if __name__ == "__main__":
    show_risk_assessment()
''',
        "compliance_monitoring.py": '''import streamlit as st

def show_compliance_monitoring():
    """Compliance Monitoring Page"""
    st.markdown("## Compliance Monitoring")
    st.info("This is the compliance monitoring page. Add your Shariah compliance tools here.")
    
    # Sample content
    st.markdown("### Shariah Compliance Status")
    st.write("Real-time Islamic finance compliance monitoring and reporting.")

if __name__ == "__main__":
    show_compliance_monitoring()
''',
        "strategic_analysis.py": '''import streamlit as st

def show_strategic_analysis():
    """Strategic Analysis Page"""
    st.markdown("## Strategic Analysis")
    st.info("This is the strategic analysis page. Add your strategic planning tools here.")
    
    # Sample content
    st.markdown("### Strategic Planning")
    st.write("Long-term strategic analysis and optimization tools.")

if __name__ == "__main__":
    show_strategic_analysis()
''',
        "financial_health.py": '''import streamlit as st

def show_financial_health():
    """Financial Health Assessment Page"""
    st.markdown("## Financial Health Assessment")
    st.info("This is the financial health page. Add your health assessment tools here.")
    
    # Sample content
    st.markdown("### Overall Health Score")
    st.write("Comprehensive financial health assessment and scoring.")

if __name__ == "__main__":
    show_financial_health()
'''
    }
    
    pages_dir.mkdir(parents=True, exist_ok=True)
    
    for filename, content in templates.items():
        filepath = pages_dir / filename
        if not filepath.exists():
            print(f"📝 Creating template: {filepath}")
            try:
                filepath.write_text(content, encoding='utf-8')
                print(f"✅ Successfully created: {filename}")
            except Exception as e:
                print(f"❌ Failed to create {filename}: {e}")
        else:
            print(f"✅ Already exists: {filepath}")

def main():
    """Main debug function"""
    print("🏦 Bank Muamalat Health Monitor - Debug Setup")
    print("=" * 60)
    
    # Check file structure
    all_good, _ = check_file_structure()
    
    # Analyze individual files first
    analyze_individual_files()
    
    # Try to fix common issues
    fix_common_issues()
    
    # Check function exports after fixes
    check_function_exports()
    
    # Generate missing functions if needed
    if not all_good:
        print("\n⚠️ Some files are missing. Generating templates...")
        generate_missing_functions()
        print("\n✅ Template files created. Please customize them with your actual code.")
    
    print("\n" + "=" * 60)
    print("🚀 Next Steps:")
    print("1. ✅ Debug script completed")
    print("2. 🔧 Check any syntax errors reported above")
    print("3. 📝 Ensure each file has the correct function name:")
    print("   - overview.py → show_overview()")
    print("   - decision_support.py → show_decision_support()")
    print("   - risk_assessment.py → show_risk_assessment()")
    print("   - compliance_monitoring.py → show_compliance_monitoring()")
    print("   - strategic_analysis.py → show_strategic_analysis()")
    print("   - financial_health.py → show_financial_health()")
    print("4. 🚀 Run: streamlit run app/main.py")
    print("5. 🔍 Check '🔧 Debug Info' in sidebar to verify module loading")
    print("=" * 60)

if __name__ == "__main__":
    main()