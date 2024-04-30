#!/bin/bash

echo "🧹 Cleaning Git History for Pulse Open Source Release"
echo "======================================================"
echo ""

# Backup current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "📌 Current branch: $CURRENT_BRANCH"
echo "📦 Creating backup branch: backup-before-clean"
git branch -f backup-before-clean HEAD

echo ""
echo "🔍 Commits to preserve:"
echo "  1. ff16922 - Pulse rust (#7) by Shyamant Achar"
echo "  2. 465b01f - Rust revamp (#11) by Aditya Jindal"  
echo "  3. 4e6a912 - chore: migrate from Bazel to Go modules"
echo "  4. Current rebranding changes"
echo ""

# Clean up any existing clean-main branch
echo "🧼 Cleaning up any existing clean-main branch..."
git branch -D clean-main 2>/dev/null || true

# Create initial commit on orphan branch
echo "🌱 Creating new orphan branch with initial commit..."
git checkout --orphan clean-main
git rm -rf . 2>/dev/null || true

# Create initial commit
echo "# Pulse" > README.md
git add README.md
git commit -m "chore: initial commit for Pulse open source"

echo ""
echo "📝 Step 1: Cherry-picking Rust foundation (ff16922)"
if ! git cherry-pick ff16922 --allow-empty 2>&1; then
    echo "⚠️  Resolving conflicts by accepting all Rust commit changes..."
    # Add all new files from the commit
    git add rust/
    # Accept all modified files from the cherry-picked commit
    git rm .bazelversion .devcontainer/devcontainer.json .gitignore .vscode/settings.json MODULE.bazel MODULE.bazel.lock tools/BUILD.bazel 2>/dev/null || true
    git checkout ff16922 -- .bazelversion .devcontainer/devcontainer.json .gitignore .vscode/settings.json MODULE.bazel MODULE.bazel.lock otel/docker-compose.yaml rust/ tools/BUILD.bazel 2>/dev/null || true
    git add -A
    GIT_EDITOR=true git cherry-pick --continue
fi

echo ""
echo "📝 Step 2: Cherry-picking Rust revamp (465b01f)"
if ! git cherry-pick 465b01f --allow-empty 2>&1; then
    echo "⚠️  Resolving conflicts..."
    git checkout 465b01f -- rust/ otel/ .github/ 2>/dev/null || true
    git add -A
    GIT_EDITOR=true git cherry-pick --continue
fi

echo ""
echo "📝 Step 3: Cherry-picking Go modules migration (4e6a912)"
if ! git cherry-pick 4e6a912 --allow-empty 2>&1; then
    echo "⚠️  Resolving conflicts..."
    git checkout 4e6a912 -- go/ otel/ .github/ README.md 2>/dev/null || true
    git add -A
    GIT_EDITOR=true git cherry-pick --continue
fi

echo ""
echo "📝 Step 4: Applying current rebranding changes"
# Get the current changes from backup
git checkout backup-before-clean -- .github/ go/ otel/ README.md LICENSE .yamllint.yml rust/ 2>/dev/null || true

# Remove cleanup scripts and guide from history
rm -f clean-history.sh GIT-CLEANUP-GUIDE.md 2>/dev/null || true

# Stage all changes
git add -A

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "   ℹ️  No additional changes to commit"
else
    echo "   ✅ Committing rebranding updates"
    git commit -m "chore: rebrand to Pulse and update documentation

- Update all README files with Pulse branding
- Fix GitHub workflows for Go, Markdown, and YAML
- Update LICENSE to 2025
- Add comprehensive contributing guidelines
- Remove all Kodo references
- Clean up issue templates

Open sourced by Machani Robotics"
fi

echo ""
echo "✅ Clean history created successfully!"
echo ""
echo "📊 New commit history:"
git log --oneline -10

echo ""
echo "🎯 Next steps:"
echo ""
echo "  1. Review the clean history:"
echo "     git log --stat"
echo ""
echo "  2. If satisfied, replace main branch:"
echo "     git checkout main"
echo "     git reset --hard clean-main"
echo "     git push origin main --force"
echo ""
echo "  3. If you want to revert:"
echo "     git checkout backup-before-clean"
echo "     git branch -D clean-main"
echo ""
echo "⚠️  WARNING: Force pushing will rewrite history!"
echo "   - All team members must re-clone the repository"
echo "   - Update any open PRs"
echo "   - Coordinate with the team before pushing"
echo ""
