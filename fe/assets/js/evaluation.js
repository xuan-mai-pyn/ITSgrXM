document.addEventListener("DOMContentLoaded", async () => {
    const statusElement = document.getElementById("evaluation-status");
    const drElement = document.getElementById("evaluation-dr");
    const farElement = document.getElementById("evaluation-far");
    const ttdElement = document.getElementById("evaluation-ttd");

    try {
        const response = await window.itsFetch("/api/dashboard");
        if (!response.ok) {
            throw new Error(`Backend trả về HTTP ${response.status}`);
        }

        const data = await response.json();
        if (!["available", "no_data"].includes(data.status)) {
            throw new Error("Backend trả về trạng thái dashboard không hợp lệ.");
        }

        const evaluation = data.latest_evaluation
            || (data.latest_simulation && data.latest_simulation.evaluation);

        if (!evaluation) {
            statusElement.textContent = data.message
                || "Backend chưa có kết quả đánh giá. Hãy chạy mô phỏng trước.";
            return;
        }

        drElement.textContent = evaluation.dr === null
            ? "Không xác định"
            : `${(evaluation.dr * 100).toFixed(1)}%`;
        if (evaluation.far === null) {
            farElement.textContent = "Không xác định";
        } else if (evaluation.far_definition === "per_hour") {
            farElement.textContent = `${evaluation.far.toFixed(2)} cảnh báo/giờ`;
        } else {
            farElement.textContent = `${(evaluation.far * 100).toFixed(1)}%`;
        }
        ttdElement.textContent = evaluation.ttd === null
            ? "Không xác định"
            : `${evaluation.ttd.toFixed(2)} (đơn vị dữ liệu)`;

        statusElement.textContent = evaluation.status === "complete"
            ? "Kết quả đánh giá mới nhất từ backend."
            : `Kết quả đánh giá một phần từ backend. Chưa xác định: ${evaluation.unavailable_metrics.join(", ") || "một số chỉ số"}.`;
    } catch (error) {
        console.error("Lỗi tải kết quả đánh giá:", error);
        statusElement.textContent = `Không thể tải kết quả từ backend: ${error.message}.`;
    }
});
