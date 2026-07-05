from memory.cognigraph import CogniGraph
from phases.wake import WakePhase
from phases.nrem import NREMPhase
from phases.rem import REMPhase

class SCNSAgent:
    def __init__(self):
        """
        The Sleep-Consolidated Neuro-Symbolic (SCNS) architecture.
        """
        self.memory = CogniGraph()
        self.wake = WakePhase(self.memory)
        self.nrem = NREMPhase(self.memory)
        self.rem = REMPhase(self.memory)
        print("\n=== SCNS Agent Online ===\n")

    def step(self, observation, tags):
        """Executes a single time-step in the environment (Wake)."""
        self.wake.observe(observation, tags)

    def sleep_cycle(self):
        """Triggers the offline consolidation and validation phases."""
        print("\n--- Initiating Sleep Cycle ---")
        self.nrem.consolidate()
        self.rem.active_dreaming()
        print("--- Sleep Cycle Complete ---\n")