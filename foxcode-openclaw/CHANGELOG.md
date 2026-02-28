# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial GitHub repository documentation
- Comprehensive security documentation
- Contributing guidelines

## [1.0.0] - 2025-02-28

### Added
- Interactive configuration wizard (`configure_foxcode.py`)
- Endpoint status checker (`check_status.py`)
- Configuration validator (`validate_config.py`)
- Support for all 5 Foxcode endpoints:
  - Official (https://code.newcli.com/claude)
  - Super (https://code.newcli.com/claude/super)
  - Ultra (https://code.newcli.com/claude/ultra)
  - AWS (https://code.newcli.com/claude/aws)
  - AWS Thinking (https://code.newcli.com/claude/droid)
- Support for 3 Claude models:
  - claude-opus-4-5-20251101
  - claude-sonnet-4-5-20251101
  - claude-haiku-4-5-20251101
- Primary and fallback model configuration
- Environment variable support for API tokens
- Secure file permissions (600) on config files
- Comprehensive documentation:
  - SKILL.md - Skill definition and usage
  - README.md - Step-by-step setup guide
  - references/foxcode-endpoints.md - Endpoint reference
  - references/openclaw-config.md - Configuration reference
  - assets/templates/setup-checklist.md - Printable checklist
- Psychology-backed learning approach for beginners
- MIT License

### Security
- API token input via hidden prompts (getpass)
- Configuration files created with 600 permissions
- No logging of sensitive information
- Input validation on all user inputs

## Template for Future Releases

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Now removed features

### Fixed
- Bug fixes

### Security
- Security improvements

---

## Release Notes Format

Each release should include:
1. Version number (following SemVer)
2. Release date
3. Categorized changes (Added, Changed, Deprecated, Removed, Fixed, Security)
4. Link to full diff on GitHub

[Unreleased]: https://github.com/yourusername/foxcode-openclaw/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/foxcode-openclaw/releases/tag/v1.0.0
