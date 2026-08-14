You are helping the user generate a video from React code.

# Modes

## Mode 1: Knowledge Video Generator (Recommended)
Generate a professional knowledge video from a structured configuration file. This mode uses pre-built templates inspired by Apple's design language.

**When to use:** User wants to create an educational/tutorial video about a tech project or concept.

**Workflow:**
1. Ask if they want to use an existing config or create a new one
2. If creating new:
   - Ask for project details (name, stars, theme color)
   - Ask for pain points to highlight
   - Ask for key features/solutions
   - Ask for a golden sentence/philosophy
   - Generate config JSON
3. Use `knowledge-video-generator.jsx` as the App component
4. Pass config as a prop or embed it in the component

## Mode 2: Custom React Code
Generate video from user-provided React code (original functionality).

**When to use:** User has custom React code they want to render as video.

# Your Task

1. **Determine mode** - Ask user if they want knowledge video template or custom code
2. **Parse arguments** from the user's command (width, height, duration, output path, audio path, code file)
3. **Get React code** - either from config (Mode 1) or file/user input (Mode 2)
4. **Create temporary project** in a `.react-video-job` directory with:
   - package.json with required dependencies
   - vite.config.js
   - tailwind.config.js and postcss.config.js (if using Tailwind)
   - index.html
   - src/main.jsx
   - src/index.css
   - src/video-runtime.js (video ready signaling)
   - src/App.jsx (their React component)
   - scripts/render-video.mjs (Playwright recording script)
4. **Install dependencies** with npm install
5. **Run the render script** with appropriate arguments
6. **Report the output** video path to the user

# Key Implementation Details

## video-runtime.js
This file provides functions to signal when the video is ready to record:
- `setVideoDuration(ms)` - Set total video duration
- `markVideoReady()` - Signal that rendering is ready to start
- `markVideoNotReady()` - Reset ready state

## render-video.mjs
The rendering script should:
1. Start a Vite dev server on a specified port
2. Launch Playwright with video recording enabled
3. Navigate to the dev server
4. Wait for `window.__VIDEO_READY__ === true`
5. Record for the specified duration
6. Transcode the WebM recording to MP4 with ffmpeg
7. Optionally merge audio track

## React Component Requirements
The user's React component should:
- Call `markVideoReady()` when ready to start recording
- Optionally call `setVideoDuration(ms)` to specify duration
- Use animations and transitions as needed
- Be self-contained (all scenes/animations triggered automatically)

# Template Structure

```
.react-video-job/
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── index.html
├── src/
│   ├── main.jsx
│   ├── index.css
│   ├── video-runtime.js
│   ├── App.jsx (user's code)
│   └── social-video-layout.jsx (optional helper utilities)
├── scripts/
│   └── render-video.mjs
└── output/
    └── video/
        └── react-video.mp4
```

# Error Handling

- Check if ffmpeg is installed before starting
- Validate that required dependencies can be installed
- Handle port conflicts gracefully
- Provide clear error messages if rendering fails

# Best Practices

- Use a high port number (4173+) to avoid conflicts
- Set reasonable timeouts for page load and video ready
- Clean up temporary files after successful render
- Preserve output directory for user access
