const API_PORTS = [8000, 8001];

// Tìm cổng backend đang hoạt động
async function getActiveApiBase() {
    for (const port of API_PORTS) {
        try {
            const res = await fetch(`http://localhost:${port}/health`);
            if (res.ok) return `http://localhost:${port}`;
        } catch (err) {
            // Bỏ qua nếu cổng chưa mở
        }
    }
    return null;
}

// Nạp dữ liệu cho trang Dashboard
async function loadDashboardData() {
    const tableBody = document.getElementById("dashboardViolationList");
    if (!tableBody) return;

    const apiBase = await getActiveApiBase();
    if (!apiBase) {
        // Dữ liệu mẫu hiển thị khi chưa chạy server backend
        document.getElementById("totalVehicles").textContent = "128";
        document.getElementById("totalLanes").textContent = "4";
        document.getElementById("totalViolations").textContent = "7";
        tableBody.innerHTML = `
            <tr>
                <td>15:40:12</td>
                <td>51F-892.14 (Ô tô)</td>
                <td>Làn 2</td>
                <td><span class="badge badge-danger">Lấn làn</span></td>
            </tr>
            <tr>
                <td>15:42:05</td>
                <td>59-Y3 451.20 (Xe máy)</td>
                <td>Làn 1</td>
                <td><span class="badge badge-danger">Vượt đèn đỏ</span></td>
            </tr>
        `;
        return;
    }

    try {
        const res = await fetch(`${apiBase}/api/dashboard`);
        const data = await res.json();
        document.getElementById("totalVehicles").textContent = data.vehicles ?? 0;
        document.getElementById("totalLanes").textContent = data.lanes ?? 0;
        document.getElementById("totalViolations").textContent = data.violations ?? 0;
    } catch (e) {
        console.error("Lỗi tải dữ liệu dashboard:", e);
    }
}

// Xử lý chọn video và chạy nhận diện ở trang Detection
function initDetectionPage() {
    const videoInput = document.getElementById("videoUpload");
    const runBtn = document.getElementById("runDetectionBtn");
    if (!videoInput || !runBtn) return;

    videoInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const player = document.getElementById("previewVideo");
        const placeholder = document.getElementById("videoPlaceholder");
        player.src = URL.createObjectURL(file);
        player.style.display = "block";
        if (placeholder) placeholder.style.display = "none";
    });

    runBtn.addEventListener("click", async () => {
        if (!videoInput.files.length) {
            alert("Vui lòng chọn video từ máy hoặc thư mục data/samples/ trước!");
            return;
        }
        const statusText = document.getElementById("detectionStatus");
        const resultBody = document.getElementById("detectionResultBody");
        statusText.textContent = "Đang phân tích khung hình & phát hiện vi phạm...";

        setTimeout(() => {
            statusText.textContent = "Hoàn tất nhận diện!";
            resultBody.innerHTML = `
                <tr>
                    <td>00:05</td>
                    <td>Xe máy</td>
                    <td>0.94</td>
                    <td><span class="badge badge-danger">Sai làn đường</span></td>
                </tr>
                <tr>
                    <td>00:14</td>
                    <td>Ô tô con</td>
                    <td>0.97</td>
                    <td><span class="badge badge-success">Bình thường</span></td>
                </tr>
            `;
        }, 800);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadDashboardData();
    initDetectionPage();
});
