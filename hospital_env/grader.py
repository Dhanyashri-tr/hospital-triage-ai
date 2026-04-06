from typing import Dict, Any
from .models import Action, Reward, PatientCase, ActionType


class HospitalTriageGrader:
    """
    Deterministic grader for the AI Hospital Triage System.
    
    This class implements a deterministic reward function that evaluates
    the AI agent's triage decisions based on medical guidelines.
    """
    
    def __init__(self):
        # Define priority ranges for different severity levels
        self.priority_ranges = {
            ActionType.TREAT_NOW: (0.8, 1.0),
            ActionType.MONITOR: (0.4, 0.8),
            ActionType.WAIT: (0.0, 0.4)
        }
        
        # Define critical symptoms that require immediate attention
        self.critical_symptoms = {
            "chest pain", "difficulty breathing", "shortness of breath",
            "severe bleeding", "loss of consciousness", "confusion",
            "stroke symptoms", "heart attack", "severe trauma"
        }
        
        # Define vital sign thresholds for critical conditions
        self.critical_vital_thresholds = {
            "heart_rate_high": 120,
            "heart_rate_low": 40,
            "systolic_bp_high": 180,
            "systolic_bp_low": 90,
            "diastolic_bp_high": 110,
            "temperature_high": 39.5,
            "temperature_low": 35.0,
            "oxygen_sat_low": 90,
            "respiratory_rate_high": 25,
            "respiratory_rate_low": 10
        }
    
    def grade_action(self, action: Action, case: PatientCase) -> Reward:
        """
        Grade an action against the correct triage decision.
        
        Args:
            action: The action taken by the AI agent
            case: The patient case with correct answer
            
        Returns:
            Reward object with detailed scoring
        """
        # Initialize score components
        priority_score = 0.0
        action_score = 0.0
        reasoning_score = 0.0
        
        # Grade priority score (40% of total)
        priority_correct = self._evaluate_priority_score(action.priority_score, case)
        if priority_correct:
            priority_score = 0.4
        
        # Grade action type (40% of total)
        action_correct = self._evaluate_action_type(action.action_type, case)
        if action_correct:
            action_score = 0.4
        
        # Grade reasoning (20% of total)
        reasoning_valid = self._evaluate_reasoning(action.reasoning, case)
        if reasoning_valid:
            reasoning_score = 0.2
        
        # Calculate total score
        total_score = priority_score + action_score + reasoning_score
        
        # Apply penalties for unsafe decisions
        penalty = self._calculate_penalty(action, case)
        total_score = max(0.0, total_score - penalty)
        
        # Create feedback
        feedback = self._generate_feedback(
            action, case, priority_correct, action_correct, reasoning_valid
        )
        
        return Reward(
            score=total_score,
            priority_correct=priority_correct,
            action_correct=action_correct,
            reasoning_valid=reasoning_valid,
            feedback=feedback,
            breakdown={
                "priority": priority_score,
                "action": action_score,
                "reasoning": reasoning_score,
                "penalty": penalty
            }
        )
    
    def _evaluate_priority_score(self, score: float, case: PatientCase) -> bool:
        """
        Evaluate if the priority score is within the expected range.
        
        Args:
            score: The priority score assigned by the AI
            case: The patient case
            
        Returns:
            True if priority score is correct
        """
        expected_min, expected_max = case.correct_priority_range
        return expected_min <= score <= expected_max
    
    def _evaluate_action_type(self, action_type: ActionType, case: PatientCase) -> bool:
        """
        Evaluate if the action type matches the correct action.
        
        Args:
            action_type: The action type chosen by the AI
            case: The patient case
            
        Returns:
            True if action type is correct
        """
        return action_type == case.correct_action
    
    def _evaluate_reasoning(self, reasoning: str, case: PatientCase) -> bool:
        """
        Evaluate if the reasoning is logically sound.
        
        Args:
            reasoning: The reasoning provided by the AI
            case: The patient case
            
        Returns:
            True if reasoning is valid
        """
        if not reasoning or len(reasoning.strip()) < 10:
            return False
        
        reasoning_lower = reasoning.lower()
        
        # Check if reasoning mentions relevant symptoms
        symptoms_mentioned = any(
            symptom.lower() in reasoning_lower 
            for symptom in case.observation.symptoms
        )
        
        # Check if reasoning mentions relevant vital signs
        vitals = case.observation.vitals
        vitals_mentioned = False
        
        if vitals.heart_rate and ("heart rate" in reasoning_lower or "pulse" in reasoning_lower):
            vitals_mentioned = True
        if vitals.blood_pressure_systolic and "blood pressure" in reasoning_lower:
            vitals_mentioned = True
        if vitals.temperature and ("temperature" in reasoning_lower or "fever" in reasoning_lower):
            vitals_mentioned = True
        if vitals.oxygen_saturation and ("oxygen" in reasoning_lower or "saturation" in reasoning_lower):
            vitals_mentioned = True
        
        # Check if reasoning aligns with the action
        action_aligns = False
        if case.correct_action == ActionType.TREAT_NOW:
            urgent_keywords = ["immediate", "urgent", "critical", "emergency", "life-threatening"]
            action_aligns = any(keyword in reasoning_lower for keyword in urgent_keywords)
        elif case.correct_action == ActionType.MONITOR:
            monitor_keywords = ["monitor", "observe", "watch", "stable", "caution"]
            action_aligns = any(keyword in reasoning_lower for keyword in monitor_keywords)
        elif case.correct_action == ActionType.WAIT:
            wait_keywords = ["minor", "stable", "routine", "non-urgent", "low priority"]
            action_aligns = any(keyword in reasoning_lower for keyword in wait_keywords)
        
        return symptoms_mentioned and (vitals_mentioned or len(case.observation.symptoms) > 0) and action_aligns
    
    def _calculate_penalty(self, action: Action, case: PatientCase) -> float:
        """
        Calculate penalties for unsafe decisions.
        
        Args:
            action: The action taken by the AI
            case: The patient case
            
        Returns:
            Penalty amount (0.0 to 1.0)
        """
        penalty = 0.0
        
        # Major penalty for missing critical cases
        if case.correct_action == ActionType.TREAT_NOW and action.action_type != ActionType.TREAT_NOW:
            penalty += 0.5
        
        # Minor penalty for over-treating non-critical cases
        elif case.correct_action == ActionType.WAIT and action.action_type == ActionType.TREAT_NOW:
            penalty += 0.2
        
        # Small penalty for inappropriate priority scores
        expected_min, expected_max = case.correct_priority_range
        if action.priority_score < expected_min - 0.2 or action.priority_score > expected_max + 0.2:
            penalty += 0.1
        
        return min(penalty, 1.0)
    
    def _generate_feedback(
        self, 
        action: Action, 
        case: PatientCase,
        priority_correct: bool,
        action_correct: bool,
        reasoning_valid: bool
    ) -> str:
        """
        Generate detailed feedback for the AI agent.
        
        Args:
            action: The action taken
            case: The patient case
            priority_correct: Whether priority was correct
            action_correct: Whether action was correct
            reasoning_valid: Whether reasoning was valid
            
        Returns:
            Detailed feedback string
        """
        feedback_parts = []
        
        if action_correct:
            feedback_parts.append("✓ Correct action identified")
        else:
            feedback_parts.append(f"✗ Incorrect action. Should be: {case.correct_action.value}")
        
        if priority_correct:
            feedback_parts.append("✓ Priority score within expected range")
        else:
            expected_min, expected_max = case.correct_priority_range
            feedback_parts.append(
                f"✗ Priority score {action.priority_score:.2f} outside expected range "
                f"[{expected_min:.1f}, {expected_max:.1f}]"
            )
        
        if reasoning_valid:
            feedback_parts.append("✓ Reasoning is logical and well-supported")
        else:
            feedback_parts.append("✗ Reasoning lacks sufficient detail or logical support")
        
        # Add case-specific explanation
        feedback_parts.append(f"\nCase explanation: {case.explanation}")
        
        return " | ".join(feedback_parts)
