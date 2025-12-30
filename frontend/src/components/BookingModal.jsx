/**
 * Booking Modal Component
 * مودال جزئیات رزرو
 */

import { translateBookingStatus, formatJalaliDate, formatCurrency } from '../utils';
import { checkIn, checkOut, cancelBooking } from '../api';
import { useState } from 'react';

export default function BookingModal({ booking, onClose, onUpdate }) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    if (!booking) return null;

    const handleAction = async (action) => {
        setLoading(true);
        setError(null);
        try {
            if (action === 'checkin') {
                await checkIn(booking.id);
            } else if (action === 'checkout') {
                await checkOut(booking.id);
            } else if (action === 'cancel') {
                await cancelBooking(booking.id);
            }
            onUpdate?.();
            onClose();
        } catch (err) {
            setError(err.response?.data?.detail || 'خطا در انجام عملیات');
        } finally {
            setLoading(false);
        }
    };

    const statusColors = {
        pending: 'bg-amber-100 text-amber-700',
        confirmed: 'bg-blue-100 text-blue-700',
        checked_in: 'bg-green-100 text-green-700',
        checked_out: 'bg-gray-100 text-gray-700',
        cancelled: 'bg-red-100 text-red-700',
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                {/* Header */}
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-bold text-gray-800">جزئیات رزرو</h2>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                    >
                        <span className="material-symbols-outlined">close</span>
                    </button>
                </div>

                {/* Booking Number */}
                <div className="bg-gray-50 rounded-lg p-4 mb-4">
                    <div className="text-sm text-gray-500">شماره رزرو</div>
                    <div className="text-xl font-mono font-bold text-primary-600">
                        {booking.booking_number}
                    </div>
                </div>

                {/* Status Badge */}
                <div className="mb-4">
                    <span className={`status-badge ${statusColors[booking.status]}`}>
                        {translateBookingStatus(booking.status)}
                    </span>
                </div>

                {/* Details Grid */}
                <div className="grid grid-cols-2 gap-4 mb-6">
                    <div>
                        <div className="text-sm text-gray-500">مهمان</div>
                        <div className="font-medium">{booking.guest_name}</div>
                    </div>
                    <div>
                        <div className="text-sm text-gray-500">تعداد شب</div>
                        <div className="font-medium">{booking.nights} شب</div>
                    </div>
                    <div>
                        <div className="text-sm text-gray-500">تاریخ ورود</div>
                        <div className="font-medium">{formatJalaliDate(booking.check_in)}</div>
                    </div>
                    <div>
                        <div className="text-sm text-gray-500">تاریخ خروج</div>
                        <div className="font-medium">{formatJalaliDate(booking.check_out)}</div>
                    </div>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">
                        {error}
                    </div>
                )}

                {/* Action Buttons */}
                <div className="flex gap-3">
                    {/* Check-in Button */}
                    {(booking.status === 'pending' || booking.status === 'confirmed') && (
                        <button
                            onClick={() => handleAction('checkin')}
                            disabled={loading}
                            className="flex-1 bg-green-500 text-white py-3 rounded-lg font-medium 
                        hover:bg-green-600 transition-colors disabled:opacity-50
                        flex items-center justify-center gap-2"
                        >
                            <span className="material-symbols-outlined">login</span>
                            ثبت ورود
                        </button>
                    )}

                    {/* Check-out Button */}
                    {booking.status === 'checked_in' && (
                        <button
                            onClick={() => handleAction('checkout')}
                            disabled={loading}
                            className="flex-1 bg-blue-500 text-white py-3 rounded-lg font-medium 
                        hover:bg-blue-600 transition-colors disabled:opacity-50
                        flex items-center justify-center gap-2"
                        >
                            <span className="material-symbols-outlined">logout</span>
                            ثبت خروج
                        </button>
                    )}

                    {/* Cancel Button */}
                    {(booking.status === 'pending' || booking.status === 'confirmed') && (
                        <button
                            onClick={() => handleAction('cancel')}
                            disabled={loading}
                            className="bg-red-100 text-red-600 py-3 px-4 rounded-lg font-medium 
                        hover:bg-red-200 transition-colors disabled:opacity-50
                        flex items-center justify-center gap-2"
                        >
                            <span className="material-symbols-outlined">cancel</span>
                            لغو
                        </button>
                    )}

                    {/* Close Button for completed bookings */}
                    {(booking.status === 'checked_out' || booking.status === 'cancelled') && (
                        <button
                            onClick={onClose}
                            className="flex-1 bg-gray-200 text-gray-700 py-3 rounded-lg font-medium 
                        hover:bg-gray-300 transition-colors"
                        >
                            بستن
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}
