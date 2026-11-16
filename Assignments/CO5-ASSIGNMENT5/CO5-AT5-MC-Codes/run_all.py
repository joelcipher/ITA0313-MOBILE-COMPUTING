"""Run all Part B simulations from the archive root."""
import os, subprocess, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
scripts = [
    "B1_Background_Work/background_simulation.py",
    "B2_Adversarial_Workload/adversarial_workloads.py",
    "B3_UI_Optimisation/ui_optimisation.py",
    "B4_Multimedia_Decision/multimedia_strategy.py",
]
for script in scripts:
    print("\n" + "=" * 72)
    print("RUNNING", script)
    print("=" * 72)
    subprocess.run([sys.executable, os.path.join(ROOT, script)], check=True)
