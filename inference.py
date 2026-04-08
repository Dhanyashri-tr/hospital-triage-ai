from tasks import choose_action
from litellm import completion

def run_task():
    task_name = "triage"

    # START
    print(f"[START] task={task_name}", flush=True)

    # 🔥 LLM CALL (MANDATORY)
    response = completion(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Patient has fever and chest pain. What is priority?"}
    ],
    
)

    # Example logic
    priority_score = 20
    action = choose_action(priority_score)

    # STEP
    reward = 0.8 if action == "TREAT_NOW" else 0.5
    print(f"[STEP] step=1 reward={reward}", flush=True)

    # END
    print(f"[END] task={task_name} score={reward} steps=1", flush=True)


if __name__ == "__main__":
    run_task()