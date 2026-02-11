# 🔧 Git Setup Guide

## Current Situation

The `endee/` subfolder contains a Git repository pointing to:
```
https://github.com/endee-io/endee.git
```

This is the **original Endee source code** repository.

## What You Need to Do

### Option 1: Keep Endee as Submodule (Recommended)
If you want to keep the Endee source code tracked separately:

```bash
# 1. Initialize your repo
git init

# 2. Add your remote
git remote add origin YOUR_GITHUB_URL_HERE

# 3. Add endee as a Git submodule
git submodule add https://github.com/endee-io/endee.git endee

# 4. Add all your project files
git add .
git commit -m "Initial commit: Support Ticket Classifier with Endee"
git push -u origin main
```

### Option 2: Remove Endee Git (Simpler)
If you just want everything in one repository:

```bash
# 1. Remove Endee's .git folder
Remove-Item -Recurse -Force endee/.git

# 2. Initialize your repo
git init

# 3. Add your remote
git remote add origin YOUR_GITHUB_URL_HERE

# 4. Add all files
git add .
git commit -m "Initial commit: Support Ticket Classifier with Endee"
git push -u origin main
```

## Your Commands (Ready to Run)

Replace `YOUR_GITHUB_URL_HERE` with your actual GitHub repo URL, then run:

```powershell
# Navigate to project
cd "c:\Users\Roshan Rony\Desktop\endee_labs"

# Remove nested Endee Git
Remove-Item -Recurse -Force endee/.git

# Initialize YOUR repository
git init

# Add YOUR remote (REPLACE URL!)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Stage all files
git add .

# First commit
git commit -m "Initial commit: AI Support Ticket Classifier with Endee Labs integration"

# Push to your repo
git branch -M main
git push -u origin main
```

## What Gets Committed

Thanks to `.gitignore`, these are **PROTECTED** (won't be committed):
- ✅ `.env` (your API keys)
- ✅ `__pycache__/` (Python cache)
- ✅ `dataset/minilm_model/` (large model files - can be re-downloaded)
- ✅ `endee/build/` (build artifacts)
- ✅ Virtual environments

These **WILL be committed**:
- ✅ Source code (`src/`, `scripts/`, `main.py`)
- ✅ Configuration (`requirements.txt`, `.env.example`, `docker-compose-endee.yml`)
- ✅ Documentation (`README.md`, `SETUP.md`, etc.)
- ✅ Sample data (`data/sample_tickets.json`)
- ✅ Endee source code (`endee/` folder - if you keep it)

## After Setup

Your GitHub repo will show:
```
YOUR_USERNAME/ticket-classifier
├── Complete README.md
├── Working code
├── Documentation
├── Setup scripts
└── Endee integration (optional)
```

---

**Next Step**: Run the commands above after replacing `YOUR_GITHUB_URL_HERE`!
