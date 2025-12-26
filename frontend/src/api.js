/**
 * API Service Layer
 * Centralized API calls using environment variables
 */

import axios from 'axios';

// Get backend URL from environment variable
const backendURL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

// Create axios instance with default config
const api = axios.create({
  baseURL: backendURL,
  timeout: 120000, // 2 minutes for large file uploads
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Upload and transcribe audio file
 * @param {FormData} formData - FormData containing audio file and optional language
 * @returns {Promise} Response data with transcript
 */
export const uploadAudio = async (formData) => {
  try {
    const response = await api.post('/api/transcribe', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Upload audio error:', error);
    throw error.response?.data || { error: 'Failed to upload audio' };
  }
};

/**
 * Transcribe live recording audio
 * @param {FormData} formData - FormData containing recorded audio blob
 * @returns {Promise} Response data with transcript
 */
export const startLiveRecording = async (formData) => {
  try {
    const response = await api.post('/api/live', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Live recording error:', error);
    throw error.response?.data || { error: 'Failed to transcribe recording' };
  }
};

/**
 * Translate text to target language
 * @param {Object} data - Translation data
 * @param {string} data.text - Text to translate
 * @param {string} data.source_lang - Source language code (or 'auto')
 * @param {string} data.target_lang - Target language code
 * @returns {Promise} Response data with translated text
 */
export const translateTranscript = async (data) => {
  try {
    const response = await api.post('/api/translate', data);
    return response.data;
  } catch (error) {
    console.error('Translation error:', error);
    throw error.response?.data || { error: 'Failed to translate text' };
  }
};

/**
 * Check backend server health
 * @returns {Promise} Server health status
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    console.error('Health check error:', error);
    throw error.response?.data || { error: 'Backend server not responding' };
  }
};

/**
 * Get backend URL for reference
 * @returns {string} Backend URL
 */
export const getBackendURL = () => backendURL;

export default api;
