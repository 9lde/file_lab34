import matplotlib.pyplot as plt
import os
def main():
        submissions_list = load_submissions()
        assignment_dict = load_assignments()
        student_dict = load_students()
        count = 0
        print('''1. Student grade
2. Assignment statistics 
3. Assignment graph''')
        user_choice = int(input('Enter your selection: '))
        if user_choice == '1':
            score = 0
            total_quiz_points = 0
            student_name = input("What is the student's name: ")
            try:
                user_selection_id = student_dict[f'{student_name}']
                for i in range(len(submissions_list)):
                    quiz_id = submissions_list[i][1]
                    if user_selection_id in submissions_list[i] and quiz_id in assignment_dict:
                        score_on_assignment = int(submissions_list[i][2])
                        assignment_info = assignment_dict[quiz_id]
                        max_points = assignment_info['points']
                        score += (score_on_assignment / 100) * max_points
                grade = ((score / 1000) * 100)
                print(f'{grade:.0f}%')
            except KeyError:
                print('Student not found')

        if user_choice == '2':
            quiz_name = input("What is the assignment name: ")
            try:
                results = assignment_stats(quiz_name, assignment_dict, submissions_list, count)
                average_grades = results[2]/results[3]
                print(f"""Min: {int(results[0]):.0f}%
Avg: {int(average_grades):.0f}%
Max: {int(results[1]):.0f}%""")
            except TypeError:
                print('Assignment not found')

        if user_choice == '3':
            try:
                all_grades = []
                quiz_name = input("What is the assignment name: ")
                results = assignment_stats(quiz_name, assignment_dict, submissions_list, count)
                for i in range(len(results[4])):
                    all_grades.append(int(results[4][i]))
                print(all_grades)
                bins = range(50,101,10)
                plt.hist(all_grades, bins=bins)
                plt.xticks(bins)
                plt.show()
            except TypeError:
                print('Assignment not found')

def assignment_stats(quiz_name, assignment_dict, submissions_list, count):
    grades_data = []
    for quiz_id, key in assignment_dict.items():
        if key['name'] == quiz_name:
            lowest_grade = submissions_list[0][2]
            highest_grade = submissions_list[0][2]
            total_student_scores = 0
            for i in range(len(submissions_list)):
                if quiz_id in submissions_list[i] and quiz_id in assignment_dict:
                    if submissions_list[i][2] < lowest_grade:
                        lowest_grade = submissions_list[i][2]
                    if submissions_list[i][2] > highest_grade:
                        highest_grade = submissions_list[i][2]
                    total_student_scores += int(submissions_list[i][2])
                    grades_data.append(submissions_list[i][2])
                    count += 1
            return lowest_grade, highest_grade, total_student_scores, count, grades_data

def load_assignments():
    assignments = {}
    with open('data/assignments.txt', 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            assignment_name = lines[i].strip()
            assignment_id = lines[i+1].strip()
            total_points = int(lines[i+2].strip())
            assignments[assignment_id] = {'name': assignment_name, 'points': total_points}
    return assignments
def load_students():
    student_ids = {}
    with open('data/students.txt', 'r') as file:
        for line in file:
            student_id = line[:3]
            student_name = line[3:].strip()
            student_ids[student_name] = student_id
    return student_ids
def load_submissions():
    submissions = []
    for files in os.listdir('data/submissions'):
        file_path = os.path.join('data/submissions', files)
        with open(file_path, 'r') as file:
            for line in file:
                student_id, assignment_id, score = line.strip().split('|')
                submissions.append([student_id, assignment_id, score])
    return submissions
if __name__ == '__main__':
    main()