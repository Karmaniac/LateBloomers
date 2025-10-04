/**
 * API Service for handling backend API calls
 */

const BASE_URL = 'http://localhost:5000';

/**
 * Generic fetch wrapper with error handling
 * @param {string} endpoint - The API endpoint to call
 * @param {object} options - Fetch options (method, headers, body, etc.)
 * @returns {Promise} - Promise that resolves to the response data
 */
const apiCall = async (endpoint, options = {}) => {
  const url = `${BASE_URL}${endpoint}`;
  
  const defaultOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);
    
    // Check if the response is ok
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`);
    }
    
    // Check if response has content
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return await response.json();
    } else {
      return await response.text();
    }
  } catch (error) {
    console.error(`API call failed for ${endpoint}:`, error);
    throw error;
  }
};

/**
 * Fetch test map data from the backend
 * @returns {Promise} - Promise that resolves to map data
 */
export const fetchTestMap = async () => {
  try {
    const data = await apiCall('/test_map');
    console.log('Test map data received:', data);
    return data;
  } catch (error) {
    console.error('Error fetching test map data:', error);
    throw new Error(`Failed to fetch test map data: ${error.message}`);
  }
};

/**
 * Generic API service object with common methods
 */
export const apiService = {
  /**
   * GET request
   * @param {string} endpoint - API endpoint
   * @returns {Promise} - Response data
   */
  get: (endpoint) => apiCall(endpoint, { method: 'GET' }),
  
  /**
   * POST request
   * @param {string} endpoint - API endpoint
   * @param {object} data - Request body data
   * @returns {Promise} - Response data
   */
  post: (endpoint, data) => apiCall(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  
  /**
   * PUT request
   * @param {string} endpoint - API endpoint
   * @param {object} data - Request body data
   * @returns {Promise} - Response data
   */
  put: (endpoint, data) => apiCall(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  
  /**
   * DELETE request
   * @param {string} endpoint - API endpoint
   * @returns {Promise} - Response data
   */
  delete: (endpoint) => apiCall(endpoint, { method: 'DELETE' }),
};

export default apiService;