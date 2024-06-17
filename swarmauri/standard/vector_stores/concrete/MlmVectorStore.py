from typing import List, Union
from swarmauri.standard.documents.concrete.Document import Document
from swarmauri.standard.vectorizers.concrete.MlmEmbedding import MlmEmbedding
from swarmauri.standard.distances.concrete.CosineDistance import CosineDistance

from swarmauri.standard.vector_stores.base.VectorStoreBase import VectorStoreBase
from swarmauri.standard.vector_stores.base.VectorStoreRetrieveMixin import VectorStoreRetrieveMixin
from swarmauri.standard.vector_stores.base.VectorStoreSaveLoadMixin import VectorStoreSaveLoadMixin    

class MlmVectorStore(VectorStoreSaveLoadMixin, VectorStoreRetrieveMixin, VectorStoreBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
                       
        self._embedding = MlmEmbedding()
        self._distance = CosineDistance()
        self.documents: List[Document] = []   

    def add_document(self, document: Document) -> None:
        self.documents.append(document)
        documents_text = [_d.content for _d in self.documents if _d.content]
        embeddings = self._embedding.fit_transform(documents_text)

        embedded_documents = [Document(id=_d.id, 
            content=_d.content, 
            metadata=_d.metadata, 
            embedding=embeddings[_count])

        for _count, _d in enumerate(self.documents) if _d.content]

        self.documents = embedded_documents

    def add_documents(self, documents: List[Document]) -> None:
        self.documents.extend(documents)
        documents_text = [_d.content for _d in self.documents if _d.content]
        embeddings = self._embedding.fit_transform(documents_text)

        embedded_documents = [Document(id=_d.id, 
            content=_d.content, 
            metadata=_d.metadata, 
            embedding=embeddings[_count]) for _count, _d in enumerate(self.documents) 
            if _d.content]

        self.documents = embedded_documents

    def get_document(self, id: str) -> Union[Document, None]:
        for document in self.documents:
            if document.id == doc_id:
                return document
        return None
        
    def get_all_documents(self) -> List[Document]:
        return self.documents

    def delete_document(self, id: str) -> None:
        self.documents = [_d for _d in self.documents if _d.id != doc_id]

    def update_document(self, id: str) -> None:
        raise NotImplementedError('Update_document not implemented on MLMVectorStore class.')
        
    def retrieve(self, query: str, top_k: int = 5) -> List[Document]:
        query_vector = self._embedding.infer_vector(query)
        document_vectors = [_d.embedding for _d in self.documents if _d.content]
        distances = self._distance.distances(query_vector, document_vectors)
        
        # Get the indices of the top_k most similar documents
        top_k_indices = sorted(range(len(distances)), key=lambda i: distances[i])[:top_k]
        
        return [self.documents[i] for i in top_k_indices]