#!/usr/bin/env python3
"""
Sensitive Information Detection & Sanitization Script
Detects passwords, secrets, API keys, tokens, and other sensitive data in text content.
Replaces matched values with ***.
"""

import re
import sys
import json
from typing import List, Tuple, Optional


# ============================================================
# Sensitive Field Name Patterns (case-insensitive)
# ============================================================
SENSITIVE_FIELD_NAMES = [
    r'password', r'passwd', r'pwd\b', r'\bpass\s*[:=]',
    r'secret', r'api_secret', r'app_secret',
    r'api_key', r'apikey', r'access_key',
    r'access_token', r'auth_token', r'refresh_token',
    r'bearer_token', r'private_key', r'privatekey',
    r'credential', r'credentials',
    r'cert', r'certificate',
]

# ============================================================
# Sensitive Value Format Patterns
# ============================================================
SENSITIVE_VALUE_PATTERNS = [
    # AWS Access Key ID
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
    # JWT Token (simplified pattern)
    (r'eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}', 'JWT Token'),
    # SSH Private Key marker
    (r'-----BEGIN[A-Z ]*PRIVATE KEY-----[\s\S]*?-----END[A-Z ]*PRIVATE KEY-----', 'SSH Private Key'),
    # OpenAI-style API key prefix
    (r'sk-[A-Za-z0-9_\-]{20,}', 'API Key (sk-)'),
    # GitHub PAT prefix
    (r'ghp_[A-Za-z0-9_]{36,}', 'GitHub PAT'),
    # Slack Bot token prefix
    (r'xoxb-[A-Za-z0-9\-]+', 'Slack Bot Token'),
    # Google API key prefix
    (r'AIza[A-Za-z0-9_\-]{35}', 'Google API Key'),
    # Generic long hex/alpha string after known fields (heuristic)
]


class SecretSanitizer:
    """Main sanitizer class for detecting and redacting sensitive information."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.replacements: List[Tuple[str, str, int]] = []  # (original, replacement, line_num)

    def sanitize_text(self, text: str) -> Tuple[str, dict]:
        """
        Sanitize all sensitive information from the given text.
        
        Returns:
            Tuple of (sanitized_text, report_dict)
        """
        original_text = text
        self.replacements = []

        # Phase 1: Detect and replace field-value patterns (field: value or field=value)
        text = self._sanitize_field_values(text)

        # Phase 2: Detect standalone value format patterns
        text = self._sanitize_value_patterns(text)

        # Phase 3: Sanitize connection strings
        text = self._sanitize_connection_strings(text)

        # Build report
        report = {
            'total_replacements': len(self.replacements),
            'replacements': self.replacements,
            'was_modified': original_text != text,
        }

        return text, report

    def _sanitize_field_values(self, text: str) -> str:
        """Find field:value or field=value patterns with sensitive field names."""
        lines = text.split('\n')
        result_lines = []
        
        for line_num, line in enumerate(lines, start=1):
            modified_line = line
            
            for field_pattern in SENSITIVE_FIELD_NAMES:
                # Match patterns like "password: value", "password = value", etc.
                patterns = [
                    rf'{field_pattern}\s*[:=]\s*["\']?([^\s"\'\n]+)["\']?',  # password: value
                    rf'{field_pattern}\s*[:=]\s*["\']([^"\']+?)["\']',       # password:"value"
                ]
                
                for pat in patterns:
                    matches = re.finditer(pat, modified_line, re.IGNORECASE)
                    for match in matches:
                        if match.group(1):
                            original_value = match.group(0)
                            # Don't replace placeholder values
                            if not self._is_placeholder(match.group(1)):
                                replacement = match.group(0).replace(match.group(1), '***')
                                modified_line = modified_line.replace(original_value, replacement, 1)
                                self.replacements.append((original_value, replacement, line_num))
            
            result_lines.append(modified_line)
        
        return '\n'.join(result_lines)

    def _sanitize_value_patterns(self, text: str) -> str:
        """Detect standalone sensitive value formats."""
        for pattern, label in SENSITIVE_VALUE_PATTERNS:
            matches = re.finditer(pattern, text)
            for match in matches:
                original_value = match.group(0)
                text = text.replace(original_value, '***', 1)
                self.replacements.append((f'{label}: {original_value[:30]}...', '***', 0))
        return text

    def _sanitize_connection_strings(self, text: str) -> str:
        """Sanitize credentials embedded in connection URLs."""
        # Database connection URL patterns
        url_patterns = [
            (r'(postgresql|mysql|mongodb|redis|postgres)://[^:]+:[^@]+@', 'DB Connection URL'),
            (r'mysql://[^:]+:[^@]+@', 'MySQL URL'),
            (r'mongodb\+srv://[^:]+:[^@]+@', 'MongoDB SRV URL'),
        ]
        
        for pattern, label in url_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                original_url = match.group(0)
                # Replace user:pass part while keeping protocol and host
                sanitized_url = re.sub(
                    r'://[^:]+:[^@]+@',
                    r'://***:***@',
                    original_url
                )
                text = text.replace(original_url, sanitized_url, 1)
                self.replacements.append((f'{label}', sanitized_url, 0))
        
        return text

    def _is_placeholder(self, value: str) -> bool:
        """Check if a value looks like a placeholder/example rather than real secret."""
        placeholders = [
            'your_password', 'your_secret', 'your_key', 'your_token',
            'changeme', 'change_me', 'replace_me', '<password>',
            'your_password_here', 'secret_here', 'xxx', '****',
            'example', 'test', 'demo', 'placeholder',
            'YOUR_PASSWORD', 'YOUR_SECRET', 'CHANGE_ME',
        ]
        value_lower = value.lower().strip()
        return any(p.lower() == value_lower for p in placeholders)


def main():
    """CLI entry point for the sanitizer."""
    if len(sys.argv) < 2:
        print("Usage: python sanitize_secrets.py <input_file> [--output <output_file>] [--json]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = None
    json_output = False
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--output':
            output_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--json':
            json_output = True
            i += 1
        else:
            i += 1
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sanitizer = SecretSanitizer()
    sanitized_content, report = sanitizer.sanitize_text(content)
    
    if json_output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(sanitized_content)
        print(f"Sanitized content written to: {output_file}")
    else:
        print(sanitized_content)


if __name__ == '__main__':
    main()
