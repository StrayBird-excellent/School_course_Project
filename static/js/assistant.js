(function () {
  "use strict";

  // 确保DOM完全加载后再执行
  function initAssistant() {
    var root = document.getElementById("bc-assistant");
    if (!root) {
      console.error("Root element not found");
      return;
    }

    var toggle = document.getElementById("bc-assistant-toggle");
    var panel = document.getElementById("bc-assistant-panel");
    var closeBtn = document.getElementById("bc-assistant-close");
    var messagesEl = document.getElementById("bc-assistant-messages");
    var form = document.getElementById("bc-assistant-form");
    var input = document.getElementById("bc-assistant-input");
    var sendBtn = document.getElementById("bc-assistant-send");
    var statusEl = document.getElementById("bc-assistant-status");
    var modelInfoEl = document.getElementById("bc-assistant-model-info");
    var ctxScript = document.getElementById("bc-assistant-context");

    var chatUrl = root.getAttribute("data-chat-url") || "/api/assistant/chat";
    var context = {};
    try {
      if (ctxScript && ctxScript.textContent) {
        context = JSON.parse(ctxScript.textContent);
      }
    } catch (e) {
      context = {};
    }

    var history = [];

    function escapeHtml(s) {
      var div = document.createElement("div");
      div.textContent = s;
      return div.innerHTML;
    }

    function appendBubble(role, text) {
      var wrap = document.createElement("div");
      wrap.className = "bc-assistant__msg bc-assistant__msg--" + role;
      var inner = document.createElement("div");
      inner.className = "bc-assistant__bubble";
      inner.innerHTML = escapeHtml(text).replace(/\n/g, "<br>");
      wrap.appendChild(inner);
      messagesEl.appendChild(wrap);
      // 自动滚动到底部
      messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    function setStatus(msg, isError) {
      statusEl.textContent = msg || "";
      statusEl.classList.toggle("bc-assistant__status--err", !!isError);
    }

    function setOpen(open) {
      if (!panel) {
        console.error("Panel element not found in setOpen");
        return;
      }
      
      if (open) {
        panel.hidden = false;
        panel.style.display = "flex";
        // 强制重新计算布局
        panel.style.visibility = 'hidden';
        panel.offsetHeight; // 触发重排
        panel.style.visibility = 'visible';
      } else {
        panel.hidden = true;
        panel.style.display = "none";
      }
      
      if (toggle) {
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
      }
      
      if (open && input) {
        input.focus();
      }
    }

    // Toggle按钮点击事件
    if (toggle) {
      toggle.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        var currentState = panel && !panel.hidden && panel.style.display !== 'none';
        setOpen(!currentState);
      });
    }

    // 关闭按钮点击事件
    if (closeBtn) {
      closeBtn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        setOpen(false);
      });
    }

    // ESC键关闭面板
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !panel.hidden) {
        setOpen(false);
      }
    });

    // 鼠标滚轮滚动功能 - 直接使用CSS的overflow-y属性，不添加额外事件监听
    // 确保滚动容器能够正常滚动
    console.log('滚动功能初始化完成');

    // 表单提交事件
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var text = (input.value || "").trim();
      if (!text) return;

      input.value = "";
      setStatus("");
      appendBubble("user", text);
      history.push({ role: "user", content: text });

      sendBtn.disabled = true;
      setStatus("正在请求AI…");

      fetch(chatUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: history,
          context: context,
        }),
      })
        .then(function (res) {
          return res.json().then(function (data) {
            return { ok: res.ok, status: res.status, data: data };
          });
        })
        .then(function (r) {
          if (!r.ok) {
            var detail = (r.data && (r.data.detail || r.data.error || r.data.hint)) || r.data || r.status;
            throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
          }
          var reply = r.data && r.data.reply;
          if (!reply) throw new Error("empty_reply");
          
          // 更新模型信息显示
          if (r.data.model && modelInfoEl) {
            modelInfoEl.textContent = r.data.model.display_name || "AI模型";
            console.log("当前使用模型:", r.data.model);
          }
          
          appendBubble("assistant", reply);
          history.push({ role: "assistant", content: reply });
          setStatus("");
          
          // 解析回复中的数据并填充到表单
          parseAndFillForm(reply);
        })
        .catch(function (err) {
          setStatus("请求失败：" + (err.message || String(err)), true);
        })
        .then(function () {
          sendBtn.disabled = false;
        });
    });

    // 解析千问助手回复并填充表单
    function parseAndFillForm(reply) {
      var fieldMap = {
        'radius mean': 'value1',
        'texture mean': 'value2',
        'perimeter mean': 'value3',
        'area mean': 'value4',
        'smoothness mean': 'value5',
        'compactness mean': 'value6',
        'concavity mean': 'value7',
        'concave points mean': 'value8',
        'symmetry mean': 'value9',
        'fractal dimension mean': 'value10',
        'radius se': 'value11',
        'texture se': 'value12',
        'perimeter se': 'value13',
        'area se': 'value14',
        'smoothness se': 'value15',
        'compactness se': 'value16',
        'concavity se': 'value17',
        'concave points se': 'value18',
        'symmetry se': 'value19',
        'fractal dimension se': 'value20',
        'radius worst': 'value21',
        'texture worst': 'value22',
        'perimeter worst': 'value23',
        'area worst': 'value24',
        'smoothness worst': 'value25',
        'compactness worst': 'value26',
        'concavity worst': 'value27',
        'concave points worst': 'value28',
        'symmetry worst': 'value29',
        'fractal dimension worst': 'value30'
      };
      
      var patterns = [
        /(radius|texture|perimeter|area|smoothness|compactness|concavity|concave points|symmetry|fractal dimension)\s*(mean|se|worst)?\s*[:：]\s*([\d.]+)/gi,
        /(radius|texture|perimeter|area|smoothness|compactness|concavity|concave[_\s]?points|symmetry|fractal[_\s]?dimension)[_\s]*(mean|se|worst)\s*[:：]\s*([\d.]+)/gi,
        /\d+\s*[.、]\s*(radius|texture|perimeter|area|smoothness|compactness|concavity|concave[_\s]?points|symmetry|fractal[_\s]?dimension)[_\s]*(mean|se|worst)\s*[:：]\s*([\d.]+)/gi
      ];
      
      patterns.forEach(function(pattern) {
        var match;
        while ((match = pattern.exec(reply)) !== null) {
          var feature = match[1].toLowerCase().replace(/_/g, ' ');
          var type = match[2] ? match[2].toLowerCase() : 'mean';
          var value = match[3];
          var fieldKey = feature + ' ' + type;
          
          fieldKey = fieldKey.replace(/\s+/g, ' ').trim();
          if (fieldKey.includes('concave') && fieldKey.includes('points')) {
            fieldKey = 'concave points ' + type;
          } else if (fieldKey.includes('fractal') && fieldKey.includes('dimension')) {
            fieldKey = 'fractal dimension ' + type;
          }
          
          var inputId = fieldMap[fieldKey];
          if (inputId) {
            var inputElement = document.getElementById(inputId);
            if (inputElement) {
              inputElement.value = value;
              console.log('填充字段:', fieldKey, '值:', value, '到输入框:', inputId);
            }
          }
        }
      });
    }

    // 初始化助手欢迎消息
    if (context.page === "home") {
      appendBubble(
        "assistant",
        "你好！本AI是专注于乳腺癌领域的信息咨询工具，并非专业医疗诊断模型，无法提供个人医疗诊断和治疗决策建议，具体健康问题请咨询专业医疗机构和医生。你可以问我：Wisconsin数据集各字段含义、乳腺癌筛查指南、治疗方案等相关问题。"
      );
    } else if (context.page === "result") {
      var pB = context.prob_benign != null ? (context.prob_benign * 100).toFixed(2) : "?";
      var pM = context.prob_malignant != null ? (context.prob_malignant * 100).toFixed(2) : "?";
      appendBubble(
        "assistant",
        "当前页面已带入本次随机森林预测结果：" +
          (context.prediction || "未知") +
          "。模型输出的概率约为：良性 " +
          pB +
          "%，恶性 " +
          pM +
          "%。本结果仅供教学演示，不能作为真实诊疗依据。你可以让我解释这些数字的含义，或咨询乳腺癌相关的医学信息。"
      );
    } else {
      appendBubble("assistant", "你好！本AI专注于乳腺癌领域的医学咨询。请提出与乳腺癌相关的问题，我将尽力为您提供专业信息。");
    }
  }

  // DOM完全加载后再初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAssistant);
  } else {
    initAssistant();
  }
})();
