"""Patched ChatOpenAI that preserves thought_signature for Gemini models.

When using Gemini via the OpenAI-compatible gateway (Google AI Studio, Vertex,
or any proxy), the API requires that the ``thought_signature`` field on
tool-call objects is echoed back verbatim in every subsequent request.

The standard ``langchain_openai.ChatOpenAI`` streaming path drops
``thought_signature`` from streaming chunks during accumulation.  This module
fixes the problem in two ways:

1. ``_get_request_payload`` re-injects signatures into the outgoing payload.
2. ``_astream`` uses non-streaming internally to ensure ``thought_signature``
   is fully preserved in the response ``AIMessage.additional_kwargs``.
"""

from __future__ import annotations

import logging
from typing import Any, AsyncIterator

from langchain_core.callbacks import AsyncCallbackManagerForLLMRun
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage
from langchain_core.outputs import ChatGenerationChunk
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


class PatchedChatOpenAI(ChatOpenAI):
    """ChatOpenAI with ``thought_signature`` preservation for Gemini via OpenAI gateway.

    Overrides both ``_get_request_payload`` (to restore signatures on outgoing
    payloads) and ``_astream`` (to use non-streaming internally so that
    ``thought_signature`` fields survive the response→AIMessage conversion).
    """

    def _get_request_payload(
        self,
        input_: LanguageModelInput,
        *,
        stop: list[str] | None = None,
        **kwargs: Any,
    ) -> dict:
        """Get request payload with ``thought_signature`` preserved."""
        original_messages = self._convert_input(input_).to_messages()
        payload = super()._get_request_payload(input_, stop=stop, **kwargs)
        payload_messages = payload.get("messages", [])

        if len(payload_messages) == len(original_messages):
            for payload_msg, orig_msg in zip(payload_messages, original_messages):
                if payload_msg.get("role") == "assistant" and isinstance(orig_msg, AIMessage):
                    _restore_tool_call_signatures(payload_msg, orig_msg)
        else:
            ai_messages = [m for m in original_messages if isinstance(m, AIMessage)]
            assistant_payloads = [
                (i, m) for i, m in enumerate(payload_messages) if m.get("role") == "assistant"
            ]
            for (_, payload_msg), ai_msg in zip(assistant_payloads, ai_messages):
                _restore_tool_call_signatures(payload_msg, ai_msg)

        return payload

    async def _astream(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: AsyncCallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        """Stream via non-streaming call to preserve thought_signatures.

        Gemini's streaming response drops ``thought_signature`` during chunk
        accumulation. By using non-streaming internally, we ensure the full
        response (with all fields) is captured and stored in AIMessage
        additional_kwargs for the next turn.

        LangGraph still gets a "stream" (of one chunk), so the pipeline works.
        """
        # Use the non-streaming path which preserves all response fields
        result = await self._agenerate(
            messages, stop=stop, run_manager=run_manager, **kwargs
        )

        if result.generations and result.generations[0]:
            generation = result.generations[0]
            msg = generation.message

            # Convert to a chunk for stream compatibility
            chunk = ChatGenerationChunk(
                message=AIMessageChunk(
                    content=msg.content,
                    additional_kwargs=msg.additional_kwargs,
                    response_metadata=msg.response_metadata if hasattr(msg, "response_metadata") else {},
                    tool_call_chunks=[],
                    id=msg.id,
                ),
                generation_info=generation.generation_info,
            )

            # Also emit tool_call_chunks if there are tool calls
            if msg.tool_calls:
                chunk.message.tool_call_chunks = [
                    {
                        "name": tc.get("name", ""),
                        "args": tc.get("args", ""),
                        "id": tc.get("id", ""),
                        "index": idx,
                    }
                    for idx, tc in enumerate(msg.tool_calls)
                ]

            if run_manager:
                await run_manager.on_llm_new_token(
                    chunk.text if chunk.text else "",
                    chunk=chunk,
                )

            yield chunk


def _restore_tool_call_signatures(payload_msg: dict, orig_msg: AIMessage) -> None:
    """Re-inject ``thought_signature`` onto tool-call objects in *payload_msg*."""
    raw_tool_calls: list[dict] = orig_msg.additional_kwargs.get("tool_calls") or []
    payload_tool_calls: list[dict] = payload_msg.get("tool_calls") or []

    if not raw_tool_calls or not payload_tool_calls:
        return

    raw_by_id: dict[str, dict] = {}
    for raw_tc in raw_tool_calls:
        tc_id = raw_tc.get("id")
        if tc_id:
            raw_by_id[tc_id] = raw_tc

    for idx, payload_tc in enumerate(payload_tool_calls):
        raw_tc = raw_by_id.get(payload_tc.get("id", ""))
        if raw_tc is None and idx < len(raw_tool_calls):
            raw_tc = raw_tool_calls[idx]

        if raw_tc is None:
            continue

        sig = raw_tc.get("thought_signature") or raw_tc.get("thoughtSignature")
        if sig:
            payload_tc["thought_signature"] = sig
