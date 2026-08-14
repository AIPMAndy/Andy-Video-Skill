# Knowledge Video Configuration Guide

This guide helps you create configuration files for knowledge videos.

## Quick Start

1. Copy `knowledge-video-config.example.json` as a starting point
2. Modify the values to match your project
3. Run: `/react-video --template knowledge --config your-config.json`

## Configuration Structure

### Root Level

```json
{
  "themeColor": "indigo",  // Main theme: indigo, orange, blue, emerald, purple, red
  "project": { ... },       // Project metadata
  "steps": [ ... ]          // Video steps/scenes
}
```

### Theme Colors

Choose a theme color that matches your project's branding:
- `indigo` - Professional, tech-focused (default)
- `orange` - Energetic, creative
- `blue` - Trustworthy, corporate
- `emerald` - Growth, eco-friendly
- `purple` - Innovative, premium
- `red` - Bold, urgent

### Project Metadata

```json
"project": {
  "name": "Your Project Name",
  "stars": "162k+",                    // GitHub stars or popularity metric
  "courseNumber": "第 340 课",          // Course/episode number
  "category": "AI 基础设施 · 开源社区"  // Category/tags
}
```

## Step Types

### 1. Cover (Opening Slide)

```json
{
  "type": "cover",
  "icon": "message",                   // Icon name from lucide-react
  "badge": "162,959+ Stars",           // Top-right badge text
  "title": "Main Title",               // Large title
  "subtitle": "Subtitle Text",         // Highlighted subtitle
  "courseNumber": "第 340 课",
  "category": "Category Name",
  "script": "Opening narration..."     // Bottom script/narration
}
```

**Available icons:** star, globe, users, bot, flame, code, search, shield, check, x, layers, database, file, json, sparkles, network, terminal, user, zap, activity, settings, arrow, message, brain, alert

### 2. Pain Point (Problem Statement)

```json
{
  "type": "pain_point",
  "icon": "brain",
  "badge": "痛点：问题描述",
  "title": "Main Problem Statement",
  "script": "Explanation of the problem...",
  "visualizer": {
    "icon": "brain",
    "badge": "Additional context",
    "items": [
      {
        "icon": "code",
        "color": "red",              // red, amber, slate, blue, etc.
        "title": "Problem 1",
        "description": "Details..."
      },
      {
        "icon": "alert",
        "color": "amber",
        "title": "Problem 2",
        "description": "Details..."
      }
    ]
  }
}
```

### 3. Feature (Solution/Capability)

```json
{
  "type": "feature",
  "icon": "globe",
  "badge": "解法：解决方案",
  "title": "Solution Title",
  "script": "How this solves the problem...",
  "visualizer": {
    "steps": [
      {
        "icon": "search",
        "color": "blue",
        "title": "Step 1",
        "description": "What it does..."
      },
      {
        "icon": "users",
        "color": "purple",
        "title": "Step 2",
        "description": "What it does..."
      }
    ]
  }
}
```

### 4. Golden Sentence (Philosophy)

```json
{
  "type": "golden_sentence",
  "subtitle": "C o l l a b o r a t i o n",  // Small subtitle
  "quote": ""Your inspirational quote here."",
  "explanation": "Additional context or explanation.",
  "script": "Closing thoughts..."
}
```

### 5. Summary (Recap)

```json
{
  "type": "summary",
  "icon": "message",
  "title": "课程总结",
  "author": "AI酋长Andy",
  "footer": "github-org / repo-name",
  "script": "Final thoughts and call to action...",
  "points": [
    {
      "icon": "users",
      "color": "indigo",
      "title": "Key Point 1",
      "description": "Detailed explanation..."
    },
    {
      "icon": "shield",
      "color": "blue",
      "title": "Key Point 2",
      "description": "Detailed explanation..."
    }
  ]
}
```

## Typical Video Structure

A standard knowledge video follows this pattern:

1. **Cover** - Introduce the project (10-15 seconds)
2. **Pain Point** - Show 1-2 problems (15-20 seconds each)
3. **Feature** - Present 2-3 solutions (15-20 seconds each)
4. **Golden Sentence** - Philosophical insight (10-15 seconds)
5. **Summary** - Recap key points (20-30 seconds)

**Total duration:** 2-3 minutes

## Tips for Great Videos

### Writing Scripts
- Keep narration concise and conversational
- Use "你" (you) to engage viewers
- Start with a hook question
- End with a clear call-to-action

### Choosing Icons
- Use consistent icon styles throughout
- Match icons to content (e.g., "flame" for performance, "shield" for security)
- Don't overuse the same icon

### Color Coordination
- Stick to your theme color for primary elements
- Use red/amber for problems
- Use blue/green for solutions
- Use slate/gray for neutral items

### Pacing
- Each step should be 15-20 seconds
- Allow time for animations to complete
- Don't rush through complex visualizations

## Examples

### Tech Project Introduction
```json
{
  "themeColor": "indigo",
  "steps": [
    { "type": "cover", ... },
    { "type": "pain_point", ... },
    { "type": "feature", ... },
    { "type": "feature", ... },
    { "type": "golden_sentence", ... },
    { "type": "summary", ... }
  ]
}
```

### Product Demo
```json
{
  "themeColor": "orange",
  "steps": [
    { "type": "cover", ... },
    { "type": "pain_point", ... },
    { "type": "feature", ... },
    { "type": "feature", ... },
    { "type": "feature", ... },
    { "type": "summary", ... }
  ]
}
```

## Troubleshooting

### Icons not showing
- Check that icon name exists in ICON_MAP
- Use lowercase names (e.g., "star" not "Star")

### Colors not applying
- Tailwind CSS requires exact color names
- Use: red, orange, amber, yellow, lime, green, emerald, teal, cyan, sky, blue, indigo, violet, purple, fuchsia, pink, rose, slate, gray, zinc, neutral, stone

### Animations not smooth
- Ensure each step has enough duration
- Check that `isActive` prop is properly passed
- Verify transition timings in CSS

## Advanced Customization

For custom visualizers beyond the built-in types, you can:

1. Create a new visualizer component in `knowledge-video-generator.jsx`
2. Add it to the `renderStep` switch statement
3. Reference it in your config with a custom type

See the source code for examples of how visualizers are structured.
