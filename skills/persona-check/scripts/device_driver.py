#!/usr/bin/env python3
"""라이브 워크스루용 디바이스 드라이버 — rundroid 핵심 컨셉(눈금자 스크린샷)을 로컬 adb로 재현.

persona-check의 워크스루(B)를 '정적 스크린샷 Read'가 아니라 '실기기 직접 조작'으로 돌리기 위한
다리(harness). rundroid(Cloudflare Workers 서버+실기기 WebSocket)가 없어도, 로컬 에뮬레이터/USB
기기를 adb로 몰며 같은 결과물(눈금자가 달린 PNG)을 만든다.

rundroid SKILL.md에서 재현한 핵심:
  - 스크린샷 상단(X축)·우측(Y축) 눈금자 + 200px 격자선 → 좌표를 '추정' 말고 '읽어서' 탭.
  - tap 후 터치 지점에 반투명 빨간 원 + 액션 후 안정화 딜레이.
  - a11y(flat) = 클릭 가능 요소를 center 좌표와 함께.
눈금자 라벨은 항상 '실제 디바이스 픽셀 좌표'다. 이미지가 축소돼도 라벨은 실좌표라 그대로 tap에 쓴다.

전제: `adb`가 PATH 또는 ~/Library/Android/sdk/platform-tools 에 있고, 기기 1대 연결됨.
      대상 앱 패키지명을 환경변수 PD_PKG로 준다(필수). 필름스트립은 PD_SESSION 설정 시 자동 보존.

사용법:
  PD_PKG=com.example.app driver.py size|reset|launch|shot|a11y
  PD_PKG=... driver.py tap X Y
  PD_PKG=... driver.py swipe x1 y1 x2 y2 [dur]
  PD_PKG=... driver.py text "문자열(ASCII/숫자)"
  PD_PKG=... driver.py key CODE        # 66 Enter, 67 Backspace, 4 Back, 3 Home
  PD_PKG=... driver.py back|home
  PD_SESSION=p01 PD_PKG=... driver.py tap 540 1200   # 액션마다 sessions/p01/NNN.png 보존

단일 기기 = 한 번에 한 페르소나만(워크스루는 직렬). 페르소나 교체 시 `reset`으로 첫 실행부터.
"""
import os, sys, subprocess, re
import time as _time
from PIL import Image, ImageDraw, ImageFont


def _adb_bin():
    cand = os.path.expanduser("~/Library/Android/sdk/platform-tools/adb")
    return cand if os.path.exists(cand) else "adb"


ADB = _adb_bin()
OUTDIR = os.environ.get("PD_OUTDIR", "/tmp/pd")
OUT = os.path.join(OUTDIR, "current.png")
GRID = 200
MAXLONG = 1500
TOP = 52
RIGHT = 104


def pkg():
    p = os.environ.get("PD_PKG")
    if not p:
        sys.exit("PD_PKG 환경변수(대상 앱 패키지명)가 필요합니다. 예: PD_PKG=com.example.app")
    return p


def adb(*args, binary=False, timeout=30):
    r = subprocess.run([ADB, *args], capture_output=True, timeout=timeout)
    return r.stdout if binary else r.stdout.decode(errors="replace")


def device_size():
    out = adb("shell", "wm", "size")
    line = [l for l in out.splitlines() if "size:" in l]
    s = (line[-1] if line else out).split(":")[-1].strip()
    w, h = s.split("x")
    return int(w), int(h)


def screencap():
    raw = adb("exec-out", "screencap", "-p", binary=True)
    p = os.path.join(OUTDIR, "_raw.png")
    with open(p, "wb") as f:
        f.write(raw)
    return Image.open(p).convert("RGB")


def font(sz):
    for path in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                 "/System/Library/Fonts/Supplemental/Arial.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, sz)
    return ImageFont.load_default()


