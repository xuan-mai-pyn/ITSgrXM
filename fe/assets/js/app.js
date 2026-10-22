document.addEventListener("DOMContentLoaded", () => {
    const startBtn = document.getElementById("start-btn");
    const pauseBtn = document.getElementById("pause-btn");
    const resetBtn = document.getElementById("reset-btn");
    const upstreamOcc = document.getElementById("upstream-occ");
    const downstreamOcc = document.getElementById("downstream-occ");
    const statusBox = document.getElementById("status-box");

    let intervalId = null;

    function runSimulation() {
        const upVal = (Math.random() * 15 + 10).toFixed(1); // Dao động 10% - 25%
        const downVal = (Math.random() * 10 + 5).toFixed(1);  // Dao động 5% - 15%

        if (upstreamOcc) upstreamOcc.textContent = `Occupancy: ${upVal}%`;
        if (downstreamOcc) downstreamOcc.textContent = `Occupancy: ${downVal}%`;

        if (statusBox) {
            if ((upVal - downVal) > 8) {
                statusBox.textContent = "Trạng thái: CẢNH BÁO - Phát hiện dấu hiệu sự cố giao thông!";
                statusBox.style.background = "#fee2e2";
                statusBox.style.color = "#991b1b";
            } else {
                statusBox.textContent = "Trạng thái: Giao thông bình thường";
                statusBox.style.background = "#dcfce7";
                statusBox.style.color = "#166534";
            }
        }
    }

    if (startBtn) {
        startBtn.addEventListener("click", () => {
            if (!intervalId) {
                intervalId = setInterval(runSimulation, 1500);
            }
        });
    }

    if (pauseBtn) {
        pauseBtn.addEventListener("click", () => {
            clearInterval(intervalId);
            intervalId = null;
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener("click", () => {
            clearInterval(intervalId);
            intervalId = null;
            if (upstreamOcc) upstreamOcc.textContent = "Occupancy: 0.0%";
            if (downstreamOcc) downstreamOcc.textContent = "Occupancy: 0.0%";
            if (statusBox) {
                statusBox.textContent = "Trạng thái: Đã đặt lại (Chưa chạy)";
                statusBox.style.background = "#f1f5f9";
                statusBox.style.color = "#475569";
            }
        });
    }
});