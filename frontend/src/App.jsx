/**
 * Hotel Management System - Front Desk App
 * سیستم مدیریت هتل - پنل پذیرش
 */

import { useState } from 'react';
import Header from './components/Header';
import DashboardStats from './components/DashboardStats';
import TapeChart from './components/TapeChart';
import RoomStatusPanel from './components/RoomStatusPanel';
import BookingModal from './components/BookingModal';

export default function App() {
    const [selectedBooking, setSelectedBooking] = useState(null);
    const [refreshKey, setRefreshKey] = useState(0);
    const [activeTab, setActiveTab] = useState('tapechart');

    const handleBookingClick = (booking) => {
        setSelectedBooking(booking);
    };

    const handleBookingUpdate = () => {
        setRefreshKey((prev) => prev + 1);
    };

    return (
        <div className="min-h-screen bg-gray-100">
            {/* Header */}
            <Header />

            {/* Main Content */}
            <main className="container mx-auto px-6 py-6">
                {/* Dashboard Stats */}
                <section className="mb-6">
                    <DashboardStats key={`stats-${refreshKey}`} />
                </section>

                {/* Tab Navigation */}
                <div className="flex gap-2 mb-6">
                    <button
                        onClick={() => setActiveTab('tapechart')}
                        className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${activeTab === 'tapechart'
                                ? 'bg-primary-500 text-white shadow-md'
                                : 'bg-white text-gray-600 hover:bg-gray-50'
                            }`}
                    >
                        <span className="material-symbols-outlined">calendar_month</span>
                        نمودار رزرواسیون
                    </button>
                    <button
                        onClick={() => setActiveTab('rooms')}
                        className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${activeTab === 'rooms'
                                ? 'bg-primary-500 text-white shadow-md'
                                : 'bg-white text-gray-600 hover:bg-gray-50'
                            }`}
                    >
                        <span className="material-symbols-outlined">bed</span>
                        وضعیت اتاق‌ها
                    </button>
                </div>

                {/* Content Sections */}
                {activeTab === 'tapechart' && (
                    <section className="animate-fade-in">
                        <TapeChart
                            key={`chart-${refreshKey}`}
                            onBookingClick={handleBookingClick}
                        />
                    </section>
                )}

                {activeTab === 'rooms' && (
                    <section className="animate-fade-in">
                        <RoomStatusPanel key={`rooms-${refreshKey}`} />
                    </section>
                )}
            </main>

            {/* Booking Modal */}
            {selectedBooking && (
                <BookingModal
                    booking={selectedBooking}
                    onClose={() => setSelectedBooking(null)}
                    onUpdate={handleBookingUpdate}
                />
            )}

            {/* Footer */}
            <footer className="bg-white border-t py-4 mt-8">
                <div className="container mx-auto px-6 text-center text-gray-500 text-sm">
                    سیستم مدیریت هتل - نسخه ۱.۰.۰
                </div>
            </footer>
        </div>
    );
}
