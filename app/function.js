// Quotes array for random sentences
const quotes = [
    "The quick brown fox jumps over the lazy dog.",
    "JavaScript is fun to learn!",
    "Practice makes perfect.",
    "Typing speed tests are challenging yet rewarding.",
    "Coding improves problem-solving skills."
];

let startTime;
let quoteText = "";

// DOM Elements
const quoteDisplay = document.getElementById("quote");
const inputField = document.getElementById("input");
const startBtn = document.getElementById("start-btn");
const resultsDiv = document.getElementById("results");

// Function to start the test
function startTest() {
    quoteText = quotes[Math.floor(Math.random() * quotes.length)];
    quoteDisplay.innerText = quoteText;
    inputField.value = "";
    inputField.disabled = false;
    inputField.focus();
    resultsDiv.innerText = "";
    startTime = new Date().getTime();
}

// Function to end the test and calculate results
function endTest() {
    const endTime = new Date().getTime();
    const timeTaken = (endTime - startTime) / 1000; // in seconds

    const typedText = inputField.value.trim();
    if (typedText === "") {
        resultsDiv.innerHTML = `<p>Please type the text to get results!</p>`;
        return; // Exit if nothing is typed
    }

    const wordCount = typedText.split(" ").length;
    const wpm = Math.round((wordCount / timeTaken) * 60);
    const wps = (wordCount / timeTaken).toFixed(2); // Calculate WPS

    let correctChars = 0;
    for (let i = 0; i < typedText.length; i++) {
        if (typedText[i] === quoteText[i]) correctChars++;
    }
    const accuracy = Math.round((correctChars / quoteText.length) * 100);

    // Log for debugging
    console.log(`Typed Text: "${typedText}"`);
    console.log(`Time Taken: ${timeTaken} seconds`);
    console.log(`Word Count: ${wordCount}`);
    console.log(`WPM: ${wpm}, WPS: ${wps}`);

    resultsDiv.innerHTML = `
        <p>Words Per Minute: ${wpm} WPM</p>
        <p>Words Per Second: ${wps} WPS</p>
        <p>Accuracy: ${accuracy}%</p>
    `;

    inputField.disabled = true;
}

inputField.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        endTest();
    }
});

// Event Listeners
startBtn.addEventListener("click", startTest);

inputField.addEventListener("input", () => {
    if (inputField.value.trim() === quoteText) {
        endTest();
    }
});
