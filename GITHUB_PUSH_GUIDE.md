# How to Push to GitHub - Permission Fix

## Problem

You're getting a 403 Permission Denied error:
```
remote: Permission to Dhruta-Technology/mock-interview-app.git denied to mmirji.
fatal: unable to access 'https://github.com/Dhruta-Technology/mock-interview-app.git/': The requested URL returned error: 403
```

This happens because:
1. You're not authenticated with GitHub
2. Or you don't have write access to the repository
3. Or your credentials are outdated

## Solutions

### Solution 1: Use Personal Access Token (Recommended)

#### Step 1: Create a GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "Mock Interview App"
4. Set expiration: 90 days (or custom)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
6. Click "Generate token"
7. **Copy the token** (you won't see it again!)

#### Step 2: Update Git Remote to Use Token

```bash
# Remove old remote
git remote remove origin

# Add new remote with token
git remote add origin https://YOUR_TOKEN@github.com/Dhruta-Technology/mock-interview-app.git

# Verify
git remote -v

# Push with upstream
git push --set-upstream origin main
```

Replace `YOUR_TOKEN` with the token you just created.

### Solution 2: Use GitHub CLI (Easiest)

#### Step 1: Install GitHub CLI

```bash
# On macOS
brew install gh

# Or download from https://cli.github.com/
```

#### Step 2: Authenticate

```bash
# Login to GitHub
gh auth login

# Follow prompts:
# ? What account do you want to log into? GitHub.com
# ? What is your preferred protocol for Git operations? HTTPS
# ? Authenticate Git with your GitHub credentials? Yes
# ? How would you like to authenticate GitHub CLI? Login with a web browser

# Complete authentication in browser
```

#### Step 3: Push

```bash
git push --set-upstream origin main
```

### Solution 3: Use SSH (Most Secure)

#### Step 1: Generate SSH Key

```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Press Enter to accept default location
# Enter passphrase (optional)

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to SSH agent
ssh-add ~/.ssh/id_ed25519
```

#### Step 2: Add SSH Key to GitHub

```bash
# Copy public key to clipboard
pbcopy < ~/.ssh/id_ed25519.pub

# Or display it
cat ~/.ssh/id_ed25519.pub
```

1. Go to https://github.com/settings/keys
2. Click "New SSH key"
3. Title: "Mac - Mock Interview App"
4. Paste your public key
5. Click "Add SSH key"

#### Step 3: Change Remote to SSH

```bash
# Remove HTTPS remote
git remote remove origin

# Add SSH remote
git remote add origin git@github.com:Dhruta-Technology/mock-interview-app.git

# Test connection
ssh -T git@github.com

# Push
git push --set-upstream origin main
```

### Solution 4: Check Repository Access

If none of the above work, you might not have write access to the repository.

#### Check Access

1. Go to https://github.com/Dhruta-Technology/mock-interview-app
2. Check if you can see a "Settings" tab
3. If not, you need to:
   - Be added as a collaborator by the owner
   - Or fork the repository

#### Request Access

Contact the repository owner (Dhruta-Technology) and ask them to:

1. Go to repository Settings
2. Click "Collaborators and teams"
3. Click "Add people"
4. Add your GitHub username: `mmirji`
5. Select role: "Write" or "Admin"

## Quick Fix Commands

### Option A: GitHub CLI (Recommended)

```bash
# Install
brew install gh

# Login
gh auth login

# Push
git push --set-upstream origin main
```

### Option B: Personal Access Token

```bash
# Get token from: https://github.com/settings/tokens

# Update remote
git remote set-url origin https://YOUR_TOKEN@github.com/Dhruta-Technology/mock-interview-app.git

# Push
git push --set-upstream origin main
```

### Option C: Use Credential Helper

```bash
# Configure credential helper
git config --global credential.helper osxkeychain

# Try push (will prompt for credentials)
git push --set-upstream origin main

# When prompted:
# Username: mmirji
# Password: YOUR_PERSONAL_ACCESS_TOKEN (not your GitHub password!)
```

## After Successful Push

Once you've pushed successfully:

### Verify Push

```bash
# Check remote branches
git branch -r

# Should show:
# origin/main

# View commit history
git log --oneline -5
```

### Next Steps for Railway

1. **Go to Railway Dashboard**
2. **Connect GitHub Repository**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `Dhruta-Technology/mock-interview-app`
3. **Configure**:
   - Set Root Directory: `backend`
   - Add environment variables
4. **Deploy!**

### Next Steps for Vercel (Frontend)

1. **Go to Vercel Dashboard**
2. **Import Project**:
   - Click "Add New..."
   - Select "Project"
   - Import from GitHub
   - Choose `mock-interview-app`
3. **Configure**:
   - Root Directory: `frontend`
   - Framework: Vite
   - Environment Variable: `VITE_API_URL=https://your-railway-url.up.railway.app`
4. **Deploy!**

## Troubleshooting

### Error: "Authentication failed"

**Solution**: Use Personal Access Token instead of password

### Error: "Repository not found"

**Solution**: Check repository name and your access

### Error: "Permission denied (publickey)"

**Solution**: Add SSH key to GitHub account

### Token Expired

**Solution**: Generate new token at https://github.com/settings/tokens

## Security Notes

⚠️ **Never commit tokens to your repository**

Add to `.gitignore`:
```
.env
*.token
credentials.json
```

🔐 **Store tokens securely**:
- Use macOS Keychain
- Or password manager
- Don't share tokens

🔄 **Rotate tokens regularly**:
- Set expiration dates
- Revoke old tokens
- Generate new ones when needed

## Alternative: Work with a Fork

If you can't get access to the main repository:

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git remote remove origin
git remote add origin https://github.com/mmirji/mock-interview-app.git

# 3. Push to your fork
git push --set-upstream origin main

# 4. Create Pull Request to main repository
```

---

**Once you've authenticated, retry the push command!** 🚀
