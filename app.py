from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdfgkjtjkkg45yfdb"

boggle_game = Boggle()

@app.route('/')
def main():
    """Show game board"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    return render_template("index.html", board=board, highscore=highscore,
                           nplays=nplays)

@app.route('/guess')
def guess():
    """gets the guess from form"""
    word = request.args["word"]
    board = session["board"]

    # create response by the response of the function if word is valid
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route('/score',methods=["POST"])
def score():
    """gets the score from the frontend and updates times played"""
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    score = request.json["score"]
    if score > highscore:
        highscore = score
    session['highscore'] = highscore
    session['nplays'] = nplays +1

    return jsonify(brokeRecord = highscore)

   