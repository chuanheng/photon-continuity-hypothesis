"""Reproduce the complete v4.22–v4.31 theoretical and synthetic batch."""
import json

from .calibration import (
    SEEDS, blind_challenge, calibration_audit, distance_certificate,
    operating_characteristics, optimize_allocation,
)
from .controlled import equivalence, hankel, positive_realization
from .optics import dispersive_identity_audit, quantum_memory


def run():
    return {
        "evidence_scope": "exact finite models and synthetic simulations; no optical measurements",
        "seeds": SEEDS,
        "v4.22": equivalence(),
        "v4.23": hankel(),
        "v4.24": positive_realization(),
        "v4.25": calibration_audit(),
        "v4.26": quantum_memory(),
        "v4.27": distance_certificate(),
        "v4.28": operating_characteristics(),
        "v4.29": optimize_allocation(),
        "v4.30": dispersive_identity_audit(),
        "v4.31": blind_challenge(),
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2, allow_nan=False))
