function renderSimpleChart(containerId, dataPoints) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = "";

    const svgNS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "180");
    svg.setAttribute("viewBox", "0 0 500 180");

    const polyline = document.createElementNS(svgNS, "polyline");
    let pointsString = "";

    const stepX = 500 / (dataPoints.length - 1 || 1);
    dataPoints.forEach((val, index) => {
        const x = index * stepX;
        const y = 160 - (val * 4);
        pointsString += `${x},${y} `;
    });

    polyline.setAttribute("points", pointsString);
    polyline.setAttribute("fill", "none");
    polyline.setAttribute("stroke", "#2563eb");
    polyline.setAttribute("stroke-width", "3");

    svg.appendChild(polyline);
    container.appendChild(svg);
}

document.addEventListener("DOMContentLoaded", () => {
    const sampleTrend = [10, 12, 15, 24, 20, 14, 11, 26, 29, 15];
    renderSimpleChart("occupancy-chart-container", sampleTrend);
});