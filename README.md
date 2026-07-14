# Sleep-Consolidated Neuro-Symbolic (SCNS) Framework

[![Patent Pending](https://img.shields.io/badge/Patent_Pending-App._No._64/110,991-blue.svg)](https://uspto.gov)

## Overview
The Sleep-Consolidated Neuro-Symbolic (SCNS) framework is a distributed, multi-phase computing architecture that enables autonomous physical agents to continuously extract, verify, and store causal physical rules from unstructured telemetry data without experiencing catastrophic forgetting or LLM hallucinations.

Modeled on biological circadian rhythms, this architecture decouples real-time physical telemetry ingestion (Edge) from heavy cognitive consolidation and logic validation (Cloud).

## Core Architecture

The SCNS framework operates in three discrete asynchronous phases:

*   **Wake Phase (Episodic Encoding):** An Edge Node deployed on the physical agent ingests high-frequency sensory telemetry in real-time. Using a localized transformer model (`all-MiniLM-L6-v2`), textual event descriptions are encoded into 384-dimensional dense vectors and written to a local `pgvector`-enabled PostgreSQL database. No LLM inference occurs here, guaranteeing zero latency impact on real-time actuator control loops.
*   **NREM Phase (Structural Extraction):** Triggered asynchronously as a batch process on the Cloud Node, this phase queries the accumulated episodic memory. It computes vector cosine similarities across traces to extract candidate Directed Acyclic Graph (DAG) edges representing potential physical cause-and-effect relationships.
*   **REM Phase (Active Dreaming & Validation):** The Cloud Node forces an LLM into a strict, zero-shot Boolean validation role. The LLM interrogates the candidate DAG edges for causal paradoxes (e.g., identical starting states resulting in mutually exclusive physical outcomes). Contradictory rules trigger a Safety Pruning Intervention. Proven, non-paradoxical rules are committed as deterministic JSON to a relational Symbolic Knowledge Graph for future querying.

## Repository Structure

*   `edge_node.py`: FastAPI service handling real-time telemetry ingestion and local vectorization.
*   `cloud_node.py`: Batch processing engine executing the NREM structural extraction and REM LLM counterfactual validation.
*   `agent.py`: The simulated physical agent interaction script.
*   `memory/`: Contains database schemas and connection handlers for the Episodic Buffer and the Symbolic Knowledge Graph (CogniGraph).
*   `phases/`: Discrete logic modules for the Wake, NREM, and REM cycles.
*   `environments/`: Task definitions (HTTP, constraint satisfaction) for benchmarking.
*   `run_benchmark.py` & `run_experiments.py`: Enterprise benchmark suites for testing proactive interference resistance and ablation.

## Getting Started

### Prerequisites
*   Docker and Docker Compose
*   An API Key for your chosen LLM validator (OpenAI, Google Gemini, or a local Ollama instance).

### Installation & Execution

1. Clone the repository:
   ```bash
   git clone [https://github.com/YourUsername/SCNS-Framework.git](https://github.com/YourUsername/SCNS-Framework.git)
   cd SCNS-Framework
Create a .env file in the root directory and add your LLM API keys:

Code snippet
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
Build and launch the multi-container architecture (Edge Node, Cloud Node, and PostgreSQL databases):

Bash
docker-compose up --build -d
Run the full enterprise benchmark suite to test continuous learning and paradox pruning:

Bash
python run_benchmark.py
Legal and Patent Notice
This framework, including the asynchronous triphasic architecture, paradox pruning algorithms, and structural graph extraction methodologies, is protected by a pending U.S. patent.

U.S. Patent Pending, App. No. 64/110,991

Licensing and Commercial Use
This framework is open-sourced under the GNU Affero General Public License v3.0 (AGPLv3).

Because this architecture involves network-connected microservices (Edge and Cloud Nodes), any modifications, integrations, or deployments used over a network must also be open-sourced in accordance with the strict provisions of the AGPLv3.

Commercial Licensing
If you are a corporate entity, defense contractor, or startup intending to integrate the SCNS Framework into a proprietary, closed-source production environment (such as proprietary robotic control software or commercial edge hardware), you must obtain a commercial license.

For commercial licensing and enterprise support inquiries, please contact: a2kaparthi@gmail.com
