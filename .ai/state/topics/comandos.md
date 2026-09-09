# Comandos de referencia rápida

```bash
tools/continuum doctor
tools/continuum task start <slug> --size small|medium|large
tools/continuum task claim <slug> <owner>
tools/continuum task close <slug>
tools/continuum handoff --message "..."
tools/continuum handoff --auto --provider claude
tools/continuum compact --topic <nombre>
tools/continuum memory-split-legacy
tools/continuum packetize <archivo> [--slug <slug>]
tools/continuum install-hooks
```

## Smoke test manual del CLI (no hay suite automatizada todavía)

Probar el ciclo completo en una copia descartable antes de tocar `template/`:

```bash
rm -rf /tmp/continuum-test && mkdir -p /tmp/continuum-test
cp -r template/. /tmp/continuum-test/
cd /tmp/continuum-test && git init -q && git add -A && git commit -qm init
tools/continuum doctor
```

## Validar los diagramas Mermaid de `ARCHITECTURE.md`

```bash
npx --yes -p @mermaid-js/mermaid-cli mmdc -i diagrama.mmd -o diagrama.svg \
  -p puppeteer-config.json   # {"args":["--no-sandbox"]}
```
