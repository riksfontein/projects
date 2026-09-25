"""Omni chain master image (first frame) on AI33 at the highest quality (Riks, 2026-09-25).

    py -3.12 _rx_first_frame_ai33.py --tag CH02EP16                 price only (free)
    py -3.12 _rx_first_frame_ai33.py --tag CH02EP16 --go            generate 2 variants, save A/B
    py -3.12 _rx_first_frame_ai33.py --tag CH02EP16 --harvest       only poll a task already paid for

Rule (Riks, 2026-09-25): first frames are made by Claude on AI33 with the best image model at its highest
quality, never in TurboFlow. Model: the newest top image model AI33 lists (a "...2.5" model when present),
otherwise gpt-image-2; 16:9, 4K, quality high, 2 variants -> Claude LOOKS at both and picks one.

Hard-won AI33 rules (ai33-capability-map, _ai33_plates_ch02_gen.py):
  - presented_credits is NOT the charge: price with POST /v1i/task/price first (real cost 3-7x);
  - credits are charged on submit: the task id is saved to a sidecar BEFORE polling, a timeout is never
    "failed", and --harvest recovers a paid task instead of paying twice;
  - GET /v1/health-check is free: if an image provider is overloaded, do not submit;
  - the image is at metadata.result_images[].imageUrl (previewUrl is a thumbnail);
  - auth header is xi-api-key (not Bearer); a 401 on /v1i/ is usually throttling -> retry with backoff.
"""
import argparse, json, os, pathlib, re, sys, time

import requests

BASE = "https://api.ai33.pro"
HERE = pathlib.Path(__file__).resolve().parent
MIN_BYTES = 200_000


def key_from(args):
    if os.environ.get(args.key_var):
        return os.environ[args.key_var]
    env = pathlib.Path(args.env) if args.env else HERE / ".env"
    for line in env.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith(args.key_var + "="):
            return line.split("=", 1)[1].split("#")[0].strip().strip("\"'")
    sys.exit(f"{args.key_var} not found in the environment or {env}")


def h(key, js=False):
    d = {"xi-api-key": key, "Accept": "application/json"}
    if js:
        d["Content-Type"] = "application/json"
    return d


def pick_model(key, forced):
    r = requests.get(f"{BASE}/v1i/models", headers=h(key), timeout=45)
    r.raise_for_status()
    rows = r.json()
    rows = rows.get("data", rows) if isinstance(rows, dict) else rows
    ids = [m.get("model_id") or m.get("id") for m in rows if isinstance(m, dict)]
    print("AI33 image models:", ", ".join(i for i in ids if i))
    if forced:
        return forced
    newer = [i for i in ids if i and re.search(r"(^|[-_ ])2\.5\b|image-2\.5", i)]
    return newer[0] if newer else "gpt-image-2"


def params(model):
    p = {"aspect_ratio": "16:9", "resolution": "4K"}
    if model.startswith("gpt-image"):
        p["quality"] = "high"
    return p


def price(key, model, prompt, n):
    body = {"model_id": model, "generations_count": n, "model_parameters": params(model), "prompt": prompt}
    r = requests.post(f"{BASE}/v1i/task/price", headers=h(key, True), json=body, timeout=45)
    if r.status_code >= 400:  # some model/resolution combos are refused: fall back to 2K once
        body["model_parameters"]["resolution"] = "2K"
        r = requests.post(f"{BASE}/v1i/task/price", headers=h(key, True), json=body, timeout=45)
    r.raise_for_status()
    return r.json(), body["model_parameters"]


def create(key, model, prompt, n, mp, tries=6):
    data = {"prompt": prompt, "model_id": model, "generations_count": str(n), "model_parameters": json.dumps(mp)}
    last = ""
    for i in range(tries):
        try:
            r = requests.post(f"{BASE}/v1i/task/generate-image", headers=h(key), data=data, timeout=90)
        except requests.exceptions.RequestException as e:
            last = f"network: {e}"[:120]
            time.sleep(10 * (i + 1))
            continue
        if r.status_code == 401:
            last = "401 (throttle, not a dead key)"
            time.sleep(15 * (i + 1))
            continue
        if r.status_code == 429 or r.status_code >= 500:
            last = f"{r.status_code}"
            time.sleep(20 * (i + 1))
            continue
        r.raise_for_status()
        j = r.json()
        if not j.get("success"):
            sys.exit(f"create refused: {str(j)[:200]}")
        return j["task_id"], j.get("ec_remain_credits")
    sys.exit(f"create failed after {tries} tries: {last} (nothing was charged unless a task id was returned)")


