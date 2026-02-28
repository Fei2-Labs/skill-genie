# Contributing to Foxcode OpenClaw Integration

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your contribution
4. Make your changes
5. Submit a pull request

## How to Contribute

### Reporting Bugs

Before creating a bug report:

1. Check if the issue already exists in the [issue tracker](https://github.com/yourusername/foxcode-openclaw/issues)
2. Use the latest version to verify the bug still exists
3. Collect information about the bug:
   - Python version
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages or logs

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Please:

1. Use a clear, descriptive title
2. Provide a detailed description of the enhancement
3. Explain why this enhancement would be useful
4. Include code examples if applicable

### Pull Requests

1. Fill in the required template
2. Follow the [coding standards](#coding-standards)
3. Include tests for new functionality
4. Update documentation as needed
5. Ensure all tests pass

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- Git

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/foxcode-openclaw.git
cd foxcode-openclaw

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Verify setup
python3 scripts/check_status.py --help
```

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update documentation in the `references/` folder
3. Ensure your code follows the [coding standards](#coding-standards)
4. Add tests for new functionality
5. Ensure all tests pass: `python3 -m pytest`
6. Update the CHANGELOG.md with your changes
7. Submit the pull request

### PR Title Format

Use one of these prefixes:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `style:` - Code style changes (formatting, missing semi colons, etc)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Example: `feat: add support for custom headers in configure script`

## Coding Standards

### Python Code Style

- Follow [PEP 8](https://pep8.org/)
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints where appropriate
- Write docstrings for all functions and classes

### Code Example

```python
def validate_api_token(token: str) -> bool:
    """
    Validate API token format.
    
    Args:
        token: The API token to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not token:
        return False
    return re.match(r'^sk-[a-zA-Z0-9_-]+$', token) is not None
```

### File Organization

```
foxcode-openclaw/
├── scripts/              # Executable Python scripts
├── references/           # Documentation
├── assets/              # Templates and resources
├── tests/               # Test files
└── .github/             # GitHub templates and workflows
```

### Documentation Standards

- Use Markdown for all documentation
- Include code examples where helpful
- Keep line length to 80 characters in Markdown files
- Use proper heading hierarchy (# ## ###)

## Testing

### Running Tests

```bash
# Run all tests
python3 -m pytest

# Run specific test file
python3 -m pytest tests/test_check_status.py

# Run with coverage
python3 -m pytest --cov=scripts
```

### Writing Tests

- Use pytest for all tests
- Test file names: `test_<module>.py`
- Test function names: `test_<function_name>`
- Include docstrings explaining what is being tested

Example:

```python
def test_validate_api_token_valid():
    """Test that valid API token format is recognized."""
    assert validate_api_token("sk-foxcode-validtoken123") is True

def test_validate_api_token_invalid():
    """Test that invalid API token format is rejected."""
    assert validate_api_token("invalid-token") is False
```

## Documentation

### Updating Documentation

When you change functionality:

1. Update relevant files in `references/`
2. Update README.md if user-facing changes
3. Update CHANGELOG.md with your changes
4. Update docstrings in code

### Documentation Style

- Use clear, concise language
- Include practical examples
- Explain the "why" not just the "how"
- Keep beginner-friendliness in mind

## Questions?

Feel free to:
- Open an issue for questions
- Join discussions in existing issues
- Reach out to maintainers

## Recognition

Contributors will be recognized in:
- Release notes
- CONTRIBUTORS.md file
- Project README

Thank you for contributing!
