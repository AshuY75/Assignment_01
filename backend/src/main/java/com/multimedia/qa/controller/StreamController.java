package com.multimedia.qa.controller;

import com.multimedia.qa.entity.MediaFile;
import com.multimedia.qa.repository.MediaFileRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.io.File;

@RestController
@RequestMapping("/api/media")
@RequiredArgsConstructor
public class StreamController {

    private final MediaFileRepository mediaFileRepository;

    @GetMapping("/stream")
    public ResponseEntity<Resource> streamMedia(@RequestParam String fileId) {
        MediaFile mediaFile = mediaFileRepository.findById(fileId)
                .orElseThrow(() -> new RuntimeException("File not found"));

        File file = new File(mediaFile.getFilePath());
        if (!file.exists()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }

        Resource resource = new FileSystemResource(file);
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.parseMediaType(mediaFile.getContentType()));
        
        return new ResponseEntity<>(resource, headers, HttpStatus.OK);
    }
}
