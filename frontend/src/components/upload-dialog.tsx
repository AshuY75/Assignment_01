"use client"

import { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import { Upload, X, File, Film, Music, Loader2 } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"
import { mediaApi } from "@/lib/api"

interface UploadDialogProps {
  onClose: () => void;
  onUploadSuccess: (file: any) => void;
}

export function UploadDialog({ onClose, onUploadSuccess }: UploadDialogProps) {
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return
    
    setIsUploading(true)
    setError(null)
    
    try {
      const response = await mediaApi.upload(acceptedFiles[0], "user-123")
      onUploadSuccess(response.data)
      onClose()
    } catch (err: any) {
      setError(err.response?.data?.message || "Failed to upload file")
    } finally {
      setIsUploading(false)
    }
  }, [onClose, onUploadSuccess])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'video/mp4': ['.mp4'],
      'video/x-matroska': ['.mkv'],
      'audio/mpeg': ['.mp3'],
      'audio/wav': ['.wav']
    },
    multiple: false
  })

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="w-full max-w-lg bg-background rounded-3xl shadow-2xl overflow-hidden border border-secondary"
      >
        <div className="p-6 border-b border-secondary flex items-center justify-between">
          <h2 className="text-xl font-bold">Upload Content</h2>
          <button onClick={onClose} className="p-2 hover:bg-secondary rounded-full transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-8">
          <div 
            {...getRootProps()} 
            className={`cursor-pointer border-2 border-dashed rounded-2xl p-12 text-center transition-all ${
              isDragActive ? 'border-primary bg-primary/5' : 'border-secondary hover:border-primary/50'
            }`}
          >
            <input {...getInputProps()} />
            
            <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center text-primary mx-auto mb-6">
              {isUploading ? <Loader2 className="w-8 h-8 animate-spin" /> : <Upload className="w-8 h-8" />}
            </div>
            
            <h3 className="text-lg font-semibold mb-2">
              {isUploading ? 'Uploading & Processing...' : 'Click or Drag File'}
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              Support for PDF, MP4, MKV, MP3, WAV (Max 50MB)
            </p>
            
            <div className="flex items-center justify-center gap-4 text-muted-foreground">
              <File className="w-4 h-4" />
              <Film className="w-4 h-4" />
              <Music className="w-4 h-4" />
            </div>
          </div>
          
          {error && (
            <div className="mt-4 p-3 bg-destructive/10 text-destructive text-sm rounded-lg border border-destructive/20">
              {error}
            </div>
          )}
        </div>

        <div className="p-6 bg-secondary/20 flex justify-end gap-3">
          <button 
            disabled={isUploading}
            onClick={onClose} 
            className="px-6 py-2 rounded-xl text-sm font-medium hover:bg-secondary transition-colors"
          >
            Cancel
          </button>
        </div>
      </motion.div>
    </div>
  )
}
