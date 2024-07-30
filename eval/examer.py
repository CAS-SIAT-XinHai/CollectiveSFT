import json
import os
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def calculate_accuracy(my_answers, correct_answers):
    # Mapping correct answers by id for easy lookup
    correct_map = {item['id']: item['answer'] for item in correct_answers}
    
    # Count correct answers and prepare for detailed statistics
    total_questions = len(my_answers)
    correct_count = 0
    accuracy_per_category = {}
    accuracy_per_subcategory = {}

    # Calculate accuracy
    for answer in my_answers:
        question_id = answer['id']
        user_answer = answer['model_answer']
        correct_answer = correct_map.get(question_id)

        if user_answer == correct_answer:
            correct_count += 1
        
        # Statistics per category
        category = answer['exam_type']
        subcategory = answer['exam_class']

        if category not in accuracy_per_category:
            accuracy_per_category[category] = {'correct': 0, 'total': 0}
        if category not in accuracy_per_subcategory:
            accuracy_per_subcategory[category] = {}

        if subcategory not in accuracy_per_subcategory[category]:
            accuracy_per_subcategory[category][subcategory] = {'correct': 0, 'total': 0}

        accuracy_per_category[category]['total'] += 1
        accuracy_per_subcategory[category][subcategory]['total'] += 1

        if user_answer == correct_answer:
            accuracy_per_category[category]['correct'] += 1
            accuracy_per_subcategory[category][subcategory]['correct'] += 1

    # Convert counts to percentages
    for category in accuracy_per_category:
        accuracy_per_category[category] = accuracy_per_category[category]['correct'] / accuracy_per_category[category]['total']

    for category in accuracy_per_subcategory:
        for subcategory in accuracy_per_subcategory[category]:
            acc = accuracy_per_subcategory[category][subcategory]
            accuracy_per_subcategory[category][subcategory] = acc['correct'] / acc['total']

    # Overall accuracy
    overall_accuracy = correct_count / total_questions

    return {
        "overall_accuracy": overall_accuracy,
        "accuracy_per_category": accuracy_per_category,
        "accuracy_per_subcategory": accuracy_per_subcategory
    }

# Load files (adjust paths as necessary)
my_answers_path = '/path/to/your/answer.json'
correct_answers_path = '/path/to/CMB-test-choice-answer.json'

my_answers = load_data(my_answers_path)
correct_answers = load_data(correct_answers_path)

# Calculate accuracy
results = calculate_accuracy(my_answers, correct_answers)

# Print results
print(json.dumps(results, indent=4,ensure_ascii=False))


# Save results to a file with the same name as my_answers but in a different directory
results_filename = os.path.basename(my_answers_path)
results_path = f'score/{results_filename}'
with open(results_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=4,ensure_ascii=False)