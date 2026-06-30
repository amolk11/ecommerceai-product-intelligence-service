"""
CommerceAI Product Intelligence Service

Default Locust Entry Point

By default, this file imports the Baseline Test scenario.

To execute another scenario directly:

    locust -f scenarios/load.py
    locust -f scenarios/stress.py
    locust -f scenarios/spike.py
    locust -f scenarios/soak.py
"""

from scenarios.baseline import BaselineUser

__all__ = [
    "BaselineUser",
]
