document.addEventListener("DOMContentLoaded", () => {
    const API_URL = "http://127.0.0.1:8000";

    const startBtn = document.getElementById("start-btn");
    const pauseBtn = document.getElementById("pause-btn");
    const resetBtn = document.getElementById("reset-btn");
    const checkBtn = document.getElementById("check-btn");

    const upstreamElement = document.getElementById("upstream-occ");
    const downstreamElement = document.getElementById("downstream-occ");
    const statusBox = document.getElementById("status-box");

    let records = [];
    let currentIndex = 0;
    let intervalId = null;
    let isPaused = false;
    let isLoading = false;
    let simulationRequestController = null;

    function setStatus(message, type = "") {
        if (!statusBox) return;

        statusBox.textContent = message;
        statusBox.className = "status-box";

        if (type) {
            statusBox.classList.add(type);
        }
    }

    function stopPlayback() {
        if (intervalId !== null) {
            clearInterval(intervalId);
            intervalId = null;
        }
    }

    function displayRecord(record) {
        if (upstreamElement) {
            upstreamElement.textContent = Number(record.occ_up).toFixed(1);
        }

        if (downstreamElement) {
            downstreamElement.textContent = Number(record.occ_down).toFixed(1);
        }

        if (record.detected) {
            setStatus(
                `Phát hiện sự cố giao thông tại chu kỳ ${currentIndex + 1}!`,
                "danger"
            );
        } else {
            setStatus(
                `Chu kỳ ${currentIndex + 1}: Giao thông bình thường.`,
                "success"
            );
        }
    }

    function playNextRecord() {
        if (currentIndex >= records.length) {
            stopPlayback();
            isPaused = false;

            setStatus("Đã phát hết dữ liệu mô phỏng.", "success");

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
            setStatus("Chưa có dữ liệu. Vui lòng chạy mô phỏng trước.", "warning");
            return;
        }

        if (currentIndex >= records.length) {
            setStatus("Đã phát hết dữ liệu. Nhấn Đặt Lại để chạy lại.", "warning");
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
            }, 1500);
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

        if (startBtn) startBtn.disabled = false;
        if (pauseBtn) pauseBtn.disabled = true;

        if (upstreamElement) upstreamElement.textContent = "--";
        if (downstreamElement) downstreamElement.textContent = "--";

        setStatus("Đã đặt lại mô phỏng.");

        if (checkBtn) checkBtn.disabled = false;
    }

    async function loadSimulation() {
        if (isLoading) return;

        isLoading = true;
        const requestController = new AbortController();
        simulationRequestController = requestController;

        if (startBtn) startBtn.disabled = true;
        if (checkBtn) checkBtn.disabled = true;

        setStatus("Đang lấy dữ liệu từ backend...");

        const requestBody = {
            scenario: "incident",
            parameters: {
                num_periods: 10,
                base_occ: 30,
                noise_std: 5,
                sample_interval: 1,
                seed: 42,
                incident_start: 3,
                incident_duration: 4,
                occ_up_peak: 50,
                occ_down_drop: 20,
                ramp_up_periods: 1,
                ramp_down_periods: 1
            },
            algorithm: {
                s1: 10,
                s2: 0.2,
                s3: 25,
                persistence: 1
            }
        };

        try {
            const response = await fetch(`${API_URL}/api/simulations`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(requestBody),
                signal: requestController.signal
            });

            if (!response.ok) {
                throw new Error(`Backend trả về HTTP ${response.status}`);
            }

            const data = await response.json();

            if (!Array.isArray(data.records) || data.records.length === 0) {
                throw new Error("Backend không trả về dữ liệu mô phỏng hợp lệ.");
            }

            records = data.records;
            currentIndex = 0;

            setStatus(
                `Đã tải ${records.length} chu kỳ dữ liệu. Nhấn Bắt Đầu để chạy.`,
                "success"
            );
        } catch (error) {
            if (requestController.signal.aborted) return;

            console.error("Lỗi tải dữ liệu mô phỏng:", error);

            setStatus(
                `Không thể kết nối backend: ${error.message}. Kiểm tra server tại ${API_URL}.`,
                "danger"
            );
        } finally {
            if (simulationRequestController === requestController) {
                simulationRequestController = null;
                isLoading = false;

                if (startBtn) startBtn.disabled = false;
                if (checkBtn) checkBtn.disabled = false;
            }
        }
    }

    // Nút Bắt Đầu: tải dữ liệu nếu chưa có, sau đó chạy mô phỏng.
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

    // Nút Tạm Dừng.
    if (pauseBtn) {
        pauseBtn.addEventListener("click", pausePlayback);
        pauseBtn.disabled = true;
    }

    // Nút Đặt Lại.
    if (resetBtn) {
        resetBtn.addEventListener("click", resetPlayback);
    }

    // Nút Kiểm Tra: kiểm tra kết nối backend.
    if (checkBtn) {
        checkBtn.addEventListener("click", async () => {
            if (isLoading) return;

            checkBtn.disabled = true;
            setStatus("Đang kiểm tra kết nối backend...");

            try {
                const response = await fetch(`${API_URL}/api/health`);

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                const data = await response.json();

                setStatus(
                    `Backend hoạt động bình thường: ${data.status}`,
                    "success"
                );
            } catch (error) {
                console.error("Lỗi kiểm tra backend:", error);

                setStatus(
                    `Không kết nối được backend. Hãy kiểm tra server tại ${API_URL}.`,
                    "danger"
                );
            } finally {
                checkBtn.disabled = false;
            }
        });
    }

    console.log("app.js đã tải thành công.");
});
