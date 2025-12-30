/**
 * Room Status Panel Component
 * پنل وضعیت اتاق‌ها
 */

import { useState, useEffect } from 'react';
import { getRooms, updateRoomStatus } from '../api';
import { translateRoomStatus } from '../utils';

export default function RoomStatusPanel() {
    const [rooms, setRooms] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('all');

    const fetchRooms = async () => {
        try {
            const params = filter !== 'all' ? { status: filter } : {};
            const response = await getRooms(params);
            setRooms(response.data);
        } catch (err) {
            console.error('Failed to fetch rooms:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRooms();
    }, [filter]);

    const handleStatusChange = async (roomId, newStatus) => {
        try {
            await updateRoomStatus(roomId, newStatus);
            fetchRooms();
        } catch (err) {
            console.error('Failed to update room status:', err);
        }
    };

    const statusColors = {
        clean: 'bg-green-100 text-green-700 border-green-300',
        dirty: 'bg-amber-100 text-amber-700 border-amber-300',
        occupied: 'bg-blue-100 text-blue-700 border-blue-300',
        maintenance: 'bg-red-100 text-red-700 border-red-300',
    };

    const statusIcons = {
        clean: 'check_circle',
        dirty: 'cleaning_services',
        occupied: 'person',
        maintenance: 'build',
    };

    if (loading) {
        return (
            <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="animate-pulse space-y-4">
                    <div className="h-8 bg-gray-200 rounded w-1/3"></div>
                    <div className="grid grid-cols-4 gap-4">
                        {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
                            <div key={i} className="h-20 bg-gray-100 rounded-lg"></div>
                        ))}
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            {/* Header */}
            <div className="p-4 border-b bg-gray-50 flex items-center justify-between">
                <h2 className="text-lg font-bold text-gray-800 flex items-center gap-2">
                    <span className="material-symbols-outlined">bed</span>
                    وضعیت اتاق‌ها
                </h2>

                {/* Filter Tabs */}
                <div className="flex gap-2">
                    {['all', 'clean', 'dirty', 'occupied', 'maintenance'].map((status) => (
                        <button
                            key={status}
                            onClick={() => setFilter(status)}
                            className={`px-3 py-1 rounded-full text-sm transition-all ${filter === status
                                    ? 'bg-primary-500 text-white'
                                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                                }`}
                        >
                            {status === 'all' ? 'همه' : translateRoomStatus(status)}
                        </button>
                    ))}
                </div>
            </div>

            {/* Room Grid */}
            <div className="p-4">
                <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-3">
                    {rooms.map((room) => (
                        <div
                            key={room.id}
                            className={`p-3 rounded-lg border-2 transition-all cursor-pointer hover:shadow-md ${statusColors[room.status]}`}
                        >
                            <div className="flex items-center justify-between mb-1">
                                <span className="font-bold text-lg">{room.room_number}</span>
                                <span className="material-symbols-outlined text-sm">{statusIcons[room.status]}</span>
                            </div>
                            <div className="text-xs opacity-75">{room.room_type_name}</div>

                            {/* Quick Status Change */}
                            {room.status === 'dirty' && (
                                <button
                                    onClick={() => handleStatusChange(room.id, 'clean')}
                                    className="mt-2 w-full text-xs bg-green-500 text-white py-1 rounded hover:bg-green-600 transition-colors"
                                >
                                    تمیز شد
                                </button>
                            )}
                        </div>
                    ))}
                </div>

                {rooms.length === 0 && (
                    <div className="text-center py-8 text-gray-500">
                        اتاقی با این فیلتر یافت نشد
                    </div>
                )}
            </div>
        </div>
    );
}
