#!/usr/bin/env python3
"""k-persona `sample` 출력(여러 인물이 한 파일)을 1인 1파일로 쪼개고 index.json을 만든다.

원칙: "브리프 1개 = 에이전트 1개". 한 컨텍스트에서 여러 인물을 연기하면 반응이 서로 오염되므로,
각 인물 브리프를 독립 파일로 분리해 두고 시뮬레이션 때 1인=1서브에이전트로 주입한다.

사용법:
  # k-persona 샘플을 세그먼트별 파일로 저장해 둔 디렉터리(예: /tmp/kp2)에 대해:
  python split_personas.py <indir> [outdir]
  # <indir>의 *.txt 각 파일을 '# 페르소나:' 경계로 쪼개 outdir에 p01.txt.. 로 저장하고
  # outdir/index.json 에 [{id,name,path,source}] 를 쓴다.

세그먼트 라벨이 필요하면 입력 파일명을 'A_서울30-44.txt'처럼 두면 source에 파일명이 남는다.
"""
import json
import re
import sys
from pathlib import Path

BOUNDARY = re.compile(r"(?m)(?=^# 페르소나:)")


def split_dir(indir: Path, outdir: Path) -> list[dict]:
    outdir.mkdir(parents=True, exist_ok=True)
    index: list[dict] = []
    n = 0
    for src in sorted(indir.glob("*.txt")):
        if src.name == "index.json":
            continue
        text = src.read_text(encoding="utf-8")
        for block in BOUNDARY.split(text):
            block = block.strip()
            if not block.startswith("# 페르소나:"):
                continue
            n += 1
            name = re.sub(r"#\s*페르소나:\s*", "", block.splitlines()[0]).strip()
            path = outdir / f"p{n:02d}.txt"
            path.write_text(block, encoding="utf-8")
            index.append(
                {"id": f"P{n:02d}", "name": name, "path": str(path), "source": src.name}
            )
    (outdir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return index


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    indir = Path(sys.argv[1])
    outdir = Path(sys.argv[2]) if len(sys.argv) > 2 else indir / "split"
    idx = split_dir(indir, outdir)
    for r in idx:
        print(r["id"], "|", r["source"], "|", r["name"])
    print(f"\n총 {len(idx)}명 → {outdir}/  (index.json 포함)")
