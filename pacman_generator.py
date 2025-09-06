import requests
import datetime
import math

USERNAME = "your-username"

# 🔹 Step 1: Get user events (last 90 days by default)
url = f"https://api.github.com/users/{USERNAME}/events"
r = requests.get(url)
events = r.json()

# 🔹 Step 2: Count commits by day
commits = {}
for e in events:
    if e.get("type") == "PushEvent":
        date = datetime.datetime.fromisoformat(e["created_at"].replace("Z", "+00:00")).date()
        commits[date] = commits.get(date, 0) + len(e["payload"]["commits"])

# 🔹 Step 3: SVG setup
CELL_SIZE = 12
GRID_W, GRID_H = 53, 7
width, height = GRID_W*CELL_SIZE, GRID_H*CELL_SIZE

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']

# Draw commit dots
for i in range(GRID_W):
    for j in range(GRID_H):
        x, y = i*CELL_SIZE + CELL_SIZE//2, j*CELL_SIZE + CELL_SIZE//2
        svg.append(f'<circle cx="{x}" cy="{y}" r="2" fill="white"/>')

# 🔹 Step 4: Pac-Man animation (moves along grid)
frames = []
for step in range(GRID_W*GRID_H):
    col, row = step % GRID_W, (step // GRID_W) % GRID_H
    x, y = col*CELL_SIZE + CELL_SIZE//2, row*CELL_SIZE + CELL_SIZE//2
    mouth_angle = 40 if step % 2 == 0 else 10  # chomping effect

    pacman = f'''
      <circle cx="10" cy="10" r="5" fill="yellow">
  <animateTransform attributeName="transform"
                    type="translate"
                    from="0 0" to="200 0"
                    dur="5s"
                    repeatCount="indefinite"/>
</circle>

    '''
    frames.append(f'<g visibility="{"visible" if step==0 else "hidden"}">{pacman}</g>')

# 🔹 Step 5: Animate frames
for i, frame in enumerate(frames):
    dur = 0.2
    svg.append(f'''
    <g>
      {frame}
      <animate attributeName="visibility" values="visible;hidden" begin="{i*dur}s" dur="{dur}s" repeatCount="indefinite"/>
    </g>
    ''')

svg.append("</svg>")

with open("pacman.svg", "w") as f:
    f.write("\n".join(svg))
