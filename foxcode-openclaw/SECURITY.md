# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible
receiving these patches depends on their maintenance status:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability,
please report it responsibly.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:
- [INSERT SECURITY EMAIL] (if available)
- Or open a private security advisory on GitHub

Please include the following information:
- Type of vulnerability
- Steps to reproduce (if applicable)
- Affected versions
- Possible impact
- Any suggested fixes (if known)

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Assessment**: Within 5 business days
- **Fix and release**: Depending on severity and complexity

## Security Best Practices

### For Users

1. **API Token Security**
   - Never commit API tokens to version control
   - Use environment variables for production deployments
   - Rotate tokens regularly
   - Use separate tokens for different environments

2. **File Permissions**
   - Configuration files should have 600 permissions (owner read/write only)
   - The setup scripts automatically set these permissions

3. **Network Security**
   - Always use HTTPS endpoints
   - Verify SSL certificates
   - Use secure networks when possible

### Security Features

This project implements the following security measures:

- API tokens are input via hidden prompts (not echoed to screen)
- Configuration files are created with restrictive permissions (600)
- Support for environment variable substitution
- No logging of sensitive information
- Input validation on all user inputs

## Known Security Considerations

### API Token Storage

The configuration file stores the API token. While we set file permissions
to 600 (owner-only access), users should:
- Ensure their home directory permissions are secure
- Use environment variables for additional security
- Never share configuration files containing tokens

### Network Requests

The scripts make HTTPS requests to Foxcode endpoints. All communication:
- Uses TLS encryption
- Validates server certificates
- Does not send tokens in query parameters

### Script Security

Our Python scripts:
- Do not execute user input as code
- Validate all inputs before use
- Use parameterized requests (not string concatenation)
- Follow secure coding practices

## Security Updates

Security updates will be:
- Released as soon as possible after verification
- Documented in the [CHANGELOG](CHANGELOG.md)
- Announced via GitHub releases
- Tagged with `security` label in issues

## Third-Party Dependencies

This project aims to minimize dependencies to reduce attack surface.
Currently, the scripts use only Python standard library modules:
- `json` - JSON parsing
- `urllib` - HTTP requests
- `argparse` - Command line arguments
- `getpass` - Secure password input
- `pathlib` - Path handling

## Verification

To verify the integrity of this project:

1. Check file hashes against release notes
2. Verify the scripts don't contain malicious code (they are readable Python)
3. Run in a sandboxed environment first
4. Check the code on [VirusTotal](https://www.virustotal.com/) if concerned

## Disclaimer

This is an unofficial integration with Foxcode. Users are responsible for:
- Securing their own API tokens
- Complying with Foxcode's terms of service
- Understanding the security implications of using third-party AI services

## Contact

For security-related questions:
- Open a private security advisory on GitHub
- Contact the maintainers directly

---

Last updated: February 2025
