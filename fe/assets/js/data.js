const trafficMockData = {
    stations: [
        { id: "UP_01", name: "Trạm Thượng Lưu (Upstream)", baseOccupancy: 14.2 },
        { id: "DOWN_01", name: "Trạm Hạ Lưu (Downstream)", baseOccupancy: 8.5 }
    ],
    historicalIncidents: [
        { id: 1, time: "10:15 - 22/10/2026", location: "Km 12+400", status: "Đã xác nhận sự cố" },
        { id: 2, time: "11:30 - 22/10/2026", location: "Km 15+800", status: "Cảnh báo giả" },
        { id: 3, time: "13:45 - 22/10/2026", location: "Km 10+100", status: "Đã xác nhận sự cố" }
    ],
    metrics: {
        detectionRate: "92.5%",
        falseAlarmRate: "4.2%",
        meanTimeToDetect: "1.8 phút"
    }
};