var quizData;
var currentQuestion = 0;
var score = 0;
var selectedAnswer = null;
var questionElement = document.getElementById("question");
var answersElement = document.getElementById("answers");
var nextElement = document.getElementById("next");
var userResponses = [];
var quizEnded = false;
function startQuiz(data) {
    document.getElementById("returnButton").addEventListener("click", function() {
        if (quizEnded) {
            sendUserResponses();
        }
    });
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
    setTimeout(() => {
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
    }, 2000);
}

function checkAnswer() {
    var questionObject = quizData[currentQuestion];
    var correctAnswer = questionObject.correct_answer;
    var isCorrect = selectedAnswer === correctAnswer;
    var category = questionObject.category;
    userResponses.push({
        question: questionObject.question,
        userAnswer: selectedAnswer,
        correctAnswer: correctAnswer,
        isCorrect: isCorrect,
        category: category,
    });

    if (isCorrect) {
        score++;
        document.querySelector(`input[value="${selectedAnswer}"]`).parentElement.classList.add('animate__animated', 'animate__shakeX', 'correct');
        setTimeout(() => { document.querySelector(`input[value="${selectedAnswer}"]`).parentElement.classList.remove('animate__animated', 'animate__shakeX', 'correct'); }, 1000);
    } else {
        document.querySelector(`input[value="${selectedAnswer}"]`).parentElement.classList.add('animate__animated', 'animate__shakeX', 'incorrect');
        setTimeout(() => { document.querySelector(`input[value="${selectedAnswer}"]`).parentElement.classList.remove('animate__animated', 'animate__shakeX', 'incorrect'); }, 1000);
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
    quizEnded = true;
    displayQuizSummary();
}

function sendUserResponses() {
    var jsonData = JSON.stringify(userResponses);
    var form = document.createElement("form");
    form.method = "POST";
    form.action = "/";
    var input = document.createElement("input");
    input.type = "hidden";
    input.name = "userResponses";
    input.value = jsonData;

    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}


function displayQuizSummary() {
    var totalQuestions = quizData.length;
    var correctAnswers = score;
    var wrongAnswers = totalQuestions - correctAnswers;

    document.getElementById("totalQuestions").textContent = totalQuestions;
    document.getElementById("correctAnswers").textContent = correctAnswers;
    document.getElementById("wrongAnswers").textContent = wrongAnswers;
    var popupModal = new bootstrap.Modal(document.getElementById('popupModal'));
    popupModal.show();
}