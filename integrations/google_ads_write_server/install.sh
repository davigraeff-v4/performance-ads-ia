#!/usr/bin/env bash
# Instala o servidor MCP de escrita do Google Ads (googleAdsServer) fora do repositório.
#
#   bash integrations/google_ads_write_server/install.sh
#
# Variáveis opcionais:
#   GOOGLE_ADS_MCP_DIR  pasta de instalação (padrão: ~/.mcp/google-ads)
#   PYTHON              Python 3.11+ a usar (padrão: o mais novo encontrado)
#
# Não registra nada no Claude e não lê nem pede credenciais: no fim, mostra os
# próximos passos. Pode rodar de novo para atualizar; .env, token e lista de
# contas existentes são preservados.
set -euo pipefail

UPSTREAM_REPO="https://github.com/cohnen/mcp-google-ads.git"
UPSTREAM_COMMIT="461a1d673cf1c369e8b95fc9b5b1d9cb7f3ebb4a"
DEST="${GOOGLE_ADS_MCP_DIR:-$HOME/.mcp/google-ads}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pick_python() {
  if [[ -n "${PYTHON:-}" ]]; then echo "$PYTHON"; return; fi
  for candidate in python3.13 python3.12 python3.11 python3; do
    if command -v "$candidate" >/dev/null 2>&1 &&
       "$candidate" -c 'import sys; raise SystemExit(sys.version_info < (3, 11))' 2>/dev/null; then
      command -v "$candidate"; return
    fi
  done
  echo "Python 3.11 ou mais novo não encontrado. Instale (ex.: brew install python@3.13) ou defina PYTHON." >&2
  exit 1
}
PY="$(pick_python)"

echo "1/5 Código do servidor em $DEST (commit fixado ${UPSTREAM_COMMIT:0:7})"
mkdir -p "$(dirname "$DEST")"
if [[ ! -d "$DEST/.git" ]]; then
  git clone -q "$UPSTREAM_REPO" "$DEST"
else
  git -C "$DEST" fetch -q origin
  git -C "$DEST" checkout -q -- google_ads_server.py requirements.txt
fi
git -C "$DEST" checkout -q "$UPSTREAM_COMMIT"

echo "2/5 Ferramentas de escrita e ajustes"
install -m 644 "$HERE/write_tools.py" "$DEST/write_tools.py"
install -m 755 "$HERE/gerar_token.py" "$DEST/gerar_token.py"
install -m 644 "$HERE/README.md" "$DEST/LEIA-ME-INSTALACAO.md"
"$PY" "$HERE/patch_server.py" "$DEST"

echo "3/5 Ambiente Python ($("$PY" --version))"
if [[ ! -x "$DEST/.venv/bin/python" ]]; then
  "$PY" -m venv "$DEST/.venv"
fi
"$DEST/.venv/bin/python" -m pip install -q --disable-pip-version-check -r "$DEST/requirements.txt"
"$DEST/.venv/bin/python" -c "import mcp.server.fastmcp, google.auth, requests, dotenv"

echo "4/5 Arquivos locais (preservados se já existirem)"
chmod 700 "$DEST"
[[ -f "$DEST/.env" ]] || install -m 600 "$HERE/.env.example" "$DEST/.env"
[[ -f "$DEST/allowed_accounts.json" ]] || install -m 600 "$HERE/allowed_accounts.example.json" "$DEST/allowed_accounts.json"
for secret in "$DEST/.env" "$DEST/allowed_accounts.json" "$DEST"/google_ads_token*.json; do
  if [[ -f "$secret" ]]; then chmod 600 "$secret"; fi
done

echo "5/5 Conferência"
"$DEST/.venv/bin/python" - "$DEST" <<'PYCHECK'
import sys
sys.path.insert(0, sys.argv[1])
src = open(f"{sys.argv[1]}/google_ads_server.py", encoding="utf-8").read()
assert "write_tools.register(" in src and 'GOOGLE_ADS_API_VERSION' in src
print("servidor pronto")
PYCHECK

cat <<EOF

Instalado em $DEST. Próximos passos (detalhes em $DEST/LEIA-ME-INSTALACAO.md):

  a) Token OAuth, se ainda não tiver:
     $DEST/.venv/bin/python $DEST/gerar_token.py --client-secrets /caminho/credentials.json
  b) Preencher $DEST/.env (developer token, MCC, caminho do token).
  c) Listar as contas que podem ser alteradas em $DEST/allowed_accounts.json.
  d) Registrar no Claude Code para todos os projetos:
     claude mcp add-json -s user googleAdsServer '{"type":"stdio","command":"$DEST/.venv/bin/python","args":["$DEST/google_ads_server.py"],"env":{}}'
     No Claude Desktop, o mesmo bloco (sem "type") vai em mcpServers de
     ~/Library/Application Support/Claude/claude_desktop_config.json.
  e) Reiniciar o Claude e testar em modo validate_only antes de trocar para execute.
EOF
