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

  if (name === "State") {
    loadState();
  }

  if (name === "Log") {
    loadLogArray();
  }

  if (name === "ScreenCap") {
    loadScreenCap();
  }
};

const loadState = () => {
  const format = (key, value) => {
    if (key === "isDebug") {
      return `调试模式：${eval(value) ? "是" : "否"}`;
    }

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

    return `${key}：${value}`;
  };

  fetch(`/getState`)
    .then((res) => res.json())
    .then((res) => {
      document.querySelector('[name="State"]').innerHTML = `
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

const autoFetchState = (() => {
  let interval;

  return (event) => {
    if (interval) {
      clearInterval(interval);

      interval = 0;

      event.currentTarget.innerHTML = "启用统计自动刷新";
    } else {
      const delay = Number(prompt("自动刷新间隔（秒）：", 60));

      if (delay > 0) {
        interval = setInterval(loadState, delay * 1000);

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

const setLogLimit = () => {
  const value = Number(prompt("日志长度", 20));

  if (value > 0) {
    fetch(`/setLogLimit?value=${value}`);
  }
};

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

const setState = (key, value) => {
  fetch(
    `/setState?key=${encodeURIComponent(key)}&value=${encodeURIComponent(
      value
    )}`
  );
};

const toggleState = (event, key) => {
  event.currentTarget.innerHTML = event.currentTarget.innerHTML.replace(
    /[启禁]用/,
    (matched) => {
      const value = matched === "启用" ? "禁用" : "启用";

      setState(key, value);

      return value;
    }
  );
};

const touchScreen = (() => {
  const delay = 1000;

  return (x, y) => {
    if (canvas.style.cursor !== "not-allowed") {
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

const swipeScreen = (() => {
  const delay = 1000;

  return (x1, y1, x2, y2) => {
    if (canvas.style.cursor !== "not-allowed") {
      fetch(`/swipeScreen?x1=${x1}&y1=${y1}&x2=${x2}&y2=${y2}`)
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

const Mouse = {
  x: 0,
  y: 0,
  mousedown: (e) => {
    Mouse.x = e.clientX;
    Mouse.y = e.clientY;
  },
  mouseup: (e) => {
    if (Mouse.x & Mouse.y) {
      if (
        Math.abs(e.clientX - Mouse.x) > 10 ||
        Math.abs(e.clientY - Mouse.y) > 10
      ) {
        const rect = canvas.getBoundingClientRect();
        const x1 = Mouse.x - rect.left;
        const y1 = Mouse.y - rect.top;
        const x2 = e.clientX - rect.left;
        const y2 = e.clientY - rect.top;

        swipeScreen(x1, y1, x2, y2);
      } else {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        touchScreen(x, y);
      }
    }

    Mouse.x = 0;
    Mouse.y = 0;
  },
};

canvas.addEventListener("mousedown", Mouse.mousedown);
canvas.addEventListener("mouseup", Mouse.mouseup);
canvas.addEventListener("mouseleave", Mouse.mouseup);

document.querySelector(".tablinks").click();

(() => {
  [...document.querySelectorAll(".checkbox-group")].forEach((group) => {
    const name = group.getAttribute("name");
    const items = group.getAttribute("items").split("|");

    group.innerHTML = `
      <div class="title">${name}</div>
      ${items
        .map((item) => {
          return `
          <label>
          <span>${item}</span>
          <input type="checkbox" checked/>
          </label>
        `;
        })
        .join("")}
    `;

    const inputs = [...group.querySelectorAll("input")];

    inputs.forEach((input) => {
      input.addEventListener("change", () => {
        const value = inputs.reduce((accumulator, currentValue) => {
          return accumulator + (currentValue.checked ? "1" : "0");
        }, "0b");

        setState(name, value);
      });
    });
  });
})();
