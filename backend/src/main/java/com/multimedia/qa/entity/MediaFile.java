package com.multimedia.qa.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "media_files")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MediaFile {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private String id;

    @Column(nullable = false)
    private String fileName;

    @Column(nullable = false)
    private String originalFileName;

    @Column(nullable = false)
    private String contentType;

    @Column(nullable = false)
    private String filePath;

    @Column(nullable = false)
    private Long fileSize;

    @Column(columnDefinition = "TEXT")
    private String summary;

    @Column(nullable = false)
    private String userId;

    @Column(nullable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
