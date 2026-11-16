import argparse, json, sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

ANDROID = "{http://schemas.android.com/apk/res/android}"

SENSITIVE = {
    "android.permission.CAMERA",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.ACCESS_BACKGROUND_LOCATION",
    "android.permission.READ_CONTACTS",
    "android.permission.RECORD_AUDIO"
}

def attr(node, name, default=None):
    return node.attrib.get(ANDROID + name, default)

def audit(manifest_path, config_path):
    root = ET.parse(manifest_path).getroot()
    cfg = json.load(open(config_path, encoding="utf-8"))
    findings = []

    requested = {p.attrib.get(ANDROID + "name", "") for p in root.findall("uses-permission")}
    required = set(cfg.get("required_permissions", []))

    for permission in sorted(requested):
        if permission in SENSITIVE and permission not in required:
            findings.append(("Permission", permission, "Over-requested permission",
                             "Remove unless a documented feature requires it", "FAIL"))
        elif permission in SENSITIVE:
            findings.append(("Permission", permission, "Sensitive permission",
                             "Request just-in-time and explain feature purpose", "CONDITIONAL"))

    app = root.find("application")
    if app is not None and attr(app, "usesCleartextTraffic", "false").lower() == "true":
        findings.append(("Network", "usesCleartextTraffic=true", "Cleartext permitted",
                         "Disable cleartext and use HTTPS with certificate validation", "FAIL"))

    if app is not None:
        for tag in ("activity", "service", "receiver", "provider"):
            for component in app.findall(tag):
                name = attr(component, "name", "unnamed")
                exported = attr(component, "exported")
                if exported == "true":
                    findings.append(("Component", name, "Exported component",
                                     "Set exported=false unless cross-app entry is required; validate callers", "FAIL"))

    for endpoint in cfg.get("network_endpoints", []):
        scheme = urlparse(endpoint).scheme.lower()
        if scheme != "https":
            findings.append(("Endpoint", endpoint, "Non-HTTPS endpoint",
                             "Use HTTPS and validate hostname/certificate chain", "FAIL"))
        else:
            findings.append(("Endpoint", endpoint, "HTTPS configured",
                             "Verify TLS validation at runtime; consider pinning for high-risk assets", "CONDITIONAL"))

    for store in cfg.get("data_stores", []):
        stype = store.get("type", "").lower()
        key = store.get("key_storage", "").lower()
        if "encrypted" not in stype or key not in ("android_keystore", "hardware_keystore", "keychain"):
            findings.append(("Storage", store.get("name","unnamed"), "At-rest protection unclear",
                             "Encrypt sensitive data and protect keys with Keystore/Keychain", "FAIL"))
        else:
            findings.append(("Storage", store.get("name","unnamed"), "Encrypted store declared",
                             "Verify key hardware backing and backup exclusions on device", "CONDITIONAL"))

    if not cfg.get("signing_configured", False):
        findings.append(("Integrity", "app signing", "Signing configuration missing",
                         "Sign release builds and verify update signer continuity", "FAIL"))
    if cfg.get("debuggable", True):
        findings.append(("Build", "debuggable=true", "Debug build configuration",
                         "Disable debugging in release build", "FAIL"))

    statuses = [x[4] for x in findings]
    verdict = "FAIL" if "FAIL" in statuses else ("CONDITIONAL" if "CONDITIONAL" in statuses else "PASS")
    return findings, verdict

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("config")
    args = ap.parse_args()
    try:
        findings, verdict = audit(args.manifest, args.config)
    except Exception as e:
        print("AUDIT_ERROR:", e, file=sys.stderr)
        raise SystemExit(2)

    print("MOBILE SECURITY AUDIT")
    print("=====================")
    for asset, name, threat, control, status in findings:
        print(f"\nAsset: {asset} / {name}\nThreat: {threat}\nControl: {control}\nResult: {status}")
    print(f"\nFINAL VERDICT: {verdict}")
    print("Note: static audit only; validate runtime behaviour separately.")

if __name__ == "__main__":
    main()
