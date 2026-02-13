"""
LLM Service - 大语言模型服务

提供 LLM 调用封装，支持 MiniMax（已配置）。
"""

import os
import logging
import httpx
from typing import Optional, Iterator
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger(__name__)


class MiniMaxLLM:
    """MiniMax LLM 服务"""
    
    def __init__(
        self,
        model: str = "MiniMax-M2.1",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ):
        """初始化 MiniMax LLM"""
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = settings.MINIMAX_API_KEY or os.getenv("MINIMAX_API_KEY")
        
        if not self.api_key:
            logger.warning("MiniMax API Key 未设置")
        
        logger.info(f"MiniMax LLM 初始化完成，模型: {self.model}")
    
    def generate(self, prompt: str) -> str:
        """生成回复"""
        if not self.api_key:
            return f"[无API密钥] {prompt}"
        
        try:
            response = httpx.post(
                "https://api.minimaxi.com/v1/text/chatcompletion_v2",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens
                },
                timeout=60.0
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.error(f"MiniMax 生成失败: {e}")
            return f"生成失败: {str(e)}"
    
    def stream(self, prompt: str) -> Iterator[str]:
        """流式生成"""
        content = self.generate(prompt)
        yield content
    
    def count_tokens(self, text: str) -> int:
        """估算 token 数量"""
        return len(text) // 2


class LLMService:
    """LLM 服务类"""
    
    PROVIDERS = {
        "minimax": MiniMaxLLM,
    }
    
    def __init__(
        self,
        provider: str = "minimax",
        model: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ):
        """初始化 LLM 服务"""
        provider_class = self.PROVIDERS.get(provider, MiniMaxLLM)
        self.llm = provider_class(
            model=model or settings.MINIMAX_MODEL or "MiniMax-M2.1",
            temperature=temperature,
            **kwargs
        )
        
        self.provider = provider
        logger.info(f"LLM 服务初始化完成，提供商: {provider}")
    
    def generate(self, prompt: str) -> str:
        """生成回复"""
        return self.llm.generate(prompt)
    
    def chat(self, message: str) -> str:
        """简单对话"""
        return self.generate(message)
    
    def stream(self, prompt: str) -> Iterator[str]:
        """流式生成"""
        return self.llm.stream(prompt)
    
    def count_tokens(self, text: str) -> int:
        """估算 token 数量"""
        return self.llm.count_tokens(text) if hasattr(self.llm, 'count_tokens') else len(text) // 4


def get_llm_service(**kwargs) -> LLMService:
    """获取 LLM 服务实例"""
    return LLMService(**kwargs)


DEFAULT_SYSTEM_PROMPT = """你是一个专业的智能客服助手。请友好、专业地回答用户的问题。"""


# 在文件末尾添加
from app.services.chat_service import ChatService, get_chat_service
