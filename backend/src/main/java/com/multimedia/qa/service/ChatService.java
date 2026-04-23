package com.multimedia.qa.service;

import dev.langchain4j.data.segment.TextSegment;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.chat.StreamingChatLanguageModel;
import dev.langchain4j.model.embedding.EmbeddingModel;
import dev.langchain4j.store.embedding.EmbeddingMatch;
import dev.langchain4j.store.embedding.EmbeddingStore;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ChatService {

    private final ChatLanguageModel chatLanguageModel;
    private final StreamingChatLanguageModel streamingChatLanguageModel;
    private final EmbeddingModel embeddingModel;
    private final EmbeddingStore<TextSegment> embeddingStore;

    public String chat(String query, String userId) {
        // Simple RAG retrieval
        List<EmbeddingMatch<TextSegment>> matches = embeddingStore.findRelevant(embeddingModel.embed(query).content(), 5);
        
        StringBuilder contextBuilder = new StringBuilder();
        for (int i = 0; i < matches.size(); i++) {
            contextBuilder.append(String.format("[%d] %s\n\n", i + 1, matches.get(i).embedded().text()));
        }
        String context = contextBuilder.toString();

        String prompt = String.format("You are a helpful AI assistant. Answer the user's question based ONLY on the provided context. " +
                "Always cite the source chunks using their numbers in brackets, e.g., [1] or [1,2].\n\nContext:\n%s\n\nQuestion: %s", context, query);

        return chatLanguageModel.generate(prompt);
    }

    public Flux<String> streamChat(String query, String userId) {
        List<EmbeddingMatch<TextSegment>> matches = embeddingStore.findRelevant(embeddingModel.embed(query).content(), 5);
        
        StringBuilder contextBuilder = new StringBuilder();
        for (int i = 0; i < matches.size(); i++) {
            contextBuilder.append(String.format("[%d] %s\n\n", i + 1, matches.get(i).embedded().text()));
        }
        String context = contextBuilder.toString();

        String prompt = String.format("You are a helpful AI assistant. Answer the user's question based ONLY on the provided context. " +
                "Always cite the source chunks using their numbers in brackets, e.g., [1] or [1,2].\n\nContext:\n%s\n\nQuestion: %s", context, query);

        return Flux.create(sink -> {
            streamingChatLanguageModel.generate(prompt, new dev.langchain4j.model.StreamingResponseHandler<dev.langchain4j.model.output.Response<dev.langchain4j.model.chat.ChatMessage>>() {
                @Override
                public void onNext(String token) {
                    sink.next(token);
                }

                @Override
                public void onComplete(dev.langchain4j.model.output.Response<dev.langchain4j.model.chat.ChatMessage> response) {
                    sink.complete();
                }

                @Override
                public void onError(Throwable error) {
                    sink.error(error);
                }
            });
        });
    }
}
