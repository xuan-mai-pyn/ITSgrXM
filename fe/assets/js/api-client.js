(() => {
    window.itsFetch = async (path, options) => {
        // 1. Nếu trang web đang chạy cùng server HTTP (ví dụ http://127.0.0.1:8000), gọi trực tiếp đường dẫn tương đối
        if (window.location.protocol.startsWith("http")) {
            try {
                return await fetch(path, options);
            } catch (ignored) {
                // Fallback xuống dưới nếu gọi tương đối không được
            }
        }

        // 2. Thử các cổng khả dụng
        const apiHost = window.location.hostname || "127.0.0.1";
        const apiPorts = [8000, 8001];
        let lastError = null;

        for (const port of apiPorts) {
            try {
                return await fetch("http://" + apiHost + ":" + port + path, options);
            } catch (error) {
                lastError = error;
            }
        }

        throw new Error(
            "Không kết nối được backend tại " + apiHost + ":" + apiPorts.join(" hoặc ") + (lastError ? ". " + lastError.message : "")
        );
    };
})();
