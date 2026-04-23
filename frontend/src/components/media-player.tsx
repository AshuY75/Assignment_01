"use client"

import { useRef, useEffect } from "react"
import { Play, Pause, RotateCcw, Volume2 } from "lucide-react"

interface MediaStore {
  file: any;
  seekTo: number | null;
}

export function AudioVideoPlayer({ file, seekTime }: { file: any, seekTime: number | null }) {
  const videoRef = useRef<HTMLVideoElement>(null)
  
  useEffect(() => {
    if (seekTime !== null && videoRef.current) {
      videoRef.current.currentTime = seekTime
      videoRef.current.play()
    }
  }, [seekTime])

  if (!file) return null

  const isVideo = file.contentType.startsWith('video/')
  const isAudio = file.contentType.startsWith('audio/')

  if (!isVideo && !isAudio) return null

  return (
    <div className="w-full bg-secondary/30 rounded-2xl overflow-hidden border border-secondary shadow-lg">
      {isVideo ? (
        <video 
          ref={videoRef} 
          controls 
          className="w-full aspect-video bg-black"
          src={`http://localhost:8080/api/media/stream?fileId=${file.id}`}
        />
      ) : (
        <div className="p-8 flex flex-col items-center gap-6">
          <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center text-primary animate-pulse">
            <Volume2 className="w-8 h-8" />
          </div>
          <audio 
            ref={videoRef as any} 
            controls 
            className="w-full"
            src={`http://localhost:8080/api/media/stream?fileId=${file.id}`}
          />
          <div className="text-center">
            <p className="text-sm font-medium">{file.originalFileName}</p>
            <p className="text-xs text-muted-foreground uppercase tracking-widest mt-1">Audio Recording</p>
          </div>
        </div>
      )}
    </div>
  )
}
