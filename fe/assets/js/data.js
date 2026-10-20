/* Frontend-only illustrative fixtures. These values are not supplied by the backend or an experiment. */
(function () {
  "use strict";

  const samples = [
    { time: "08:00", station: "A", occupancy: 12, incident: false },
    { time: "08:00", station: "B", occupancy: 9, incident: false },
    { time: "08:05", station: "A", occupancy: 14, incident: false },
    { time: "08:05", station: "B", occupancy: 11, incident: false },
    { time: "08:10", station: "A", occupancy: 18, incident: false },
    { time: "08:10", station: "B", occupancy: 13, incident: false },
    { time: "08:15", station: "A", occupancy: 42, incident: true },
    { time: "08:15", station: "B", occupancy: 15, incident: false },
    { time: "08:20", station: "A", occupancy: 57, incident: true },
    { time: "08:20", station: "B", occupancy: 17, incident: false },
    { time: "08:25", station: "A", occupancy: 36, incident: true },
    { time: "08:25", station: "B", occupancy: 19, incident: false },
    { time: "08:30", station: "A", occupancy: 21, incident: false },
    { time: "08:30", station: "B", occupancy: 16, incident: false },
    { time: "08:35", station: "A", occupancy: 16, incident: false },
    { time: "08:35", station: "B", occupancy: 12, incident: false }
  ];

  const simulation = [
    { time: "08:00", A: 12, B: 9, incidentA: false, incidentB: false },
    { time: "08:05", A: 14, B: 11, incidentA: false, incidentB: false },
    { time: "08:10", A: 18, B: 13, incidentA: false, incidentB: false },
    { time: "08:15", A: 42, B: 15, incidentA: true, incidentB: false },
    { time: "08:20", A: 57, B: 17, incidentA: true, incidentB: false },
    { time: "08:25", A: 36, B: 19, incidentA: true, incidentB: false },
    { time: "08:30", A: 21, B: 16, incidentA: false, incidentB: false },
    { time: "08:35", A: 16, B: 12, incidentA: false, incidentB: false }
  ];

  window.ITSgrXMData = Object.freeze({
    source: "frontend-static-sample",
    disclaimer: "Illustrative sample data only; not backend data or experimental results.",
    metrics: Object.freeze({
      detectionRate: { value: 0.92, display: "92%", label: "Minh họa" },
      falseAlarmRate: { value: 0.08, display: "8%", label: "Minh họa" },
      meanTimeToDetect: { value: 3.4, display: "3.4 phút", label: "Minh họa" }
    }),
    samples: Object.freeze(samples.map(function (sample) { return Object.freeze(sample); })),
    simulation: Object.freeze(simulation.map(function (sample) { return Object.freeze(sample); })),
    stations: Object.freeze([
      { id: "A", name: "Trạm A · Tuyến Bắc", status: "Đang giám sát (mẫu)" },
      { id: "B", name: "Trạm B · Tuyến Nam", status: "Đang giám sát (mẫu)" }
    ])
  });
}());
