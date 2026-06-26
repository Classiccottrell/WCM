#!/usr/bin/env python3
"""wcm — West Coast Modern hero-image pipeline CLI.

Subcommands:
  run    Run the two-stage pipeline on a single property folder.
  watch  Watch a parent directory and auto-process new property subfolders.

Install:
    pip install -e Hero-Image-Agent/
    export ANTHROPIC_API_KEY="sk-ant-..."

Usage:
    wcm run /path/to/PropertyName [--top 12] [--workers 5] [--resume]
    wcm watch /path/to/Parent [--top 12] [--workers 5] [--scan-existing]
"""
from __future__ import annotations

import argparse
import sys
import threading
import time
from pathlib import Path

import hero_select as hs


# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------

def cmd_run(args):
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    folder = Path(args.folder)
    if not folder.is_dir():
        sys.stderr.write("ERROR: not a directory: %s\n" % folder)
        return 1

    images = hs.find_images(folder)
    print("Found %d image(s) in %s" % (len(images), folder))

    if not images and not args.resume:
        sys.stderr.write(
            "ERROR: no supported images (%s) in %s\n"
            % (", ".join(sorted(hs.IMAGE_EXTS)), folder)
        )
        return 1

    client = hs.make_client()
    hs.process_folder(
        client, folder,
        top_n=args.top,
        workers=args.workers,
        skill_path=args.skill,
        images=images if images else None,
        resume=args.resume,
    )
    return 0


# ---------------------------------------------------------------------------
# watch
# ---------------------------------------------------------------------------

def cmd_watch(args):
    from watch_folder import FolderTracker, _Handler
    from watchdog.observers import Observer

    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    parent = Path(args.parent)
    if not parent.is_dir():
        sys.stderr.write("ERROR: not a directory: %s\n" % parent)
        return 1

    client = hs.make_client()

    tracker = FolderTracker(parent, client, args.top, args.workers, args.skill)
    if args.scan_existing:
        tracker.seed_existing()

    observer = Observer()
    observer.schedule(_Handler(tracker), str(parent.resolve()), recursive=True)
    observer.start()

    monitor = threading.Thread(target=tracker.monitor_loop, daemon=True)
    monitor.start()

    print(
        "[watch] watching %s (stable=30s, top=%d, workers=%d). Ctrl-C to stop."
        % (parent, args.top, args.workers)
    )
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[watch] stopping...")
    finally:
        tracker.stop = True
        observer.stop()
        observer.join()
    return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="wcm",
        description="West Coast Modern — hero-image selection pipeline.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  wcm run /shoots/HarbourView --top 20 --workers 8\n"
            "  wcm run /shoots/HarbourView --resume\n"
            "  wcm watch /shoots --scan-existing\n"
            "  wcm watch /shoots --top 20 --workers 8\n"
        ),
    )
    sub = ap.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    # -- run --
    rp = sub.add_parser(
        "run",
        help="Run the two-stage pipeline on a single property folder.",
        description=(
            "Stage 1: score every image 0-60 with a fast model in parallel.\n"
            "Stage 2: send the top-N to a strong model for the full Hero Report.\n\n"
            "Outputs written into the property folder:\n"
            "  triage_scores.csv  — every image scored\n"
            "  hero_report.md     — the Hero Report\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    rp.add_argument("folder", help="Path to the property photo folder")
    rp.add_argument(
        "--top", type=int, default=hs.DEFAULT_TOP_N, metavar="N",
        help="How many top-scoring images go to Stage 2 (default: %(default)s)",
    )
    rp.add_argument(
        "--workers", type=int, default=hs.DEFAULT_WORKERS, metavar="N",
        help="Parallel workers for Stage 1 triage (default: %(default)s)",
    )
    rp.add_argument(
        "--skill", default=None, metavar="PATH",
        help="Path to SKILL.md (default: SKILL.md next to hero_select.py)",
    )
    rp.add_argument(
        "--resume", action="store_true",
        help=(
            "Skip Stage 1 and reload triage scores from an existing "
            "triage_scores.csv — useful when Stage 1 finished but Stage 2 failed"
        ),
    )
    rp.set_defaults(func=cmd_run)

    # -- watch --
    wp = sub.add_parser(
        "watch",
        help="Watch a parent directory and auto-process new property subfolders.",
        description=(
            "Monitors a parent directory. When a new property subfolder appears\n"
            "and its contents stabilise for ~30 seconds (copy finished), the\n"
            "two-stage pipeline runs automatically. Folders that already have\n"
            "hero_report.md are skipped.\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    wp.add_argument("parent", help="Parent directory to watch")
    wp.add_argument(
        "--top", type=int, default=hs.DEFAULT_TOP_N, metavar="N",
        help="Passed through to 'run' (default: %(default)s)",
    )
    wp.add_argument(
        "--workers", type=int, default=hs.DEFAULT_WORKERS, metavar="N",
        help="Passed through to 'run' (default: %(default)s)",
    )
    wp.add_argument(
        "--skill", default=None, metavar="PATH",
        help="Path to SKILL.md (default: SKILL.md next to hero_select.py)",
    )
    wp.add_argument(
        "--scan-existing", action="store_true",
        help="Also process pre-existing subfolders that have no report yet",
    )
    wp.set_defaults(func=cmd_watch)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
