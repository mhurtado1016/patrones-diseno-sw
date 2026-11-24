"""Compara el tiempo de N requests GET /products: código original vs refactorizado.

Uso:  python benchmarks/benchmark.py [N]
Extrae la versión original del primer commit de Git a una carpeta temporal.
"""
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
import textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 500

RUNNER = textwrap.dedent("""
    import sys, time, statistics
    sys.path.insert(0, ".")
    {setup}
    c = app.test_client()
    H = {{"Authorization": "abcd1234" if {orig} else "abcd12345"}}
    assert c.get("/products", headers=H).status_code == 200
    times = []
    for _ in range({n}):
        t = time.perf_counter(); c.get("/products", headers=H); times.append(time.perf_counter() - t)
    print(sum(times))
""")


def run(cwd, setup, orig):
    code = RUNNER.format(setup=setup, orig=orig, n=N)
    out = subprocess.run([sys.executable, "-c", code], cwd=cwd, capture_output=True, text=True, check=True)
    return float(out.stdout.strip().splitlines()[-1])


def main():
    first = subprocess.check_output(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=ROOT, text=True).split()[0]
    with tempfile.TemporaryDirectory() as tmp:
        orig_dir, new_dir = os.path.join(tmp, "orig"), os.path.join(tmp, "new")
        os.makedirs(orig_dir)
        subprocess.run(f"git archive {first} | tar -x -C {orig_dir}", shell=True, cwd=ROOT, check=True)
        orig_dir = os.path.join(orig_dir, "course_desing_patterns") if os.path.isdir(
            os.path.join(orig_dir, "course_desing_patterns")) else orig_dir
        shutil.copytree(ROOT, new_dir, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        res = {"original": [], "refactorizado": []}
        for _ in range(5):
            res["original"].append(run(orig_dir, "import app as m; app = m.app", True))
            res["refactorizado"].append(run(new_dir, "from app import create_app; app = create_app()", False))
    print(f"{N} requests GET /products (mediana de 5 corridas)")
    for k, v in res.items():
        print(f"  {k:14s}: {statistics.median(v):.3f} s total, {statistics.median(v)/N*1000:.2f} ms/request")
    print(f"  mejora: x{statistics.median(res['original'])/statistics.median(res['refactorizado']):.1f}")


if __name__ == "__main__":
    main()
