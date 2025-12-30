/**
 * Tape Chart Component
 * نمودار نواری رزرواسیون (Timeline View)
 * 
 * Shows rooms on Y-axis, dates on X-axis, and bookings as colored blocks.
 */

import { useState, useEffect, useMemo } from 'react';
import { getTapeChartData } from '../api';
import {
    formatJalaliShort,
    getWeekdayName,
    getDateRange,
    formatDateForApi,
    translateBookingStatus,
    toJalali
} from '../utils';

export default function TapeChart({ onBookingClick }) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [startOffset, setStartOffset] = useState(0);
    const [daysToShow, setDaysToShow] = useState(14);

    // Generate date columns
    const dateColumns = useMemo(() => getDateRange(startOffset, daysToShow), [startOffset, daysToShow]);

    const startDate = formatDateForApi(dateColumns[0]);
    const endDate = formatDateForApi(dateColumns[dateColumns.length - 1]);

    // Fetch tape chart data
    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await getTapeChartData(startDate, endDate);
                setData(response.data);
                setError(null);
            } catch (err) {
                setError('خطا در دریافت اطلاعات');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [startDate, endDate]);

    // Navigate to previous/next period
    const goToPrevious = () => setStartOffset(prev => prev - 7);
    const goToNext = () => setStartOffset(prev => prev + 7);
    const goToToday = () => setStartOffset(0);

    // Calculate booking position and width
    const getBookingStyle = (booking, dateColumns) => {
        const bookingStart = new Date(booking.check_in);
        const bookingEnd = new Date(booking.check_out);
        const chartStart = dateColumns[0];
        const chartEnd = dateColumns[dateColumns.length - 1];

        // Calculate visible portion
        const visibleStart = bookingStart < chartStart ? chartStart : bookingStart;
        const visibleEnd = bookingEnd > chartEnd ? chartEnd : bookingEnd;

        // Calculate position (days from chart start)
        const startDay = Math.floor((visibleStart - chartStart) / (1000 * 60 * 60 * 24));
        const duration = Math.ceil((visibleEnd - visibleStart) / (1000 * 60 * 60 * 24));

        // Cell width is 48px
        const cellWidth = 48;
        const left = startDay * cellWidth;
        const width = duration * cellWidth - 4; // -4 for padding

        return {
            right: `${left}px`,
            width: `${width}px`,
        };
    };

    // Check if a date is today
    const isToday = (date) => {
        const today = new Date();
        return date.toDateString() === today.toDateString();
    };

    // Check if a date is a weekend (Friday in Iran)
    const isWeekend = (date) => {
        return date.getDay() === 5; // Friday
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 text-red-600 p-4 rounded-lg text-center">
                {error}
                <button onClick={() => setStartOffset(0)} className="mr-4 underline">
                    تلاش مجدد
                </button>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            {/* Header Controls */}
            <div className="flex items-center justify-between p-4 border-b bg-gray-50">
                <div className="flex items-center gap-2">
                    <button
                        onClick={goToPrevious}
                        className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
                        title="هفته قبل"
                    >
                        <span className="material-symbols-outlined">chevron_right</span>
                    </button>
                    <button
                        onClick={goToToday}
                        className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
                    >
                        امروز
                    </button>
                    <button
                        onClick={goToNext}
                        className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
                        title="هفته بعد"
                    >
                        <span className="material-symbols-outlined">chevron_left</span>
                    </button>
                </div>

                <div className="text-lg font-bold text-gray-700">
                    {formatJalaliShort(dateColumns[0])} - {formatJalaliShort(dateColumns[dateColumns.length - 1])}
                </div>

                <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-600">نمایش:</span>
                    <select
                        value={daysToShow}
                        onChange={(e) => setDaysToShow(Number(e.target.value))}
                        className="border rounded-lg px-3 py-2 text-sm"
                    >
                        <option value={7}>۷ روز</option>
                        <option value={14}>۱۴ روز</option>
                        <option value={21}>۲۱ روز</option>
                        <option value={30}>۳۰ روز</option>
                    </select>
                </div>
            </div>

            {/* Legend */}
            <div className="flex items-center gap-4 px-4 py-2 bg-gray-50 border-b text-sm">
                <span className="text-gray-600">وضعیت رزرو:</span>
                <span className="flex items-center gap-1">
                    <span className="w-3 h-3 rounded bg-amber-500"></span>
                    در انتظار
                </span>
                <span className="flex items-center gap-1">
                    <span className="w-3 h-3 rounded bg-blue-500"></span>
                    تایید شده
                </span>
                <span className="flex items-center gap-1">
                    <span className="w-3 h-3 rounded bg-green-500"></span>
                    ورود انجام شد
                </span>
            </div>

            {/* Tape Chart Grid */}
            <div className="tape-chart-container max-h-[600px]">
                <div className="min-w-max">
                    {/* Date Header Row */}
                    <div className="flex sticky top-0 z-30 bg-white">
                        {/* Room Label Column Header */}
                        <div className="w-32 flex-shrink-0 bg-gray-100 border-b border-l p-2 sticky right-0 z-40">
                            <span className="font-bold text-gray-700">اتاق</span>
                        </div>

                        {/* Date Columns */}
                        {dateColumns.map((date, idx) => {
                            const jalali = toJalali(date);
                            return (
                                <div
                                    key={idx}
                                    className={`w-12 flex-shrink-0 border-b border-l p-1 text-center ${isToday(date) ? 'bg-primary-100 font-bold' :
                                            isWeekend(date) ? 'bg-red-50' : 'bg-gray-100'
                                        }`}
                                >
                                    <div className="text-xs text-gray-500">{getWeekdayName(date).slice(0, 2)}</div>
                                    <div className={`text-sm font-bold ${isToday(date) ? 'text-primary-600' : 'text-gray-700'}`}>
                                        {jalali.day}
                                    </div>
                                    {jalali.day === 1 && (
                                        <div className="text-[10px] text-gray-400">
                                            {['فرو', 'ارد', 'خرد', 'تیر', 'مرد', 'شهر', 'مهر', 'آبا', 'آذر', 'دی', 'بهم', 'اسف'][jalali.month - 1]}
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </div>

                    {/* Room Rows */}
                    {data?.rooms?.map((room) => (
                        <div key={room.room_id} className="flex relative">
                            {/* Room Label */}
                            <div
                                className={`w-32 flex-shrink-0 border-b border-l p-2 sticky right-0 z-20 
                  ${room.status === 'clean' ? 'bg-green-50' :
                                        room.status === 'dirty' ? 'bg-amber-50' :
                                            room.status === 'occupied' ? 'bg-blue-50' :
                                                room.status === 'maintenance' ? 'bg-red-50' : 'bg-gray-50'}`}
                            >
                                <div className="font-bold text-gray-800">{room.room_number}</div>
                                <div className="text-xs text-gray-500">{room.room_type}</div>
                            </div>

                            {/* Date Cells */}
                            <div className="flex relative">
                                {dateColumns.map((date, idx) => (
                                    <div
                                        key={idx}
                                        className={`w-12 h-12 flex-shrink-0 border-b border-l ${isToday(date) ? 'bg-primary-50' :
                                                isWeekend(date) ? 'bg-red-50/30' : 'bg-white'
                                            }`}
                                    />
                                ))}

                                {/* Booking Blocks */}
                                {room.bookings?.map((booking) => (
                                    <div
                                        key={booking.id}
                                        className={`booking-block booking-${booking.status}`}
                                        style={getBookingStyle(booking, dateColumns)}
                                        onClick={() => onBookingClick?.(booking)}
                                        title={`${booking.guest_name} - ${translateBookingStatus(booking.status)}`}
                                    >
                                        <div className="truncate">{booking.guest_name}</div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Empty State */}
            {(!data?.rooms || data.rooms.length === 0) && (
                <div className="p-8 text-center text-gray-500">
                    <span className="material-symbols-outlined text-4xl mb-2">hotel</span>
                    <p>اتاقی برای نمایش وجود ندارد</p>
                </div>
            )}
        </div>
    );
}
