from agent import SCNSAgent
from environments.http_task import run_http_task
from environments.constraint_task import run_constraint_task

def run_live_framework():
    agent = SCNSAgent()
    
    # Run the environments
    run_http_task(agent)
    run_constraint_task(agent)

if __name__ == "__main__":
    run_live_framework()