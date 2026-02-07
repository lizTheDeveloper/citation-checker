# Citation Hallucination Checker

A lightweight, dependency-free git hook and CLI tool that detects hallucinated academic citations in AI-generated text. Prevents fabricated references from entering your codebase or documentation.

## Features

- **Zero dependencies** - Pure Python 3 with regex, no NLP libraries required
- **Fast** - Regex-based extraction, processes files in milliseconds
- **Git hook integration** - Auto-check commits, pre-commit, or post-response
- **Citation database** - Maintains verified citations, flags suspicious ones
- **Multiple input modes** - stdin, file, or text argument
- **JSON/human output** - Machine-readable or terminal-friendly reports

## Why This Matters

AI language models (GPT-4, Claude, etc.) occasionally hallucinate academic citations - generating plausible-sounding references to papers that don't exist. This can:

- Mislead researchers who trust the citations
- Damage credibility when fabricated references are discovered
- Waste time tracking down non-existent papers
- Propagate misinformation

This tool catches these hallucinations **before** they enter your repository.

## Installation

### Quick Start (Copy-Paste)

```bash
# 1. Download the checker script
curl -o citationChecker.py https://raw.githubusercontent.com/lizTheDeveloper/citation-checker/main/citationChecker.py
chmod +x citationChecker.py

# 2. Create citation database directories
mkdir -p research
touch research/BIBLIOGRAPHY.md
touch research/COMMONLY_HALLUCINATED_CITATIONS.md

# 3. Install as git hook (optional)
curl -o .git/hooks/pre-commit https://raw.githubusercontent.com/lizTheDeveloper/citation-checker/main/pre-commit-hook
chmod +x .git/hooks/pre-commit
```

### Manual Installation

1. **Copy `citationChecker.py`** to your project (e.g., `scripts/` or `tools/`)
2. **Create citation database** (see Database Setup below)
3. **Install git hook** (optional, see Git Hook Integration below)

## Usage

### Command Line

```bash
# Check text directly
python citationChecker.py --text "According to Smith et al. (2023)..."

# Check a file
python citationChecker.py --file response.txt

# Pipe from stdin
echo "Jones (2024) found that..." | python citationChecker.py --stdin

# JSON output
python citationChecker.py --file paper.md --json

# Quiet mode (exit code only)
python citationChecker.py --file draft.txt --quiet
echo $?  # 0 = all verified, 1 = unverified/suspicious found
```

### Git Hook Integration

#### Pre-Commit Hook

Checks staged files before commit:

```bash
# Install hook
cp pre-commit-hook .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Now all commits will be checked
git add research/paper_notes.md
git commit -m "Add research notes"
# → Hook runs, blocks commit if hallucinated citations found
```

#### Post-Response Hook (For AI Coding Tools)

Checks AI responses in real-time:

```bash
# For Claude Code, Cursor, etc.
cp citation-check.sh .claude/hooks/citation-check.sh

# Configure as post-response hook in your tool
# Warns when AI generates unverified citations
```

## Database Setup

The checker verifies citations against multiple sources:

### 1. Bibliography (`research/BIBLIOGRAPHY.md`)

Your project's authoritative citation list:

```markdown
# Bibliography

## Climate Science

- Richardson et al. (2023) - "Earth beyond six of nine planetary boundaries"
- Steffen et al. (2015) - "Planetary boundaries: Guiding human development"

## AI Safety

- Hendrycks et al. (2023) - "Natural Selection Favors AIs over Humans"
```

### 2. Commonly Hallucinated Citations (`research/COMMONLY_HALLUCINATED_CITATIONS.md`)

Known fabricated references to flag:

```markdown
# Commonly Hallucinated Citations

## Non-Existent Papers

- Johnson & Smith (2025) - This paper doesn't exist, frequently hallucinated
- arXiv:2501.12345 - Fake arXiv ID (404 error)
```

### 3. Citation Correction Files (`research/CITATION_CORRECTIONS_APPLIED_*.md`)

Track fixed citations:

```markdown
# Citation Corrections Applied - 2024-11-15

## Fixed Citations

- ✅ Richardson et al. (2023) - Verified in Nature journal
- ❌ Thompson (2024) - FABRICATED, removed from codebase
```

### 4. PDF Review Files (`research/pdf_review_*.md`)

Verified academic papers:

```markdown
# PDF Review: Richardson et al. (2023)

**Status: ✅ VERIFIED**

**Paper:** Earth beyond six of nine planetary boundaries
**Authors:** Richardson, Steffen, et al.
**Journal:** Science Advances
**Year:** 2023
```

## Citation Patterns Detected

The checker recognizes common academic citation formats:

- `Author et al. (2024)` or `Author et al. (2024)`
- `Author & Author (2024)`
- `Author (2024)`
- `(Author et al., 2024)`
- `(Author, 2024)`

