TASK 4 — MOBILE SECURITY AUDIT
------------------------------
Run:
python task4/security_audit.py task4/sample_manifest.xml task4/audit_config.json

The auditor performs static checks for:
- sensitive permissions,
- exported components,
- cleartext traffic,
- HTTP endpoints,
- insecure/shared storage declarations.

It emits findings and a PASS / CONDITIONAL / FAIL verdict. Static analysis does not
prove runtime security; combine it with TLS/network testing, log review and device checks.
