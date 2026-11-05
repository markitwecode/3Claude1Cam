#!/bin/bash
# Publish the shareable part of the studio to the public GitHub repo.
#   engine/tools/publish.sh "commit message"
# Never push this local repo itself: its history holds lecture material and voice samples. This copies
# the working tree into a separate clone of the public repo, filtered by engine/publish.gitignore
# (which also becomes the public .gitignore), then commits and pushes there.
set -euo pipefail
STUDIO="$(cd "$(dirname "$0")/../.." && pwd)"
PUB="${VK_PUBLISH_DIR:-$HOME/.cache/3claude1cam-public}"
REMOTE="https://github.com/markitwecode/3Claude1Cam.git"
MSG="${1:?usage: publish.sh \"commit message\"}"
[ -d "$PUB/.git" ] || git clone -q "$REMOTE" "$PUB"
git -C "$PUB" pull -q --ff-only
rsync -a --delete --exclude=.git --exclude=.gitignore \
      --exclude-from="$STUDIO/engine/publish.gitignore" "$STUDIO/" "$PUB/"
cp "$STUDIO/engine/publish.gitignore" "$PUB/.gitignore"
cd "$PUB"
git add -A
if git diff --cached --quiet; then echo "nothing to publish"; exit 0; fi
# refuse anything that looks private or too big
bad=$(git diff --cached --name-only --diff-filter=AM | grep -E '(^|/)source/|\.wav$|\.mp4$|engine/assets/voice/' || true)
[ -z "$bad" ] || { echo "refusing, private material staged:"; echo "$bad"; exit 1; }
big=$(git diff --cached --name-only --diff-filter=AM -z | xargs -0 du -k 2>/dev/null | awk '$1 > 20000 {print}' || true)
[ -z "$big" ] || { echo "refusing, files over 20 MB:"; echo "$big"; exit 1; }
git diff --cached --stat | tail -1
git -c user.name="$(git -C "$STUDIO" config user.name)" -c user.email="$(git -C "$STUDIO" config user.email)" \
    commit -q -m "$MSG"
git push -q origin main
echo "published $(git log --oneline -1)"
