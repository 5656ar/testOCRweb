document.addEventListener('DOMContentLoaded', () => {
    const captureButton = document.getElementById('captureButton');
    const camera = document.getElementById('camera');
    const snapshot = document.getElementById('snapshot');
    const result = document.getElementById('result');

    let stream;

    // เริ่มต้นกล้อง
    async function startCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            camera.srcObject = stream;
            camera.hidden = false;
        } catch (error) {
            console.error('Error accessing camera:', error);
            result.textContent = 'Cannot access the camera.';
        }
    }

    // หยุดกล้อง
    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        camera.hidden = true;
    }

    // ถ่ายภาพจากกล้อง
    captureButton.addEventListener('click', () => {
        const context = snapshot.getContext('2d');
        snapshot.width = camera.videoWidth;
        snapshot.height = camera.videoHeight;
        context.drawImage(camera, 0, 0, snapshot.width, snapshot.height);
        snapshot.toBlob(blob => {
            uploadImage(blob);
        });
    });

    // อัปโหลดภาพไปยังเซิร์ฟเวอร์
    async function uploadImage(file) {
        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
            result.textContent = `Detected Numbers: ${data.numbers}`;
        } catch (error) {
            result.textContent = 'Error uploading image.';
        }
    }

    // เรียกใช้กล้องเมื่อโหลดหน้าเว็บ
    startCamera();

    // หยุดกล้องเมื่อออกจากหน้าเว็บ
    window.addEventListener('beforeunload', stopCamera);
});
