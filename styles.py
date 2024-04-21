import tkinter as tk
from PIL import Image, ImageTk
from aima.logic import *


class DentistExpertSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dentist ExpertSystem")
        self.geometry("500x500")

        self.symptoms = {
            "Tooth Pain": "ToothPain",
            "Chewing Difficulty": "Chewing",
            "Sensitivity to Hot/Cold": "Sensitivity",
            "Swollen Gums": "SwollenGums",
            "Red Gums": "RedGums",
            "Bleeding Gums": "BleedingGums",
            "Bad Breath": "BadBreath",
            "Tooth Sensitivity": "ToothSensitivity",
            "Tooth Discoloration": "ToothDiscoloration",
            "Jaw Pain": "JawPain",
            "Clicking Sounds": "ClickingSound",
            "Mouth Lesions": "MouthLesion",
            "Tooth Mobility": "ToothMobility",
            "Spontaneous Bleeding": "Bleeding",
            "Halitosis": "Halitosis",
            "Dental Trauma": "DentalTrauma"
        }

        self.selected_symptoms = []

        self.create_interface()

    def create_interface(self):
     # Create label to prompt user to select symptoms
     self.label = tk.Label(self, text="Please select symptoms:")
     self.label.pack()
     # Create symptom checkbuttons
     for symptom_label in self.symptoms.keys():
        symptom = self.symptoms[symptom_label].lower()  # Convert symptom to lowercase
        var = tk.IntVar()
        cb = tk.Checkbutton(self, text=symptom_label, variable=var, command=lambda s=symptom_label: self.toggle_symptom(s))
        cb.pack()
     # Create the bottom frame with light blue background
     self.bottom_frame = tk.Frame(self, bg="light blue")
     self.bottom_frame.pack(fill=tk.BOTH, expand=True)
     # Create Diagnose button
     self.diagnose_button = tk.Button(self.bottom_frame, text="Diagnose", command=self.diagnose)
     self.diagnose_button.pack(pady=10)  # Add padding between the buttons
     # Create result label
     self.result_label = tk.Label(self.bottom_frame, text="")
     self.result_label.pack()


    def toggle_symptom(self, symptom):
        if symptom in self.selected_symptoms:
            self.selected_symptoms.remove(symptom)
        else:
            self.selected_symptoms.append(symptom)

    def diagnose(self):
        if not self.selected_symptoms:
            self.result_label.config(text="Please select at least one symptom.", fg="red")
            return

        KB = FolKB()
        KB.tell(expr('ToothPain(x) & Chewing(x) & Sensitivity(x, hot_cold) ==> Diagnosis(x, ToothDecay)'))
        KB.tell(expr('SwollenGums(x) & RedGums(x) & BleedingGums(x) & BadBreath(x) ==> Diagnosis(x, GumDisease)'))
        KB.tell(expr('ToothSensitivity(x, hot_cold) & NoVisibleDecay(x) ==> Diagnosis(x, EnamelErosion)'))
        KB.tell(expr('ToothDiscoloration(x) ==> Diagnosis(x, DentalStaining)'))
        KB.tell(expr('JawPain(x) & ClickingSound(x) ==> Diagnosis(x, TMJDisorder)'))
        KB.tell(expr('MouthLesion(x) & NoHealing(x) ==> Diagnosis(x, OralCancer)'))
        KB.tell(expr('ToothMobility(x) ==> Diagnosis(x, GumDisease)'))
        KB.tell(expr('Bleeding(x) & Spontaneous(x) ==> Diagnosis(x, SystemicCondition)'))
        KB.tell(expr('Halitosis(x) & Persistent(x) ==> Diagnosis(x, ChronicHalitosis)'))
        KB.tell(expr('DentalTrauma(x) & Recent(x) ==> Diagnosis(x, DentalInjury)'))

        diagnosis_per_symptom = {}
        for clause in KB.clauses:
            if clause.op == '==>' and isinstance(clause.args[1], Expr):
                consequent = clause.args[1]
                for symptom in self.selected_symptoms:
                    if symptom.lower() in str(consequent).lower():
                        diagnosis_expr = consequent.args[0]
                        if isinstance(diagnosis_expr, Expr):
                            diagnosis = diagnosis_expr.args[1]
                            if symptom in diagnosis_per_symptom:
                                diagnosis_per_symptom[symptom].append(diagnosis)
                            else:
                                diagnosis_per_symptom[symptom] = [diagnosis]

        if diagnosis_per_symptom:
            all_diagnoses = [diagnosis for diagnoses in diagnosis_per_symptom.values() for diagnosis in diagnoses]
            if all_diagnoses:
                diagnoses_str = ", ".join(str(diagnosis) for diagnosis in all_diagnoses)
                self.result_label.config(text="Diagnosis: " + diagnoses_str)
            else:
                self.result_label.config(text="No diagnosis found.")
        else:
            self.result_label.config(text="No diagnosis found.")

            

if __name__ == "__main__":
    app = DentistExpertSystem()
    app.mainloop()
 