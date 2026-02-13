"""
对话图节点模块
定义 LangGraph 工作流中的各个节点
"""
import logging
from typing import Dict, Any, List, Optional
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from app.services.vector_store import VectorStoreService
from app.core.config import settings

logger = logging.getLogger(__name__)


class ChatGraphNodes:
    """对话图节点类"""
    
    def __init__(
        self,
        llm: ChatOpenAI,
        vector_store: VectorStoreService,
        similarity_top_k: int = 5,
        confidence_threshold: float = 0.7,
    ):
        """
        初始化节点类
        
        Args:
            llm: ChatOpenAI 实例
            vector_store: 向量存储服务
            similarity_top_k: 检索返回的最大文档数
            confidence_threshold: 置信度阈值
        """
        self.llm = llm
        self.vector_store = vector_store
        self.similarity_top_k = similarity_top_k
        self.confidence_threshold = confidence_threshold
    
    def retrieve_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        检索节点：从知识库中检索相关文档
        
        Args:
            state: 当前状态
            
        Returns:
            更新后的状态
        """
        logger.info("Executing retrieve_node")
        
        # 获取用户问题
        question = state.get("messages", [])[-1].content if state.get("messages") else ""
        
        if not question:
            logger.warning("No question found in state")
            return state
        
        try:
            # 执行相似度搜索
            documents = self.vector_store.similarity_search(
                query=question,
                top_k=self.similarity_top_k,
            )
            
            # 提取文档内容作为上下文
            context = "\n\n".join([doc.page_content for doc in documents])
            
            # 保存检索结果
            state["retrieved_docs"] = documents
            state["context"] = context
            state["retrieved_count"] = len(documents)
            
            logger.info(f"Retrieved {len(documents)} documents")
            
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            state["retrieved_docs"] = []
            state["context"] = ""
            state["retrieved_count"] = 0
            state["error"] = str(e)
        
        return state
    
    def generate_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成节点：基于检索的上下文生成回答
        
        Args:
            state: 当前状态
            
        Returns:
            更新后的状态
        """
        logger.info("Executing generate_node")
        
        question = state.get("messages", [])[-1].content if state.get("messages") else ""
        context = state.get("context", "")
        conversation_history = state.get("messages", [])
        
        if not question:
            logger.warning("No question found for generation")
            return state
        
        # 构建提示词
        if context:
            prompt = f"""基于以下上下文信息回答用户问题。如果上下文中没有相关信息，请明确说明。

上下文信息：
{context}

用户问题：{question}

请提供准确、有帮助的回答："""
        else:
            # 没有检索到相关文档时的处理
            prompt = f"""用户问题：{question}

请基于你的知识库提供回答。如果这是一个需要特定领域知识的问题，请说明需要更多信息。"""
        
        try:
            # 调用 LLM 生成回答
            response = self.llm.invoke(prompt)
            answer = response.content if hasattr(response, 'content') else str(response)
            
            state["generated_answer"] = answer
            state["last_node"] = "generate"
            
            logger.info(f"Generated answer: {len(answer)} characters")
            
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            state["generated_answer"] = "抱歉，生成回答时出现错误。"
            state["error"] = str(e)
        
        return state
    
    def evaluate_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估节点：评估生成回答的质量
        
        Args:
            state: 当前状态
            
        Returns:
            更新后的状态，包含 confidence 分数
        """
        logger.info("Executing evaluate_node")
        
        question = state.get("messages", [])[-1].content if state.get("messages") else ""
        answer = state.get("generated_answer", "")
        context = state.get("context", "")
        
        if not question or not answer:
            state["confidence"] = 0.0
            state["needs_clarification"] = True
            return state
        
        # 评估标准
        score = 0.0
        reasons = []
        
        # 1. 检查回答长度是否合理
        if len(answer) < 20:
            score += 0.1
            reasons.append("回答过短")
        elif len(answer) > 50:
            score += 0.2
        else:
            score += 0.3
        
        # 2. 检查是否包含上下文中信息（如果有上下文）
        if context:
            context_keywords = set(context.lower().split()[:50])
            answer_keywords = set(answer.lower().split()[:50])
            overlap = len(context_keywords & answer_keywords)
            if overlap > 5:
                score += 0.3
            else:
                score += 0.1
                reasons.append("回答与上下文关联度低")
        else:
            score += 0.2
        
        # 3. 检查回答是否明确表示无法回答
        uncertainty_phrases = [
            "抱歉，我不清楚",
            "我不知道",
            "没有找到相关信息",
            "需要更多信息",
        ]
        if any(phrase in answer for phrase in uncertainty_phrases):
            score *= 0.5
            reasons.append("回答表示不确定性")
        
        # 4. 检查回答格式
        if answer.strip() == answer:
            score += 0.1
        
        # 5. 简单的问题类型检查
        intent = state.get("intent", "")
        if intent in ["greeting", "farewell"]:
            score = 1.0  # 问候语总是高置信度
        
        # 归一化分数到 0-1
        confidence = min(score, 1.0)
        
        state["confidence"] = confidence
        state["evaluation_reasons"] = reasons
        state["needs_clarification"] = confidence < self.confidence_threshold
        
        logger.info(f"Evaluation complete: confidence={confidence:.2f}, reasons={reasons}")
        
        return state
    
    def clarify_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        澄清节点：请求用户澄清问题
        
        Args:
            state: 当前状态
            
        Returns:
            更新后的状态
        """
        logger.info("Executing clarify_node")
        
        question = state.get("messages", [])[-1].content if state.get("messages") else ""
        context = state.get("context", "")
        confidence = state.get("confidence", 0.0)
        
        # 生成澄清问题
        if not context or context == "":
            prompt = f"""用户的问题: {question}

当前置信度: {confidence:.2f}

请生成一个友好的澄清问题，询问用户更多细节以便提供更准确的回答。"""
        else:
            # 有上下文但置信度低
            prompt = f"""用户的问题: {question}

检索到的上下文: {context[:200]}...

当前置信度: {confidence:.2f}

请生成一个澄清问题，询问用户是否需要更详细的信息或确认理解是否正确。"""
        
        try:
            response = self.llm.invoke(prompt)
            clarification = response.content if hasattr(response, 'content') else str(response)
            
            # 如果 LLM 生成的内容不合适，使用默认澄清
            if not clarification or len(clarification.strip()) < 5:
                clarification = "为了更好地帮助您，能否详细说明一下您的问题？"
            
            state["clarification"] = clarification
            state["needs_clarification"] = True
            state["last_node"] = "clarify"
            
        except Exception as e:
            logger.error(f"Clarification failed: {e}")
            state["clarification"] = "为了更好地帮助您，能否详细说明一下您的问题？"
            state["error"] = str(e)
        
        return state
    
    def fallback_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        异常处理节点：处理各种异常情况
        
        Args:
            state: 当前状态
            
        Returns:
            更新后的状态
        """
        logger.info("Executing fallback_node")
        
        error = state.get("error", "Unknown error")
        question = state.get("messages", [])[-1].content if state.get("messages") else ""
        
        # 生成友好的错误回答
        fallback_responses = [
            "抱歉，我现在遇到了一些技术问题。请稍后再试或联系客服获得帮助。",
            "抱歉，处理您的问题时出现了临时故障。请您重新描述一下问题，我会尽力帮助您。",
            "抱歉，我暂时无法回答这个问题。建议您查看我们的帮助中心或直接联系人工客服。",
        ]
        
        import random
        fallback = random.choice(fallback_responses)
        
        state["final_answer"] = fallback
        state["error"] = error
        state["last_node"] = "fallback"
        state["needs_human"] = True
        
        logger.error(f"Fallback triggered: {error}")
        
        return state
    
    def respond_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        响应节点：生成最终响应消息
        
        Args:
            state: 当前状态
            
        Returns:
            更新后的状态
        """
        logger.info("Executing respond_node")
        
        # 优先使用澄清节点的结果
        if state.get("needs_clarification") and state.get("clarification"):
            answer = state["clarification"]
        elif state.get("generated_answer"):
            answer = state["generated_answer"]
        else:
            answer = "抱歉，我无法回答您的问题。"
        
        # 更新置信度
        confidence = state.get("confidence", 0.0)
        
        # 添加引用来源（如果有）
        retrieved_docs = state.get("retrieved_docs", [])
        if retrieved_docs:
            sources = []
            for i, doc in enumerate(retrieved_docs[:3]):
                filename = doc.metadata.get("filename", f"Document {i+1}")
                sources.append(f"[{i+1}] {filename}")
            if sources:
                answer += f"\n\n参考来源：\n" + "\n".join(sources)
        
        # 创建响应消息
        response_message = AIMessage(content=answer)
        
        # 更新消息历史
        messages = state.get("messages", [])
        messages.append(response_message)
        
        state["messages"] = messages
        state["final_answer"] = answer
        state["last_node"] = "respond"
        
        logger.info(f"Response generated: {len(answer)} characters")
        
        return state


# 创建节点实例的工厂函数
def create_nodes(
    llm: ChatOpenAI,
    vector_store: VectorStoreService,
    **kwargs
) -> ChatGraphNodes:
    """
    创建对话图节点实例
    
    Args:
        llm: ChatOpenAI 实例
        vector_store: 向量存储服务
        **kwargs: 其他配置参数
        
    Returns:
        ChatGraphNodes 实例
    """
    return ChatGraphNodes(
        llm=llm,
        vector_store=vector_store,
        similarity_top_k=kwargs.get("similarity_top_k", 5),
        confidence_threshold=kwargs.get("confidence_threshold", 0.7),
    )
