import argparse
import base64
import json
import os
from datetime import datetime
from pathlib import Path

from openai import OpenAI
from tqdm import tqdm


def parse_args():
    """Parse command-line arguments for batch inference."""
    parser = argparse.ArgumentParser(
        description="Run batch inference for FCMBench-Video release instructions."
    )
    parser.add_argument("--input_file", required=True, help="Path to a single instruction JSONL file (e.g. FCMBench-Video_v1.0_full.jsonl).")
    parser.add_argument("--output_dir", required=True, help="Directory for model result JSONL files.")
    parser.add_argument("--model", required=True, help="Model name passed to the OpenAI-compatible API.")
    parser.add_argument("--base_url", required=True, help="OpenAI-compatible API base URL.")
    parser.add_argument("--api_key", default=os.environ.get("OPENAI_API_KEY", "EMPTY"))
    parser.add_argument(
        "--video_root",
        default=".",
        help="Base directory used when video_prefix is relative.",
    )
    parser.add_argument("--fps", type=int, default=2, help="Requested video sampling FPS.")
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Skip task_id values already present in the output file.",
    )
    parser.add_argument(
        "--run_id",
        dest="run_id",
        default=datetime.now().strftime("%Y%m%d"),
        help="Suffix used in output filenames.",
    )
    return parser.parse_args()


def resolve_video_path(item: dict, video_root: Path) -> Path:
    """Resolve the absolute path for the video referenced by one instruction item."""
    video_prefix = Path(str(item.get("video_prefix", "")))
    video_path = Path(str(item.get("video_path", "")))
    if video_prefix.is_absolute():
        return video_prefix / video_path
    return video_root / video_prefix / video_path


def encode_video_to_base64(video_path: Path) -> str | None:
    """Read a video file and encode it as a data URL for API submission."""
    if not video_path.exists():
        return None
    with video_path.open("rb") as f:
        payload = base64.b64encode(f.read()).decode("utf-8")
    return f"data:video/mp4;base64,{payload}"


def load_completed(output_file: Path) -> set[str]:
    """Load task IDs already present in an output file for resume mode."""
    completed = set()
    if not output_file.exists():
        return completed
    with output_file.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except Exception:
                continue
            task_id = item.get("task_id")
            if task_id:
                completed.add(task_id)
    return completed


def output_path_for(input_file: Path, output_dir: Path, model: str, run_id: str) -> Path:
    """Build the result filename for one instruction file."""
    return output_dir / f"{input_file.stem}_{model}_{run_id}.jsonl"


def call_model(client: OpenAI, model: str, prompt: str, encoded_video: str, fps: float, temperature: float) -> str:
    """Send one prompt-video pair to the API and return the raw model response."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "video_url", "video_url": {"url": encoded_video}},
                ],
            }
        ],
        temperature=temperature,
        extra_body={
            "mm_processor_kwargs": {
                "fps": fps,
                "do_sample_frames": True,
            }
        },
    )
    return response.choices[0].message.content


def infer_file(input_file: Path, output_file: Path, client: OpenAI, args) -> None:
    """Run inference over one instruction file and append JSONL responses to disk."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    completed = load_completed(output_file) if args.resume else set()

    with input_file.open("r", encoding="utf-8") as f:
        lines = [line for line in f if line.strip()]

    print(f"\nFILE: {input_file.name}")
    print(f"Output: {output_file}")
    print(f"Total: {len(lines)} | Resume hits: {len(completed)}")

    mode = "a" if args.resume and output_file.exists() else "w"
    with output_file.open(mode, encoding="utf-8") as out:
        for line in tqdm(lines, desc=input_file.name, unit="sample"):
            item = json.loads(line)
            task_id = item.get("task_id")
            if task_id in completed:
                continue

            video_file = resolve_video_path(item, Path(args.video_root))
            encoded_video = encode_video_to_base64(video_file)
            if encoded_video is None:
                item["response"] = f"Error: video file not found: {video_file}"
                out.write(json.dumps(item, ensure_ascii=False) + "\n")
                out.flush()
                continue

            try:
                item["response"] = call_model(
                    client=client,
                    model=args.model,
                    prompt=item.get("prompt", ""),
                    encoded_video=encoded_video,
                    fps=args.fps,
                    temperature=args.temperature,
                )
            except Exception as exc:
                item["response"] = f"Error: {exc}"

            out.write(json.dumps(item, ensure_ascii=False) + "\n")
            out.flush()


def main():
    """Entry point for batch inference."""
    args = parse_args()
    input_file = Path(args.input_file)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = OpenAI(api_key=args.api_key, base_url=args.base_url)
    output_file = output_path_for(input_file, output_dir, args.model, args.run_id)
    infer_file(input_file, output_file, client, args)


if __name__ == "__main__":
    main()
