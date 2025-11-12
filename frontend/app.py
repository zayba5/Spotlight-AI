import json
import os
import uuid
from typing import Any, Dict, List, Optional, Tuple

import requests
import streamlit as st


BACKEND_URL_DEFAULT = os.getenv("BACKEND_URL", "http://localhost:8000")
REQUEST_TIMEOUT = 30

st.set_page_config(
    page_title="Spotlight AI",
    page_icon="✨",
    layout="wide",
)


def _init_session_state() -> None:
    if "backend_url" not in st.session_state:
        st.session_state.backend_url = BACKEND_URL_DEFAULT
    if "user_id" not in st.session_state:
        st.session_state.user_id = f"user-{uuid.uuid4().hex[:8]}"
    if "active_user_id" not in st.session_state:
        st.session_state.active_user_id = st.session_state.user_id
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = None
    if "messages" not in st.session_state:
        st.session_state.messages: List[Dict[str, Any]] = []
    if "location_hint" not in st.session_state:
        st.session_state.location_hint = ""
    if "preferences" not in st.session_state:
        st.session_state.preferences = {}
    for field in ("diet", "budget", "vibe", "must_have"):
        key = f"pref_{field}"
        if key not in st.session_state:
            st.session_state[key] = ""


def reset_conversation() -> None:
    st.session_state.messages = []
    st.session_state.conversation_id = None


@st.cache_data(show_spinner=False, ttl=30)
def check_backend_health(base_url: str) -> Tuple[bool, str]:
    url = base_url.rstrip("/") + "/health"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        status = data.get("status", "unknown")
        return status == "ok", f"Status: {status}"
    except requests.RequestException as exc:
        return False, f"Cannot reach backend ({exc})"
    except ValueError:
        return False, "Invalid health response"


