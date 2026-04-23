package com.multimedia.qa.service;

import com.multimedia.qa.entity.MediaFile;
import com.multimedia.qa.entity.TopicTimestamp;
import com.multimedia.qa.repository.MediaFileRepository;
import com.multimedia.qa.repository.TopicTimestampRepository;
import dev.langchain4j.data.document.Document;
import dev.langchain4j.data.document.DocumentSplitter;
import dev.langchain4j.data.document.parser.apache.tika.ApacheTikaDocumentParser;
import dev.langchain4j.data.document.splitter.DocumentSplitters;
import dev.langchain4j.data.segment.TextSegment;
import dev.langchain4j.model.embedding.EmbeddingModel;
import dev.langchain4j.store.embedding.EmbeddingStore;
import dev.langchain4j.store.embedding.EmbeddingStoreIngestor;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class IngestionService {

    private final MediaFileRepository mediaFileRepository;
    private final TopicTimestampRepository topicTimestampRepository;
    private final EmbeddingModel embeddingModel;
    private final EmbeddingStore<TextSegment> embeddingStore;

    private final Path root = Paths.get("uploads");

    public MediaFile uploadFile(MultipartFile file, String userId) throws IOException {
        if (!Files.exists(root)) {
            Files.createDirectory(root);
        }

        String id = UUID.randomUUID().toString();
        String fileName = id + "_" + file.getOriginalFilename();
        Files.copy(file.getInputStream(), this.root.resolve(fileName));

        MediaFile mediaFile = MediaFile.builder()
                .id(id)
                .fileName(fileName)
                .originalFileName(file.getOriginalFilename())
                .contentType(file.getContentType())
                .filePath(this.root.resolve(fileName).toString())
                .fileSize(file.getSize())
                .userId(userId)
                .build();

        mediaFile = mediaFileRepository.save(mediaFile);

        processFile(mediaFile);

        return mediaFile;
    }

    private void processFile(MediaFile mediaFile) {
        if (mediaFile.getContentType().equals("application/pdf")) {
            ingestPdf(mediaFile);
        } else if (mediaFile.getContentType().startsWith("audio/") || mediaFile.getContentType().startsWith("video/")) {
            // Audio/Video processing would go here (Transcription -> Ingestion)
            // transcriptionService.transcribe(mediaFile);
        }
    }

    private void ingestPdf(MediaFile mediaFile) throws IOException {
        Document document = new ApacheTikaDocumentParser().parse(Files.newInputStream(Paths.get(mediaFile.getFilePath())));
        
        // Generate summary
        String summary = chatLanguageModel.generate("Summarize this document in 2-3 concise sentences: " + document.text().substring(0, Math.min(2000, document.text().length())));
        mediaFile.setSummary(summary);
        mediaFileRepository.save(mediaFile);

        // Add metadata to fragments
        document.metadata().add("file_id", mediaFile.getId());
        document.metadata().add("user_id", mediaFile.getUserId());

        EmbeddingStoreIngestor ingestor = EmbeddingStoreIngestor.builder()
                .documentSplitter(DocumentSplitters.recursive(500, 50))
                .embeddingModel(embeddingModel)
                .embeddingStore(embeddingStore)
                .build();

        ingestor.ingest(document);
    }
}
