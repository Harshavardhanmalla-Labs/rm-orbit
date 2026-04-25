import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'X-Org-Id': 'org-demo',
    'X-User-Id': 'user-demo',
    'X-User-Role': 'member',
    'Content-Type': 'application/json',
  },
})

export default api
