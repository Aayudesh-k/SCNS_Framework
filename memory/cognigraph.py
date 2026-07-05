from memory.episodic_buffer import EpisodicBuffer
from memory.knowledge_graph import SymbolicKnowledgeGraph

class CogniGraph:
    def __init__(self):
        """
        The 3-tier memory manager that handles the dichotomy between 
        sub-symbolic deep learning and classical symbolic reasoning.
        """
        # 1. Short-term buffer (Wake Phase)
        self.episodic = EpisodicBuffer()
        
        # 2. Long-term symbolic store (NREM/REM Phase)
        self.semantic = SymbolicKnowledgeGraph()

    def route_to_episodic(self, raw_text, vector, tags, reward=0):
        """Routes fast-access encoding into the short-term buffer."""
        return self.episodic.add_episode(raw_text, vector, tags, reward)

    def route_to_semantic(self, concept_a, concept_b, weight, context=""):
        """Consolidates vectors into the symbolic knowledge graph."""
        self.semantic.add_or_update_rule(concept_a, concept_b, weight, context)