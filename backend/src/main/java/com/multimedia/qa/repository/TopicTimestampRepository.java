package com.multimedia.qa.repository;

import com.multimedia.qa.entity.TopicTimestamp;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface TopicTimestampRepository extends JpaRepository<TopicTimestamp, Long> {
    List<TopicTimestamp> findByMediaFileIdOrderByTimestampSecondsAsc(String mediaFileId);
}
