# Quick Start Guide

Get the citation checker running in under 5 minutes.

## 1. Install (30 seconds)

```bash
# Download the checker
curl -o citationChecker.py https://raw.githubusercontent.com/lizTheDeveloper/citation-checker/main/citationChecker.py
chmod +x citationChecker.py

# Create citation database (empty for now)
mkdir research
touch research/BIBLIOGRAPHY.md
```

## 2. Test It (1 minute)

```bash
# Test with example text
python3 citationChecker.py --text "According to Smith et al. (2023), AI is advancing rapidly."

# Output will show:
# ⚠️  CITATION VERIFICATION REPORT
# ============================================================
# Citations found: 1
# ✅ Verified: 0
# ❓ Unverified: 1
# ❌ Suspicious: 0
```

## 3. Add Your First Verified Citation (1 minute)

```bash
# Edit research/BIBLIOGRAPHY.md
echo "## AI Research" >> research/BIBLIOGRAPHY.md
echo "" >> research/BIBLIOGRAPHY.md
echo "- Smith et al. (2023) - Real paper title here" >> research/BIBLIOGRAPHY.md
```

## 4. Test Again (30 seconds)

```bash
# Same text as before
python3 citationChecker.py --text "According to Smith et al. (2023), AI is advancing rapidly."

# Now output shows:
# Citations found: 1
# ✅ Verified: 1  ← Changed!
# ❓ Unverified: 0
# ❌ Suspicious: 0
```

## 5. Install Git Hook (1 minute)

```bash
# Download pre-commit hook
curl -o .git/hooks/pre-commit https://raw.githubusercontent.com/lizTheDeveloper/citation-checker/main/pre-commit-hook
chmod +x .git/hooks/pre-commit

# Now every commit will check citations automatically
```

## 6. Track Known Hallucinations (1 minute)

```bash
# Create hallucination database
cat > research/COMMONLY_HALLUCINATED_CITATIONS.md << 'EOF'
# Known Hallucinations

- Johnson & Williams (2025) - This paper doesn't exist
- arXiv:2501.99999 - Fake arXiv ID (404)
EOF
```

## Done! 🎉

Your repository now has automatic citation verification.

## Next Steps

- **Add more verified citations** to `research/BIBLIOGRAPHY.md`
- **Test on existing files**: `python3 citationChecker.py --file your-notes.md`
- **Customize hook behavior**: Edit `.git/hooks/pre-commit` (block vs warn)
- **Read full docs**: See [README.md](README.md) for advanced usage

## Common Issues

### "No citations detected"
- Check citation format: Must be `Author (YEAR)` or `Author et al. (YEAR)`
- Ensure capital letters: `smith (2023)` won't match, use `Smith (2023)`

### "All citations unverified"
- Add them to `research/BIBLIOGRAPHY.md`
- Format: `- Author et al. (YEAR) - Title`

### Git hook not running
- Check it's executable: `chmod +x .git/hooks/pre-commit`
- Verify location: Must be in `.git/hooks/` not `.githooks/`

## Example Workflow

```bash
# 1. Write some notes with citations
echo "Richardson et al. (2023) studied planetary boundaries." > notes.md

# 2. Check citations
python3 citationChecker.py --file notes.md
# → Shows "unverified"

# 3. Verify the paper exists (manual step - Google Scholar, etc.)

# 4. Add to verified database
echo "- Richardson et al. (2023) - Earth beyond six planetary boundaries" >> research/BIBLIOGRAPHY.md

# 5. Check again
python3 citationChecker.py --file notes.md
# → Shows "verified" ✅

# 6. Commit (git hook runs automatically)
git add notes.md research/BIBLIOGRAPHY.md
git commit -m "Add research notes"
# → Hook checks citations, allows commit ✅
```

## Help

- **Full documentation**: [README.md](README.md)
- **Real-world example**: [CASE_STUDY.md](CASE_STUDY.md)
- **Issues**: https://github.com/lizTheDeveloper/citation-checker/issues
