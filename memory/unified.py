"""Unified memory system bridging PyRIT CentralMemory with Neo4j attack graph.

Combines PyRIT's conversation memory with Pandora's knowledge graph for
persistent tracking of AI red team attack chains.
"""

from typing import Optional
from datetime import datetime


class UnifiedMemory:
    """Combines PyRIT CentralMemory with Pandora Neo4j attack graph.

    PyRIT handles conversation-level prompt/response storage with embeddings.
    Neo4j handles attack chain topology and MITRE ATT&CK mapping.
    """

    def __init__(
        self,
        sqlite_path: str = "~/.pandora/pyrit_memory.db",
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "pandora",
    ):
        self.sqlite_path = sqlite_path
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password

        # Lazy import PyRIT components
        self._pyrit_memory = None
        self._kg = None

    @property
    def pyrit_memory(self):
        """Lazy-load PyRIT CentralMemory."""
        if self._pyrit_memory is None:
            try:
                from oracle.memory import CentralMemory
                from oracle.memory.sqlite_memory import SQLiteMemory

                sqlite_mem = SQLiteMemory(db_path=self.sqlite_path)
                CentralMemory.set_memory_instance(sqlite_mem)
                self._pyrit_memory = CentralMemory.get_memory_instance()
            except ImportError:
                # PyRIT not available, use fallback
                self._pyrit_memory = None
        return self._pyrit_memory

    @property
    def kg(self):
        """Lazy-load Neo4j knowledge graph."""
        if self._kg is None:
            try:
                from neo4j import GraphDatabase

                self._kg = GraphDatabase.driver(
                    self.neo4j_uri,
                    auth=(self.neo4j_user, self.neo4j_password),
                )
            except Exception:
                self._kg = None
        return self._kg

    def save_interaction(
        self,
        prompt: str,
        response: str,
        scores: dict,
        attack_type: str = "",
        mitre_tactics: list[str] = None,
    ) -> str:
        """Save a prompt/response interaction to both memory systems.

        Args:
            prompt: User prompt
            response: Model response
            scores: Scoring results (bypass_score, refusal_score, etc.)
            attack_type: Type of attack (e.g., "dan_jailbreak", "base64_injection")
            mitre_tactics: List of MITRE ATT&CK technique IDs

        Returns:
            Interaction ID
        """
        interaction_id = f"INT-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Save to PyRIT memory
        if self.pyrit_memory:
            try:
                self.pyrit_memory.save_prompt(
                    prompt=prompt,
                    response=response,
                    labels=[attack_type] if attack_type else [],
                    metadata=scores,
                )
            except Exception:
                pass  # Fallback if PyRIT memory fails

        # Save to Neo4j attack graph
        if self.kg:
            try:
                with self.kg.session() as session:
                    session.run(
                        """
                        MERGE (i:Interaction {id: $id})
                        SET i.prompt = $prompt,
                            i.response = $response,
                            i.scores = $scores,
                            i.attack_type = $attack_type,
                            i.timestamp = $timestamp
                        """,
                        id=interaction_id,
                        prompt=prompt,
                        response=response,
                        scores=str(scores),
                        attack_type=attack_type,
                        timestamp=datetime.now().isoformat(),
                    )

                    # Link tactics
                    for tactic in (mitre_tactics or []):
                        session.run(
                            """
                            MATCH (i:Interaction {id: $id})
                            MERGE (t:Tactic {id: $tactic})
                            MERGE (i)-[:USES_TACTIC]->(t)
                            """,
                            id=interaction_id,
                            tactic=tactic,
                        )
            except Exception:
                pass  # Fallback if Neo4j fails

        return interaction_id

    def get_successful_chains(self, min_score: float = 0.7) -> list[dict]:
        """Retrieve successful attack chains from memory.

        Args:
            min_score: Minimum bypass score threshold

        Returns:
            List of successful attack chain configurations
        """
        chains = []

        if self.pyrit_memory:
            try:
                # Query PyRIT memory for successful interactions
                results = self.pyrit_memory.query_labels(["successful"])
                for entry in results:
                    if entry.metadata.get("bypass_score", 0) >= min_score:
                        chains.append({
                            "prompt": entry.prompt,
                            "response": entry.response,
                            "score": entry.metadata.get("bypass_score"),
                            "attack_type": entry.labels[0] if entry.labels else "unknown",
                        })
            except Exception:
                pass

        return chains

    def record_attack_step(
        self,
        step_type: str,
        prompt: str,
        response: str,
        success: bool,
        technique: str = "",
    ):
        """Record a step in the attack chain to Neo4j.

        Args:
            step_type: Type of step (recon, exploit, bypass, etc.)
            prompt: The prompt used
            response: The model's response
            success: Whether the step succeeded
            technique: MITRE technique ID
        """
        if not self.kg:
            return

        try:
            with self.kg.session() as session:
                session.run(
                    """
                    MERGE (s:Step {type: $type, prompt_hash: $prompt_hash})
                    SET s.prompt = $prompt,
                        s.response = $response,
                        s.success = $success,
                        s.technique = $technique,
                        s.timestamp = $timestamp
                    """,
                    type=step_type,
                    prompt_hash=str(hash(prompt)),
                    prompt=prompt,
                    response=response,
                    success=success,
                    technique=technique,
                    timestamp=datetime.now().isoformat(),
                )
        except Exception:
            pass

    def close(self):
        """Close connections."""
        if self._kg:
            self._kg.close()
            self._kg = None


# Singleton instance
_unified_memory: Optional[UnifiedMemory] = None


def get_unified_memory() -> UnifiedMemory:
    """Get or create the singleton UnifiedMemory instance."""
    global _unified_memory
    if _unified_memory is None:
        _unified_memory = UnifiedMemory()
    return _unified_memory
