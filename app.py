from flask import Flask, render_template, request
from gpt_helper import select_best_questions, generate_personality_profile
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_intro = request.form['intro']
        questions = select_best_questions(user_intro)

        # ✅ Ensure questions is always a list of clean sentences
        if isinstance(questions, str):
            # Split on numbered questions like "1. question", "2. question" or by periods
            split_by_numbering = re.split(r'\d+\.\s*', questions)
            cleaned_questions = [q.strip() for q in split_by_numbering if len(q.strip()) > 5]
            if len(cleaned_questions) > 1:
                questions = cleaned_questions
            else:
                # fallback split by period if numbering fails
                questions = [q.strip() for q in questions.split('.') if len(q.strip()) > 5]

        return render_template('index.html', intro=user_intro, questions=questions)
    return render_template('index.html', intro=None, questions=None)

@app.route('/submit', methods=['POST'])
def submit():
    user_intro = request.form['intro']
    questions = request.form.getlist('questions')
    answers = [request.form.get(f'answer_{i}') for i in range(len(questions))]
    qa_pairs = list(zip(questions, answers))
    profile = generate_personality_profile(user_intro, qa_pairs)
    return render_template('index.html', intro=user_intro, profile=profile)

if __name__ == '__main__':
    app.run(debug=True)
