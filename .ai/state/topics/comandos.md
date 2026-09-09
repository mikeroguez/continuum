# Comandos de referencia rápida

```bash
tools/continuum doctor [--fix] [--dry-run|--no-dry-run]
tools/continuum session start [--json]
tools/continuum session end [--message "..."] [--auto] [--provider <p>] [--role <r>] [--json]
tools/continuum status [--json]

tools/continuum context [--task <slug>] [--why] [--json]
tools/continuum tokens [--json]
tools/continuum metrics snapshot [--dry-run|--no-dry-run] [--json]
tools/continuum metrics report [--json]
tools/continuum metrics export [--format json|csv] [--anonymize] [--json]
tools/continuum metrics compare [--json]
tools/continuum task start <slug> --size small|medium|large
tools/continuum task claim <slug> <owner>
tools/continuum task current [--json]
tools/continuum task resume [<slug>] [--json]
tools/continuum task close <slug>

tools/continuum handoff --message "..."
tools/continuum handoff --auto --provider claude|codex|gemini
tools/continuum compact --topic <nombre>
tools/continuum memory-split-legacy
tools/continuum packetize <archivo> [--slug <slug>]
tools/continuum install-hooks
tools/continuum sync [--check|--dry-run|--apply] [--json]
tools/continuum export status|refresh
tools/continuum release <versión> [--dry-run|--no-dry-run] [--json]
tools/continuum github protect [--print|--apply] [--json]
tools/continuum roles list



tools/continuum roles sync   # regenerar tras clonar o tras cambios en .ai/roles/
```

## Suite de tests

```bash
python3 -m unittest discover -s tests -t . -v
```

Ver `CONTRIBUTING.md` § Tests.

## Validar los diagramas Mermaid de `ARCHITECTURE.md`

```bash
npx --yes -p @mermaid-js/mermaid-cli mmdc -i diagrama.mmd -o diagrama.svg \
  -p puppeteer-config.json   # {"args":["--no-sandbox"]}
```
