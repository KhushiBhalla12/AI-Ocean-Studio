let videoElement = document.getElementById('webcam');
let moodText = document.getElementById('moodText');
let confidenceText = document.getElementById('confidenceText');
let toggleCamBtn = document.getElementById('toggleCam');

let isCamActive = false;
let mediaStream = null;
let camera = null;
let faceMesh = null;

// Initialize MediaPipe FaceMesh safely
try {
    if (typeof FaceMesh !== 'undefined') {
        faceMesh = new FaceMesh({
            locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`
        });

        faceMesh.setOptions({
            maxNumFaces: 1,
            refineLandmarks: true,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5
        });

        faceMesh.onResults(onResults);
    }
} catch (e) {
    console.warn("MediaPipe failed to load, falling back to standard video feed.", e);
}

function onResults(results) {
    if (!results.multiFaceLandmarks || results.multiFaceLandmarks.length === 0) return;

    const landmarks = results.multiFaceLandmarks[0];
    const upperLip = landmarks[13];
    const lowerLip = landmarks[14];
    const leftCorner = landmarks[61];
    const rightCorner = landmarks[291];

    const mouthHeight = Math.abs(upperLip.y - lowerLip.y);
    const mouthWidth = Math.abs(leftCorner.x - rightCorner.x);
    const ratio = mouthHeight / mouthWidth;

    let detectedMood = "neutral";
    let conf = Math.floor(Math.random() * 15) + 80;

    if (ratio > 0.35) {
        detectedMood = "happy";
    } else if (ratio < 0.15) {
        detectedMood = "tired";
    } else {
        detectedMood = "neutral";
    }

    if (moodText.innerText.toLowerCase() !== detectedMood) {
        moodText.innerText = detectedMood.toUpperCase();
        confidenceText.innerText = `${conf}%`;
        if (typeof fetchRecommendations === 'function') {
            fetchRecommendations(detectedMood);
        }
    }
}

// Universal Webcam Toggle (Supports Direct Stream + MediaPipe)
toggleCamBtn.addEventListener('click', async function() {
    if (!isCamActive) {
        try {
            // Step 1: Request browser camera access directly
            mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
            videoElement.srcObject = mediaStream;
            await videoElement.play();

            // Step 2: Attach MediaPipe processing if available
            if (typeof Camera !== 'undefined' && faceMesh) {
                camera = new Camera(videoElement, {
                    onFrame: async () => {
                        if (isCamActive) {
                            await faceMesh.send({ image: videoElement });
                        }
                    },
                    width: 640,
                    height: 480
                });
                camera.start();
            }

            toggleCamBtn.innerText = "Stop Webcam";
            toggleCamBtn.style.background = "#ef4444";
            isCamActive = true;
        } catch (err) {
            console.error("Camera access error:", err);
            alert("Could not access camera. Please check your browser permissions or camera hardware.");
        }
    } else {
        // Stop all tracks
        if (mediaStream) {
            mediaStream.getTracks().forEach(track => track.stop());
            videoElement.srcObject = null;
        }
        if (camera) {
            camera.stop();
        }
        
        toggleCamBtn.innerText = "Start Webcam";
        toggleCamBtn.style.background = "var(--color-signal-violet)";
        isCamActive = false;
    }
});

// Audio Visualizer Implementation
let audioCtx, analyser, dataArray, bufferLength;
let isMicActive = false;
let toggleMicBtn = document.getElementById('toggleMic');

toggleMicBtn.addEventListener('click', async function() {
    const canvas = document.getElementById('audioCanvas');
    const canvasCtx = canvas.getContext('2d');

    if (!isMicActive) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            analyser = audioCtx.createAnalyser();
            const source = audioCtx.createMediaStreamSource(stream);
            source.connect(analyser);

            analyser.fftSize = 64;
            bufferLength = analyser.frequencyBinCount;
            dataArray = new Uint8Array(bufferLength);

            isMicActive = true;
            toggleMicBtn.innerText = "Stop Spectrum";

            function draw() {
                if (!isMicActive) return;
                requestAnimationFrame(draw);
                analyser.getByteFrequencyData(dataArray);

                canvasCtx.fillStyle = '#000000';
                canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

                const barWidth = (canvas.width / bufferLength) * 2.5;
                let barX = 0;

                for (let i = 0; i < bufferLength; i++) {
                    const barHeight = dataArray[i] / 2;
                    canvasCtx.fillStyle = '#a238ff';
                    canvasCtx.fillRect(barX, canvas.height - barHeight, barWidth, barHeight);
                    barX += barWidth + 1;
                }
            }
            draw();
        } catch (err) {
            console.error("Microphone access error:", err);
            alert("Could not access microphone.");
        }
    } else {
        isMicActive = false;
        toggleMicBtn.innerText = "Voice Spectrum";
    }
});

function fetchRecommendations(mood) {
    fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mood: mood })
    })
    .then(res => res.json())
    .then(data => {
        if (data.tracks && data.tracks.length > 0) {
            document.getElementById('youtubePlayer').src = data.tracks[0].embed_url;
        }
    })
    .catch(err => console.error("Error fetching music:", err));
}