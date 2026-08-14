# Contributing to Andy Liquid

Thank you for your interest in contributing to Andy Liquid!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/AIPMAndy/andy-liquid.git
cd andy-liquid
```

2. Install dependencies:
```bash
pnpm install
```

3. Start development:
```bash
pnpm dev
```

## Project Structure

```
andy-liquid/
├── packages/
│   ├── core/         # Core effects engine
│   └── react/        # React components
├── apps/
│   └── docs/         # Documentation site
├── skills/           # Agent Skills
├── design/           # Design principles
└── examples/         # Usage examples
```

## Development Guidelines

### Code Style

- Use TypeScript for all code
- Follow the existing code style
- Run `pnpm lint` before committing
- Run `pnpm format` to auto-format

### Commit Messages

Follow conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `test:` - Test additions/changes

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make your changes
4. Test thoroughly
5. Commit with conventional commits
6. Push and create a pull request

### Testing

- Write tests for new features
- Ensure all tests pass: `pnpm test`
- Test on multiple devices (desktop, mobile)
- Test accessibility features
- Test performance (Lighthouse score >90)

## Design Principles

Read [design/principles.md](design/principles.md) before contributing components.

Key principles:
- Anti-slop: No templated designs
- Performance-first: 60fps, GPU-optimized
- Accessibility: WCAG AA compliance

## Adding New Components

1. Create component in `packages/react/src/components/`
2. Add TypeScript types
3. Export from `packages/react/src/index.ts`
4. Add documentation
5. Add usage examples
6. Write tests

## Performance Requirements

All components must:
- Use GPU-safe animations (`transform`, `opacity` only)
- Support `prefers-reduced-motion`
- Support `prefers-reduced-transparency`
- Achieve Lighthouse score >90
- Work on mobile devices

## Documentation

- Document all public APIs
- Include usage examples
- Add TypeScript types
- Update README if needed

## Questions?

- Open an issue for bugs
- Start a discussion for questions
- Join our Discord (coming soon)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
