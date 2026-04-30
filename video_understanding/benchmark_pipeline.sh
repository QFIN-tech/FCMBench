#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage:"
  echo "  $0 --input_file <instructions_file> --output_dir <result_dir> --video_root <video_root> --model <model> --base_url <base_url> [options]"
  echo ""
  echo "Options:"
  echo "  --api_key <key>       API key. Defaults to OPENAI_API_KEY or EMPTY."
  echo "  --fps <fps>           Video sampling FPS. Default: 2.0."
  echo "  --temperature <temp>  Sampling temperature. Default: 0.1."
  echo "  --resume             Append only missing task_id values to existing outputs."
  echo "  --skip_infer         Evaluate existing result files in output_dir."
  echo "  --run_id <id>         Output filename suffix. Default: current date in inference script."
}

INPUT_FILE=""
OUTPUT_DIR=""
VIDEO_ROOT=""
MODEL=""
BASE_URL=""
API_KEY="${OPENAI_API_KEY:-EMPTY}"
FPS="2.0"
TEMPERATURE="0.1"
RESUME=0
SKIP_INFER=0
RUN_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input_file)
      INPUT_FILE="$2"
      shift 2
      ;;
    --output_dir)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --video_root)
      VIDEO_ROOT="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    --base_url)
      BASE_URL="$2"
      shift 2
      ;;
    --api_key)
      API_KEY="$2"
      shift 2
      ;;
    --fps)
      FPS="$2"
      shift 2
      ;;
    --temperature)
      TEMPERATURE="$2"
      shift 2
      ;;
    --resume)
      RESUME=1
      shift
      ;;
    --skip_infer)
      SKIP_INFER=1
      shift
      ;;
    --run_id)
      RUN_ID="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR unknown argument: $1"
      usage
      exit 1
      ;;
  esac
done

if [[ -z "${OUTPUT_DIR}" ]]; then
  echo "ERROR --output_dir is required"
  usage
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFER_SCRIPT="${SCRIPT_DIR}/benchmark_infer.py"
EVAL_SCRIPT="${SCRIPT_DIR}/benchmark_eval.py"

mkdir -p "${OUTPUT_DIR}"

if [[ "${SKIP_INFER}" -eq 0 ]]; then
  if [[ -z "${INPUT_FILE}" || -z "${VIDEO_ROOT}" || -z "${MODEL}" || -z "${BASE_URL}" ]]; then
    echo "ERROR --input_file, --video_root, --model, and --base_url are required unless --skip_infer is set"
    usage
    exit 1
  fi

  infer_cmd=(
    python "${INFER_SCRIPT}"
    --input_file "${INPUT_FILE}"
    --output_dir "${OUTPUT_DIR}"
    --video_root "${VIDEO_ROOT}"
    --model "${MODEL}"
    --base_url "${BASE_URL}"
    --api_key "${API_KEY}"
    --fps "${FPS}"
    --temperature "${TEMPERATURE}"
  )

  if [[ "${RESUME}" -eq 1 ]]; then
    infer_cmd+=(--resume)
  fi
  if [[ -n "${RUN_ID}" ]]; then
    infer_cmd+=(--run_id "${RUN_ID}")
  fi

  "${infer_cmd[@]}"
fi

# Detect whether the output file contains ground-truth ('answer' field).
# If yes → run evaluation; if no → inference-only mode.
OUTPUT_JSONL=$(ls -t "${OUTPUT_DIR}"/*.jsonl 2>/dev/null | head -1)
if [[ -z "${OUTPUT_JSONL}" ]]; then
  echo "WARNING: no output JSONL file found in ${OUTPUT_DIR}, skipping evaluation."
  exit 0
fi

HAS_GT=$(python3 -c "
import json
with open('${OUTPUT_JSONL}', 'r') as f:
    for line in f:
        if line.strip() and 'answer' in json.loads(line):
            print('yes')
            break
    else:
        print('no')
")

if [[ "${HAS_GT}" == "yes" ]]; then
  echo "Ground-truth detected → running evaluation."
  python "${EVAL_SCRIPT}" --result_dir "${OUTPUT_DIR}" --output_dir "${OUTPUT_DIR}"
else
  echo "No ground-truth in input → inference-only mode, skipping evaluation."
  echo "Inference output: ${OUTPUT_JSONL}"
fi
