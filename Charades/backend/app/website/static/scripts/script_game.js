var quizData;
var currentQuestion = 0;
var score = 0;
var selectedAnswer = null;
var questionElement = document.getElementById("question");
var answersElement = document.getElementById("answers");
var nextElement = document.getElementById("next");

function startQuiz(data) {
    quizData = data.results;
    console.log("startQuiz - quizData:", quizData);
    displayQuestion();
    displayAnswers();
    nextElement.addEventListener("click", nextQuestion);
}

function displayQuestion() {
    var questionObject = quizData[currentQuestion];
    questionElement.innerHTML = questionObject.question;
    console.log("displayQuestion - Question:", questionObject.question);
}

function displayAnswers() {
    var questionObject = quizData[currentQuestion];
    var correctAnswer = questionObject.correct_answer;
    var incorrectAnswers = questionObject.incorrect_answers;
    var allAnswers = [correctAnswer].concat(incorrectAnswers);
    for (var i = allAnswers.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = allAnswers[i];
        allAnswers[i] = allAnswers[j];
        allAnswers[j] = temp;
    }
    for (var i = 0; i < allAnswers.length; i++) {
        var answerText = allAnswers[i];
        var answerElement = document.createElement("div");
        answerElement.classList.add("form-check");
        answerElement.innerHTML =
            '<input class="form-check-input" type="radio" name="answer" id="answer' +
            i +
            '" value="' +
            answerText +
            '">' +
            '<label class="form-check-label" for="answer' +
            i +
            '">' +
            answerText +
            "</label>";
        answersElement.appendChild(answerElement);
        answerElement.addEventListener("click", selectAnswer);
        console.log("displayAnswers - Answer:", answerText);
    }
}

function selectAnswer(event) {
    selectedAnswer = event.target.value;
    nextElement.disabled = false;
    console.log("selectAnswer - Selected Answer:", selectedAnswer);
}

function nextQuestion() {
    checkAnswer();
    currentQuestion++;
    if (currentQuestion < quizData.length) {
        displayQuestion();
        clearAnswers();
        displayAnswers();
        nextElement.disabled = true;
    } else {
        endQuiz();
    }
    console.log("nextQuestion - Current Question:", currentQuestion);
}

function checkAnswer() {
    var questionObject = quizData[currentQuestion];
    var correctAnswer = questionObject.correct_answer;
    if (selectedAnswer === correctAnswer) {
        score++;
        answersElement.classList.add('animate__animated', 'animate__shakeX', 'correct');
        setTimeout(() => { answersElement.classList.remove('animate__animated', 'animate__shakeX', 'correct'); }, 1000);
    } else {
        answersElement.classList.add('animate__animated', 'animate__shakeX', 'incorrect');
        setTimeout(() => { answersElement.classList.remove('animate__animated', 'animate__shakeX', 'incorrect'); }, 1000);
    }
    console.log("checkAnswer - Correct Answer:", correctAnswer);
    console.log("checkAnswer - Score:", score);
}

function clearAnswers() {
    while (answersElement.firstChild) {
        answersElement.removeChild(answersElement.firstChild);
    }
    console.log("clearAnswers - Answers cleared");
}

function endQuiz() {
    questionElement.innerHTML =
        "You scored " + score + " out of " + quizData.length + ".";
    clearAnswers();
    nextElement.style.display = "none";
    console.log("endQuiz - Quiz Ended - Score:", score);
}
