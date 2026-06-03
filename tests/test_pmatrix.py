#!/usr/bin/env python3
"""Drive pmatrix through work -> break -> work and verify the screen."""
import os, pty, time, select, sys

ROWS, COLS = 40, 120

import pyte
screen = pyte.Screen(COLS, ROWS)
stream = pyte.ByteStream(screen)

pid, fd = pty.fork()
if pid == 0:
    os.environ["TERM"] = "xterm-256color"
    os.environ["LINES"], os.environ["COLUMNS"] = str(ROWS), str(COLS)
    binary = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pmatrix")
    os.execv(binary, ["pmatrix"])

def pump(seconds):
    end = time.time() + seconds
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.05)
        if r:
            try:
                data = os.read(fd, 65536)
            except OSError:
                break
            if not data:
                break
            stream.feed(data)

def text():
    return "\n".join(screen.display)

def reverse_cells():
    """Coordinates of reverse-video cells (the big clock blocks)."""
    out = []
    for y in range(ROWS):
        row = screen.buffer[y]
        for x in range(COLS):
            if row[x].reverse:
                out.append((y, x))
    return out

failures = []

# --- Phase 1: work mode ---
pump(1.5)
t = text()
rv = reverse_cells()
if "POMODORO #1" not in t:
    failures.append("work: POMODORO #1 label missing")
if not any(y <= 7 and x > COLS // 2 for y, x in rv):
    failures.append("work: no big clock blocks in top-right corner")
print(f"[work]  label={'POMODORO #1' in t}  big-clock-cells={len(rv)}")

# --- Phase 1b: space pauses rain AND clock ---
os.write(fd, b" ")
pump(0.8)
t1 = text()
if "PAUSED #1" not in t1:
    failures.append("pause: PAUSED #1 label missing")
pump(1.3)  # > 1s so both rain and clock would visibly move if not frozen
t2 = text()
if t1 != t2:
    failures.append("pause: screen changed while paused (rain or clock not frozen)")
os.write(fd, b" ")  # resume
pump(1.3)
t3 = text()
if "POMODORO #1" not in t3:
    failures.append("pause: POMODORO #1 label not restored after resume")
if t2 == t3:
    failures.append("pause: screen identical after resume (rain did not restart)")
print(f"[pause] label={'PAUSED #1' in t1}  frozen={t1 == t2}  resumed={t2 != t3}")

# --- Phase 2: skip into break ---
os.write(fd, b"s")
pump(1.5)
t = text()
rv = reverse_cells()
mid = [c for c in rv if ROWS // 3 < c[0] < 2 * ROWS // 3]
if "B R E A K" not in t:
    failures.append("break: B R E A K title missing")
if "rain resumes after break" not in t:
    failures.append("break: hint line missing")
if not mid:
    failures.append("break: no big clock blocks in screen center")
if "POMODORO #1" in t:
    failures.append("break: work HUD residue still on screen")
print(f"[break] title={'B R E A K' in t}  center-clock-cells={len(mid)}")

# --- Phase 2b: space pauses the break clock too ---
os.write(fd, b" ")
pump(0.8)
b1 = text()
if "P A U S E D" not in b1:
    failures.append("break-pause: P A U S E D title missing")
pump(1.3)  # > 1s: break countdown would tick if not frozen
b2 = text()
if b1 != b2:
    failures.append("break-pause: screen changed while paused (break clock not frozen)")
os.write(fd, b" ")  # resume break
pump(1.3)
b3 = text()
if "B R E A K" not in b3:
    failures.append("break-pause: B R E A K title not restored after resume")
print(f"[break-pause] title={'P A U S E D' in b1}  frozen={b1 == b2}  resumed={'B R E A K' in b3}")

# --- Phase 3: skip back to work, check residue ---
os.write(fd, b"s")
pump(2.0)
t = text()
rv = reverse_cells()
center_rv = [c for c in rv if c[0] > 8]
if "B R E A K" in t:
    failures.append("work2: 'B R E A K' residue left on screen")
if "rain resumes" in t:
    failures.append("work2: break hint residue left on screen")
if center_rv:
    failures.append(f"work2: {len(center_rv)} leftover clock blocks below HUD")
if "POMODORO #2" not in t:
    failures.append("work2: POMODORO #2 label missing")
print(f"[work2] label#2={'POMODORO #2' in t}  break-residue={'B R E A K' in t or 'rain resumes' in t}  stray-blocks={len(center_rv)}")

# Visual dumps
print("\n--- top-right corner during work #2 ---")
for line in screen.display[:8]:
    print("|" + line[COLS - 42:] + "|")

os.write(fd, b"s")  # back into break for a visual of the banner
pump(1.5)
print("\n--- break banner ---")
for line in screen.display[ROWS // 2 - 6: ROWS // 2 + 5]:
    print("|" + line[20:COLS - 20] + "|")

os.write(fd, b"q")
pump(0.5)
try:
    os.kill(pid, 9)
except ProcessLookupError:
    pass

print()
if failures:
    print("FAILURES:")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("ALL CHECKS PASSED")
