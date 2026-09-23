#!/usr/bin/env python3
"""
HTML Quality Check Script
Validates generated HTML files for common issues before delivery.
"""

import re
import sys
import json
from pathlib import Path


class HTMLChecker:
    """Validates HTML files for quality and safety issues."""

    def __init__(self, html_path: str):
        self.html_path = Path(html_path)
        self.errors = []
        self.warnings = []

    def check_all(self) -> dict:
        """Run all checks and return a report."""
        if not self.html_path.exists():
            return {
                'status': 'error',
                'message': f'File not found: {self.html_path}',
                'errors': [],
                'warnings': []
            }

        with open(self.html_path, 'r', encoding='utf-8') as f:
            self.content = f.read()

        # Run all checks
        self._check_file_structure()
        self._check_forbidden_patterns()
        self._check_template_markers()
        self._check_sensitive_data_leaks()
        self._check_basic_accessibility()

        status = 'pass' if len(self.errors) == 0 else 'fail'
        
        return {
            'status': status,
            'file': str(self.html_path),
            'errors': self.errors,
            'warnings': self.warnings,
            'error_count': len(self.errors),
            'warning_count': len(self.warnings)
        }

    def _check_file_structure(self):
        """Check basic HTML structure."""
        if not re.search(r'<!doctype\s+html', self.content, re.IGNORECASE):
            self.errors.append('Missing DOCTYPE declaration')
        
        if not re.search(r'<html[^>]*>', self.content, re.IGNORECASE):
            self.errors.append('Missing <html> tag')
        
        if not re.search(r'<head>', self.content, re.IGNORECASE):
            self.errors.append('Missing <head> section')
        
        if not re.search(r'<body>', self.content, re.IGNORECASE):
            self.errors.append('Missing <body> section')
        
        if not re.search(r'<title[^>]*>.*?</title>', self.content, re.IGNORECASE | re.DOTALL):
            self.warnings.append('Missing or empty <title> tag')

    def _check_forbidden_patterns(self):
        """Check for patterns that should not appear in delivered HTML."""
        forbidden = [
            (r'file://', 'Do not ship file:// references'),
            (r'\bblob:', 'Do not ship Blob URL references'),
            (r'\blocalhost\b|127\.0\.0\.1|0\.0\.0\.0', 'Do not ship temporary server references'),
        ]
        
        for pattern, message in forbidden:
            if re.search(pattern, self.content, re.IGNORECASE):
                self.errors.append(f'{message}')

    def _check_template_markers(self):
        """Check for leftover template markers."""
        template_patterns = [
            r'\{\{[A-Z_]+\}\}',  # {{TITLE}}
            r'\{%.*?%\}',        # {% if %}
            r'<%.*?%>',          # <% variable %>
        ]
        
        for pattern in template_patterns:
            matches = re.findall(pattern, self.content)
            if matches:
                self.errors.append(f'Unreplaced template markers found: {matches[:3]}...')

    def _check_sensitive_data_leaks(self):
        """Check for obvious sensitive data that should have been sanitized."""
        # This is a basic heuristic check - the main sanitization should happen earlier
        suspicious = [
            (r'password\s*[:=]\s*["\']?[a-zA-Z0-9_@#$%^&*]{6,}["\']?', 'Potential password value exposed'),
            (r'secret\s*[:=]\s*["\']?[a-zA-Z0-9_@#$%^&*]{8,}["\']?', 'Potential secret value exposed'),
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID detected'),
            (r'sk-[a-zA-Z0-9]{20,}', 'API key (sk-) detected'),
        ]
        
        for pattern, message in suspicious:
            if re.search(pattern, self.content, re.IGNORECASE):
                self.warnings.append(f'{message} - verify this is intentional')

    def _check_basic_accessibility(self):
        """Basic accessibility checks."""
        # Check for lang attribute on html
        if not re.search(r'<html[^>]*\slang=["\'][a-z]{2}', self.content, re.IGNORECASE):
            self.warnings.append('Consider adding lang attribute to <html> tag')
        
        # Check viewport meta
        if not re.search(r'<meta[^>]*name=["\']viewport["\']', self.content, re.IGNORECASE):
            self.warnings.append('Missing viewport meta tag for responsive design')


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python check_html.py <html_file> [--json]")
        sys.exit(1)
    
    html_file = sys.argv[1]
    json_output = '--json' in sys.argv
    
    checker = HTMLChecker(html_file)
    report = checker.check_all()
    
    if json_output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        # Human-readable output
        status_symbol = '✅' if report['status'] == 'pass' else '❌'
        print(f"{status_symbol} HTML check: {report['status'].upper()}")
        print(f"Path: {report['file']}")
        
        if report['errors']:
            print(f"\nErrors ({len(report['errors'])}):")
            for error in report['errors']:
                print(f"  - {error}")
        
        if report['warnings']:
            print(f"\nWarnings ({len(report['warnings'])}):")
            for warning in report['warnings']:
                print(f"  - {warning}")
        
        if report['status'] == 'pass':
            print("\nAll checks passed!")
    
    sys.exit(0 if report['status'] == 'pass' else 1)


if __name__ == '__main__':
    main()
