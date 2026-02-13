"""
向量存储服务模块
封装 Milvus/Chroma 操作，提供文档存储和相似度搜索功能
"""
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_milvus import Milvus as LangChainMilvus
from langchain_chroma import Chroma as LangChainChroma

from app.core.config import settings

logger = logging.getLogger(__name__)


class VectorStoreService:
    """向量存储服务类"""
    
    def __init__(self, embedding_model: Embeddings):
        """
        初始化向量存储服务
        
        Args:
            embedding_model: 嵌入模型实例
        """
        self.embedding_model = embedding_model
        self._client: Optional[LangChainMilvus | LangChainChroma] = None
        self._collection_name = settings.VECTOR_COLLECTION_NAME
    
    def _get_client(self) -> LangChainMilvus | LangChainChroma:
        """获取向量存储客户端"""
        if self._client is not None:
            return self._client
        
        vector_db_type = settings.VECTOR_DB_TYPE
        
        if vector_db_type == "milvus":
            self._client = LangChainMilvus(
                embedding_function=self.embedding_model,
                collection_name=self._collection_name,
                connection_args={
                    "uri": settings.MILVUS_URI,
                    "token": settings.MILVUS_TOKEN,
                },
                index_params={
                    "index_type": "IVF_FLAT",
                    "metric_type": "COSINE",
                    "params": {"nlist": 1024},
                },
                search_params={"params": {"nprobe": 10}},
            )
        elif vector_db_type == "chroma":
            self._client = LangChainChroma(
                embedding_function=self.embedding_model,
                collection_name=self._collection_name,
                persist_directory=str(settings.CHROMA_PERSIST_DIR),
            )
        else:
            raise ValueError(f"Unsupported vector database type: {vector_db_type}")
        
        logger.info(f"Initialized vector store client: {vector_db_type}")
        return self._client
    
    def add_documents(
        self,
        documents: List[Document],
        ids: Optional[List[str]] = None,
        **kwargs
    ) -> List[str]:
        """
        添加文档到向量存储
        
        Args:
            documents: 文档列表
            ids: 可选的文档ID列表
            **kwargs: 其他参数
            
        Returns:
            添加的文档ID列表
        """
        try:
            client = self._get_client()
            ids = client.add_documents(documents, ids=ids, **kwargs)
            logger.info(f"Added {len(documents)} documents to vector store")
            return ids
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    def similarity_search(
        self,
        query: str,
        top_k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[Document]:
        """
        执行相似度搜索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            filter: 可选的过滤条件
            **kwargs: 其他参数
            
        Returns:
            相似度最高的文档列表
        """
        try:
            client = self._get_client()
            documents = client.similarity_search(
                query, 
                k=top_k,
                filter=filter,
                **kwargs
            )
            logger.info(f"Similarity search returned {len(documents)} documents")
            return documents
        except Exception as e:
            logger.error(f"Failed to perform similarity search: {e}")
            raise
    
    def similarity_search_with_score(
        self,
        query: str,
        top_k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[tuple[Document, float]]:
        """
        执行相似度搜索并返回分数
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            filter: 可选的过滤条件
            **kwargs: 其他参数
            
        Returns:
            (文档, 相似度分数) 列表
        """
        try:
            client = self._get_client()
            results = client.similarity_search_with_relevance_scores(
                query,
                k=top_k,
                filter=filter,
                **kwargs
            )
            logger.info(f"Similarity search with score returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Failed to perform similarity search with score: {e}")
            raise
    
    def delete_collection(self) -> bool:
        """
        删除整个向量集合
        
        Returns:
            是否删除成功
        """
        try:
            if self._client is not None:
                # 根据不同的向量存储类型调用不同的删除方法
                if hasattr(self._client, 'delete_collection'):
                    self._client.delete_collection()
                elif hasattr(self._client, 'clear'):
                    self._client.clear()
                
                logger.info(f"Deleted vector store collection: {self._collection_name}")
                self._client = None
                return True
            return True
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            raise
    
    def delete_documents(
        self,
        ids: Optional[List[str]] = None,
        filter: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> bool:
        """
        删除指定文档
        
        Args:
            ids: 要删除的文档ID列表
            filter: 要删除的文档过滤条件
            **kwargs: 其他参数
            
        Returns:
            是否删除成功
        """
        try:
            client = self._get_client()
            
            if ids is not None:
                client.delete(ids=ids, **kwargs)
            elif filter is not None:
                client.delete(filter=filter, **kwargs)
            else:
                raise ValueError("Either ids or filter must be provided")
            
            logger.info("Deleted documents from vector store")
            return True
        except Exception as e:
            logger.error(f"Failed to delete documents: {e}")
            raise
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        获取集合信息
        
        Returns:
            集合信息字典
        """
        try:
            client = self._get_client()
            
            # 获取文档数量
            count = len(client.get())
            
            return {
                "collection_name": self._collection_name,
                "document_count": count,
                "embedding_model": str(type(self.embedding_model).__name__),
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return {}
    
    def close(self):
        """关闭向量存储连接"""
        try:
            if self._client is not None and hasattr(self._client, 'close'):
                self._client.close()
            self._client = None
            logger.info("Closed vector store connection")
        except Exception as e:
            logger.error(f"Failed to close vector store: {e}")
