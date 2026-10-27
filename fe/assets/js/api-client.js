(() => {
    const apiHost = window.location.hostname || "127.0.0.1";
    const apiPorts = [8000, 8001];

    window.itsFetch = async (path, options) => {
        let lastError;

        for (const port of apiPorts) {
            try {
                return await fetch(`http://${apiHost}:${port}${path}`, options);
            } catch (error) {
                lastError = error;
            }
        }

        throw new Error(
            `Không kết nối được backend tại ${apiHost}:${apiPorts.join(" hoặc ")}. ${lastError.message}`
        );
    };
})();