def urls(task):
    out = [it["imageUrl"] for it in ((task.get("metadata") or {}).get("result_images") or [])
           if isinstance(it, dict) and isinstance(it.get("imageUrl"), str)]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True, help="CH02EP16 -> reads _FLOW/CH02EP16_omni_first_frame.txt")
    ap.add_argument("--go", action="store_true", help="spend credits and generate")
    ap.add_argument("--harvest", action="store_true", help="poll the saved task only (no new charge)")
    ap.add_argument("--model", help="force a model id")
    ap.add_argument("--n", type=int, default=2, help="variants (Claude picks one)")
    ap.add_argument("--key-var", default="AI33_API_KEY_CH02")
    ap.add_argument("--env", help=".env path (default: next to this script)")
    ap.add_argument("--flow", default=str(HERE / "_FLOW"))
    a = ap.parse_args()
    flow = pathlib.Path(a.flow)
    prompt = (flow / f"{a.tag}_omni_first_frame.txt").read_text(encoding="utf-8").strip()
    out_dir = flow / "first_frames"
    out_dir.mkdir(parents=True, exist_ok=True)            # destination exists BEFORE any paid call
    sidecar = out_dir / f"{a.tag}_ff_task.json"
    key = key_from(a)

    if not a.harvest:
        hc = requests.get(f"{BASE}/v1/health-check", headers=h(key), timeout=30).json()
        print("health:", hc)
        bad = [k for k, v in (hc or {}).items() if v != "good" and k in ("gemini", "openai", "image")]
        model = pick_model(key, a.model)
        quote, mp = price(key, model, prompt, a.n)
        print(f"model {model} {mp} x{a.n}: price {json.dumps(quote)[:300]}")
        if not a.go:
            print("price only - rerun with --go to generate")
            return
        if bad:
            sys.exit(f"provider not healthy ({bad}) - not submitting; poll /v1/health-check and retry later")
        if sidecar.exists() and not json.loads(sidecar.read_text()).get("done"):
            sys.exit(f"a paid task is already pending in {sidecar} - use --harvest, do not pay twice")
        tid, remain = create(key, model, prompt, a.n, mp)
        sidecar.write_text(json.dumps({"task_id": tid, "model": model, "params": mp, "n": a.n,
                                       "t0": time.time(), "remain_after": remain}, indent=1))
        print(f"submitted {tid} (credits left: {remain})")

    st = json.loads(sidecar.read_text())
    t_end = time.time() + 30 * 60
    while time.time() < t_end:
        r = requests.get(f"{BASE}/v1/task/{st['task_id']}", headers=h(key, True), timeout=30)
        if r.status_code >= 500:
            time.sleep(15)
            continue
        task = r.json()
        s = task.get("status")
        if s in ("done", "success", "succeeded"):
            got = urls(task)
            if not got:
                sys.exit(f"finished but no imageUrl - task kept in {sidecar}: {str(task)[:300]}")
            for i, u in enumerate(got[: a.n]):
                img = requests.get(u, timeout=240)
                img.raise_for_status()
                if len(img.content) < MIN_BYTES:
                    print(f"variant {i}: {len(img.content)} bytes looks like a preview, skipped")
                    continue
                p = out_dir / f"{a.tag}_ff_{'AB'[i]}.png"
                p.write_bytes(img.content)
                print(f"saved {p} ({len(img.content) // 1024} KB)")
            st["done"] = True
            st["credit_cost"] = task.get("credit_cost")
            sidecar.write_text(json.dumps(st, indent=1))
            print(f"credit cost: {task.get('credit_cost')}")
            return
        if s in ("error", "failed"):
            st["done"] = True
            st["error"] = str(task.get("error"))[:300]
            sidecar.write_text(json.dumps(st, indent=1))
            sys.exit(f"task failed: {st['error']}")
        time.sleep(15)
    print(f"still running after 30 min - it is paid; run --harvest later (task {st['task_id']})")


if __name__ == "__main__":
    main()
