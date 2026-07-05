import networkx as nx

class SymbolicKnowledgeGraph:
    def __init__(self):
        """
        Initializes the System 2 long-term memory.
        This provides verifiable, deterministic logic to counter neural brittleness.
        """
        self.graph = nx.DiGraph()
        print("[SYSTEM] Symbolic Knowledge Graph (NetworkX) Initialized.")

    def add_or_update_rule(self, concept_a, concept_b, weight, context=""):
        """
        Hebbian weight update: Memories that co-occur wire together.
        """
        if self.graph.has_edge(concept_a, concept_b):
            # Synaptic strengthening
            self.graph[concept_a][concept_b]['weight'] += weight
            self.graph[concept_a][concept_b]['contexts'].append(context)
        else:
            # Create new symbolic edge
            self.graph.add_edge(
                concept_a, 
                concept_b, 
                weight=weight,
                contexts=[context],
                verified=False # Requires REM phase active dreaming to become True
            )

    def prune_weak_connections(self, threshold=0.2):
        """
        Synaptic downscaling during NREM sleep.
        Removes edges that haven't been reinforced to prevent memory bloat.
        """
        edges_to_remove = [
            (u, v) for u, v, data in self.graph.edges(data=True) 
            if data['weight'] < threshold
        ]
        self.graph.remove_edges_from(edges_to_remove)
        return len(edges_to_remove)

    def get_unverified_rules(self):
        """
        Fetches candidate rules for counterfactual testing in the REM phase.
        """
        return [
            (u, v, data) for u, v, data in self.graph.edges(data=True) 
            if not data.get('verified', False)
        ]
        
    def mark_rule_verified(self, concept_a, concept_b):
        """
        Commits an abstracted logical rule to permanent semantic memory 
        after surviving REM phase counterfactual validation.
        """
        if self.graph.has_edge(concept_a, concept_b):
            self.graph[concept_a][concept_b]['verified'] = True