def send_chat_request(base_url: str, payload: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    url = base_url.rstrip("/") + "/chat"
    try:
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json(), None
    except requests.HTTPError:
        try:
            error_detail = response.json()
        except ValueError:
            error_detail = response.text
        return None, f"Backend error: {error_detail}"
    except requests.RequestException as exc:
        return None, f"Request failed: {exc}"


def ingest_items(base_url: str, items: List[Dict[str, Any]]) -> Tuple[bool, str]:
    url = base_url.rstrip("/") + "/ingest"
    payload = {"items": items}
    try:
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        inserted = data.get("inserted", len(items))
        return True, f"Inserted {inserted} item(s)."
    except requests.HTTPError:
        try:
            error_detail = response.json()
        except ValueError:
            error_detail = response.text
        return False, f"Ingest failed: {error_detail}"
    except requests.RequestException as exc:
        return False, f"Ingest request failed: {exc}"


def build_preferences_dict() -> Dict[str, str]:
    prefs: Dict[str, str] = {}
    for field in ("diet", "budget", "vibe", "must_have"):
        value = st.session_state.get(f"pref_{field}", "").strip()
        if value:
            prefs[field] = value
    st.session_state.preferences = prefs
    return prefs


def parse_uploaded_items(file) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    try:
        # Ensure pointer at start
        file.seek(0)
        payload = json.load(file)
    except json.JSONDecodeError as exc:
        return None, f"Invalid JSON file: {exc}"

    if isinstance(payload, dict) and "items" in payload:
        items = payload["items"]
    elif isinstance(payload, list):
        items = payload
    else:
        return None, "JSON must be a list of items or an object with an 'items' list."

    if not isinstance(items, list):
        return None, "'items' must be a list."

    normalized: List[Dict[str, Any]] = []
    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return None, f"Item {idx} is not an object."
        doc_id = item.get("id")
        text = item.get("text")
        if not doc_id or not text:
            return None, f"Item {idx} must include 'id' and 'text'."
        normalized.append(
            {
                "id": doc_id,
                "title": item.get("title"),
                "url": item.get("url"),
                "location": item.get("location"),
                "tags": item.get("tags"),
                "text": text,
            }
        )
    return normalized, None


def main() -> None:
    _init_session_state()

    st.title("Spotlight AI ✨")
    st.markdown(
        "Ask natural-language questions and get personalized local recommendations backed by real reviews."
    )

    with st.sidebar:
        st.header("Session Settings")
        st.text_input("Backend URL", key="backend_url", help="FastAPI server base URL.")
        backend_url = st.session_state.backend_url.strip() or BACKEND_URL_DEFAULT

        health_ok, health_msg = check_backend_health(backend_url)
        if health_ok:
            st.success(health_msg, icon="✅")
        else:
            st.error(health_msg, icon="⚠️")

        st.text_input("User ID", key="user_id", help="Use a stable ID so the backend can remember preferences.")
        if not st.session_state.user_id.strip():
            st.warning("User ID cannot be empty; reverting to previous value.")
            st.session_state.user_id = st.session_state.active_user_id

        if st.session_state.user_id != st.session_state.active_user_id:
            reset_conversation()
            st.session_state.active_user_id = st.session_state.user_id

        st.text_input("Location hint", key="location_hint", placeholder="e.g., Seattle, Capitol Hill")

        st.divider()
        st.markdown("**Personalization**")
        st.text_input("Dietary preference", key="pref_diet", placeholder="vegetarian, vegan, gluten-free")
        st.text_input("Budget", key="pref_budget", placeholder="budget-friendly, premium")
        st.text_input("Vibe", key="pref_vibe", placeholder="quiet, lively, cozy")
        st.text_input("Must-have features", key="pref_must_have", placeholder="outdoor seating, Wi-Fi")

        st.button("New conversation", use_container_width=True, on_click=reset_conversation)

    chat_tab, ingest_tab = st.tabs(["💬 Chat", "📥 Ingest Data"])

    with chat_tab:
        st.subheader("Chat with Spotlight AI")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message.get("citations"):
                    st.caption("Sources:")
                    for cite in message["citations"]:
                        parts = []
                        title = cite.get("title") or cite.get("id") or "Source"
                        url = cite.get("url")
                        if url:
                            parts.append(f"[{title}]({url})")
                        else:
                            parts.append(title)
                        st.markdown(f"- {' '.join(parts)}")

        prompt = st.chat_input("Ask for recommendations...")
        if prompt:
            prefs_payload = build_preferences_dict()
            location_hint = st.session_state.location_hint.strip() or None

            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            payload = {
                "user_id": st.session_state.user_id,
                "query": prompt,
                "location_hint": location_hint,
                "update_preferences": prefs_payload or None,
                "conversation_id": st.session_state.conversation_id,
            }

            with st.chat_message("assistant"):
                with st.spinner("Spotlight AI is thinking..."):
                    result, error = send_chat_request(backend_url, payload)
                if error:
                    st.error(error)
                elif not result:
                    st.error("No response from backend.")
                else:
                    answer = result.get("answer", "")
                    citations = result.get("citations", [])
                    st.markdown(answer or "_No answer returned._")
                    if citations:
                        st.caption("Sources:")
                        for cite in citations:
                            title = cite.get("title") or cite.get("id") or "Source"
                            url = cite.get("url")
                            if url:
                                st.markdown(f"- [{title}]({url})")
                            else:
                                st.markdown(f"- {title}")
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer or "_No answer returned._",
                            "citations": citations,
                        }
                    )
                    st.session_state.conversation_id = result.get("conversation_id")

    with ingest_tab:
        st.subheader("Ingest New Data")
        st.markdown(
            "Add snippets from Yelp, Google Places, menus, or custom notes. "
            "They will be indexed in ChromaDB for future conversations."
        )

        with st.form("ingest_single_item"):
            doc_id = st.text_input("Document ID*", help="Unique identifier for this document (e.g., place slug).")
            title = st.text_input("Title")
            url = st.text_input("URL")
            location = st.text_input("Location")
            tags_str = st.text_input("Tags", help="Comma-separated tags (e.g., coffee, quiet, Wi-Fi).")
            text = st.text_area("Content*", height=200, help="Paste reviews, menu highlights, or summaries.")
            submitted = st.form_submit_button("Ingest Document", use_container_width=True)

            if submitted:
                if not doc_id or not text.strip():
                    st.warning("Document ID and Content are required.")
                else:
                    tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()] if tags_str else []
                    success, message = ingest_items(
                        backend_url,
                        [
                            {
                                "id": doc_id,
                                "title": title or None,
                                "url": url or None,
                                "location": location or None,
                                "tags": tags or None,
                                "text": text.strip(),
                            }
                        ],
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

        st.markdown("#### Bulk ingest via JSON")
        st.caption("Upload JSON with `[{...}]` or `{ \"items\": [{...}] }`. Each item must include `id` and `text`.")
        uploaded_file = st.file_uploader("Upload JSON file", type=["json"])
        if uploaded_file:
            items, error = parse_uploaded_items(uploaded_file)
            if error:
                st.error(error)
            elif items:
                success, message = ingest_items(backend_url, items)
                if success:
                    st.success(message)
                else:
                    st.error(message)


if __name__ == "__main__":
    main()


