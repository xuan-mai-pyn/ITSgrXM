document.addEventListener("DOMContentLoaded", async () => {
    const statusElement = document.getElementById("dashboard-status");
    const detectionCountElement = document.getElementById("dashboard-detection-count");
    const drElement = document.getElementById("dashboard-dr");
    const farElement = document.getElementById("dashboard-far");
    const ttdElement = document.getElementById("dashboard-ttd");

    const formatPercent = (value) =>
        value === null || value === undefined
            ? "Chưa có dữ liệu"
            : `${(value * 100).toFixed(1)}%`;
    const formatFar = (evaluation) => {
        if (evaluation.far === null || evaluation.far === undefined) {
            return "Chưa có dữ liệu";
        }

        if (evaluation.far_definition === "per_hour") {
            return `${evaluation.far.toFixed(2)} cảnh báo/giờ`;
        }

        return formatPercent(evaluation.far);
    };

    try {
        const response = await window.itsFetch("/api/dashboard");
        if (!response.ok) {
            throw new Error(`Backend trả về HTTP ${response.status}`);
        }

        const data = await response.json();
        if (!["available", "no_data"].includes(data.status)) {
            throw new Error("Backend trả về trạng thái dashboard không hợp lệ.");
        }

        const simulation = data.latest_simulation;
        const evaluation = data.latest_evaluation
            || (simulation && simulation.evaluation);

        detectionCountElement.textContent = simulation
            ? String(simulation.detection_count)
            : "Chưa có dữ liệu";
        drElement.textContent = evaluation
            ? formatPercent(evaluation.dr)
            : "Chưa có dữ liệu";
        farElement.textContent = evaluation
            ? formatFar(evaluation)
            : "Chưa có dữ liệu";
        ttdElement.textContent = evaluation
            && evaluation.ttd !== null
            && evaluation.ttd !== undefined
            ? `${evaluation.ttd.toFixed(2)} (đơn vị dữ liệu)`
            : "Chưa có dữ liệu";
        statusElement.textContent = data.status === "available"
            ? `Đang hiển thị kết quả backend${simulation ? ` — kịch bản ${simulation.scenario}` : ""}.`
            : data.message || "Backend chưa có kết quả mô phỏng hoặc đánh giá.";
    } catch (error) {
        console.error("Lỗi tải dữ liệu dashboard:", error);
        statusElement.textContent = `Không thể tải dữ liệu từ backend: ${error.message}.`;
    }
});
