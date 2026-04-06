from typing import List
from datetime import datetime
import uuid
from .models import PatientCase, Observation, ActionType, Vitals


class HospitalTriageTasks:
    """
    Collection of hospital triage tasks at different difficulty levels.
    
    This class provides patient cases for the AI agent to triage,
    categorized by difficulty level.
    """
    
    def __init__(self):
        self.easy_cases = self._create_easy_cases()
        self.medium_cases = self._create_medium_cases()
        self.hard_cases = self._create_hard_cases()
    
    def get_cases_by_difficulty(self, difficulty: str) -> List[PatientCase]:
        """
        Get all cases for a specific difficulty level.
        
        Args:
            difficulty: "EASY", "MEDIUM", or "HARD"
            
        Returns:
            List of patient cases
        """
        difficulty = difficulty.upper()
        if difficulty == "EASY":
            return self.easy_cases
        elif difficulty == "MEDIUM":
            return self.medium_cases
        elif difficulty == "HARD":
            return self.hard_cases
        else:
            raise ValueError(f"Invalid difficulty level: {difficulty}")
    
    def _create_easy_cases(self) -> List[PatientCase]:
        """
        Create easy difficulty cases with simple symptoms.
        
        Returns:
            List of easy patient cases
        """
        cases = []
        
        # Case 1: Simple cold
        cases.append(PatientCase(
            case_id="EASY_001",
            observation=Observation(
                patient_id=f"patient_{uuid.uuid4().hex[:8]}",
                symptoms=["runny nose", "sore throat", "mild cough"],
                vitals=Vitals(
                    heart_rate=75,
                    blood_pressure_systolic=120,
                    blood_pressure_diastolic=80,
                    temperature=37.2,
                    respiratory_rate=16,
                    oxygen_saturation=98.0,
                    pain_level=1
                ),
                age=25,
                gender="M",
                medical_history=[],
                timestamp=datetime.now().isoformat()
            ),
            correct_action=ActionType.WAIT,
            correct_priority_range=(0.0, 0.3),
            difficulty="EASY",
            explanation="Patient presents with mild cold symptoms, normal vitals, and no distress. This is a non-urgent case that can wait for routine care."
        ))
        
        # Case 2: Mild fever
        cases.append(PatientCase(
            case_id="EASY_002",
            observation=Observation(
                patient_id=f"patient_{uuid.uuid4().hex[:8]}",
                symptoms=["fever", "headache", "fatigue"],
                vitals=Vitals(
                    heart_rate=85,
                    blood_pressure_systolic=118,
                    blood_pressure_diastolic=75,
                    temperature=38.1,
                    respiratory_rate=18,
                    oxygen_saturation=97.0,
                    pain_level=3
                ),
                age=32,
                gender="F",
                medical_history=[],
                timestamp=datetime.now().isoformat()
            ),
            correct_action=ActionType.WAIT,
            correct_priority_range=(0.1, 0.4),
            difficulty="EASY",
            explanation="Patient has mild fever and headache but stable vitals. This can be managed with supportive care and doesn't require immediate attention."
        ))
        
        # Case 3: Minor sprain
        cases.append(PatientCase(
            case_id="EASY_003",
            observation=Observation(
                patient_id=f"patient_{uuid.uuid4().hex[:8]}",
                symptoms=["ankle pain", "swelling", "difficulty walking"],
                vitals=Vitals(
                    heart_rate=70,
                    blood_pressure_systolic=125,
                    blood_pressure_diastolic=82,
                    temperature=36.8,
                    respiratory_rate=15,
                    oxygen_saturation=99.0,
                    pain_level=4
                ),
                age=28,
                gender="M",
                medical_history=[],
                timestamp=datetime.now().isoformat()
            ),
            correct_action=ActionType.WAIT,
            correct_priority_range=(0.0, 0.3),
            difficulty="EASY",
            explanation="Minor ankle sprain with normal vitals. This is a non-emergency case that can be treated in routine care."
        ))
        
        return cases
    
    def _create_medium_cases(self) -> List[PatientCase]:
        """
        Create medium difficulty cases with moderate complexity.
        
        Returns:
            List of medium patient cases
        """
        cases = []
        
        # Case 1: Dehydration
        cases.append(PatientCase(
            case_id="MEDIUM_001",
            observation=Observation(
                patient_id=f"patient_{uuid.uuid4().hex[:8]}",
                symptoms=["dizziness", "dry mouth", "dark urine", "fatigue"],
                vitals=Vitals(
                    heart_rate=95,
                    blood_pressure_systolic=105,
                    blood_pressure_diastolic=65,
                    temperature=37.0,
                    respiratory_rate=20,
                    oxygen_saturation=96.0,
                    pain_level=2
                ),
                age=45,
                gender="F",
                medical_history=["diabetes"],
                timestamp=datetime.now().isoformat()
            ),
            correct_action=ActionType.MONITOR,
            correct_priority_range=(0.4, 0.7),
            difficulty="MEDIUM",
            explanation="Patient shows signs of moderate dehydration with elevated heart rate and low blood pressure. Requires monitoring and fluid replacement but not immediate emergency care."
        ))
        
        # Case 2: Possible infection
        cases.append(PatientCase(
            case_id="MEDIUM_002",
            observation=Observation(
                patient_id=f"patient_{uuid.uuid4().hex[:8]}",
                symptoms=["fever", "chills", "body aches", "localized pain in right lower abdomen"],
                vitals=Vitals(
                    heart_rate=100,
                    blood_pressure_systolic=130,
                    blood_pressure_diastolic=85,
                    temperature=38.8,
                    respiratory_rate=22,
                    oxygen_saturation=95.0,
                    pain_level=6
                ),
                age=35,
                gender="M",
                medical_history=[],
                timestamp=datetime.now().isoformat()
            ),
            correct_action=ActionType.MONITOR,
            correct_priority_range=(0.5, 0.8),
            difficulty="MEDIUM",
            explanation="Patient has fever and localized abdominal pain that could indicate appendicitis or another infection. Requires monitoring and further evaluation."
        ))
        
        # Case 3: Asthma exacerbation
        cases.append(PatientCase(
            case_id="MEDIUM_003",
            observation=Observation(
                patient_id=f"patient_{uuid.uuid4().hex[:8]}",
                symptoms=["wheezing", "shortness of breath", "chest tightness", "cough"],
                vitals=Vitals(
                    heart_rate=110,
                    blood_pressure_systolic=140,
                    blood_pressure_diastolic=90,
                    temperature=37.5,
                    respiratory_rate=24,
                    oxygen_saturation=92.0,
                    pain_level=3
                ),
                age=29,
                gender="F",
                medical_history=["asthma"],
                timestamp=datetime.now().isoformat()
            ),
            correct_action=ActionType.MONITOR,
            correct_priority_range=(0.6, 0.8),
            difficulty="MEDIUM",
            explanation="Patient with known asthma having moderate exacerbation. Oxygen saturation is slightly low and breathing is elevated. Requires close monitoring and treatment."
        ))
        
        return cases
    
    def _create_hard_cases(self) -> List[PatientCase]:
        """
        Create hard difficulty cases with critical conditions and multiple symptoms.
        
        Returns:
            List of hard patient cases
        """
        cases = []
        
        # Case 1: Heart attack
        cases.append(PatientCase(
            case_id="HARD_001",
            observation=Observation(
                patient_id=f"patient_{uuid.uuid4().hex[:8]}",
                symptoms=["chest pain", "shortness of breath", "sweating", "nausea", "pain radiating to left arm"],
                vitals=Vitals(
                    heart_rate=115,
                    blood_pressure_systolic=160,
                    blood_pressure_diastolic=95,
                    temperature=36.9,
                    respiratory_rate=26,
                    oxygen_saturation=91.0,
                    pain_level=8
                ),
                age=58,
                gender="M",
                medical_history=["hypertension", "high cholesterol"],
                timestamp=datetime.now().isoformat()
            ),
            correct_action=ActionType.TREAT_NOW,
            correct_priority_range=(0.8, 1.0),
            difficulty="HARD",
            explanation="Classic signs of myocardial infarction with chest pain radiating to arm, diaphoresis, and elevated vitals. Requires immediate emergency treatment."
        ))
        
        # Case 2: Stroke
        cases.append(PatientCase(
            case_id="HARD_002",
            observation=Observation(
                patient_id=f"patient_{uuid.uuid4().hex[:8]}",
                symptoms=["sudden confusion", "slurred speech", "facial drooping on right side", "weakness in left arm", "vision problems"],
                vitals=Vitals(
                    heart_rate=92,
                    blood_pressure_systolic=185,
                    blood_pressure_diastolic=110,
                    temperature=37.1,
                    respiratory_rate=18,
                    oxygen_saturation=94.0,
                    pain_level=2
                ),
                age=67,
                gender="F",
                medical_history=["atrial fibrillation", "hypertension"],
                timestamp=datetime.now().isoformat()
            ),
            correct_action=ActionType.TREAT_NOW,
            correct_priority_range=(0.9, 1.0),
            difficulty="HARD",
            explanation="Classic stroke symptoms with facial droop, slurred speech, and weakness. Very high blood pressure suggests hemorrhagic stroke. Time-critical emergency."
        ))
        
        # Case 3: Sepsis
        cases.append(PatientCase(
            case_id="HARD_003",
            observation=Observation(
                patient_id=f"patient_{uuid.uuid4().hex[:8]}",
                symptoms=["high fever", "confusion", "rapid breathing", "low blood pressure", "rash", "extreme weakness"],
                vitals=Vitals(
                    heart_rate=125,
                    blood_pressure_systolic=85,
                    blood_pressure_diastolic=50,
                    temperature=39.8,
                    respiratory_rate=28,
                    oxygen_saturation=89.0,
                    pain_level=5
                ),
                age=72,
                gender="M",
                medical_history=["diabetes", "kidney disease"],
                timestamp=datetime.now().isoformat()
            ),
            correct_action=ActionType.TREAT_NOW,
            correct_priority_range=(0.9, 1.0),
            difficulty="HARD",
            explanation="Signs of septic shock with high fever, hypotension, tachycardia, and confusion. This is a life-threatening emergency requiring immediate intervention."
        ))
        
        # Case 4: Multiple trauma
        cases.append(PatientCase(
            case_id="HARD_004",
            observation=Observation(
                patient_id=f"patient_{uuid.uuid4().hex[:8]}",
                symptoms=["severe abdominal pain", "bleeding from wound", "dizziness", "difficulty breathing", "loss of consciousness"],
                vitals=Vitals(
                    heart_rate=130,
                    blood_pressure_systolic=80,
                    blood_pressure_diastolic=45,
                    temperature=36.5,
                    respiratory_rate=30,
                    oxygen_saturation=85.0,
                    pain_level=9
                ),
                age=41,
                gender="M",
                medical_history=[],
                timestamp=datetime.now().isoformat()
            ),
            correct_action=ActionType.TREAT_NOW,
            correct_priority_range=(1.0, 1.0),
            difficulty="HARD",
            explanation="Multiple trauma with hypovolemic shock - very low blood pressure, high heart rate, and decreased consciousness. Immediate life-saving intervention required."
        ))
        
        return cases
