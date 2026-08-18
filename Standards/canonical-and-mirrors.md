# Canonical and mirrors

Every document is one of three things, and it says which in its frontmatter.

## The three kinds

**Canonical.** The vault owns this. Nothing upstream.

```yaml
canonical: true
authors: [person-slug]
revised: 2026-08-18
```

**Mirror.** A faithful copy of something the vault does not own.

```yaml
canonical: false
canonical_source: "../Repositories/thing/docs/spec.md"
canonical_ref: "5edaa77"
revised: 2026-08-18
```

**Summary.** A vault-authored note *about* an external artifact that it does not
copy. Canonical in its own right, because the summary is original work.

```yaml
canonical: true
related: ["[[The External Thing]]"]
```

## The rules

1. **The canonical source wins on divergence.** Always, without exception. If
   the mirror and the source disagree, the mirror is wrong by definition.
2. **A mirror is never edited to introduce new content.** Wrong content in a
   mirror is fixed upstream, then re-synced, then `revised` is bumped.
3. **A mirror states its read cost and known drift** in the owning leaf's
   `| File | When to load |` row.
4. **Prefer a summary over a mirror** for anything the vault does not need
   verbatim. Mirrors are a standing maintenance liability; every one of them is
   a promise to re-sync that somebody has to keep.
5. **A mirror whose `revised` is more than thirty days old is stale**, and the
   triage view surfaces it as such.
