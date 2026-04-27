#!/bin/bash
# Start backend and frontend for PrefQuest Study 2.
#
# Usage:
#   bash study2_app/start.sh              # default provider (qwen3)
#   bash study2_app/start.sh qwen3        # explicit qwen3 (remote ollama)
#   bash study2_app/start.sh gpt5-chat    # gpt-5-chat via gptsapi.net
#
# Or override via env: LLM_PROVIDER=gpt5-chat bash study2_app/start.sh
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# ------------------------------------------------------------------
# Provider switch — first CLI arg wins, then $LLM_PROVIDER, default qwen3.
# ------------------------------------------------------------------
PROVIDER="${1:-${LLM_PROVIDER:-qwen3}}"

case "$PROVIDER" in
  qwen3|ollama)
    export LLM_BACKEND="ollama"
    export LLM_MODEL="qwen3"
    export LLM_BASE_URL="http://110.42.252.68:8080"
    unset LLM_API_KEY
    ;;
  gpt5-chat|gpt5|openai)
    export LLM_BACKEND="openai"
    export LLM_MODEL="gpt-5-chat"
    export LLM_BASE_URL="https://api.gptsapi.net/v1"
    export LLM_API_KEY="sk-SBW375246ecb7151533516297e5c382b866154a68fdfd9uZ"
    ;;
  *)
    echo "ERROR: unknown LLM provider '$PROVIDER'. Supported: qwen3 | gpt5-chat" >&2
    exit 1
    ;;
esac

# Resolve Python/uvicorn. Priority:
#   1. $PREFQUEST_PYTHON_BIN  (explicit override: dir containing `uvicorn`)
#   2. Activated conda env    ($CONDA_PREFIX/bin)
#   3. `uvicorn` on PATH
if [ -n "$PREFQUEST_PYTHON_BIN" ]; then
  UVICORN="$PREFQUEST_PYTHON_BIN/uvicorn"
elif [ -n "$CONDA_PREFIX" ] && [ -x "$CONDA_PREFIX/bin/uvicorn" ]; then
  UVICORN="$CONDA_PREFIX/bin/uvicorn"
elif command -v uvicorn >/dev/null 2>&1; then
  UVICORN="$(command -v uvicorn)"
else
  echo "ERROR: cannot find 'uvicorn'. Activate your conda env (e.g. 'conda activate behavior'),"
  echo "       or set PREFQUEST_PYTHON_BIN=/path/to/env/bin"
  exit 1
fi

# Backend only calls direct endpoints (ollama / openai / Dashscope).
# Unset every proxy variable so neither HTTP nor WebSocket calls are routed
# through a local proxy (clash etc.), which adds 5–10 s latency to TTS/STT
# and can fail outright if the proxy is dead. Belt + braces with NO_PROXY
# entries for the specific hosts in case some library reads its own variant.
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY \
      ws_proxy wss_proxy WS_PROXY WSS_PROXY 2>/dev/null
LLM_HOST="$(printf '%s' "$LLM_BASE_URL" | sed -E 's|^[a-z]+://([^:/]+).*|\1|')"
export NO_PROXY="localhost,127.0.0.1,${LLM_HOST},dashscope.aliyuncs.com,dashscope-finance.aliyuncs.com"
export no_proxy="$NO_PROXY"

# STT via Aliyun Dashscope (paraformer-realtime-v2).
export DASHSCOPE_API_KEY="${DASHSCOPE_API_KEY:-sk-515fc7843e934051bc2d59978fc9e030}"

BACKEND_PORT="${BACKEND_PORT:-8000}"

echo "Using uvicorn: $UVICORN"
echo "LLM provider:  $PROVIDER ($LLM_BACKEND @ $LLM_BASE_URL, model=$LLM_MODEL)"
if [ -z "$DASHSCOPE_API_KEY" ]; then
  echo "WARNING: DASHSCOPE_API_KEY is not set — voice STT will fail."
fi

echo "Starting backend on http://127.0.0.1:$BACKEND_PORT ..."
cd "$ROOT"
"$UVICORN" study2_app.backend.main:app --host 127.0.0.1 --port "$BACKEND_PORT" --reload &
BACKEND_PID=$!

echo "Starting frontend on http://localhost:5173 ..."
cd "$ROOT/study2_app/frontend"
npm run dev &
FRONTEND_PID=$!

cleanup() {
  kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null
  # uvicorn --reload occasionally leaves orphan workers on the backend port
  lsof -tiTCP:"$BACKEND_PORT" -sTCP:LISTEN 2>/dev/null | xargs -r kill -9 2>/dev/null
}
trap cleanup EXIT INT TERM

echo ""
echo "Backend:  http://127.0.0.1:$BACKEND_PORT/docs"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both."

wait
