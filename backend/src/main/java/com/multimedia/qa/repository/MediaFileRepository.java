package com.multimedia.qa.repository;

import com.multimedia.qa.entity.MediaFile;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface MediaFileRepository extends JpaRepository<MediaFile, String> {
    List<MediaFile> findByUserId(String userId);
}
