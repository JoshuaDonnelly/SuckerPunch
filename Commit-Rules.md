# Commit Rules

This project follows **Conventional Commits**. -> [https://www.conventionalcommits.org/en/v1.0.0/#summary]  
Your commit message must clearly explain *what* changed and *why*.  
If your commit message says things like "fix stuff", rewrite it.

### Format
<type>[optional scope]: <description>


### Allowed types

| Type | When to use it |
|------|----------------|
| `feat` | Adding a new feature |
| `fix` | Fixing a bug or broken behavior |
| `docs` | Changing documentation (README, comments, etc.) |
| `refactor` | Improving code structure without changing functionality |
| `chore` | Maintenance tasks (dependency update, config change, etc.) |
| `test` | Adding or modifying tests |

### Rules

1. **One logical change per commit.**  
   If you fixed a bug and updated docs, that's **two commits**, not one.

2. **Write in the imperative form.**  
   ✅ `feat: add scraping for match data`  
   ❌ `added scraping for match data`

3. **Be specific.**  
   “Better scraping” is useless. What changed?

4. **No essay commits.**
   The message should explain the change, not tell a life story.

---

### Examples

✅ Good:

feat(scraper): extract player age from detailed table
fix(parser): correct market value selector after DOM change
docs: add commit rules to README

❌ Bad:

final fixes
stuff works now
update file