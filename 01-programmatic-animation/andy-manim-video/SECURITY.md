# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of Andy Manim Video seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do Not** Open a Public Issue

Security vulnerabilities should not be disclosed publicly until a fix is available.

### 2. Report via Email

Send details to: **security@example.com** (or use GitHub Security Advisory)

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Release**: Depends on severity (1-30 days)

### 4. Disclosure Process

Once a fix is released:
1. We will credit you in the security advisory (if you wish)
2. A CVE will be requested for severe vulnerabilities
3. Public disclosure will happen after users have time to update

## Security Best Practices

When using Andy Manim Video:

- Keep dependencies up to date: `npm update && pip install --upgrade manim`
- Review generated scripts before execution
- Use virtual environments for Python dependencies
- Don't execute untrusted templates from unknown sources

## Known Security Considerations

- **Code Execution**: Generated Python scripts are executed by Manim. Only run templates from trusted sources.
- **File System Access**: The CLI creates files in the output directory. Ensure proper permissions.

Thank you for helping keep Andy Manim Video secure! 🔒
