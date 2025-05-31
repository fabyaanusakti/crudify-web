document.addEventListener('DOMContentLoaded', function () {
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const photo = document.getElementById('photo');
        const captureBtn = document.getElementById('capture-btn');
        const imageData = document.getElementById('image_data');
        const defaultImage = "{% static 'images/default.png' %}";
        const cameraModal = document.getElementById('cameraModal');

        let stream = null;

        function startCamera() {
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ video: true })
                    .then(s => {
                        stream = s;
                        video.srcObject = stream;
                    })
                    .catch(err => {
                        console.error("Webcam error:", err);
                    });
            }
        }

        function stopCamera() {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
                video.srcObject = null;
                stream = null;
            }
        }

        // Capture button inside modal
        captureBtn.addEventListener('click', function () {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

            const imageUrl = canvas.toDataURL('image/jpeg', 0.9);
            photo.src = imageUrl;
            imageData.value = imageUrl;

            const bsModal = bootstrap.Modal.getInstance(cameraModal);
            bsModal.hide();  // Close modal
            stopCamera();
        });

        // Close camera when modal is closed
        cameraModal.addEventListener('hidden.bs.modal', function () {
            stopCamera();
        });

        // Start camera when modal is opened
        cameraModal.addEventListener('shown.bs.modal', function () {
            startCamera();
        });
    });