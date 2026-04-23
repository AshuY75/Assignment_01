package com.multimedia.qa.service;

import dev.langchain4j.data.segment.TextSegment;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.chat.StreamingChatLanguageModel;
import dev.langchain4j.model.embedding.EmbeddingModel;
import dev.langchain4j.store.embedding.EmbeddingMatch;
import dev.langchain4j.store.embedding.EmbeddingStore;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.Collections;
import java.util.List;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ChatServiceTest {

    @Mock
    private ChatLanguageModel chatLanguageModel;
    @Mock
    private StreamingChatLanguageModel streamingChatLanguageModel;
    @Mock
    private EmbeddingModel embeddingModel;
    @Mock
    private EmbeddingStore<TextSegment> embeddingStore;

    @InjectMocks
    private ChatService chatService;

    @Test
    void chat_ShouldReturnResponse() {
        // Arrange
        String query = "What is the report about?";
        String mockAnswer = "It is about Q1 performance.";
        dev.langchain4j.data.embedding.Embedding mockEmbedding = dev.langchain4j.data.embedding.Embedding.from(new float[]{0.1f});
        TextSegment segment = TextSegment.from("Q1 report details...");
        EmbeddingMatch<TextSegment> match = new EmbeddingMatch<>(0.9, "1", mockEmbedding, segment);

        when(embeddingModel.embed(anyString())).thenReturn(dev.langchain4j.model.output.Response.from(mockEmbedding));
        when(embeddingStore.findRelevant(any(), anyInt())).thenReturn(Collections.singletonList(match));
        when(chatLanguageModel.generate(anyString())).thenReturn(mockAnswer);

        // Act
        String result = chatService.chat(query, "user-123");

        // Assert
        assertEquals(mockAnswer, result);
    }
}
