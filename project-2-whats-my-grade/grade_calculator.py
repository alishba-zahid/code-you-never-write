import json

def load_scores(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def calculate_grade(scores):
    # Rules
    # Quizzes: 20% (drop lowest)
    # Assignments: 10% (average)
    # Midterm: 30%
    # Final Exam: 40% (not taken yet)
    
    # 1. Quizzes
    quizzes = scores.get('quizzes', [])
    if len(quizzes) > 1:
        sorted_quizzes = sorted(quizzes)
        dropped = sorted_quizzes[0]
        active_quizzes = sorted_quizzes[1:]
        quiz_avg = sum(active_quizzes) / len(active_quizzes)
    else:
        dropped = None
        quiz_avg = sum(quizzes) / len(quizzes) if quizzes else 0.0

    # 2. Assignments
    assignments = scores.get('assignments', [])
    assign_avg = sum(assignments) / len(assignments) if assignments else 0.0

    # 3. Midterm
    midterm = scores.get('midterm', 0.0)

    # Weights
    w_quiz = 0.20
    w_assign = 0.10
    w_midterm = 0.30
    w_total_current = w_quiz + w_assign + w_midterm # 0.60
    
    # Weighted points
    pts_quiz = quiz_avg * w_quiz
    pts_assign = assign_avg * w_assign
    pts_midterm = midterm * w_midterm
    pts_current = pts_quiz + pts_assign + pts_midterm
    
    # Running percentage (out of 100%)
    running_grade = (pts_current / w_total_current)
    
    return {
        'quiz_avg': quiz_avg,
        'quiz_dropped': dropped,
        'assign_avg': assign_avg,
        'midterm': midterm,
        'pts_current': pts_current,
        'running_grade': running_grade,
        'current_weight': w_total_current
    }

def get_final_exam_required(pts_current, target_grade):
    # Target = pts_current + 0.40 * FinalExam
    # FinalExam = (Target - pts_current) / 0.40
    required = (target_grade - pts_current) / 0.40
    return required

def main():
    json_file = 'scores.json'
    print("=" * 60)
    print("ACADEMIC GRADE CALCULATOR & STRATEGY ENGINE")
    print("=" * 60)
    
    try:
        scores = load_scores(json_file)
    except Exception as e:
        print(f"Error loading {json_file}: {e}")
        return

    results = calculate_grade(scores)
    
    print("[1] Category Details:")
    if results['quiz_dropped'] is not None:
        print(f"  * Quizzes Average (after dropping lowest score {results['quiz_dropped']}): {results['quiz_avg']:.2f}%")
    else:
        print(f"  * Quizzes Average: {results['quiz_avg']:.2f}%")
    print(f"  * Assignments Average: {results['assign_avg']:.2f}%")
    print(f"  * Midterm Exam: {results['midterm']:.2f}%")
    print()

    print("[2] Current Weighted Standing:")
    print(f"  * Total current weighted points: {results['pts_current']:.2f} / 60.00")
    print(f"  * Current Running Grade: {results['running_grade']:.2f}%")
    print()

    print("[3] Final Exam Targets (Weight: 40%):")
    targets = [90, 85, 80, 70]
    for t in targets:
        req = get_final_exam_required(results['pts_current'], t)
        if req > 100:
            status = "IMPOSSIBLE (Exceeds 100%)"
        elif req < 0:
            status = "GUARANTEED (Required score below 0%)"
        else:
            status = f"Required score: {req:.2f}%"
        print(f"  * To secure grade of {t}% (Grade Threshold): {status}")
    print("=" * 60)

if __name__ == "__main__":
    main()
