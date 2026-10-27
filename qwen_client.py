# -*- coding: utf-8 -*-
"""Server-side call to Alibaba Cloud DashScope (通义千问) text generation API."""
"""支持本地部署大模型作为优先调用渠道，通义千问作为备选"""
import json
import os
import ssl
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# ========== 通义千问配置 ==========
# Default mainland endpoint; override with DASHSCOPE_API_URL for intl, e.g.
# https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
DEFAULT_URL = (
    "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
)

# 备用国际端点
INTERNATIONAL_URL = (
    "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
)

# ========== 本地部署模型配置 ==========
# 本地模型优先，失败自动降级到通义千问
LOCAL_MODEL_ENABLED = os.environ.get("LOCAL_MODEL_ENABLED", "true").lower() in ("true", "1", "yes")
LOCAL_MODEL_URL = os.environ.get("LOCAL_MODEL_URL", "http://localhost:11434/v1/chat/completions")
LOCAL_MODEL_NAME = os.environ.get("LOCAL_MODEL_NAME", "gemma3:27b")


def get_dashscope_api_key():
    """DashScope Bearer token: prefer DASHSCOPE_API_KEY, else ALIYUN_API_KEY (common in .env)."""
    return (
        os.environ.get("DASHSCOPE_API_KEY", "").strip()
        or os.environ.get("ALIYUN_API_KEY", "").strip()
    )


def _read_json_response(raw):
    """Safely read JSON response, handle non-JSON content."""
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", errors="replace")
    
    # 检查是否是HTML内容
    if raw.strip().startswith('<'):
        # 提取HTML中的错误信息
        if '<title>' in raw and '</title>' in raw:
            start = raw.find('<title>') + 7
            end = raw.find('</title>')
            title = raw[start:end].strip()
            return {"error": f"Received HTML response: {title}"}
        return {"error": "Received non-JSON response (HTML)"}
    
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        # 返回原始内容的前200字符用于调试
        return {"error": f"JSON parse error: {str(e)}", "raw": raw[:200]}


def _extract_assistant_text(data):
    """Parse DashScope text-generation (result_format=message) response."""
    if not isinstance(data, dict):
        return None, "invalid_response"
    
    # 检查是否有错误信息
    if "error" in data:
        return None, data["error"]
    
    output = data.get("output") or {}
    choices = output.get("choices")
    if choices:
        msg = (choices[0] or {}).get("message") or {}
        content = msg.get("content")
        if content:
            return content, None
    text = output.get("text")
    if text:
        return text, None
    err = data.get("message") or data.get("msg") or data.get("code")
    return None, err or "empty_model_output"


