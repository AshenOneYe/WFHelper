const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

const switchTab = (event, name) => {
  [...document.querySelectorAll(".tablinks")].forEach((item) => {
    if (item === event.currentTarget) {
      item.className = "tablinks active";
    } else {
      item.className = "tablinks";
    }
  });

  [...document.querySelectorAll(".tabcontent")].forEach((item) => {
    if (item.getAttribute("name") === name) {
      item.style.display = "block";
    } else {
      item.style.display = "none";
    }
  });

  if (name === "Summary") {
    loadSummary();
  }

  if (name === "Log") {
    loadLogArray();
  }

  if (name === "ScreenCap") {
    loadScreenCap();
  }
};

const loadSummary = () => {
  const format = (key, value) => {
    if (key === "startTime") {
      return `开始时间：${
        value ? new Date(value * 1000).toLocaleString() : ""
      }`;
    }

    if (key === "lastActionTime") {
      return `活跃时间：${
        value ? new Date(value * 1000).toLocaleString() : ""
      }`;
    }

    if (key === "isRunning") {
      return `当前状态：${eval(value) ? "启用" : "暂停"}`;
    }

    if (key === "currentTargets") {
      return `当前任务：${value}`;
    }

    if (key === "completeCount") {
      return `完成次数：${value}`;
    }

    if (key === "levelupCount") {
      return `升级次数：${value}`;
    }

    return `${key}:${value}`;
  };

  fetch(`/getSummary`)
    .then((res) => res.json())
    .then((res) => {
      document.querySelector('[name="Summary"]').innerHTML = `
              <ul class="list">${Object.entries(res)
                .map(([key, value]) => `<li>${format(key, value)}</li>`)
                .join("")}
              </ul>
            `;
    });
};

const loadLogArray = () => {
  fetch(`/getLogArray`)
    .then((res) => res.json())
    .then((res) => {
      document.querySelector('[name="Log"]').innerHTML = `
              <ul class="list">${res
                .map((item) => `<li>${item}</li>`)
                .reverse()
                .join("")}
              </ul>
            `;
    });
};

const loadScreenCap = () => {
  fetch(`/getScreenShot`)
    .then((res) => res.blob())
    .then((blob) => {
      const img = new Image();

      img.src = URL.createObjectURL(blob);
      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;

        ctx.drawImage(img, 0, 0);

        img.remove();
      };
    });
};

const start = () => {
  fetch(`/start`);
};

const stop = () => {
  fetch(`/stop`);
};

const autoFetchSummary = (() => {
  let interval;

  return (event) => {
    if (interval) {
      clearInterval(interval);

      interval = 0;

      event.currentTarget.innerHTML = "启用统计自动刷新";
    } else {
      const delay = Number(prompt("自动刷新间隔（秒）：", 60));

      if (delay > 0) {
        interval = setInterval(loadSummary, delay * 1000);

        event.currentTarget.innerHTML = "停止统计自动刷新";
      }
    }
  };
})();

const autoFetchLog = (() => {
  let interval;

  return (event) => {
    if (interval) {
      clearInterval(interval);

      interval = 0;

      event.currentTarget.innerHTML = "启用日志自动刷新";
    } else {
      const delay = Number(prompt("自动刷新间隔（秒）：", 60));

      if (delay > 0) {
        interval = setInterval(loadLogArray, delay * 1000);

        event.currentTarget.innerHTML = "停止日志自动刷新";
      }
    }
  };
})();

const setTaskCycle = (() => {
  let timeout;
  let isRunning = false;

  const run = (duration, interval) => {
    if (isRunning === false) {
      isRunning = true;

      timeout = setTimeout(() => run(duration, interval), duration);

      start();
    } else {
      isRunning = false;

      timeout = setTimeout(() => run(duration, interval), interval);

      stop();
    }
  };

  return (event) => {
    if (timeout) {
      clearTimeout(timeout);

      timeout = 0;
      isRunning = false;

      event.currentTarget.innerHTML = "设置任务周期";
    } else {
      const input = prompt("每运行x分钟休息y分钟（x,y）：", "180,120") || "";
      const matched = input.match(/^(\d+),(\d+)$/);

      if (matched) {
        const duration = Number(matched[1]);
        const interval = Number(matched[2]);

        if (duration && interval) {
          run(duration * 60 * 1000, interval * 60 * 1000);

          event.currentTarget.innerHTML = `当前任务周期：每运行 ${duration} 分钟休息 ${interval} 分钟`;
        }
      }
    }
  };
})();

const setLogLimit = () => {
  const value = Number(prompt("日志长度", 20));

  if (value > 0) {
    fetch(`/setLogLimit?value=${value}`);
  }
};

const touchScreen = (() => {
  const delay = 5000;

  return (e) => {
    if (canvas.style.cursor !== "not-allowed") {
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      fetch(`/touchScreen?x=${x}&y=${y}`)
        .then(() => {
          canvas.style.cursor = "not-allowed";

          ctx.globalCompositeOperation = "destination-out";
          ctx.fillStyle = "rgba(255, 255, 255, 0.5)";
          ctx.beginPath();
          ctx.fillRect(0, 0, canvas.width, canvas.height);
          ctx.fill();
          ctx.globalCompositeOperation = "source-over";
        })
        .then(() => new Promise((resolve) => setTimeout(resolve, delay)))
        .then(() => {
          canvas.style.cursor = "auto";
        })
        .then(loadScreenCap);
    }
  };
})();

canvas.addEventListener("mousedown", touchScreen);

document.querySelector(".tablinks").click();
