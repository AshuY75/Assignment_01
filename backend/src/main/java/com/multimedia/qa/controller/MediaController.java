package com.multimedia.qa.controller;

import com.multimedia.qa.entity.MediaFile;
import com.multimedia.qa.entity.TopicTimestamp;
import com.multimedia.qa.repository.TopicTimestampRepository;
import com.multimedia.qa.service.IngestionService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api/media")
@RequiredArgsConstructor
public class MediaController {

    private final IngestionService ingestionService;
    private final TopicTimestampRepository topicTimestampRepository;

    @PostMapping("/upload")
    public ResponseEntity<MediaFile> upload(@RequestParam("file") MultipartFile file, 
                                            @RequestParam("userId") String userId) throws IOException {
        return ResponseEntity.ok(ingestionService.uploadFile(file, userId));
    }

    @GetMapping("/{fileId}/timestamps")
    public ResponseEntity<List<TopicTimestamp>> getTimestamps(@PathVariable String fileId) {
        return ResponseEntity.ok(topicTimestampRepository.findByMediaFileIdOrderByTimestampSecondsAsc(fileId));
    }
}
