"""Flask web application for text-based emotion detection."""

from flask import Flask, jsonify, render_template, request

from EmotionDetection import EmotionDetectorError, emotion_detector

app = Flask(__name__)


@app.get("/")
def home():
    """Render the application home page."""
    return render_template("index.html")


@app.get("/emotionDetector")
def emotion_detector_route():
    """Return a human-readable prediction for the web interface."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    result = emotion_detector(text_to_analyze)

    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    scores = ", ".join(
        f"'{emotion}': {result[emotion]}"
        for emotion in ("anger", "disgust", "fear", "joy", "sadness")
    )
    return (
        f"For the given statement, the system response is {scores}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


@app.get("/api/emotionDetector")
def emotion_detector_api():
    """Return the prediction as JSON for programmatic clients."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    result = emotion_detector(text_to_analyze)

    if result["dominant_emotion"] is None:
        return jsonify({"error": "Invalid text! Please try again!", **result}), 400

    return jsonify(result)


@app.errorhandler(EmotionDetectorError)
def handle_emotion_detector_error(error: EmotionDetectorError):
    """Return a clear error response when Watson NLP is unavailable."""
    app.logger.warning("Emotion detection failed: %s", error)
    if request.path.startswith("/api/"):
        return jsonify({"error": str(error)}), 502
    return (
        "The emotion detection service is temporarily unavailable. Please try again.",
        502,
    )


if __name__ == "__main__":
    # debug=False avoids enabling the interactive debugger by default.
    app.run(host="127.0.0.1", port=5000, debug=False)
