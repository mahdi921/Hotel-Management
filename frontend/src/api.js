/**
 * API Client for Hotel Management System
 * کلاینت API برای سیستم مدیریت هتل
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Dashboard
export const getDashboardStats = () => api.get('/api/dashboard/stats');

// Rooms
export const getRooms = (params) => api.get('/api/rooms', { params });
export const getRoom = (id) => api.get(`/api/rooms/${id}`);
export const updateRoomStatus = (id, status) => api.patch(`/api/rooms/${id}/status`, { status });
export const getAvailableRooms = (checkIn, checkOut, guests) =>
    api.get('/api/rooms/available', { params: { check_in: checkIn, check_out: checkOut, guests } });
export const suggestBestRooms = (checkIn, checkOut, guests, limit = 5) =>
    api.get('/api/rooms/suggest', { params: { check_in: checkIn, check_out: checkOut, guests, limit } });

// Guests
export const getGuests = (search) => api.get('/api/guests', { params: { search } });
export const createGuest = (data) => api.post('/api/guests', data);

// Bookings
export const getBookings = (params) => api.get('/api/bookings', { params });
export const createBooking = (data) => api.post('/api/bookings', data);
export const checkIn = (bookingId) => api.post(`/api/bookings/${bookingId}/check-in`);
export const checkOut = (bookingId) => api.post(`/api/bookings/${bookingId}/check-out`);
export const cancelBooking = (bookingId) => api.post(`/api/bookings/${bookingId}/cancel`);

// Tape Chart
export const getTapeChartData = (startDate, endDate) =>
    api.get('/api/tape-chart', { params: { start_date: startDate, end_date: endDate } });

// Health Check
export const healthCheck = () => api.get('/api/health');

export default api;
