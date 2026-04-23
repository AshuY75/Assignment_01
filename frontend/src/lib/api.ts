import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080/api',
});

export const mediaApi = {
  upload: (file: File, userId: string) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('userId', userId);
    return api.post('/media/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getTimestamps: (fileId: string) => api.get(`/media/${fileId}/timestamps`),
};

export const chatApi = {
  chat: (query: string, userId: string) => api.post('/chat', null, { params: { query, userId } }),
  // Streaming chat requires EventSource or fetch
  streamChat: (query: string, userId: string, onToken: (token: string) => void) => {
    const url = `${api.defaults.baseURL}/chat/stream?query=${encodeURIComponent(query)}&userId=${userId}`;
    const eventSource = new EventSource(url);
    
    eventSource.onmessage = (event) => {
      onToken(event.data);
    };
    
    eventSource.onerror = (err) => {
      console.error('EventSource failed:', err);
      eventSource.close();
    };
    
    return () => eventSource.close();
  },
};
