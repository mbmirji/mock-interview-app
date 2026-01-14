#!/bin/bash

# Quick GitHub Push Fix Script
# This script helps you authenticate and push to GitHub

echo "🔐 GitHub Authentication Helper"
echo "================================"
echo ""

# Check if gh CLI is installed
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI is installed"
    echo ""
    echo "Option 1: Authenticate with GitHub CLI"
    echo "---------------------------------------"
    echo "Run these commands:"
    echo ""
    echo "  gh auth login"
    echo "  git push --set-upstream origin main"
    echo ""
else
    echo "❌ GitHub CLI not installed"
    echo ""
    echo "Install with: brew install gh"
    echo ""
fi

echo "Option 2: Use Personal Access Token"
echo "------------------------------------"
echo "1. Create token: https://github.com/settings/tokens"
echo "2. Scopes: repo, workflow"
echo "3. Copy the token"
echo "4. Run:"
echo ""
echo "  git remote set-url origin https://YOUR_TOKEN@github.com/Dhruta-Technology/mock-interview-app.git"
echo "  git push --set-upstream origin main"
echo ""

echo "Option 3: Use Credential Helper"
echo "--------------------------------"
echo "Run these commands:"
echo ""
echo "  git config --global credential.helper osxkeychain"
echo "  git push --set-upstream origin main"
echo ""
echo "When prompted:"
echo "  Username: mmirji"
echo "  Password: YOUR_PERSONAL_ACCESS_TOKEN"
echo ""

echo "📖 For detailed instructions, see: GITHUB_PUSH_GUIDE.md"
echo ""
