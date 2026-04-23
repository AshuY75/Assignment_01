package com.multimedia.qa.config;

import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.chat.StreamingChatLanguageModel;
import dev.langchain4j.model.embedding.EmbeddingModel;
import dev.langchain4j.model.googleai.GoogleAiGeminiChatModel;
import dev.langchain4j.model.googleai.GoogleAiGeminiStreamingChatModel;
import dev.langchain4j.model.googleai.GoogleAiGeminiEmbeddingModel;
import dev.langchain4j.store.embedding.EmbeddingStore;
import dev.langchain4j.data.segment.TextSegment;
import dev.langchain4j.store.embedding.faiss.FaissEmbeddingStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.nio.file.Paths;

@Configuration
public class AIConfig {

    @Value("${langchain4j.google-ai-gemini.chat-model.api-key}")
    private String apiKey;

    @Bean
    public ChatLanguageModel chatLanguageModel() {
        return GoogleAiGeminiChatModel.builder()
                .apiKey(apiKey)
                .modelName("gemini-1.5-flash")
                .build();
    }

    @Bean
    public StreamingChatLanguageModel streamingChatLanguageModel() {
        return GoogleAiGeminiStreamingChatModel.builder()
                .apiKey(apiKey)
                .modelName("gemini-1.5-flash")
                .build();
    }

    @Bean
    public EmbeddingModel embeddingModel() {
        return GoogleAiGeminiEmbeddingModel.builder()
                .apiKey(apiKey)
                .modelName("text-embedding-004")
                .build();
    }

    @Bean
    public EmbeddingStore<TextSegment> embeddingStore() {
        // Simple local FAISS store
        return new FaissEmbeddingStore(Paths.get("embeddings.faiss"), true);
    }
}
