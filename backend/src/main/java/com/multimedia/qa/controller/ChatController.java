package com.multimedia.qa.controller;

import com.multimedia.qa.service.ChatService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/api/chat")
@RequiredArgsConstructor
public class ChatController {

    private final ChatService chatService;

    @PostMapping(path = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> streamChat(@RequestParam String query, @RequestParam String userId) {
        return chatService.streamChat(query, userId);
    }

    @PostMapping
    public String chat(@RequestParam String query, @RequestParam String userId) {
        return chatService.chat(query, userId);
    }
}
