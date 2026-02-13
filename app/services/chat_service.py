"""
Chat Service - 对话服务

整合 RAG 检索和 LLM 生成，提供完整的对话功能。
"""

import logging
import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime
from collections import defaultdict

from app.core.config import settings
from app.services.rag_service import RAGService, RetrievalResult
from app.services.llm_service import LLMService, DEFAULT_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class ChatService:
    """
    对话服务类
    
    提供完整的对话功能：
    - 对话历史管理
    - 上下文构建
    - RAG + LLM 整合
    - 多轮对话支持
    
    Example:
        ```python
        chat_service = ChatService()
        
        # 发送消息
        response = chat_service.chat(
            message="你们的服务怎么收费？",
            session_id="user-123"
        )
        print(response)
        
        # 获取历史
        history = chat_service.get_history("user-123")
        ```
    """
    
    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        rag_service: Optional[RAGService] = None,
        max_history: int = 10,
        system_prompt: Optional[str] = None
    ):
        """
        初始化对话服务
        
        Args:
            llm_service: LLM 服务实例
            rag_service: RAG 服务实例
            max_history: 最大对话历史轮数
            system_prompt: 系统提示词
        """
        self.llm_service = llm_service or LLMService(
            provider="minimax",  # 使用 MiniMax（用户已配置）
            temperature=0.7
        )
        
        self.rag_service = rag_service or RAGService()
        
        self.max_history = max_history
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        
        # 对话历史存储（内存，生产环境应使用数据库）
        self._sessions: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        
        logger.info("ChatService 初始化完成")
    
    def chat(
        self,
        message: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        use_rag: bool = True,
        top_k: int = 5,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        发送对话消息
        
        Args:
            message: 用户消息
            session_id: 会话ID（可选，自动生成）
            user_id: 用户ID（可选）
            use_rag: 是否使用 RAG 检索
            top_k: RAG 检索返回的最大结果数
            stream: 是否流式输出
            
        Returns:
            Dict[str, Any]: 包含响应、会话ID、时间戳等
            
        Example:
            ```python
            result = chat_service.chat(
                message="我想了解你们的定价",
                session_id="user-123"
            )
            print(result["response"])
            print(result["sources"])
            ```
        """
        # 生成或使用会话ID
        session_id = session_id or f"session_{uuid.uuid4().hex[:8]}"
        
        # 检索知识库
        context = ""
        sources = []
        confidence = 0.0
        
        if use_rag:
            try:
                results = self.rag_service.retrieve_documents(
                    query=message,
                    top_k=top_k
                )
                
                # 构建上下文
                context_parts = []
                for result in results:
                    context_parts.append(
                        f"[来源: {result.metadata.get('filename', '未知')}]\n"
                        f"{result.content}"
                    )
                    sources.append({
                        "content": result.content,
                        "score": result.score,
                        "filename": result.metadata.get("filename", "未知"),
                        "chunk_id": result.chunk_id
                    })
                
                context = "\n\n".join(context_parts)
                confidence = results[0].score if results else 0.0
                
                logger.info(f"RAG 检索完成，找到 {len(results)} 个相关文档")
                
            except Exception as e:
                logger.warning(f"RAG 检索失败: {e}")
                use_rag = False  # 降级处理
        
        # 构建消息
        messages = self._build_messages(
            user_message=message,
            session_id=session_id,
            context=context,
            use_rag=use_rag
        )
        
        # 生成回复
        try:
            if stream:
                # 流式生成
                response_text = ""
                for chunk in self.llm_service.stream(messages):
                    response_text += chunk
            else:
                # 普通生成
                response_text = self.llm_service.generate(messages)
                
        except Exception as e:
            logger.error(f"LLM 生成失败: {e}")
            response_text = "抱歉，我现在无法回答您的问题。请稍后再试。"
        
        # 保存对话历史
        self._save_message(
            session_id=session_id,
            role="user",
            content=message,
            metadata={"use_rag": use_rag, "sources_count": len(sources)}
        )
        self._save_message(
            session_id=session_id,
            role="assistant",
            content=response_text,
            metadata={"confidence": confidence, "sources": sources}
        )
        
        logger.info(f"对话完成，会话: {session_id}")
        
        return {
            "response": response_text,
            "session_id": session_id,
            "sources": sources,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }
    
    def _build_messages(
        self,
        user_message: str,
        session_id: str,
        context: str = "",
        use_rag: bool = True
    ) -> List[Dict[str, str]]:
        """
        构建消息列表
        
        Args:
            user_message: 用户消息
            session_id: 会话ID
            context: RAG 检索的上下文
            use_rag: 是否使用 RAG
            
        Returns:
            List[Dict]: 消息列表
        """
        messages = []
        
        # 系统提示词
        if use_rag and context:
            system_msg = (
                f"{self.system_prompt}\n\n"
                f"=== 知识库内容 ===\n{context}\n"
                f"=== 知识库结束 ===\n\n"
                f"请根据上面的知识库内容回答用户的问题。"
                f"如果知识库中没有相关信息，请说\"抱歉，我没有找到相关信息\"。"
            )
        else:
            system_msg = self.system_prompt
        
        messages.append({"role": "system", "content": system_msg})
        
        # 对话历史
        history = self._sessions.get(session_id, [])
        for msg in history[-self.max_history:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # 当前用户消息
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def _save_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        保存消息到历史
        
        Args:
            session_id: 会话ID
            role: 角色 (user/assistant)
            content: 消息内容
            metadata: 元数据
        """
        self._sessions[session_id].append({
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        })
        
        # 限制历史长度
        max_messages = (self.max_history + 1) * 2  # user + assistant pairs
        if len(self._sessions[session_id]) > max_messages:
            # 保留最近的历史
            self._sessions[session_id] = self._sessions[session_id][-max_messages:]
    
    def get_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        获取对话历史
        
        Args:
            session_id: 会话ID
            limit: 最大返回消息数
            
        Returns:
            List[Dict]: 消息历史列表
        """
        history = self._sessions.get(session_id, [])
        
        if limit:
            history = history[-limit:]
        
        return history
    
    def clear_history(self, session_id: str) -> bool:
        """
        清除对话历史
        
        Args:
            session_id: 会话ID
            
        Returns:
            bool: 是否成功清除
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info(f"清除对话历史: {session_id}")
            return True
        return False
    
    def get_session_count(self) -> int:
        """
        获取会话数量
        
        Returns:
            int: 会话数量
        """
        return len(self._sessions)
    
    def add_knowledge(
        self,
        file_path: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        添加知识库文档
        
        Args:
            file_path: 文件路径
            **kwargs: 其他参数
            
        Returns:
            Dict: 处理结果
        """
        try:
            chunk_count = self.rag_service.ingest_file(file_path)
            logger.info(f"知识库文档添加成功: {file_path}, {chunk_count} 个块")
            
            return {
                "status": "success",
                "filename": file_path.split("/")[-1],
                "chunks": chunk_count
            }
        except Exception as e:
            logger.error(f"添加知识库文档失败: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def search_knowledge(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        搜索知识库
        
        Args:
            query: 查询文本
            top_k: 返回结果数
            
        Returns:
            List[Dict]: 搜索结果
        """
        results = self.rag_service.retrieve_documents(query, top_k=top_k)
        
        return [
            {
                "content": r.content,
                "score": r.score,
                "metadata": r.metadata
            }
            for r in results
        ]


# 便捷函数
def get_chat_service(**kwargs) -> ChatService:
    """
    获取 ChatService 实例
    
    Args:
        **kwargs: 初始化参数
        
    Returns:
        ChatService 实例
    """
    return ChatService(**kwargs)
