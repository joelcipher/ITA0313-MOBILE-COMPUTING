"""B4: Device-aware heuristic for resolution, bitrate and upload timing."""
PROFILES = {
    "LOW": {"resolution": "480p", "bitrate_mbps": 0.8, "encode_cost": 1.0},
    "BALANCED": {"resolution": "720p", "bitrate_mbps": 2.0, "encode_cost": 2.0},
    "HIGH": {"resolution": "1080p", "bitrate_mbps": 4.5, "encode_cost": 4.0},
}

def choose_profile(device, network):
    battery = device["battery"]
    if battery < 15:
        profile, timing = "LOW", "DEFER unless user requests immediate upload"
    elif network["type"] in ("WEAK", "METERED") or network["mbps"] < 3:
        profile, timing = "LOW", "WAIT for Wi-Fi if clip is not urgent"
    elif battery > 40 and network["type"] == "WIFI" and network["mbps"] >= 20 and device["encoder"] == "HIGH":
        profile, timing = "HIGH", "UPLOAD NOW"
    else:
        profile, timing = "BALANCED", "UPLOAD NOW if stable; otherwise defer"
    return profile, timing

def estimate(device, network, clip_seconds=20):
    name = device["name"]
    selected, timing = choose_profile(device, network)
    p = PROFILES[selected]
    size_megabits = p["bitrate_mbps"] * clip_seconds
    throughput = max(0.1, network["mbps"])
    upload_seconds = size_megabits / throughput
    # Transparent proxy units, not physical joules or measured battery percentage.
    energy_proxy = p["encode_cost"] * clip_seconds / 10 + upload_seconds * (1.5 if network["type"] != "WIFI" else 0.7)
    estimated_battery_points = energy_proxy * 0.08
    return {
        "device": name, "profile": selected, "resolution": p["resolution"],
        "bitrate": p["bitrate_mbps"], "timing": timing,
        "upload_seconds": upload_seconds, "energy_proxy": energy_proxy,
        "battery_before": device["battery"],
        "battery_after_estimate": max(0, device["battery"] - estimated_battery_points)
    }

def main():
    samples = [
        ({"name":"Device A mid-range","battery":78,"encoder":"HIGH"},
         {"type":"WIFI","mbps":30}),
        ({"name":"Device B entry-level","battery":24,"encoder":"LOW"},
         {"type":"WEAK","mbps":2}),
        ({"name":"Device C flagship","battery":52,"encoder":"HIGH"},
         {"type":"WIFI","mbps":15}),
        ({"name":"Device D low battery","battery":12,"encoder":"HIGH"},
         {"type":"WIFI","mbps":50}),
    ]
    print("B4 heuristic decisions (estimates are model proxies, not device measurements)")
    for device, network in samples:
        r = estimate(device, network)
        print(f"\n{r['device']}: {r['resolution']} at {r['bitrate']} Mbps; {r['timing']}")
        print(f"  upload estimate={r['upload_seconds']:.2f}s; energy proxy={r['energy_proxy']:.2f}; "
              f"battery estimate={r['battery_before']:.2f}% -> {r['battery_after_estimate']:.2f}%")
    # Deliberate challenge: strong Wi-Fi and battery trigger HIGH although thermal/scene data is absent.
    challenging_device = {"name":"Counter-example: hot device, noisy low-light scene",
                          "battery":70,"encoder":"HIGH"}
    challenging_network = {"type":"WIFI","mbps":40}
    chosen, _ = choose_profile(challenging_device, challenging_network)
    print(f"\nCounter-example: heuristic chooses {chosen}; a 720p balanced profile may be better")
    print("because thermal headroom and scene quality are not inputs to this simple rule.")

if __name__ == "__main__":
    main()
