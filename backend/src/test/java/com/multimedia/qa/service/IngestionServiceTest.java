package com.multimedia.qa.service;

import com.multimedia.qa.entity.MediaFile;
import com.multimedia.qa.repository.MediaFileRepository;
import com.multimedia.qa.repository.TopicTimestampRepository;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.embedding.EmbeddingModel;
import dev.langchain4j.store.embedding.EmbeddingStore;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.mock.web.MockMultipartFile;
import java.io.IOException;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class IngestionServiceTest {

    @Mock
    private MediaFileRepository mediaFileRepository;
    @Mock
    private TopicTimestampRepository topicTimestampRepository;
    @Mock
    private EmbeddingModel embeddingModel;
    @Mock
    private EmbeddingStore<?> embeddingStore;
    @Mock
    private ChatLanguageModel chatLanguageModel;

    @InjectMocks
    private IngestionService ingestionService;

    @Test
    void uploadFile_ShouldSaveAndReturnMetadata() throws IOException {
        // Arrange
        MockMultipartFile file = new MockMultipartFile("file", "test.pdf", "application/pdf", "dummy content".getBytes());
        MediaFile savedFile = MediaFile.builder().id("123").fileName("123_test.pdf").build();
        
        when(mediaFileRepository.save(any(MediaFile.class))).thenReturn(savedFile);

        // Act
        MediaFile result = ingestionService.uploadFile(file, "user-1");

        // Assert
        assertNotNull(result);
        assertEquals("123", result.getId());
        verify(mediaFileRepository, atLeastOnce()).save(any(MediaFile.class));
    }
}
