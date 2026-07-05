def run_http_task(agent):
    print(">>> Starting HTTP 403 Environment Task")
    agent.step("HTTP API request sent to server endpoint.", ["HTTP", "Request"])
    agent.step("HTTP API returned a catastrophic 403 Forbidden state.", ["Request", "403_Error"])
    agent.step("API protocol verification requires explicit authentication headers.", ["403_Error", "Auth_Header"])
    agent.sleep_cycle()