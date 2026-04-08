import sys
import time

def choose_action(priority_score):
    if priority_score >= 25:
        return "TREAT_NOW"
    elif priority_score >= 15:
        return "MONITOR"
    else:
        return "WAIT"

def run_task():
    task_name = "triage"

    # START block
    print(f"[START] task={task_name}", flush=True)

    # Example input (you can modify logic later)
    priority_score = 20

    # Step 1
    action = choose_action(priority_score)
    reward = 0.8 if action == "TREAT_NOW" else 0.5

    print(f"[STEP] step=1 reward={reward}", flush=True)

    # Simulate processing (optional)
    time.sleep(0.5)

    # END block
    final_score = reward
    steps = 1

    print(f"[END] task={task_name} score={final_score} steps={steps}", flush=True)


if __name__ == "__main__":
    run_task()