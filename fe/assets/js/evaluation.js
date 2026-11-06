document.addEventListener("DOMContentLoaded", async () => {
    const scenarioSelect = document.getElementById("eval-scenario-select");
    const btnRunEval = document.getElementById("btn-run-eval");
    const statusMsg = document.getElementById("eval-status-msg");

    const drValEl = document.getElementById("card-dr-val");
    const farValEl = document.getElementById("card-far-val");
    const ttdValEl = document.getElementById("card-ttd-val");
    const piValEl = document.getElementById("card-pi-val");

    const statIncidentsEl = document.getElementById("stat-incidents");
    const statTpEl = document.getElementById("stat-tp");
    const statFnEl = document.getElementById("stat-fn");
    const statFpEl = document.getElementById("stat-fp");
    const statRepeatedEl = document.getElementById("stat-repeated");

    function renderEvaluation(evalData, scenarioName) {
        if (!evalData) {
            statusMsg.textContent = "Chưa có dữ liệu đánh giá.";
            return;
        }

        // 1. Detection Rate (DR)
        let drPercent = null;
        if (evalData.dr !== null && evalData.dr !== undefined) {
            drPercent = evalData.dr * 100;
            drValEl.textContent = drPercent.toFixed(1) + "%";
        } else {
            drValEl.textContent = "N/A";
        }

        // 2. False Alarm Rate (FAR)
        let farPercent = 0.0;
        if (evalData.far !== null && evalData.far !== undefined) {
            farPercent = evalData.far * 100;
            farValEl.textContent = farPercent.toFixed(2) + "%";
        } else {
            farValEl.textContent = "0.00%";
        }

        // 3. Mean Time To Detect (MTTD / TTD)
        if (evalData.ttd !== null && evalData.ttd !== undefined) {
            ttdValEl.textContent = evalData.ttd.toFixed(1) + " chu kỳ";
        } else {
            ttdValEl.textContent = "N/A";
        }

        // 4. Performance Index (PI): PI = [(100 - DR)/100]^m * FAR^n * MTTD^p (m=1, n=1, p=1)
        if (drPercent !== null && evalData.ttd !== null && evalData.ttd !== undefined) {
            const pi = ((100 - drPercent) / 100) * farPercent * evalData.ttd;
            piValEl.textContent = pi.toFixed(4);
        } else if (farPercent === 0) {
            piValEl.textContent = "0.0000";
        } else {
            piValEl.textContent = "N/A";
        }

        // 5. Thống kê biến cố
        statIncidentsEl.textContent = evalData.n_incidents !== undefined ? evalData.n_incidents : 0;
        statTpEl.textContent = evalData.tp !== undefined ? evalData.tp : 0;
        statFnEl.textContent = evalData.fn !== undefined ? evalData.fn : 0;
        statFpEl.textContent = evalData.fp !== undefined ? evalData.fp : 0;
        statRepeatedEl.textContent = evalData.repeated_alarms !== undefined ? evalData.repeated_alarms : 0;

        const timeStr = new Date().toLocaleTimeString("vi-VN");
        statusMsg.innerHTML = '<span style="color: #16a34a; font-weight: 600;">Hoàn tất đánh giá</span> lúc ' + timeStr + ' (Kịch bản: <strong>' + scenarioName + '</strong>)';
    }

    async function executeEvaluation(scenario) {
        btnRunEval.disabled = true;
        btnRunEval.textContent = "Đang đánh giá...";
        statusMsg.textContent = "Đang gửi dữ liệu mô phỏng và tính toán chỉ số...";

        try {
            const response = await window.itsFetch("/api/simulations", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ scenario: scenario })
            });

            if (!response.ok) {
                throw new Error("Lỗi HTTP " + response.status);
            }

            const data = await response.json();
            const scenarioLabels = {
                "incident": "Sự cố giao thông",
                "normal": "Giao thông bình thường",
                "edge_congestion": "Ùn tắc tự nhiên"
            };
            const label = scenarioLabels[scenario] || scenario;
            renderEvaluation(data.evaluation, label);
        } catch (err) {
            console.error("Lỗi khi đánh giá:", err);
            statusMsg.innerHTML = '<span style="color: #dc2626; font-weight: 600;">Không thể đánh giá:</span> ' + err.message;
        } finally {
            btnRunEval.disabled = false;
            btnRunEval.textContent = "▶ Đánh Giá Nhanh";
        }
    }

    btnRunEval.addEventListener("click", () => {
        executeEvaluation(scenarioSelect.value);
    });

    // Khi vừa tải trang, kiểm tra dashboard trước, nếu chưa có thì chạy mẫu kịch bản 'incident'
    try {
        const dashRes = await window.itsFetch("/api/dashboard");
        if (dashRes.ok) {
            const dashData = await dashRes.json();
            const evaluation = dashData.latest_evaluation
                || (dashData.latest_simulation && dashData.latest_simulation.evaluation);
            if (evaluation) {
                const scen = (dashData.latest_simulation && dashData.latest_simulation.scenario) || "incident";
                const scenarioLabels = {
                    "incident": "Sự cố giao thông",
                    "normal": "Giao thông bình thường",
                    "edge_congestion": "Ùn tắc tự nhiên"
                };
                renderEvaluation(evaluation, scenarioLabels[scen] || scen);
                return;
            }
        }
    } catch (e) {
        // bỏ qua lỗi kiểm tra ban đầu
    }

    // Mặc định chạy đánh giá kịch bản incident
    executeEvaluation("incident");
});
