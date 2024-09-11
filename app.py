from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class QandA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(500), nullable=True)
    is_template = db.Column(db.Boolean, default=False)
    is_confirmed = db.Column(db.Boolean, default=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/questioner')
def questioner():
    questions = QandA.query.with_entities(QandA.question).filter_by(is_template=True).all()
    question_list = [q.question for q in questions]
    return render_template('questioner.html', questions=question_list)

@app.route('/get_answer', methods=['POST'])
def get_answer():
    user_question = request.form['question']
    qanda = QandA.query.filter(QandA.question.like(f"%{user_question}%")).first()
    
    if qanda and not qanda.is_confirmed:
        return jsonify({'answer': qanda.answer, 'question_id': qanda.id})
    else:
        return jsonify({'answer': 'Sorry, I do not have an answer for that question or it has already been confirmed.'})

@app.route('/answer')
def answer():
    new_questions = QandA.query.filter(QandA.answer == None).all()
    return render_template('answer.html', questions=new_questions)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    question_id = request.form['question_id']
    answer = request.form['answer']
    qanda = QandA.query.get(question_id)
    qanda.answer = answer
    qanda.is_template = True
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/submit_question', methods=['POST'])
def submit_question():
    question = request.form['question']
    new_question = QandA(question=question, answer=None, is_template=False)
    db.session.add(new_question)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/confirm_answer', methods=['POST'])
def confirm_answer():
    question_id = request.form['question_id']
    qanda = QandA.query.get(question_id)
    qanda.is_confirmed = True
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/history')
def history():
    all_qandas = QandA.query.filter(QandA.answer != None).all()
    return render_template('history.html', qandas=all_qandas)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
