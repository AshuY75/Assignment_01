package com.multimedia.qa.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "topic_timestamps")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TopicTimestamp {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "media_file_id", nullable = false)
    private MediaFile mediaFile;

    @Column(nullable = false)
    private Double timestampSeconds;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String topic;

    @Column(columnDefinition = "TEXT")
    private String context;
}