def render(tap=None, out=OUT):
    img = screencap()
    W, H = img.size
    scale = min(1.0, MAXLONG / max(W, H))
    sw, sh = int(W * scale), int(H * scale)
    base = img.resize((sw, sh))
    canvas = Image.new("RGB", (sw + RIGHT, sh + TOP), (250, 250, 250))
    canvas.paste(base, (0, TOP))
    d = ImageDraw.Draw(canvas, "RGBA")
    f = font(22)
    gs = int(GRID * scale)

    i, x = 0, 0
    while x <= W:
        sx = int(x * scale)
        d.line([(sx, TOP), (sx, TOP + sh)], fill=(0, 160, 255, 80), width=1)
        col = (230, 70, 70) if i % 2 == 0 else (60, 110, 230)
        d.rectangle([sx, 0, sx + gs, TOP], fill=col)
        d.text((sx + 4, 14), str(x), fill=(255, 255, 255), font=f)
        x += GRID; i += 1

    i, y = 0, 0
    while y <= H:
        sy = int(y * scale) + TOP
        d.line([(0, sy), (sw, sy)], fill=(0, 160, 255, 80), width=1)
        col = (230, 70, 70) if i % 2 == 0 else (60, 110, 230)
        d.rectangle([sw, sy, sw + RIGHT, sy + gs], fill=col)
        d.text((sw + 8, sy + 8), str(y), fill=(255, 255, 255), font=f)
        y += GRID; i += 1

    if tap:
        tx, ty = tap
        cx, cy = int(tx * scale), int(ty * scale) + TOP
        r = 32
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=(255, 0, 0, 110), outline=(255, 0, 0, 230), width=3)

    canvas.save(out)
    sess = os.environ.get("PD_SESSION")
    saved = ""
    if sess:
        sdir = os.path.join(OUTDIR, "sessions", sess)
        os.makedirs(sdir, exist_ok=True)
        cfile = os.path.join(sdir, ".counter")
        n = (int(open(cfile).read().strip()) + 1) if os.path.exists(cfile) else 0
        open(cfile, "w").write(str(n))
        canvas.save(os.path.join(sdir, f"{n:03d}.png"))
        saved = "  -> " + os.path.join(sdir, f"{n:03d}.png")
    print(f"{out}  device={W}x{H} shown={scale:.2f}x  grid={GRID}px"
          + (f"  tap=({tap[0]},{tap[1]})" if tap else "") + saved)


def a11y_flat():
    adb("shell", "uiautomator", "dump", "/sdcard/_pd.xml")
    xml = adb("shell", "cat", "/sdcard/_pd.xml")
    rows = []
    for m in re.finditer(r'<node[^>]*>', xml):
        tag = m.group(0)
        def attr(name):
            mm = re.search(name + r'="([^"]*)"', tag)
            return mm.group(1) if mm else ""
        clickable = attr("clickable") == "true"
        text = attr("text"); desc = attr("content-desc")
        if not (clickable or text or desc):
            continue
        b = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', tag)
        if not b:
            continue
        x1, y1, x2, y2 = map(int, b.groups())
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        rows.append((cy, cx, f"[{'TAP' if clickable else '   '}] ({cx},{cy})  \"{(text or desc).strip()}\""))
    for _, _, line in sorted(rows):
        print(line)


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    if len(sys.argv) < 2:
        print(__doc__); return
    cmd, a = sys.argv[1], sys.argv[2:]
    if cmd == "size":
        print("%dx%d" % device_size())
    elif cmd == "reset":
        print(adb("shell", "pm", "clear", pkg()).strip())
    elif cmd == "launch":
        print(adb("shell", "monkey", "-p", pkg(), "-c",
                  "android.intent.category.LAUNCHER", "1").strip())
        _time.sleep(2.5); render()
    elif cmd == "shot":
        render()
    elif cmd == "tap":
        x, y = int(a[0]), int(a[1])
        adb("shell", "input", "tap", str(x), str(y)); _time.sleep(0.6)
        render(tap=(x, y))
    elif cmd == "swipe":
        dur = a[4] if len(a) > 4 else "300"
        adb("shell", "input", "swipe", a[0], a[1], a[2], a[3], dur); _time.sleep(0.6)
        render()
    elif cmd == "text":
        adb("shell", "input", "text", a[0].replace(" ", "%s")); _time.sleep(0.4)
        render()
    elif cmd == "key":
        adb("shell", "input", "keyevent", a[0]); _time.sleep(0.4); render()
    elif cmd == "back":
        adb("shell", "input", "keyevent", "4"); _time.sleep(0.4); render()
    elif cmd == "home":
        adb("shell", "input", "keyevent", "3"); _time.sleep(0.4); render()
    elif cmd == "a11y":
        a11y_flat()
    else:
        print("unknown:", cmd); print(__doc__)


if __name__ == "__main__":
    main()
