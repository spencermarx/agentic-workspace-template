# Confidentiality standards

## What never leaves the vault

Client material is written on the assumption that it stays here. Before any
artifact goes outward, whether an email, a deck, a published page, a shared
document, or a message to a third party, it is checked for:

- Named clients and named individuals, unless the artifact is for them.
- Commercial terms: rates, margins, contract values, renewal dates.
- Anything a signed agreement covers.
- Internal assessments of people or organizations.

An agent does not send outward on its own judgment. Publishing is a human act.

## Credentials never enter a note

Access notes record the system, the account identifier, the owner, and where the
credential lives: a password manager item name, or a path under `.credentials/`.
They never record the credential itself.

A token pasted into a note is in git history permanently, and git history is
what the whole workspace is built to preserve.

## PII minimisation

A person note carries what you need to work with someone: role, organization,
how to reach them, how they prefer to work, what they are trying to achieve.

It does not carry home addresses, identification numbers, financial details,
health information, or anything about their family, unless there is a concrete
working reason and they know you have it.

The test: if they read the note, would it be a normal thing for a colleague to
have written?
