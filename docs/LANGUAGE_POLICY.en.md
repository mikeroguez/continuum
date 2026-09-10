# Language policy

> [Leer en español](LANGUAGE_POLICY.md)

**Source version:** `1dacfc8` (2026-09-09). The Spanish policy is canonical if
the two versions differ.

Continuum began with a team whose working language is Spanish. Making the
project accessible does not mean replacing that language; it means declaring
the source of truth clearly and giving other contributors a reliable path in.

## Principle

Spanish is the project’s canonical editorial language. When an English
translation exists, it identifies its source document and version. If texts
differ, the Spanish text takes precedence until maintainers resolve the
discrepancy.

Do not mix languages within a document body, except for proper names, commands,
code, paths, and technical terms whose translation would make them less precise.

## What is available in both languages

The documents needed to evaluate, begin using, or contribute to Continuum are
maintained in Spanish and English:

- overview, installation, and core usage (`README.md` / `README.en.md`);
- contribution guide (`CONTRIBUTING.md` / `CONTRIBUTING.en.md`);
- this policy and the English documentation index (`docs/en/README.md`).

CLI messages, file names, and configuration examples remain stable technical
interfaces. Localising them is outside this policy unless it can be maintained
without changing scripts, automation, or output consumed by other tools.

## Specialised documentation

Architecture, research, protocol, metrics, and product-planning documents are
initially maintained in Spanish. `docs/en/README.md` describes their purpose in
English and links to the canonical originals.

A complete English translation of a specialised document is added only when:

1. its content is stable enough that two versions will not immediately drift;
   and
2. any hypothesis, method, result, or sensitive data has passed the relevant
   scientific, privacy, and publication review.

Translations must not disclose research results, usage metrics, or details
reserved for a future paper or evaluation.

## Files and maintenance

- Spanish originals keep their existing paths.
- English root documents use an `.en.md` suffix; specialised English material
  lives in `docs/en/`.
- Guides distributed in `template/docs/` use explicitly paired Spanish and
  English titles and are linked from their own index.
- Each translation begins with a link to its original and a `Source version:`
  line naming the source tag or commit.
- Anyone changing a paired document reviews its counterpart in the same change.
  If they cannot update it, they mark the translation stale and describe the
  gap in the related pull request or issue.

Translations are not automated in a release. They are editorial work that must
preserve meaning, limits, and tone rather than merely replace words.

## Navigation

Each root README links to its counterpart. `docs/en/README.md` gives
international readers a route to every specialised document, even before a
full translation is ready.

This keeps the project accessible today without obscuring which text has
authority or claiming parity that does not yet exist.
