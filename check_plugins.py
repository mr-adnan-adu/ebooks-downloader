import os
import ast
import sys

def check_plugin_syntax(file_path):
    """Check if a Python file has syntax errors"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse the file
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def check_for_tilde_operator(file_path):
    """Check for potential misuse of ~ operator"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        issues = []
        for i, line in enumerate(lines, 1):
            if '~' in line:
                # Check if it's likely a problematic usage
                if '~filters' in line or '~F' in line:
                    issues.append(f"Line {i}: {line.strip()}")
        
        return issues
    except Exception:
        return []

def main():
    plugins_dir = "plugins"
    
    if not os.path.exists(plugins_dir):
        print(f"❌ {plugins_dir} directory not found!")
        return
    
    print("🔍 Checking plugin files for syntax errors...")
    print("=" * 50)
    
    total_files = 0
    error_files = 0
    
    for root, dirs, files in os.walk(plugins_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                total_files += 1
                
                # Check syntax
                is_valid, error = check_plugin_syntax(file_path)
                
                if not is_valid:
                    error_files += 1
                    print(f"❌ {file_path}")
                    print(f"   Error: {error}")
                    
                    # Check for tilde operator issues
                    tilde_issues = check_for_tilde_operator(file_path)
                    if tilde_issues:
                        print(f"   Potential ~ operator issues:")
                        for issue in tilde_issues:
                            print(f"     {issue}")
                    print()
                else:
                    print(f"✅ {file_path}")
    
    print("=" * 50)
    print(f"📊 Summary: {total_files} files checked, {error_files} errors found")
    
    if error_files > 0:
        print(f"\n🔧 Fix the files marked with ❌ to resolve the bot errors")
        print("Common fixes:")
        print("1. Replace ~filters.text with filters.text")
        print("2. Replace ~F with F")
        print("3. Check for any other misused ~ operators")

if __name__ == "__main__":
    main()
