# Canonical workspace

Use `docker --context orbstack` explicitly. Container: `ashish-work-directory-dev`; persistent volume: `ashish-work-directory-workspace`; workspace: `/workspaces/Ashish-work-directory`; source: `/workspaces/Ashish-work-directory/repo`.

Edits, analysis, project runtimes, checks and artifact generation run in this repository-specific container. Host copies are for review and guarded publication only. Do not mount home folders, credentials or the Docker socket. Preserve the named volume.

Run structural verification in an unprivileged, read-only, network-none container using the pinned Python image. Root guidance, catalog/CSV and 33 capability READMEs must agree; local links must resolve. This directory initialization needs structure/link checks, not implementation-mirroring unit tests or claims of tested security controls.

Before publishing, verify reviewed source hashes, reject unexpected remote/path changes, preserve existing remote content, refuse a moving main branch and verify the full resulting public file set and bytes. Never force-push to publish a directory update.
