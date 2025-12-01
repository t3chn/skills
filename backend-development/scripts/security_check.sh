#!/bin/bash
# Security check script for backend projects
# Runs multiple security scanners and reports findings

set -e

echo "========================================="
echo "Backend Security Check"
echo "========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
SECURITY_ISSUES=0

# Detect project type
detect_project_type() {
    if [ -f "package.json" ]; then
        echo "node"
    elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
        echo "python"
    elif [ -f "go.mod" ]; then
        echo "go"
    elif [ -f "Cargo.toml" ]; then
        echo "rust"
    else
        echo "unknown"
    fi
}

PROJECT_TYPE=$(detect_project_type)
echo -e "Detected project type: ${GREEN}$PROJECT_TYPE${NC}"
echo ""

# Node.js security checks
check_node_security() {
    echo -e "${YELLOW}Running npm audit...${NC}"
    if npm audit --audit-level=high 2>/dev/null; then
        echo -e "${GREEN}npm audit passed${NC}"
    else
        echo -e "${RED}npm audit found high severity vulnerabilities${NC}"
        SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
    fi
    echo ""

    # Check for outdated packages
    echo -e "${YELLOW}Checking for outdated packages...${NC}"
    npm outdated || true
    echo ""

    # Run Snyk if available
    if command -v snyk &> /dev/null; then
        echo -e "${YELLOW}Running Snyk scan...${NC}"
        snyk test || SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
    else
        echo -e "${YELLOW}Snyk not installed. Run: npm install -g snyk${NC}"
    fi
}

# Python security checks
check_python_security() {
    # pip-audit (modern alternative to safety)
    echo -e "${YELLOW}Running pip-audit...${NC}"
    if command -v pip-audit &> /dev/null; then
        pip-audit || SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
    elif command -v uv &> /dev/null; then
        uv pip install pip-audit
        pip-audit || SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
    else
        echo -e "${YELLOW}pip-audit not installed. Run: uv pip install pip-audit${NC}"
    fi
    echo ""

    # Bandit for code security
    echo -e "${YELLOW}Running Bandit (Python security linter)...${NC}"
    if command -v bandit &> /dev/null; then
        bandit -r src/ -ll || SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
    else
        echo -e "${YELLOW}Bandit not installed. Run: uv pip install bandit${NC}"
    fi
    echo ""

    # Ruff security checks
    echo -e "${YELLOW}Running Ruff security checks...${NC}"
    if command -v ruff &> /dev/null; then
        ruff check --select=S . || true
    else
        echo -e "${YELLOW}Ruff not installed. Run: uv pip install ruff${NC}"
    fi
}

# Go security checks
check_go_security() {
    echo -e "${YELLOW}Running govulncheck...${NC}"
    if command -v govulncheck &> /dev/null; then
        govulncheck ./... || SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
    else
        echo -e "${YELLOW}govulncheck not installed. Run: go install golang.org/x/vuln/cmd/govulncheck@latest${NC}"
    fi
    echo ""

    echo -e "${YELLOW}Running gosec...${NC}"
    if command -v gosec &> /dev/null; then
        gosec ./... || SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
    else
        echo -e "${YELLOW}gosec not installed. Run: go install github.com/securego/gosec/v2/cmd/gosec@latest${NC}"
    fi
}

# Rust security checks
check_rust_security() {
    echo -e "${YELLOW}Running cargo audit...${NC}"
    if command -v cargo-audit &> /dev/null; then
        cargo audit || SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
    else
        echo -e "${YELLOW}cargo-audit not installed. Run: cargo install cargo-audit${NC}"
    fi
}

# Docker security checks
check_docker_security() {
    if [ -f "Dockerfile" ]; then
        echo -e "${YELLOW}Running Dockerfile lint (hadolint)...${NC}"
        if command -v hadolint &> /dev/null; then
            hadolint Dockerfile || true
        else
            docker run --rm -i hadolint/hadolint < Dockerfile || true
        fi
        echo ""

        echo -e "${YELLOW}Running Trivy container scan...${NC}"
        if command -v trivy &> /dev/null; then
            trivy fs . --security-checks vuln,config || SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
        else
            echo -e "${YELLOW}Trivy not installed. Install from: https://trivy.dev${NC}"
        fi
    fi
}

# Secrets scanning
check_secrets() {
    echo -e "${YELLOW}Scanning for secrets...${NC}"
    if command -v gitleaks &> /dev/null; then
        gitleaks detect --source . --no-git || SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
    else
        echo -e "${YELLOW}gitleaks not installed. Install from: https://github.com/gitleaks/gitleaks${NC}"
    fi
    echo ""

    # Check for common secret patterns
    echo -e "${YELLOW}Checking for common secret patterns...${NC}"
    if grep -rn --include="*.py" --include="*.js" --include="*.ts" --include="*.env*" \
        -E "(password|secret|api_key|apikey|token)\s*=\s*['\"][^'\"]+['\"]" . 2>/dev/null | \
        grep -v "node_modules" | grep -v ".venv"; then
        echo -e "${RED}Potential hardcoded secrets found!${NC}"
        SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
    else
        echo -e "${GREEN}No obvious hardcoded secrets found${NC}"
    fi
}

# Run checks based on project type
case $PROJECT_TYPE in
    "node")
        check_node_security
        ;;
    "python")
        check_python_security
        ;;
    "go")
        check_go_security
        ;;
    "rust")
        check_rust_security
        ;;
    *)
        echo -e "${YELLOW}Unknown project type, running generic checks${NC}"
        ;;
esac

# Always run these checks
check_docker_security
check_secrets

# Summary
echo ""
echo "========================================="
if [ $SECURITY_ISSUES -eq 0 ]; then
    echo -e "${GREEN}Security check passed!${NC}"
    exit 0
else
    echo -e "${RED}Found $SECURITY_ISSUES security issue(s)${NC}"
    exit 1
fi
