/**
 * Created by raeste on 09.03.17.
 */
function showAnswer() {
    var answer = document.getElementById('answer')
    var showAnswerButton = document.getElementById('show_answer');
    var displaySetting = answer.style.display;

    if(displaySetting == 'block') {
        answer.style.display = 'none';
        showAnswerButton.innerHTML = 'Zeige die Antwort';
    } else {
        answer.style.display = 'block';
        showAnswerButton.innerHTML = 'Verstecke die Antwort';
    }
}