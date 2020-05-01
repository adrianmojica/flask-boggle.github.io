class BoggleGame {
    constructor(boardId, secs = 60) {
        console.log('constructed');
        this.secs = secs; // game length
        this.showTimer();
    
        this.score = 0;
        this.words = new Set();
        this.board = $("#" + boardId);
    
        this.timer = setInterval(this.updateClock.bind(this), 1000);
    
        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
        console.log('constructed');
    }

    async handleSubmit(evt){
        evt.preventDefault();
        const $word = $(".word", this.board);
        let word = $word.val();
        console.log('word', word);

        if (!word) return;

        if (this.words.has(word)) {
        this.showMessage(`Already used ${word}`, "error");
        return;
        }

        const resp = await axios.get('/guess',{params:{word:word}});
        console.log(resp.data.result);
        if (resp.data.result === "not-word") {
            this.showMessage(`${word} is not a word`, "error");
        }
        else if (resp.data.result === "not-on-board") {
            this.showMessage(`${word} is not on the board`, "error");
        }
        else if (resp.data.result === "ok") {
            this.showMessage(`${word} is valid! yay!`, "success");
            this.score += word.length;
            this.showScore();
            this.words.add(word);  //add word to set
        }

    }

    showTimer() {
        // update the timer
        $(".timer", this.board).text(this.secs);
    }

    showScore(){
        // update the score
        $(".score", this.board).text(this.score);
    }

    showHighScore(){
        $(".score", this.board).text(this.score);
    }

    showMessage(msg, cls) {
        $(".msg", this.board)
          .text(msg)
          .removeClass()
          .addClass(`msg ${cls}`);
    }

    async scoreGame() {
        $(".add-word", this.board).hide();
        this.showMessage('GAME OVER', "game-over");
        const response = await axios.post('/score',{score:this.score});
        console.log(response)
        

    }

    async updateClock() {
        this.secs -= 1;
        this.showTimer();
    
        if (this.secs === 0) {
          clearInterval(this.timer);
          await this.scoreGame();
        }
    }


    
   
    
}


