#!/bin/zsh
set -eu

cd "/Users/iriswu/Documents/Codex/things-of-korean/2-line-7-30-9-00"

export PUBLISH_HANHAN_IMAGES_GITHUB=1
export PUSH_HANHAN_LINE=1
export PYTHON="/Users/iriswu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"

"/Users/iriswu/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node" scripts/generate-ig-images.mjs
