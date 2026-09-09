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
