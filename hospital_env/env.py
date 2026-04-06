from typing import Dict, Any, Tuple, Optional, List
import random
from .models import (
    Observation, Action, Reward, PatientCase, EnvironmentState,
    ActionType
)
from .tasks import HospitalTriageTasks
from .grader import HospitalTriageGrader


class HospitalTriageEnv:
    def __init__(self, difficulty: str = "MEDIUM", max_steps: int = 10, seed: Optional[int] = None):
        self.difficulty = difficulty
        self.max_steps = max_steps
        self.seed = seed

        if seed is not None:
            random.seed(seed)

        self.tasks = HospitalTriageTasks()
        self.grader = HospitalTriageGrader()

        self.state = EnvironmentState(max_steps=max_steps)
        self.current_cases = []

    # -----------------------------
    # RESET
    # -----------------------------
    def reset(self) -> Optional[PatientCase]:
        self.state = EnvironmentState(max_steps=self.max_steps)

        self.current_cases = self.tasks.get_cases_by_difficulty(self.difficulty)
        random.shuffle(self.current_cases)

        first_case = self._load_next_case()
        self.state.current_case = first_case

        return first_case

    # -----------------------------
    # STEP (SAFE VERSION)
    # -----------------------------
    def step(self, action: Action) -> Tuple[Optional[PatientCase], float, bool, Dict[str, Any]]:

        if self.state.current_case is None:
            raise ValueError("No active case. Call reset() first.")

        # Grade action
        reward = self.grader.grade_action(
            action=action,
            case=self.state.current_case
        )

        # Update history
        self.state.history.append({
            "step": self.state.current_step,
            "case_id": self.state.current_case.case_id,
            "action": action.dict(),
            "reward": reward.dict()
        })

        self.state.cases_completed += 1
        self.state.current_step += 1

        # Update score
        self.state.total_score = (
            (self.state.total_score * (self.state.cases_completed - 1) + reward.score)
            / self.state.cases_completed
        )

        # -----------------------------
        # LOAD NEXT CASE SAFELY
        # -----------------------------
        next_case = self._load_next_case()

        if next_case is None or self.state.current_step >= self.max_steps:
            self.state.current_case = None
            self.state.episode_done = True

            return None, reward.score, True, {
                "episode_complete": True,
                "total_score": self.state.total_score,
                "cases_completed": self.state.cases_completed,
                "difficulty": self.difficulty
            }

        # Continue episode
        self.state.current_case = next_case

        return next_case, reward.score, False, {
            "episode_complete": False,
            "current_score": self.state.total_score,
            "cases_completed": self.state.cases_completed
        }

    # -----------------------------
    # LOAD CASE (SAFE)
    # -----------------------------
    def _load_next_case(self) -> Optional[PatientCase]:
        if not self.current_cases:
            return None

        return self.current_cases.pop(0)

    # -----------------------------
    def get_action_space(self) -> List[str]:
        return [action.value for action in ActionType]

    def get_observation_space(self) -> Dict[str, Any]:
        return {
            "symptoms": "List of symptoms",
            "vitals": "Vitals data",
            "age": "Age",
            "medical_history": "History"
        }

    def render(self):
        if self.state.current_case is None:
            print("No active case")
            return

        case = self.state.current_case

        print(f"Case: {case.case_id}")
        print(f"Symptoms: {case.observation.symptoms}")
        print(f"Score: {self.state.total_score:.3f}")