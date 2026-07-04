/* ============================================================
   AIRREM 领航 —— 推广位配置（唯一需要改动的文件）
   aff  : 各机场官网推广跳转链接（slug 为键）
   code : 优惠码（留空则页面自动隐藏优惠码框）
   改完重新发布即可全站生效。
   ============================================================ */
window.SITE = {
  aff: {
    mitce:      "https://t.rtxk.us/t/ycfdvtk",   // Mitce 官网推广跳转
    westdata:   "https://t.rtxk.us/t/x2m8qpb",   // 西部数据 官网推广跳转
    candycloud: "https://t.rtxk.us/t/vubhdhq"    // 糖果云 官网推广跳转
  },
  code: {
    mitce:      "like20",     // Mitce 8折码（以官网为准）
    westdata:   "",           // 西部数据 常年折扣，无固定码
    candycloud: "Candytally"  // 糖果云 6折码（以官网为准）
  }
};

/* ---- 自动把配置写入页面按钮，无需改动 ---- */
(function () {
  function apply() {
    var S = window.SITE || { aff: {}, code: {} };
    document.querySelectorAll("[data-aff]").forEach(function (el) {
      var key = el.getAttribute("data-aff");
      var url = (S.aff && S.aff[key]) ? S.aff[key].trim() : "";
      if (url) {
        el.setAttribute("href", url);
        el.setAttribute("target", "_blank");
        el.setAttribute("rel", "nofollow sponsored noopener");
        el.removeAttribute("data-pending");
      } else {
        el.setAttribute("data-pending", "1");
        el.setAttribute("title", "推广链接待配置");
      }
    });
    document.querySelectorAll("[data-code]").forEach(function (el) {
      var key = el.getAttribute("data-code");
      var code = (S.code && S.code[key]) ? S.code[key].trim() : "";
      var box = el.closest("[data-codebox]");
      if (code) { el.textContent = code; }
      else if (box) { box.style.display = "none"; }
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", apply);
  else apply();
})();
