# Contributing

## Reporting Bugs

Open an issue using the **Bug Report** template. Include:
- Steps to reproduce
- Expected vs actual behavior
- Skill name + version
- Your environment (OS, Claude Code version)

## Requesting a New Skill

Use the **Feature Request** template. Describe:
- What the skill should do
- Which category it fits
- Whether you have source code or need it built

## Submitting a Skill via PR

1. Fork this repo
2. Place your skill under the appropriate category:
   ```
   0X-category-name/your-skill-name/
   ```
3. Naming: `andy-*` prefix strongly preferred; otherwise descriptive kebab-case
4. Required files in your skill dir:
   - `SKILL.md` (or `skill.md`) with frontmatter
   - `README.md` for humans
   - `LICENSE` (MIT recommended)
5. Update `CATALOG.md` to add your skill row
6. Update `CHANGELOG.md` under `## [Unreleased]`
7. Open a PR — maintainers will review

## Naming Conventions

- Skill directory: `kebab-case` (e.g. `andy-p5js`)
- Skill name in frontmatter: same as directory
- Category directories: `0X-descriptive-name` with two-digit prefix

## License

By contributing, you agree your contribution is licensed under MIT.
