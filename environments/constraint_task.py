def run_constraint_task(agent):
    print(">>> Starting Fruit Salad Constraint Task")
    agent.step("Jack wants to make a fruit salad but needs a bowl.", ["Fruit_Salad", "Bowl"])
    agent.step("The bowl in the kitchen is completely shattered.", ["Bowl", "Broken_Object"])
    agent.step("A store downstairs sells bowls.", ["Broken_Object", "Hardware_Store"])
    agent.sleep_cycle()