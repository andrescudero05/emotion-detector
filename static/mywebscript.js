"use strict";

const emotionForm = document.getElementById("emotion-form");
const textInput = document.getElementById("textToAnalyze");
const resultElement = document.getElementById("system_response");
const analyzeButton = document.getElementById("analyze-button");

emotionForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const textToAnalyze = textInput.value.trim();

    if (!textToAnalyze) {
        resultElement.textContent = "Invalid text! Please enter a statement.";
        textInput.focus();
        return;
    }

    analyzeButton.disabled = true;
    resultElement.textContent = "Analyzing...";

    try {
        const query = new URLSearchParams({ textToAnalyze });
        const response = await fetch(`/emotionDetector?${query.toString()}`);
        const message = await response.text();
        resultElement.textContent = response.ok
            ? message
            : `Error: ${message}`;
    } catch (_error) {
        resultElement.textContent =
            "Could not reach the application. Please try again.";
    } finally {
        analyzeButton.disabled = false;
    }
});
