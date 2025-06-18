document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const photo = document.getElementById('photo');
    const captureBtn = document.getElementById('capture-btn');
    const imageData = document.getElementById('image_data');
    const cameraModal = document.getElementById('cameraModal');
    let stream = null;

    function startCamera() {
        if (navigator.mediaDevices?.getUserMedia) {
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

    captureBtn?.addEventListener('click', function () {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageUrl = canvas.toDataURL('image/jpeg', 0.9);
        photo.src = imageUrl;
        imageData.value = imageUrl;

        try {
            let bsModal = bootstrap.Modal.getInstance(cameraModal);
            if (!bsModal) {
                bsModal = new bootstrap.Modal(cameraModal);
            }
            bsModal.hide();
        } catch (err) {
            console.error("Modal closing fallback:", err);
            document.getElementById('closeModalBtn')?.click();
        }

        stopCamera();
    });

    cameraModal?.addEventListener('shown.bs.modal', startCamera);
    cameraModal?.addEventListener('hidden.bs.modal', stopCamera);
});