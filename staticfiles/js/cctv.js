document.addEventListener("DOMContentLoaded", function() {
    const video = document.getElementById("video");

    video.addEventListener("canplay", () => {
        video.play();
    });

    // Handle video playback errors
    video.addEventListener("error", () => {
        alert("An error occurred while playing the video.");
    });
});
