class Patient:
    next_id = 0

    def __init__(self, id: int, symptoms: list[str], position: tuple[float, float]):
        self.id = Patient.next_id
        self.symptoms = symptoms
        self.predicted_disease = None
        self.position = position
        Patient.next_id += 1


class PatientPrioritizer:
    def __init__(self, model_name: str):
        self.model = PatientPrioritizer.create_prioritizer_model(model_name)

        # Biến cho bệnh nhân
        self.P = self.model("P")
        self.P0 = self.model("P0")
        self.P1 = self.model("P1")
        self.P2 = self.model("P2")
        # Biến cho tier
        self.T1 = self.model("T1")
        self.T2 = self.model("T2")
        self.T3 = self.model("T3")
        # Biến cho triệu chứng
        self.S = self.model("S")
        self.S0 = self.model("S0")
        self.S1 = self.model("S1")
        self.S2 = self.model("S2")
        # Biến cho bệnh
        self.D1 = self.model("D1")
        self.D2 = self.model("D2")

        self.patient = self.model("patient") # Predicate patient(X) => X là bệnh nhân
        self.symptom = self.model("symptom") # Predicate symptom(P, S) => P có triệu chứng S
        self.disease = self.model("disease") # Predicate disease(P, D) => P có bệnh D

        self.higher_tier = self.model("higher_tier") # Predicate higher_tier(T1, T2) => T1 là tier cao hơn T2
        self.same_tier = self.model("same_tier")     # Predicate same_tier(T1, T2) => T1 cao bằng T2

        self.symptom_tier = self.model("symptom_tier")                          # symptom_tier(S, T) => Tier của triệu chứng S là T
        self.higher_symptom_severity = self.model("higher_symptom_severity")    # higher_symptom_severity(S1, S2) => triệu chứng S1 nặng hơn S2
        self.same_symptom_severity = self.model("same_symptom_severity")        # same_symptom_severity(S1, S2) => triệu chứng S1 nặng bằng S2
        self.highest_symptom_severity = self.model("highest_symptom_severity")  # highest_symptom_severity(P, S) => bệnh nhân P có triệu chứng S nặng nhất

        self.disease_tier = self.model("disease_tier")                          # disease_tier(D, T) => tier của bệnh D là T
        self.higher_disease_severity = self.model("higher_disease_severity")    # higher_disease_severity(D1, D2) => bệnh D1 nặng hơn bệnh D2

        self.higher_priority = self.model("higher_priority")    # higher_priority(P1, P2) => bệnh nhân P1 được ưu tiên hơn P2
        self.highest_priority = self.model("highest_priority")    # highest_prority(P) => bệnh nhân P được ưu tiên cao nhất
        

    @staticmethod
    def create_prioritizer_model(name: str):
        if name == "pyDatalog":
            try:
                from pyDatalog.pyParser import Term
                return Term
            except:
                raise ImportError("PatientPrioritizer.create_prioritizer_model(): Trouble importing pyDatalog")
            
        raise ValueError(f"PatientPrioritizer.create_prioritizer_model(): Unknown model name: {name}")
    
    
    def load_knowledge_base(self, knowledge_base: str):
        local_context = {
            "P": self.P, "P0": self.P0, "P1": self.P1, "P2": self.P2,
            "T1": self.T1, "T2": self.T2, "T3": self.T3,
            "S": self.S, "S0": self.S0,
            "S1": self.S1, "S2": self.S2, "D1": self.D1, "D2": self.D2,
            "patient": self.patient, "symptom": self.symptom, "disease": self.disease,
            "disease_tier": self.disease_tier, "symptom_tier": self.symptom_tier,
            "higher_tier": self.higher_tier, "same_tier": self.same_tier,
            "higher_symptom_severity": self.higher_symptom_severity,
            "same_symptom_severity": self.same_symptom_severity,
            "highest_symptom_severity": self.highest_symptom_severity,
            "higher_disease_severity": self.higher_disease_severity,
            "higher_priority": self.higher_priority,
            "highest_prority": self.highest_priority
        }

        with open(knowledge_base, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    exec(line, globals(), local_context)
                except Exception as e:
                    raise ValueError(f"Error executing knowledge base at line:\n{line}\n\n{e}")


    def get_most_prioritized_patients(self, patients: list[Patient]) -> list[Patient]:
        for p in patients:
            + self.patient(p)
            for s in p.symptoms:
                + self.symptom(p, s)
            
            + self.disease(p, p.predicted_disease)
            
        self.highest_priority(self.P)
        ans = self.P.data.copy()

        for p in patients:
            - self.patient(p)
            for s in p.symptoms:          
                - self.symptom(p, s)
            - self.disease(p, p.predicted_disease)

        return ans
