(function () {
  "use strict";

  const SVG_NS = "http://www.w3.org/2000/svg";

  function makeSvgElement(name, attributes, text) {
    const element = document.createElementNS(SVG_NS, name);
    Object.keys(attributes || {}).forEach(function (key) {
      element.setAttribute(key, attributes[key]);
    });
    if (text !== undefined) element.textContent = text;
    return element;
  }

  function renderLineChart(container, data) {
    if (!container || !Array.isArray(data) || data.length === 0) return;
    const width = 640;
    const height = 220;
    const margin = { top: 14, right: 16, bottom: 28, left: 35 };
    const plotWidth = width - margin.left - margin.right;
    const plotHeight = height - margin.top - margin.bottom;
    const maxValue = 100;
    const svg = makeSvgElement("svg", {
      viewBox: "0 0 " + width + " " + height,
      role: "img",
      "aria-label": "Biểu đồ occupancy mẫu của trạm A và trạm B"
    });

    [0, 25, 50, 75, 100].forEach(function (tick) {
      const y = margin.top + plotHeight - (tick / maxValue) * plotHeight;
      svg.appendChild(makeSvgElement("line", {
        x1: margin.left, y1: y, x2: width - margin.right, y2: y, class: "chart-gridline"
      }));
      svg.appendChild(makeSvgElement("text", {
        x: margin.left - 9, y: y + 3, "text-anchor": "end", class: "chart-label"
      }, String(tick)));
    });

    function pointAt(index, value) {
      return {
        x: margin.left + (data.length === 1 ? plotWidth / 2 : (index / (data.length - 1)) * plotWidth),
        y: margin.top + plotHeight - (value / maxValue) * plotHeight
      };
    }

    ["A", "B"].forEach(function (station) {
      const points = data.map(function (sample, index) {
        const point = pointAt(index, sample[station]);
        return point.x + "," + point.y;
      }).join(" ");
      svg.appendChild(makeSvgElement("polyline", {
        points: points, class: station === "A" ? "chart-line-a" : "chart-line-b"
      }));
      data.forEach(function (sample, index) {
        const point = pointAt(index, sample[station]);
        svg.appendChild(makeSvgElement("circle", {
          cx: point.x, cy: point.y, r: 3.5, class: station === "A" ? "chart-dot-a" : "chart-dot-b"
        }));
      });
    });

    data.forEach(function (sample, index) {
      if (index % 2 === 0 || index === data.length - 1) {
        const point = pointAt(index, 0);
        svg.appendChild(makeSvgElement("text", {
          x: point.x, y: height - 6, "text-anchor": "middle", class: "chart-label"
        }, sample.time));
      }
    });
    container.replaceChildren(svg);
  }

  window.ITSgrXMCharts = Object.freeze({ renderLineChart: renderLineChart });
}());
