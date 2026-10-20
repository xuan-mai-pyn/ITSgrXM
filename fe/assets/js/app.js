(function () {
  "use strict";

  const data = window.ITSgrXMData;

  function setupNavigation() {
    const toggle = document.querySelector(".menu-toggle");
    const nav = document.querySelector(".site-nav");
    if (!toggle || !nav) return;
    toggle.addEventListener("click", function () {
      const isOpen = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!isOpen));
      toggle.setAttribute("aria-label", isOpen ? "Mở menu" : "Đóng menu");
      nav.classList.toggle("is-open", !isOpen);
    });
    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Mở menu");
      }
    });
  }

  function renderSharedData() {
    if (!data) {
      console.error("ITSgrXM frontend sample data is unavailable.");
      return;
    }
    document.querySelectorAll("[data-metric]").forEach(function (element) {
      const metric = data.metrics[element.dataset.metric];
      if (metric) element.textContent = metric.display;
    });
    const incidentCount = data.samples.filter(function (sample) { return sample.incident; }).length;
    document.querySelectorAll("[data-stat='incident-count']").forEach(function (element) {
      element.textContent = String(incidentCount);
    });

    const table = document.querySelector("[data-record-table]");
    if (table) {
      const rows = data.samples.slice(-6).reverse().map(function (sample) {
        const row = document.createElement("tr");
        [
          sample.time,
          "Trạm " + sample.station,
          sample.occupancy + "%",
          sample.incident ? "Có dấu hiệu sự cố" : "Bình thường",
          "Dữ liệu mẫu"
        ].forEach(function (value, index) {
          const cell = document.createElement("td");
          if (index === 3) {
            const tag = document.createElement("span");
            tag.className = "state-tag" + (sample.incident ? " alert" : "");
            tag.textContent = value;
            cell.appendChild(tag);
          } else {
            cell.textContent = value;
          }
          row.appendChild(cell);
        });
        return row;
      });
      table.replaceChildren.apply(table, rows);
    }

    const stationList = document.querySelector("[data-station-list]");
    if (stationList) {
      const rows = data.stations.map(function (station) {
        const latest = data.simulation[data.simulation.length - 1];
        const row = document.createElement("div");
        row.className = "station-row";
        const name = document.createElement("span");
        name.className = "station-name";
        const title = document.createElement("strong");
        title.textContent = station.name;
        const subtitle = document.createElement("small");
        subtitle.textContent = station.status;
        name.append(title, subtitle);
        const details = document.createElement("span");
        details.className = "station-name";
        const occupancy = document.createElement("strong");
        occupancy.className = "station-occupancy";
        occupancy.textContent = latest[station.id] + "%";
        const status = document.createElement("small");
        status.className = "station-status" + (latest["incident" + station.id] ? " alert" : "");
        status.textContent = latest["incident" + station.id] ? "Có dấu hiệu sự cố" : "Bình thường";
        details.append(occupancy, status);
        row.append(name, details);
        return row;
      });
      stationList.replaceChildren.apply(stationList, rows);
    }

    const dashboardChart = document.querySelector("[data-chart='dashboard']");
    if (dashboardChart && window.ITSgrXMCharts) window.ITSgrXMCharts.renderLineChart(dashboardChart, data.simulation);
  }

  function setupSimulation() {
    const startButton = document.querySelector("[data-simulation-start]");
    if (!startButton) return;
    const pauseButton = document.querySelector("[data-simulation-pause]");
    const resetButton = document.querySelector("[data-simulation-reset]");
    const status = document.querySelector("[data-simulation-status]");
    const chart = document.querySelector("[data-chart='simulation']");
    let currentIndex = 0;
    let timer = null;

    function showSample(index) {
      const sample = data.simulation[index];
      ["A", "B"].forEach(function (station) {
        const incident = sample["incident" + station];
        const state = document.querySelector("[data-station-state='" + station + "']");
        const occupancy = document.querySelector("[data-occupancy='" + station + "']");
        const meter = document.querySelector("[data-meter='" + station + "']");
        const time = document.querySelector("[data-station-time='" + station + "']");
        occupancy.replaceChildren(document.createTextNode(String(sample[station])));
        const unit = document.createElement("small");
        unit.textContent = "%";
        occupancy.appendChild(unit);
        state.textContent = incident ? "Có dấu hiệu sự cố" : "Bình thường";
        state.classList.toggle("alert", incident);
        meter.style.width = sample[station] + "%";
        meter.classList.toggle("alert", incident);
        time.textContent = sample.time + " · Mẫu " + String(index + 1).padStart(2, "0");
      });
      if (chart && window.ITSgrXMCharts) {
        window.ITSgrXMCharts.renderLineChart(chart, data.simulation.slice(0, index + 1));
      }
    }

    function stopSimulation() {
      if (timer !== null) {
        window.clearInterval(timer);
        timer = null;
      }
      startButton.disabled = false;
      pauseButton.disabled = true;
      status.innerHTML = '<span class="status-dot"></span> ĐANG TẠM DỪNG';
    }

    startButton.addEventListener("click", function () {
      if (timer !== null) return;
      if (currentIndex >= data.simulation.length - 1) currentIndex = 0;
      showSample(currentIndex);
      startButton.disabled = true;
      pauseButton.disabled = false;
      status.innerHTML = '<span class="status-dot"></span> ĐANG CHẠY MẪU';
      timer = window.setInterval(function () {
        if (currentIndex >= data.simulation.length - 1) {
          stopSimulation();
          return;
        }
        currentIndex += 1;
        showSample(currentIndex);
      }, 1100);
    });

    pauseButton.addEventListener("click", stopSimulation);
    resetButton.addEventListener("click", function () {
      stopSimulation();
      currentIndex = 0;
      showSample(currentIndex);
    });

    showSample(currentIndex);
  }

  document.addEventListener("DOMContentLoaded", function () {
    setupNavigation();
    renderSharedData();
    setupSimulation();
  });
}());
