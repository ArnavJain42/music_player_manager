document.addEventListener("DOMContentLoaded", () => {
  const rows = 9;
  const columns = 9;
  const total = rows * columns;
  const baseAngle = 0;

  const container = document.createElement("div");
  container.className = "magnet-background";

  for (let i = 0; i < total; i++) {
    const span = document.createElement("span");
    span.style.setProperty("--rotate", `${baseAngle}deg`);
    container.appendChild(span);
  }

  document.body.appendChild(container);

  const items = container.querySelectorAll("span");

  const onPointerMove = (pointer) => {
    items.forEach((item) => {
      const rect = item.getBoundingClientRect();
      const centerX = rect.x + rect.width / 2;
      const centerY = rect.y + rect.height / 2;

      const b = pointer.x - centerX;
      const a = pointer.y - centerY;
      const c = Math.sqrt(a * a + b * b) || 1;
      const r = (Math.acos(b / c) * 180) / Math.PI * (pointer.y > centerY ? 1 : -1);

      item.style.setProperty("--rotate", `${r}deg`);
    });
  };

  window.addEventListener("pointermove", onPointerMove);
});
