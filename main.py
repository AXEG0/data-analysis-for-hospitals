import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', 8)

# Reading files
general_dataframe = pd.read_csv("csv_data\\general.csv")
prenatal_dataframe = pd.read_csv("csv_data\\prenatal.csv")
sports_dataframe = pd.read_csv("csv_data\\sports.csv")

# Bringing columns to a general view
prenatal_dataframe.rename(columns={"HOSPITAL": "hospital", "Sex": "gender"}, inplace=True)
sports_dataframe.rename(columns={"Hospital": "hospital", "Male/female": "gender"}, inplace=True)

# Merging files
merged_dataframe = pd.concat([general_dataframe, prenatal_dataframe, sports_dataframe], ignore_index=True, join="inner")

# Removing empties
merged_dataframe.drop(columns="Unnamed: 0", inplace=True)
merged_dataframe.dropna(how="all", inplace=True)

# Bringing values to a general view
merged_dataframe.gender = merged_dataframe.gender.replace({"man": 'm', "male": 'm', "woman": 'f', "female": 'f'})
merged_dataframe.gender = merged_dataframe.groupby("hospital")["gender"].fillna('f')

# Bringing height values to a general view
merged_dataframe['height'].mask(merged_dataframe['hospital'] == 'sports', lambda x: round(x / 3.5, 3), inplace=True)

# Filling empty values
merged_dataframe[["bmi", "diagnosis", "blood_test", "ecg", "ultrasound", "mri", "xray", "children", "months"]] \
       = merged_dataframe[["bmi", "diagnosis", "blood_test", "ecg", "ultrasound", "mri", "xray", "children",
                           "months"]].fillna(value=0)

# Creating different views for analysis
number_of_patients = merged_dataframe.groupby("hospital").size()
diagnoses_by_hospital = merged_dataframe.groupby(["hospital", "diagnosis"]).size()
median_patient_info_by_hospital = merged_dataframe.pivot_table(index="hospital", aggfunc='median')
blood_tests_by_hospital = merged_dataframe.groupby(["hospital", "blood_test"]).size()
blood_tests_taken = blood_tests_by_hospital[['t' in i for i in blood_tests_by_hospital.index]]
all_diagnoses = merged_dataframe.groupby("diagnosis").size()
height_by_hospital = merged_dataframe.set_index("hospital")["height"]

print("Questions for data analysis:\n")

print("Q1. Which hospital has the highest number of patients?")
biggest_hospital = number_of_patients.idxmax()
print(f"The answer to the 1st question is {biggest_hospital}\n")

print("Q2. What share of the patients in the general hospital suffers from stomach-related issues?")
patients_in_general = number_of_patients["general"]
stomach_in_general = diagnoses_by_hospital["general"]["stomach"]
stomach_share_in_general = round(stomach_in_general / patients_in_general, 3)
print(f"The answer to the 2nd question is {stomach_share_in_general}\n")

print("Q3. What share of the patients in the sports hospital suffers from dislocation-related issues?")
patients_in_sports = number_of_patients["sports"]
dislocation_in_sports = diagnoses_by_hospital["sports"]["dislocation"]
dislocation_share_in_sports = round(dislocation_in_sports / patients_in_sports, 3)
print(f"The answer to the 3rd question is {dislocation_share_in_sports}\n")

print("Q4. What is the difference in the median ages of the patients in the general and sports hospitals?")
median_age_in_general = median_patient_info_by_hospital["age"]["general"]
median_age_in_sports = median_patient_info_by_hospital["age"]["sports"]
difference_of_median_age_in_general_and_sports = round(median_age_in_general - median_age_in_sports)
print(f"The answer to the 4th question is {difference_of_median_age_in_general_and_sports}\n")

print("Q5. In which hospital the blood test was taken the most often? How many blood tests were taken?")
biggest_blood_tests_hospital = blood_tests_taken.idxmax()[0]
biggest_blood_tests_count = blood_tests_taken.max()
print(f"The answer to the 5th question is {biggest_blood_tests_hospital}, {biggest_blood_tests_count} blood tests\n")

print("Questions for plot analysis:\n")

print("Q6. What is the most common age of a patient among all hospitals?")
print("The answer to the 6th question: 15-35\n")

print("Q7. What is the most common diagnosis among patients in all hospitals?")
print("The answer to the 7th question: pregnancy\n")

print("Q8. What is the main reason for the gap in height values distribution by hospitals?")
print("Q9. Which correspond to the relatively small and big values?")
print("""The answers to the 8th and 9th question:
         There was a strange metrics for height of sports patients, so I entered factor '3.5' to normalize
         the height to a normal distribution. And now in sports hospital the most common height is athletic
         especially compered with pregnant hospital where common patient is ordinary women.
         So the answer to question 8th: different groups of patients,
         and question 9th: women from the pregnancy hospital and athletes from the sports hospital""")

# Visualization:

# Data
age_ranges = [0, 15, 35, 55, 70, 80]
diagnosis_labels = all_diagnoses.index.tolist()
violins_data = [height_by_hospital["general"], height_by_hospital["prenatal"], height_by_hospital["sports"]]

# Frame
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
ax1, ax2, ax3 = axes

# Histogram
ax1.hist(merged_dataframe["age"], bins=age_ranges, color="orange", edgecolor="white")
ax1.set_title("Age of all patients")
ax1.set_xlabel("Age")
ax1.set_ylabel("Number of patients")

# Pie chart
ax2.pie(all_diagnoses, labels=diagnosis_labels, autopct="%1.1f%%")
ax2.set_title("Diagnoses of all patients")

# Violin chart (seaborn chart over the matplotlib.pyplot chart)
ax3.violinplot(violins_data, showextrema=False, showmeans=False, showmedians=False)
sns.violinplot(data=violins_data)
ax3.set_title("Height by hospital")
ax3.set_xlabel("Data density")
ax3.set_ylabel("Height")
ax3.set_xticklabels(("general", "prenatal", "sports"))

plt.show()

# Printing all columns
# with pd.option_context('display.max_columns', None, 'display.max_rows', None):
#     print(merged_dataframe)
