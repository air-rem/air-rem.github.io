/* ============================================================
   AIRREM 领航 —— 推广位配置（唯一需要你/我改动的文件）
   ------------------------------------------------------------
   把每个机场的「推广链接」换成你的专属邀请/推广链接即可。
   改完重新发布（推送）就会全站生效，无需改动其它文件。
   - aff  : 你的推广/邀请注册链接（留空时按钮会退回到本站评测页）
   - code : 优惠码（留空则页面自动隐藏优惠码框）
   - 优惠码为搜集到的公开值，可能失效，请以机场官网为准。
   ============================================================ */
window.SITE = {
  aff: {
    mitce:      "",   // 例: https://mitce.com/#/register?code=你的邀请码
    westdata:   "",   // 例: https://westdata.xxx/#/register?code=你的邀请码
    candycloud: ""    // 例: https://tangguo.xxx/#/register?code=你的邀请码
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
    // 推广链接
    document.querySelectorAll("[data-aff]").forEach(function (el) {
      var key = el.getAttribute("data-aff");
      var url = (S.aff && S.aff[key]) ? S.aff[key].trim() : "";
      if (url) {
        el.setAttribute("href", url);
        el.setAttribute("target", "_blank");
        el.setAttribute("rel", "nofollow sponsored noopener");
        el.removeAttribute("data-pending");
      } else {
        // 未配置推广链接时，按钮退回到本站对应评测页，站点依然可用
        el.setAttribute("data-pending", "1");
        el.setAttribute("title", "推广链接待配置");
      }
    });
    // 优惠码
    document.querySelectorAll("[data-code]").forEach(function (el) {
      var key = el.getAttribute("data-code");
      var code = (S.code && S.code[key]) ? S.code[key].trim() : "";
      var box = el.closest("[data-codebox]");
      if (code) {
        el.textContent = code;
      } else if (box) {
        box.style.display = "none";
      }
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", apply);
  } else { apply(); }
})();
