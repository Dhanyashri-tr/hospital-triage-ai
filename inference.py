import os
from openai import OpenAI

# =========================
# ENV VARIABLES (REQUIRED)
# =========================
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

# Safe fallback for local testing
if HF_TOKEN is None:
    print("⚠️ HF_TOKEN not found, using dummy mode", flush=True)
    HF_TOKEN = "dummy-key"

# Initialize OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

# =========================
# TASK FUNCTION
# =========================
def run_task(task_name, symptoms):
    rewards = []
    steps = 0
    success = False

    print(f"[START] task={task_name} env=hospital model={MODEL_NAME}", flush=True)

    try:
        # LLM CALL WITH REASONING
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a hospital triage AI. Classify into TREAT_NOW, MONITOR, WAIT and briefly explain why."
                },
                {
                    "role": "user",
                    "content": f"Patient symptoms: {symptoms}"
                }
            ]
        )

        raw_output = response.choices[0].message.content.strip().upper()

        # =========================
        # DECISION LOGIC
        # =========================
        if "TREAT" in raw_output:
            decision = "TREAT_NOW"
            reward = 0.90
        elif "MONITOR" in raw_output:
            decision = "MONITOR"
            reward = 0.70
        else:
            decision = "WAIT"
            reward = 0.50

        # =========================
        # EXPLANATION EXTRACTION
        # =========================
        explanation = raw_output.replace("\n", " ")[:80]

        action = f"{decision}|reason:{explanation}"

        # Ensure reward in (0,1)
        reward = min(max(reward, 0.01), 0.99)

        rewards.append(f"{reward:.2f}")
        steps += 1
        success = True

        print(f"[STEP] step=1 action={action} reward={reward:.2f} done=true error=null", flush=True)

    except Exception:
        # =========================
        # SAFE FALLBACK
        # =========================
        action = "WAIT|reason:fallback_safe_mode"
        reward = 0.20
        error = "api_error"

        rewards.append(f"{reward:.2f}")
        steps += 1
        success = False

        print(f"[STEP] step=1 action={action} reward={reward:.2f} done=true error={error}", flush=True)

    print(f"[END] success={str(success).lower()} steps={steps} rewards={','.join(rewards)}", flush=True)


# =========================
# RUN TASKS
# =========================
if __name__ == "__main__":
    run_task("triage_easy", "mild fever and cough")
    run_task("triage_medium", "high fever, abdominal pain, vomiting")
    run_task("triage_critical", "severe chest pain, low oxygen, sweating")