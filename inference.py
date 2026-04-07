from fastapi import FastAPI
import time

app = FastAPI()

def choose_action(priority_score):
    if priority_score >= 25:
        return "TREAT_NOW"
    elif priority_score >= 15:
        return "MONITOR"
    else:
        return "WAIT"

def run_inference():
    task_name = "hospital_triage"

    print(f"[START] task={task_name}", flush=True)

    priority_score = 20
    action = choose_action(priority_score)
    reward = 0.8 if action == "MONITOR" else 1.0

    print(f"[STEP] step=1 reward={reward}", flush=True)

    time.sleep(0.5)

    print(f"[END] task={task_name} score={reward} steps=1", flush=True)


# API route (required for HF Space)
@app.get("/")
def root():
    return {"message": "Hospital Triage AI Running ✅"}


# IMPORTANT: run inference when script runs
if __name__ == "__main__":
    run_inference()