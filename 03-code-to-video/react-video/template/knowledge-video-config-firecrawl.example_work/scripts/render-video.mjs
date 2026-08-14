import { spawn } from "node:child_process";
import { existsSync, mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname, "..");

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function parseArgs(argv) {
  const args = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      continue;
    }
    const key = token.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    index += 1;
  }
  return args;
}

function runCommand(command, args, options = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      stdio: "pipe",
      ...options,
    });

    child.stdout.on("data", (buf) => process.stdout.write(buf.toString()));
    child.stderr.on("data", (buf) => process.stderr.write(buf.toString()));
    child.on("error", reject);
    child.on("exit", (code) => {
      if (code === 0) {
        resolve();
        return;
      }
      reject(new Error(`${command} exited with code ${code}`));
    });
  });
}

async function startServer(port) {
  return new Promise((resolve, reject) => {
    const child = spawn(
      "npm",
      ["run", "dev", "--", "--host", "127.0.0.1", "--port", String(port)],
      {
        cwd: root,
        stdio: "pipe",
        env: { ...process.env, BROWSER: "none" },
      }
    );

    let resolved = false;
    const finish = () => {
      if (!resolved) {
        resolved = true;
        resolve(child);
      }
    };

    child.stdout.on("data", (buf) => {
      const text = buf.toString();
      process.stdout.write(text);
      if (text.includes(`http://127.0.0.1:${port}`)) {
        finish();
      }
    });
    child.stderr.on("data", (buf) => process.stderr.write(buf.toString()));
    child.on("error", reject);
    child.on("exit", (code) => {
      if (!resolved) {
        reject(new Error(`vite exited early with code ${code}`));
      }
    });

    setTimeout(finish, 5000);
  });
}

async function transcodeToMp4(inputPath, outputPath, width, height, trimStartSec, audioPath) {
  const args = [
    "-y",
  ];

  if (trimStartSec > 0) {
    args.push("-ss", trimStartSec.toFixed(3));
  }

  args.push(
    "-i",
    inputPath,
  );

  if (audioPath) {
    args.push("-i", audioPath);
  }

  args.push(
    "-vf",
    `scale=${width}:${height}:force_original_aspect_ratio=decrease,pad=${width}:${height}:(ow-iw)/2:(oh-ih)/2:color=black`,
    "-c:v",
    "libx264",
    "-preset",
    "slow",
    "-crf",
    "18",
    "-pix_fmt",
    "yuv420p",
    "-movflags",
    "+faststart",
  );

  if (audioPath) {
    args.push(
      "-map",
      "0:v:0",
      "-map",
      "1:a:0",
      "-c:a",
      "aac",
      "-b:a",
      "192k",
      "-shortest",
    );
  } else {
    args.push("-an");
  }

  args.push(outputPath);
  await runCommand("ffmpeg", args);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const width = Number(args.width || 2400);
  const height = Number(args.height || 3200);
  const renderWidth = Number(args["render-width"] || width);
  const renderHeight = Number(args["render-height"] || height);
  const explicitDurationMs = args.duration ? Math.round(Number(args.duration) * 1000) : 0;
  const fallbackDurationMs = 8000;
  const port = Number(args.port || 4173);
  const outputPath = path.resolve(args.output || path.join(root, "output", "video", "react-video.mp4"));
  const audioPath = args.audio ? path.resolve(args.audio) : "";

  const tmpDir = path.join(root, "output", "tmp");
  mkdirSync(tmpDir, { recursive: true });
  mkdirSync(path.dirname(outputPath), { recursive: true });

  const server = await startServer(port);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: renderWidth, height: renderHeight },
    deviceScaleFactor: 1,
    recordVideo: {
      dir: tmpDir,
      size: { width: renderWidth, height: renderHeight },
    },
  });
  const page = await context.newPage();

  try {
    const recordStart = Date.now();
    await page.goto(`http://127.0.0.1:${port}`, { waitUntil: "networkidle" });
    await page.waitForFunction(() => window.__VIDEO_READY__ === true, undefined, {
      timeout: 30000,
    });
    const trimStartMs = Date.now() - recordStart;

    const pageDuration = await page.evaluate(() => {
      const value = window.__VIDEO_DURATION_MS__;
      return Number.isFinite(value) ? value : 0;
    });
    const durationMs = explicitDurationMs > 0 ? explicitDurationMs : pageDuration > 0 ? pageDuration : fallbackDurationMs;
    await wait(durationMs);

    const video = page.video();
    await context.close();
    const webmPath = await video.path();
    await transcodeToMp4(
      webmPath,
      outputPath,
      width,
      height,
      trimStartMs / 1000,
      audioPath && existsSync(audioPath) ? audioPath : "",
    );
    console.log(outputPath);
  } finally {
    await browser.close();
    server.kill("SIGTERM");
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