## Output Format

### Human-Readable

```
⚠️  CITATION VERIFICATION REPORT
============================================================
Citations found: 3
✅ Verified: 2
❓ Unverified: 1
❌ Suspicious: 0

DETAILS:
------------------------------------------------------------

1. Richardson et al. (2023)
   Status: ✅ VERIFIED

2. Smith (2024)
   Status: ❓ UNVERIFIED
   ⚠️  Not found in verified database - possible hallucination

3. Jones et al. (2022)
   Status: ✅ VERIFIED

============================================================
⚠️  WARNING: Unverified or suspicious citations detected!
These may be hallucinated. Please verify manually.
```

### JSON Output

```json
{
  "citations_found": 3,
  "verified": 2,
  "suspicious": 0,
  "unverified": 1,
  "all_verified": false,
  "results": [
    {
      "citation": "Richardson et al. (2023)",
      "original_text": "Richardson et al. (2023)",
      "verified": true,
      "suspicious": false,
      "status": "✅ VERIFIED",
      "author": "Richardson",
      "year": "2023"
    },
    {
      "citation": "Smith (2024)",
      "original_text": "Smith (2024)",
      "verified": false,
      "suspicious": false,
      "status": "❓ UNVERIFIED",
      "author": "Smith",
      "year": "2024"
    }
  ]
}
```

## Exit Codes

- `0` - All citations verified (safe to commit)
- `1` - Unverified or suspicious citations found (review needed)

## Real-World Example: Oct 2025 Citation Crisis

This tool was born from a real incident:

**Problem:** An AI agent generated 50+ citations for a research simulation project. Upon manual verification, **40% were completely fabricated** - plausible-looking references to papers that didn't exist.

**Impact:**
- 2 weeks wasted tracking down non-existent papers
- Loss of confidence in AI research assistance
- Manual audit of entire codebase required

**Solution:** This tool now runs on every commit, catching hallucinations immediately.

**Case study:** See `docs/case-studies/research-citation-crisis.md` in this repo for full details.

## Configuration

### Custom Database Paths

Edit `citationChecker.py` to customize paths:

```python
class CitationChecker:
    def __init__(self, repo_root: Path = None):
        self.repo_root = repo_root or Path(__file__).parent

        # Customize these paths
        self.bibliography = self.repo_root / "docs/citations.md"
        self.hallucinated = self.repo_root / "docs/known_hallucinations.md"
```

### Strict Mode (Block Commits)

By default, the git hook **warns** but doesn't block commits. To enforce strict verification:

Edit `.git/hooks/pre-commit`:

```bash
# Change from:
exit 0  # Warn but allow

# To:
exit 1  # Block commit if unverified
```

## Testing

```bash
# Run test suite
python test_citationChecker.py

# Test with sample text
echo "Richardson et al. (2023) found that Earth has crossed 6 of 9 planetary boundaries" \
  | python citationChecker.py --stdin
```

## How It Works

1. **Extract citations** using regex patterns (no NLP required)
2. **Normalize formats** to canonical form (`Author et al. (YYYY)`)
3. **Check databases** for verified/suspicious citations
4. **Flag unverified** citations for manual review
5. **Exit with code** (0 = safe, 1 = review needed)

## Limitations

- **Regex-based** - May miss unusual citation formats
- **Database maintenance** - Requires manual curation of verified citations
- **Author-year only** - Doesn't verify titles or DOIs (future enhancement)
- **English citations** - Optimized for English-language papers

## Roadmap

- [ ] Support for DOI/arXiv ID verification
- [ ] Web API integration (CrossRef, arXiv)
- [ ] Multi-language citation detection
- [ ] Citation correction suggestions
- [ ] Browser extension for real-time checking

## Contributing

Pull requests welcome! Areas of interest:

- Additional citation pattern detection
- Integration with citation managers (Zotero, Mendeley)
- Performance optimization for large codebases
- Web service deployment

## License

MIT License - See LICENSE file for details.

## Citation

If you use this tool in academic work:

```
@software{citation_hallucination_checker_2025,
  title = {Citation Hallucination Checker},
  author = {Howard, Liz (Future Infinitive)},
  year = {2025},
  url = {https://github.com/lizTheDeveloper/citation-checker}
}
```

## Support

- **Issues:** https://github.com/lizTheDeveloper/citation-checker/issues
- **Discussions:** https://github.com/lizTheDeveloper/citation-checker/discussions

## Credits

Created by **Liz The Developer** (aka **Future Infinitive ☸️**)

Born from the October 2025 citation crisis in the "Super-Alignment to Utopia" research simulation project.

---

**Remember:** AI is powerful, but trust, then verify. Especially citations. 📚✅