def qwen_chat(messages, model=None, timeout=120, retries=2):
    """
    Call DashScope Qwen chat completion with retry support.

    messages: list of {"role": "system"|"user"|"assistant", "content": str}
    Returns: (assistant_text: str or None, error_message: str or None)
    """
    api_key = get_dashscope_api_key()
    if not api_key:
        return None, "missing_api_key"

    url = os.environ.get("DASHSCOPE_API_URL", DEFAULT_URL).strip() or DEFAULT_URL
    model = (model or os.environ.get("QWEN_MODEL", "qwen-turbo")).strip()

    payload = {
        "model": model,
        "input": {"messages": messages},
        "parameters": {"result_format": "message"},
    }

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json; charset=utf-8",
        "Content-Length": str(len(body)),
    }

    # 创建SSL上下文 - 使用默认配置以避免密码套件问题
    context = ssl.create_default_context()
    
    # 支持的端点列表（用于重试）
    endpoints = [url]
    if url == DEFAULT_URL:
        endpoints.append(INTERNATIONAL_URL)
    
    last_error = None
    
    for attempt in range(retries + 1):
        for endpoint in endpoints:
            try:
                print(f"=== Qwen API Call (Attempt {attempt + 1}, Endpoint: {endpoint}) ===")
                print(f"Model: {model}")
                print(f"Messages count: {len(messages)}")
                
                req = Request(endpoint, data=body, headers=headers, method="POST")
                
                with urlopen(req, timeout=timeout, context=context) as resp:
                    content_type = resp.headers.get('Content-Type', '')
                    print(f"Response Content-Type: {content_type}")
                    
                    raw_data = resp.read()
                    print(f"Response length: {len(raw_data)} bytes")
                    
                    data = _read_json_response(raw_data)
                
                text, err = _extract_assistant_text(data)
                if err:
                    last_error = f"API Error: {err}"
                    print(f"API Error: {err}")
                    continue
                return text, None
                
            except HTTPError as e:
                try:
                    raw_data = e.read()
                    data = _read_json_response(raw_data)
                    msg = data.get("message") or data.get("msg") or data.get("error") or str(data)
                except Exception as ex:
                    msg = f"HTTP {e.code}: {e.reason}"
                
                if e.code == 401:
                    return None, "Unauthorized: Invalid API key"
                elif e.code == 429:
                    last_error = "Rate limit exceeded"
                    print("Rate limit exceeded, retrying...")
                    continue
                else:
                    last_error = msg
                    print(f"HTTP Error: {last_error}")
                    continue
                    
            except URLError as e:
                last_error = f"Network Error: {str(e.reason) if e.reason else str(e)}"
                print(f"URL Error: {last_error}")
                continue
            except ssl.SSLError as e:
                last_error = f"SSL Error: {str(e)}"
                print(f"SSL Error: {last_error}")
                continue
            except Exception as e:
                last_error = f"Unexpected Error: {str(e)}"
                print(f"Error: {last_error}")
                continue
        
        # 如果所有端点都失败，等待后重试
        if attempt < retries:
            wait_time = (attempt + 1) * 2
            print(f"All endpoints failed, retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    return None, last_error or "Unknown error"


# ========== 本地部署模型调用 ==========
def _extract_local_model_text(data):
    """解析 OpenAI 兼容 API 的响应格式"""
    if not isinstance(data, dict):
        return None, "invalid_response"
    
    # 检查是否有错误信息
    if "error" in data:
        err_msg = data.get("error", {}).get("message") or str(data.get("error"))
        return None, err_msg
    
    choices = data.get("choices")
    if choices and len(choices) > 0:
        msg = choices[0].get("message") or {}
        content = msg.get("content")
        if content:
            return content, None
    return None, "empty_model_output"


def local_model_chat(messages, model=None, timeout=120):
    """
    调用本地部署模型（OpenAI 兼容格式）
    优先级高于通义千问
    """
    if not LOCAL_MODEL_ENABLED:
        return None, "local_model_disabled"
    
    model = model or LOCAL_MODEL_NAME
    url = LOCAL_MODEL_URL
    
    print(f"=== Local Model Call (Model: {model}) ===")
    print(f"Endpoint: {url}")
    print(f"Messages count: {len(messages)}")
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Content-Length": str(len(body)),
    }
    
    context = ssl.create_default_context()
    
    try:
        req = Request(url, data=body, headers=headers, method="POST")
        
        with urlopen(req, timeout=timeout, context=context) as resp:
            content_type = resp.headers.get('Content-Type', '')
            print(f"Local Model Response - Status: {resp.status}, Content-Type: {content_type}")
            
            raw_data = resp.read()
            data = _read_json_response(raw_data)
        
        text, err = _extract_local_model_text(data)
        if err:
            print(f"Local Model Error: {err}")
            return None, err
        print(f"Local Model Success")
        return text, None
        
    except HTTPError as e:
        try:
            raw_data = e.read()
            data = _read_json_response(raw_data)
            msg = data.get("error", {}).get("message") or str(data.get("error")) or str(e)
        except Exception:
            msg = f"HTTP {e.code}: {e.reason}"
        print(f"Local Model HTTP Error: {msg}")
        return None, msg
        
    except URLError as e:
        print(f"Local Model Connection Error: {e.reason}")
        return None, f"connection_failed: {e.reason}"
        
    except ssl.SSLError as e:
        print(f"Local Model SSL Error: {e}")
        return None, f"ssl_error: {e}"
        
    except Exception as e:
        print(f"Local Model Error: {e}")
        return None, f"unknown_error: {e}"


