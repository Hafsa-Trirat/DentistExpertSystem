import tkinter as tk

root = tk.Tk()
root.title("Clinique Dentaire")
root.geometry("700x600")
root.configure(bg="#add8e6")  
root.resizable(False, False)

symptoms = [
    "ToothPain", "Chewing", "Sensitivity", "SwollenGums", "RedGums", "BleedingGums", 
    "BadBreath", "ToothSensitivity", "ToothDiscoloration", "JawPain", "ClickingSound",
    "MouthLesion", "ToothMobility", "Bleeding", "Halitosis", "DentalTrauma"
]

symptom_vars = {}
for index, symptom in enumerate(symptoms):
    var = tk.BooleanVar()
    symptom_vars[symptom] = var
    column = index % 4
    row = index // 4
    tk.Checkbutton(root, text=symptom, variable=var, onvalue=True, offvalue=False,
                   bg="#add8e6", fg="#000", font=("Helvetica", 12)).grid(row=row, column=column, sticky="w", padx=5, pady=5)

run_button = tk.Button(root, text="diagnostic",command=diagnosis, bg="#3c8ce7", fg="#fff", font=("Helvetica", 12))
run_button.grid(row=row + 1, columnspan=4, pady=10)

result_text = tk.Text(root, height=7, width=40)
result_text.grid(row=row + 2, columnspan=4, pady=10)

remaining_space = 600 - (len(symptoms) // 4 * 40) - 40 - 10 - 10
root.grid_rowconfigure(row + 3, minsize=remaining_space)

root.mainloop()
 
