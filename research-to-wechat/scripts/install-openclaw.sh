#!/usr/bin/env bash
#
# research-to-wechat OpenClaw Skill Installer
#
# Copies skill files to ~/.openclaw/skills/research-to-wechat
# For ClawHub users: clawhub install research-to-wechat
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/Fei2-Labs/skill-genie/main/research-to-wechat/scripts/install-openclaw.sh | bash
#

set -e

REPO="Fei2-Labs/skill-genie"
SKILL_NAME="research-to-wechat"
INSTALL_DIR="${HOME}/.openclaw/skills/${SKILL_NAME}"
GITHUB_ARCHIVE="https://github.com/${REPO}/archive/refs/heads/main.tar.gz"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()    { printf "${BLUE}ℹ${NC} %s\n" "$1"; }
success() { printf "${GREEN}✓${NC} %s\n" "$1"; }
warn()    { printf "${YELLOW}⚠${NC} %s\n" "$1"; }
error()   { printf "${RED}✗${NC} %s\n" "$1" >&2; exit 1; }

# Header
printf "\n"
printf "${BLUE}================================================${NC}\n"
printf "${BLUE}   research-to-wechat OpenClaw Skill Installer${NC}\n"
printf "${BLUE}================================================${NC}\n"
printf "\n"

# Check for ClawHub first
if command -v clawhub &>/dev/null; then
    info "检测到 clawhub CLI / ClawHub CLI detected"
    printf "\n"
    printf "推荐使用 ClawHub 安装 / Recommend using ClawHub:\n"
    printf "  ${GREEN}clawhub install research-to-wechat${NC}\n"
    printf "\n"
    read -p "继续手动安装？/ Continue manual install? [y/N] " -n 1 -r
    printf "\n"
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 0
fi

# Check prerequisites
command -v curl &>/dev/null || command -v wget &>/dev/null || \
    error "需要 curl 或 wget / Need curl or wget"

command -v python3 &>/dev/null || \
    warn "未检测到 python3 / python3 not found (needed for fetch_wechat_article.py)"

# Check if OpenClaw is installed (optional warning)
if [[ ! -d "${HOME}/.openclaw" ]]; then
    warn "未检测到 OpenClaw 安装 / OpenClaw not detected"
    info "请先安装 OpenClaw: https://openclaw.ai/"
    info "Install OpenClaw first: https://openclaw.ai/"
    printf "\n"
    read -p "仍要继续安装技能？/ Continue installing skill anyway? [y/N] " -n 1 -r
    printf "\n"
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 0
fi

# Handle existing installation
if [[ -d "$INSTALL_DIR" ]]; then
    warn "已存在安装 / Existing installation: $INSTALL_DIR"
    read -p "覆盖？/ Overwrite? [y/N] " -n 1 -r
    printf "\n"
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 0
    rm -rf "$INSTALL_DIR"
fi

# Download and extract
info "下载技能文件 / Downloading skill files..."

TEMP_DIR=$(mktemp -d)
ARCHIVE="${TEMP_DIR}/repo.tar.gz"

if command -v curl &>/dev/null; then
    curl -fsSL "$GITHUB_ARCHIVE" -o "$ARCHIVE"
else
    wget -q "$GITHUB_ARCHIVE" -O "$ARCHIVE"
fi

tar -xzf "$ARCHIVE" -C "$TEMP_DIR"

# Find extracted directory
EXTRACTED=$(find "$TEMP_DIR" -maxdepth 1 -type d -name "skill-genie-*" | head -n 1)
[[ -z "$EXTRACTED" ]] && error "下载失败 / Download failed"

# Verify skill directory exists in archive
SKILL_SRC="${EXTRACTED}/research-to-wechat"
[[ ! -d "$SKILL_SRC" ]] && error "技能目录不存在 / Skill directory not found in archive"

# Install
mkdir -p "$INSTALL_DIR"
cp -r "${SKILL_SRC}/"* "$INSTALL_DIR/"
chmod +x "${INSTALL_DIR}/scripts/"*.py 2>/dev/null || true
chmod +x "${INSTALL_DIR}/scripts/"*.sh 2>/dev/null || true

# Cleanup
rm -rf "$TEMP_DIR"

success "安装完成 / Installation complete!"

# Show configuration instructions
printf "\n"
printf "${BLUE}================================================${NC}\n"
printf "${BLUE}   配置说明 / Configuration${NC}\n"
printf "${BLUE}================================================${NC}\n"
printf "\n"

CONFIG_FILE="${HOME}/.openclaw/openclaw.json"

if [[ -f "$CONFIG_FILE" ]]; then
    printf "${YELLOW}检测到已有配置文件 / Existing config found${NC}\n"
    printf "\n"
    printf "请在 ${GREEN}~/.openclaw/openclaw.json${NC} 的 skills.entries 中添加:\n"
    printf "Add to skills.entries in your existing config:\n"
    printf "\n"
    printf "${GREEN}"
    cat << 'EOF'
"research-to-wechat": {
  "enabled": true,
  "env": {
    "WECHAT_APPID": "your-appid",
    "WECHAT_SECRET": "your-secret"
  }
}
EOF
    printf "${NC}\n"
else
    printf "创建配置文件 / Create config file:\n"
    printf "${GREEN}~/.openclaw/openclaw.json${NC}\n"
    printf "\n"
    printf "${GREEN}"
    cat << 'EOF'
{
  "skills": {
    "entries": {
      "research-to-wechat": {
        "enabled": true,
        "env": {
          "WECHAT_APPID": "your-appid",
          "WECHAT_SECRET": "your-secret"
        }
      }
    }
  }
}
EOF
    printf "${NC}\n"
fi

printf "\n"
printf "${YELLOW}注意 / Note:${NC}\n"
printf "  • WECHAT_APPID/SECRET 仅草稿上传需要，研究和写作不需要\n"
printf "  • WECHAT_APPID/SECRET only needed for draft upload, not for research/writing\n"
printf "  • 排版设计需要 Pencil MCP 服务 / Design templates require Pencil MCP server\n"
printf "  • HTML 转换需要 md2wechat 技能 / HTML rendering needs md2wechat skill\n"
printf "\n"
printf "安装路径 / Installed to: ${GREEN}%s${NC}\n" "$INSTALL_DIR"
printf "文档 / Documentation: https://github.com/${REPO}/tree/main/research-to-wechat#readme\n"
printf "\n"