# ========== 统一调用接口（本地优先，自动降级）==========
def get_model_info(model=None):
    """
    Get the current model info without making a call
    Returns: dict with model information
    """
    if LOCAL_MODEL_ENABLED:
        return {
            "used": "local",
            "model_name": model or LOCAL_MODEL_NAME,
            "endpoint": LOCAL_MODEL_URL,
            "display_name": f"本地模型 ({model or LOCAL_MODEL_NAME})"
        }
    else:
        qwen_model = (model or os.environ.get("QWEN_MODEL", "qwen-turbo")).strip()
        url = os.environ.get("DASHSCOPE_API_URL", DEFAULT_URL).strip() or DEFAULT_URL
        return {
            "used": "qwen",
            "model_name": qwen_model,
            "endpoint": url,
            "display_name": f"通义千问 ({qwen_model})"
        }


def qwen_chat(messages, model=None, timeout=120, retries=2):
    """
    智能调用大模型：优先本地部署模型，失败自动降级到通义千问
    
    messages: list of {"role": "system"|"user"|"assistant", "content": str}
    Returns: (assistant_text: str or None, error_message: str or None, model_info: dict)
    """
    # 第1步：尝试本地部署模型
    if LOCAL_MODEL_ENABLED:
        print("=" * 50)
        print("[Step 1] Trying Local Model...")
        local_text, local_err = local_model_chat(messages, model, timeout)
        if local_text:
            print("[Success] Using Local Model")
            print("=" * 50)
            model_info = {
                "used": "local",
                "model_name": model or LOCAL_MODEL_NAME,
                "endpoint": LOCAL_MODEL_URL,
                "display_name": f"本地模型 ({model or LOCAL_MODEL_NAME})"
            }
            return local_text, None, model_info
        else:
            print(f"[Failed] Local Model: {local_err}")
            print("=" * 50)
    
    # 第2步：降级到通义千问（原有逻辑）
    print("[Step 2] Falling back to Qwen...")
    
    api_key = get_dashscope_api_key()
    if not api_key:
        return None, "missing_api_key", None

    url = os.environ.get("DASHSCOPE_API_URL", DEFAULT_URL).strip() or DEFAULT_URL
    qwen_model = (model or os.environ.get("QWEN_MODEL", "qwen-turbo")).strip()

    payload = {
        "model": qwen_model,
        "input": {"messages": messages},
        "parameters": {"result_format": "message"},
    }

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json; charset=utf-8",
        "Content-Length": str(len(body)),
    }

    context = ssl.create_default_context()
    
    endpoints = [url]
    if url == DEFAULT_URL:
        endpoints.append(INTERNATIONAL_URL)
    
    last_error = None
    
    for attempt in range(retries + 1):
        for endpoint in endpoints:
            try:
                print(f"=== Qwen API Call (Attempt {attempt + 1}, Endpoint: {endpoint}) ===")
                print(f"Model: {qwen_model}")
                
                req = Request(endpoint, data=body, headers=headers, method="POST")
                
                with urlopen(req, timeout=timeout, context=context) as resp:
                    raw_data = resp.read()
                    data = _read_json_response(raw_data)
                
                text, err = _extract_assistant_text(data)
                if err:
                    last_error = f"API Error: {err}"
                    continue
                model_info = {
                    "used": "qwen",
                    "model_name": qwen_model,
                    "endpoint": endpoint,
                    "display_name": f"通义千问 ({qwen_model})"
                }
                return text, None, model_info
                
            except HTTPError as e:
                try:
                    raw_data = e.read()
                    data = _read_json_response(raw_data)
                    msg = data.get("message") or data.get("msg") or data.get("error") or str(data)
                except Exception:
                    msg = f"HTTP {e.code}: {e.reason}"
                
                if e.code == 401:
                    return None, "Unauthorized: Invalid API key", None
                last_error = msg
                continue
                
            except Exception as e:
                last_error = str(e)
                continue
        
        if attempt < retries:
            wait_time = (attempt + 1) * 2
            print(f"Qwen retry in {wait_time} seconds...")
            time.sleep(wait_time)
    
    return None, last_error or "All providers failed", None