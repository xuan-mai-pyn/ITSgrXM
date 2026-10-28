document.addEventListener("DOMContentLoaded", () => {
    console.log("app.js v2.1 loaded: Bắt đầu khởi tạo hệ thống mô phỏng California #1...");

    const startBtn = document.getElementById("start-btn");
    const pauseBtn = document.getElementById("pause-btn");
    const resetBtn = document.getElementById("reset-btn");
    const checkBtn = document.getElementById("check-btn");
    const scenarioSelect = document.getElementById("scenario-select");

    const upstreamElement = document.getElementById("upstream-occ");
    const downstreamElement = document.getElementById("downstream-occ");
    const currentCycleElement = document.getElementById("current-cycle");
    const totalCyclesElement = document.getElementById("total-cycles");
    const statusBox = document.getElementById("status-box");

    // Bảng soi 3 bước kiểm tra
    const calcDiffVal = document.getElementById("calc-diff-val");
    const calcDiffVerdict = document.getElementById("calc-diff-verdict");
    const calcRdfVal = document.getElementById("calc-rdf-val");
    const calcRdfVerdict = document.getElementById("calc-rdf-verdict");
    const calcDocdVal = document.getElementById("calc-docd-val");
    const calcDocdVerdict = document.getElementById("calc-docd-verdict");
    const fsmStateVal = document.getElementById("fsm-state-val");
    const fsmStateDesc = document.getElementById("fsm-state-desc");

    // Canvas biểu đồ
    const chartCanvas = document.getElementById("occ-chart-canvas");

    // Ngưỡng chuẩn theo Slide 43 của Thầy Lê Văn Quốc Anh
    const T1 = 20.0, T2 = 0.25, T3 = 0.50;

    let records = [];
    let currentIndex = 0;
    let intervalId = null;
    let isPaused = false;
    let isLoading = false;
    let simulationRequestController = null;

    // Dữ liệu biểu đồ tích lũy
    let chartUpData = [];
    let chartDownData = [];
    let chartIncidentZones = [];

    // FSM State máy trạng thái
    let fsmState = "NORMAL";

    function setStatus(message, type) {
        if (!statusBox) return;
        statusBox.textContent = message;
        statusBox.className = "status-box";
        if (type) statusBox.classList.add(type);
    }

    function stopPlayback() {
        if (intervalId !== null) {
            clearInterval(intervalId);
            intervalId = null;
        }
    }

    // ===== VẼ BIỂU ĐỒ CANVAS THỜI GIAN THỰC =====
    function drawChart() {
        if (!chartCanvas) return;
        const container = chartCanvas.parentElement;
        if (!container) return;

        const W = container.clientWidth || 800;
        const H = container.clientHeight || 240;

        // Cập nhật kích thước canvas theo thực tế
        if (chartCanvas.width !== W || chartCanvas.height !== H) {
            chartCanvas.width = W;
            chartCanvas.height = H;
        }

        const ctx = chartCanvas.getContext("2d");
        ctx.clearRect(0, 0, W, H);

        const padLeft = 45, padRight = 20, padTop = 20, padBottom = 28;
        const plotW = Math.max(10, W - padLeft - padRight);
        const plotH = Math.max(10, H - padTop - padBottom);

        const totalPts = (records && records.length > 0) ? records.length : 60;
        const maxOcc = 100;
        const stepX = plotW / Math.max(totalPts - 1, 1);
        const scaleY = plotH / maxOcc;

        // 1. Gridlines ngang + nhãn trục Y
        ctx.strokeStyle = "#e2e8f0";
        ctx.lineWidth = 1;
        ctx.fillStyle = "#94a3b8";
        ctx.font = "11px Arial, sans-serif";
        ctx.textAlign = "right";

        for (let v = 0; v <= 100; v += 20) {
            const y = padTop + plotH - v * scaleY;
            ctx.beginPath();
            ctx.moveTo(padLeft, y);
            ctx.lineTo(padLeft + plotW, y);
            ctx.stroke();
            ctx.fillText(v + "%", padLeft - 6, y + 4);
        }

        // 2. Nếu chưa có dữ liệu nào, vẽ dòng chữ gợi ý ở giữa
        if (chartUpData.length === 0) {
            ctx.fillStyle = "#94a3b8";
            ctx.font = "italic 13px Arial, sans-serif";
            ctx.textAlign = "center";
            ctx.fillText("Nhấn nút [Bắt Đầu] để bắt đầu vẽ luồng dữ liệu thời gian thực...", W / 2, H / 2);

            // Vẽ trục X mờ
            for (let i = 0; i < totalPts; i += 10) {
                const x = padLeft + i * stepX;
                ctx.fillText(String(i + 1), x, H - 6);
            }
            return;
        }

        // 3. Vùng sự cố thực tế (highlight đỏ nhạt)
        if (chartIncidentZones.length > 0) {
            ctx.fillStyle = "rgba(254, 202, 202, 0.4)";
            let inZone = false;
            let zoneStartX = 0;
            for (let i = 0; i < chartIncidentZones.length; i++) {
                const x = padLeft + i * stepX;
                if (chartIncidentZones[i] && !inZone) {
                    zoneStartX = x;
                    inZone = true;
                } else if (!chartIncidentZones[i] && inZone) {
                    ctx.fillRect(zoneStartX, padTop, x - zoneStartX, plotH);
                    inZone = false;
                }
            }
            if (inZone) {
                const lastX = padLeft + (chartIncidentZones.length - 1) * stepX;
                ctx.fillRect(zoneStartX, padTop, Math.max(lastX - zoneStartX + stepX, 4), plotH);
            }
        }

        // 4. Vẽ đường Upstream (xanh dương #2563eb)
        if (chartUpData.length > 0) {
            ctx.beginPath();
            ctx.strokeStyle = "#2563eb";
            ctx.lineWidth = 2.5;
            ctx.lineJoin = "round";
            for (let i = 0; i < chartUpData.length; i++) {
                const x = padLeft + i * stepX;
                const y = padTop + plotH - chartUpData[i] * scaleY;
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.stroke();
        }

        // 5. Vẽ đường Downstream (xanh lá #16a34a)
        if (chartDownData.length > 0) {
            ctx.beginPath();
            ctx.strokeStyle = "#16a34a";
            ctx.lineWidth = 2.5;
            ctx.lineJoin = "round";
            for (let i = 0; i < chartDownData.length; i++) {
                const x = padLeft + i * stepX;
                const y = padTop + plotH - chartDownData[i] * scaleY;
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.stroke();
        }

        // 6. Nhãn trục X (số chu kỳ)
        ctx.fillStyle = "#94a3b8";
        ctx.font = "11px Arial, sans-serif";
        ctx.textAlign = "center";
        const xLabelStep = Math.max(1, Math.floor(totalPts / 10));
        for (let i = 0; i < totalPts; i += xLabelStep) {
            const x = padLeft + i * stepX;
            ctx.fillText(String(i + 1), x, H - 6);
        }

        // 7. Chấm tròn định vị chu kỳ hiện tại
        if (chartUpData.length > 0) {
            const lastIdx = chartUpData.length - 1;
            const cx = padLeft + lastIdx * stepX;

            // Chấm tròn Upstream
            const cyUp = padTop + plotH - chartUpData[lastIdx] * scaleY;
            ctx.beginPath();
            ctx.arc(cx, cyUp, 5, 0, Math.PI * 2);
            ctx.fillStyle = "#2563eb";
            ctx.fill();
            ctx.strokeStyle = "#ffffff";
            ctx.lineWidth = 1.5;
            ctx.stroke();

            // Chấm tròn Downstream
            const cyDown = padTop + plotH - chartDownData[lastIdx] * scaleY;
            ctx.beginPath();
            ctx.arc(cx, cyDown, 5, 0, Math.PI * 2);
            ctx.fillStyle = "#16a34a";
            ctx.fill();
            ctx.strokeStyle = "#ffffff";
            ctx.lineWidth = 1.5;
            ctx.stroke();
        }
    }

    // ===== BẢNG SOI 3 BƯỚC + MÁY TRẠNG THÁI (FSM) =====
    function updateCalcTable(occUp, occDown) {
        const diff = occUp - occDown;
        const ratioUp = occUp > 0 ? diff / occUp : 0;
        const ratioDown = occDown > 0 ? diff / occDown : 0;

        const cond1 = diff > T1;
        const cond2 = ratioUp > T2;
        const cond3 = ratioDown > T3;

        // Cập nhật Bước 1
        if (calcDiffVal) calcDiffVal.textContent = diff.toFixed(1) + "%";
        if (calcDiffVerdict) {
            calcDiffVerdict.textContent = cond1 ? "VƯỢT NGƯỠNG (> 20)" : "DƯỚI NGƯỠNG";
            calcDiffVerdict.className = "calc-verdict " + (cond1 ? "verdict-fail" : "verdict-pass");
        }

        // Cập nhật Bước 2
        if (calcRdfVal) calcRdfVal.textContent = ratioUp.toFixed(3);
        if (calcRdfVerdict) {
            calcRdfVerdict.textContent = cond2 ? "VƯỢT NGƯỠNG (> 0.25)" : "DƯỚI NGƯỠNG";
            calcRdfVerdict.className = "calc-verdict " + (cond2 ? "verdict-fail" : "verdict-pass");
        }

        // Cập nhật Bước 3
        if (calcDocdVal) calcDocdVal.textContent = ratioDown.toFixed(3);
        if (calcDocdVerdict) {
            calcDocdVerdict.textContent = cond3 ? "VƯỢT NGƯỠNG (> 0.50)" : "DƯỚI NGƯỠNG";
            calcDocdVerdict.className = "calc-verdict " + (cond3 ? "verdict-fail" : "verdict-pass");
        }

        // Cập nhật Máy Trạng Thái FSM chuẩn Slide 42
        if (fsmState === "NORMAL") {
            if (cond1 && cond2 && cond3) {
                fsmState = "TENTATIVE";
            }
        } else if (fsmState === "TENTATIVE") {
            if (cond2 && cond3) {
                fsmState = "INCIDENT";
            } else {
                fsmState = "NORMAL";
            }
        } else if (fsmState === "INCIDENT") {
            // Chú ý 1: Kết thúc nếu T2 không còn vượt nữa
            if (!cond2) {
                fsmState = "NORMAL";
            }
        }

        if (fsmStateVal) {
            fsmStateVal.textContent = fsmState;
            fsmStateVal.className = "fsm-state";
            if (fsmState === "NORMAL") {
                fsmStateVal.classList.add("state-normal");
                if (fsmStateDesc) fsmStateDesc.textContent = "Giao thông bình thường. Không có dấu hiệu sự cố.";
            } else if (fsmState === "TENTATIVE") {
                fsmStateVal.classList.add("state-tentative");
                if (fsmStateDesc) fsmStateDesc.textContent = "Nghi ngờ sự cố! Cả 3 bước đạt. Chờ chu kỳ kế tiếp xác nhận...";
            } else if (fsmState === "INCIDENT") {
                fsmStateVal.classList.add("state-incident");
                if (fsmStateDesc) fsmStateDesc.textContent = "XÁC NHẬN SỰ CỐ! T₂ và T₃ tiếp tục vượt ngưỡng ở chu kỳ liên tiếp.";
            }
        }
    }

    // Hiển thị một chu kỳ dữ liệu
    function displayRecord(record) {
        const occUp = Number(record.occ_up);
        const occDown = Number(record.occ_down);

        if (upstreamElement) upstreamElement.textContent = occUp.toFixed(1) + "%";
        if (downstreamElement) downstreamElement.textContent = occDown.toFixed(1) + "%";
        if (currentCycleElement) currentCycleElement.textContent = String(currentIndex + 1);

        // 1. Cập nhật biểu đồ
        chartUpData.push(occUp);
        chartDownData.push(occDown);
        chartIncidentZones.push(record.actual_incident || false);
        drawChart();

        // 2. Cập nhật bảng soi 3 bước
        updateCalcTable(occUp, occDown);

        // 3. Cập nhật Status Box
        if (record.detected || fsmState === "INCIDENT") {
            setStatus(
                "🚨 PHÁT HIỆN SỰ CỐ TẠI CHU KỲ " + (currentIndex + 1) + "! " +
                "(OCC Thượng lưu: " + occUp.toFixed(1) + "%, Hạ lưu: " + occDown.toFixed(1) + "%)",
                "danger"
            );
        } else if (fsmState === "TENTATIVE") {
            setStatus(
                "⚠️ Chu kỳ " + (currentIndex + 1) + ": Nghi ngờ sự cố (Tentative) — đang chờ chu kỳ tiếp theo xác nhận...",
                "tentative"
            );
        } else {
            setStatus(
                "✅ Chu kỳ " + (currentIndex + 1) + ": Giao thông bình thường.",
                "success"
            );
        }
    }

    function playNextRecord() {
        if (currentIndex >= records.length) {
            stopPlayback();
            isPaused = false;
            setStatus("Đã hoàn thành toàn bộ " + records.length + " chu kỳ mô phỏng.", "success");
            if (startBtn) startBtn.disabled = false;
            if (pauseBtn) pauseBtn.disabled = true;
            return;
        }

        const record = records[currentIndex];
        displayRecord(record);
        currentIndex++;
    }

    function startPlayback() {
        if (records.length === 0) {
            setStatus("Chưa có dữ liệu. Vui lòng bấm Bắt Đầu để tải mô phỏng.", "warning");
            return;
        }

        if (currentIndex >= records.length) {
            setStatus("Đã phát hết dữ liệu. Nhấn Đặt Lại để chạy lại từ đầu.", "warning");
            return;
        }

        if (intervalId !== null) return;

        isPaused = false;
        if (startBtn) startBtn.disabled = true;
        if (pauseBtn) pauseBtn.disabled = false;

        playNextRecord();

        if (currentIndex < records.length) {
            intervalId = setInterval(() => {
                playNextRecord();
            }, 700); // 700ms mỗi chu kỳ
        }
    }

    function pausePlayback() {
        stopPlayback();
        isPaused = true;
        if (startBtn) startBtn.disabled = false;
        if (pauseBtn) pauseBtn.disabled = true;
        setStatus("Mô phỏng đã tạm dừng.", "warning");
    }

    function resetPlayback() {
        stopPlayback();

        if (simulationRequestController !== null) {
            simulationRequestController.abort();
            simulationRequestController = null;
        }

        records = [];
        currentIndex = 0;
        isPaused = false;
        isLoading = false;
        fsmState = "NORMAL";
        chartUpData = [];
        chartDownData = [];
        chartIncidentZones = [];

        if (startBtn) startBtn.disabled = false;
        if (pauseBtn) pauseBtn.disabled = true;
        if (upstreamElement) upstreamElement.textContent = "20.0%";
        if (downstreamElement) downstreamElement.textContent = "20.0%";
        if (currentCycleElement) currentCycleElement.textContent = "0";
        if (totalCyclesElement) totalCyclesElement.textContent = "60";

        // Reset bảng soi
        if (calcDiffVal) calcDiffVal.textContent = "0.0%";
        if (calcDiffVerdict) { calcDiffVerdict.textContent = "Chờ chạy..."; calcDiffVerdict.className = "calc-verdict verdict-idle"; }
        if (calcRdfVal) calcRdfVal.textContent = "0.000";
        if (calcRdfVerdict) { calcRdfVerdict.textContent = "Chờ chạy..."; calcRdfVerdict.className = "calc-verdict verdict-idle"; }
        if (calcDocdVal) calcDocdVal.textContent = "0.000";
        if (calcDocdVerdict) { calcDocdVerdict.textContent = "Chờ chạy..."; calcDocdVerdict.className = "calc-verdict verdict-idle"; }
        if (fsmStateVal) { fsmStateVal.textContent = "NORMAL"; fsmStateVal.className = "fsm-state state-normal"; }
        if (fsmStateDesc) fsmStateDesc.textContent = "Giao thông bình thường. Đang chờ bắt đầu mô phỏng...";

        // Vẽ lại khung biểu đồ trống
        drawChart();

        setStatus("Đã đặt lại mô phỏng. Chọn kịch bản rồi nhấn Bắt Đầu.");
        if (checkBtn) checkBtn.disabled = false;
    }

    // Bộ sinh dữ liệu offline dự phòng (Chuẩn simulator.py của Cường)
    function generateFallbackRecords(scenario) {
        const numPeriods = 60;
        const res = [];
        let state = "NORMAL";

        for (let t = 0; t < numPeriods; t++) {
            let occUp = 20.0 + (Math.sin(t * 0.5) * 1.5) + (Math.random() * 2 - 1);
            let occDown = 20.0 + (Math.cos(t * 0.5) * 1.5) + (Math.random() * 2 - 1);
            let actualIncident = false;

            if (scenario === "incident") {
                // Sự cố từ chu kỳ 20 đến 40
                if (t >= 20 && t < 40) {
                    actualIncident = true;
                    // Ramping up
                    const progress = Math.min((t - 20) / 3, 1.0);
                    occUp = 20.0 + (55.0 - 20.0) * progress + (Math.random() * 2 - 1);
                    occDown = 20.0 - (20.0 - 8.0) * progress + (Math.random() * 2 - 1);
                } else if (t >= 40 && t < 45) {
                    // Dọn dẹp sự cố
                    const recover = (45 - t) / 5;
                    occUp = 20.0 + (55.0 - 20.0) * recover * 0.6;
                    occDown = 20.0 - (20.0 - 8.0) * recover * 0.6;
                }
            } else if (scenario === "edge_congestion") {
                // Ùn tắc giờ cao điểm từ 15 đến 35
                if (t >= 15 && t < 35) {
                    occUp = 45.0 + (Math.random() * 3 - 1.5);
                    occDown = 44.0 + (Math.random() * 3 - 1.5);
                }
            }

            occUp = Math.max(1, Math.min(99, occUp));
            occDown = Math.max(1, Math.min(99, occDown));

            // Chạy thuật toán California #1
            const diff = occUp - occDown;
            const rUp = diff / occUp;
            const rDown = diff / occDown;
            const c1 = diff > T1;
            const c2 = rUp > T2;
            const c3 = rDown > T3;

            let detected = false;
            if (state === "NORMAL") {
                if (c1 && c2 && c3) state = "TENTATIVE";
            } else if (state === "TENTATIVE") {
                if (c2 && c3) { state = "INCIDENT"; detected = true; }
                else state = "NORMAL";
            } else if (state === "INCIDENT") {
                if (c2) detected = true;
                else state = "NORMAL";
            }

            res.push({
                timestamp: t + 1,
                occ_up: occUp,
                occ_down: occDown,
                actual_incident: actualIncident,
                detected: detected
            });
        }
        return res;
    }

    async function loadSimulation() {
        if (isLoading) return;

        isLoading = true;
        const requestController = new AbortController();
        simulationRequestController = requestController;

        if (startBtn) startBtn.disabled = true;
        if (checkBtn) checkBtn.disabled = true;

        const selectedScenario = scenarioSelect ? scenarioSelect.value : "incident";
        setStatus("Đang gửi yêu cầu mô phỏng [" + selectedScenario + "] đến backend...");

        let parameters = {
            num_periods: 60,
            base_occ: 20.0,
            noise_std: 2.0,
            sample_interval: 30
        };

        if (selectedScenario === "incident") {
            parameters.seed = 123;
            parameters.incident_start = 20;
            parameters.incident_duration = 20;
            parameters.occ_up_peak = 55.0;
            parameters.occ_down_drop = 8.0;
            parameters.ramp_up_periods = 3;
            parameters.ramp_down_periods = 5;
        } else if (selectedScenario === "normal") {
            parameters.seed = 42;
        } else if (selectedScenario === "edge_congestion") {
            parameters.seed = 456;
            parameters.congestion_start = 15;
            parameters.congestion_duration = 20;
            parameters.congestion_occ = 45.0;
        }

        const requestBody = {
            scenario: selectedScenario,
            parameters: parameters,
            algorithm: {
                s1: T1,
                s2: T2,
                s3: T3,
                persistence: 2
            }
        };

        try {
            console.log("Gửi request POST /api/simulations...");
            const response = await window.itsFetch("/api/simulations", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(requestBody),
                signal: requestController.signal
            });

            if (!response.ok) {
                throw new Error("Backend trả về HTTP " + response.status);
            }

            const data = await response.json();

            if (!Array.isArray(data.records) || data.records.length === 0) {
                throw new Error("Backend không trả về dữ liệu mô phỏng hợp lệ.");
            }

            records = data.records;
            setStatus(
                "Đã kết nối backend thành công! Tải xong " + records.length + " chu kỳ [" + data.scenario + "].",
                "success"
            );
        } catch (error) {
            if (requestController.signal && requestController.signal.aborted) return;
            console.warn("Backend chưa chạy hoặc không kết nối được. Kích hoạt bộ sinh mô phỏng offline:", error);

            // Tự động kích hoạt bộ sinh mô phỏng dự phòng để demo không bao giờ gián đoạn
            records = generateFallbackRecords(selectedScenario);
            setStatus(
                "⚡ Đang chạy mô phỏng trực tiếp trên trình duyệt (60 chu kỳ kịch bản [" + selectedScenario + "]).",
                "warning"
            );
        } finally {
            currentIndex = 0;
            fsmState = "NORMAL";
            chartUpData = [];
            chartDownData = [];
            chartIncidentZones = [];

            if (totalCyclesElement) totalCyclesElement.textContent = String(records.length);
            if (currentCycleElement) currentCycleElement.textContent = "0";

            if (simulationRequestController === requestController) {
                simulationRequestController = null;
                isLoading = false;
                if (startBtn) startBtn.disabled = false;
                if (checkBtn) checkBtn.disabled = false;
            }
        }
    }

    // === Gắn sự kiện ===
    if (scenarioSelect) {
        scenarioSelect.addEventListener("change", () => {
            resetPlayback();
        });
    }

    if (startBtn) {
        startBtn.addEventListener("click", async () => {
            if (isLoading) return;
            if (records.length === 0) {
                await loadSimulation();
            }
            if (records.length > 0) {
                startPlayback();
            }
        });
    }

    if (pauseBtn) {
        pauseBtn.addEventListener("click", pausePlayback);
        pauseBtn.disabled = true;
    }

    if (resetBtn) {
        resetBtn.addEventListener("click", resetPlayback);
    }

    if (checkBtn) {
        checkBtn.addEventListener("click", async () => {
            if (isLoading) return;
            checkBtn.disabled = true;
            setStatus("Đang kiểm tra kết nối backend tại http://127.0.0.1:8000...");
            try {
                const response = await window.itsFetch("/api/health");
                if (!response.ok) throw new Error("HTTP " + response.status);
                const data = await response.json();
                setStatus("✅ Backend hoạt động bình thường: " + data.status + " (" + data.service + ")", "success");
            } catch (error) {
                console.error("Lỗi kiểm tra backend:", error);
                setStatus("⚠️ Chưa bật server backend (uvicorn). Hãy chạy 'python -m uvicorn src.api:app --reload'.", "danger");
            } finally {
                checkBtn.disabled = false;
            }
        });
    }

    // Vẽ biểu đồ khởi động ngay khi load trang
    drawChart();

    // Tự động vẽ lại biểu đồ khi resize màn hình
    window.addEventListener("resize", () => {
        drawChart();
    });

    console.log("Khởi tạo mô phỏng hoàn tất. Sẵn sàng!");
});
