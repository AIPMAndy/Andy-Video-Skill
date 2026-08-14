# Demo Assets TODO

## 需要创建的演示资源

### 1. Demo GIF/Video for README
- [ ] 录制 Attention Mechanism 完整演示（10-15秒）
- [ ] 转换为高质量 GIF（< 5MB）
- [ ] 上传到 `docs/assets/demo.gif`
- [ ] 更新 README.md 和 README_EN.md 中的占位链接

### 2. 截图资源
- [ ] CLI 工具使用截图
- [ ] 生成的视频效果截图（4个场景）
- [ ] 颜色方案对比图

### 3. 示例视频
- [ ] 上传完整的 Attention Mechanism 视频到 YouTube
- [ ] 创建播放列表
- [ ] 在 README 中添加视频链接

## 创建命令

```bash
# 1. 渲染高质量视频
cd examples/attention_mechanism
./render_all.sh production

# 2. 合并场景
ffmpeg -i intro.mp4 -i basics.mp4 -i math.mp4 -i conclusion.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0[outv]" \
  -map "[outv]" full_demo.mp4

# 3. 转换为 GIF
ffmpeg -i full_demo.mp4 -vf "fps=15,scale=800:-1:flags=lanczos" \
  -c:v gif demo.gif

# 4. 优化 GIF 大小
gifsicle -O3 --colors 256 demo.gif -o demo_optimized.gif
```

## 替换占位符

在 README.md 和 README_EN.md 中：

```markdown
# 当前占位符
![Demo Animation](https://via.placeholder.com/800x450/171717/00FFFF?text=Demo+Coming+Soon)

# 替换为
![Demo Animation](docs/assets/demo.gif)
```
