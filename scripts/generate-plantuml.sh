# From your kata repo root
COURSE_REPO="$HOME/e252025/SDP-Powered-by-AI-Agents-2026-04-06"
mkdir -p hooks
cp "$COURSE_REPO/scripts/hooks/validate-plantuml.sh" hooks/
chmod +x hooks/validate-plantuml.sh
