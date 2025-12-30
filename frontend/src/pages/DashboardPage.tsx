import { useState, useEffect } from 'react';
import { Calendar, Users, DollarSign, Bed, TrendingUp, Clock } from 'lucide-react';
import axios from 'axios';

interface Booking {
    id: number;
    guest: { username: string };
    room: { room_number: string };
    check_in: string;
    check_out: string;
    status: string;
    total_price: number;
}

interface Room {
    id: number;
    room_number: string;
    status: string;
    room_type: { name: string };
}

export default function DashboardPage() {
    const [rooms, setRooms] = useState<Room[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get('/api/rooms/')
            .then(res => {
                setRooms(res.data);
                setLoading(false);
            })
            .catch(() => setLoading(false));
    }, []);

    const stats = {
        totalRooms: rooms.length,
        available: rooms.filter(r => r.status === 'available').length,
        occupied: rooms.filter(r => r.status === 'occupied').length,
        occupancyRate: rooms.length > 0
            ? Math.round((rooms.filter(r => r.status === 'occupied').length / rooms.length) * 100)
            : 0,
    };

    const recentActivity = [
        { type: 'check_in', guest: 'John Doe', room: '101', time: '2 hours ago' },
        { type: 'booking', guest: 'Jane Smith', room: '205', time: '4 hours ago' },
        { type: 'check_out', guest: 'Mike Johnson', room: '302', time: '6 hours ago' },
        { type: 'booking', guest: 'Sarah Wilson', room: '108', time: '1 day ago' },
    ];

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-white border-b">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
                    <p className="text-gray-500">Hotel management overview</p>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    {[
                        { label: 'Total Rooms', value: stats.totalRooms, icon: Bed, color: 'bg-blue-500' },
                        { label: 'Available', value: stats.available, icon: Calendar, color: 'bg-green-500' },
                        { label: 'Occupied', value: stats.occupied, icon: Users, color: 'bg-orange-500' },
                        { label: 'Occupancy Rate', value: `${stats.occupancyRate}%`, icon: TrendingUp, color: 'bg-purple-500' },
                    ].map((stat, i) => (
                        <div key={i} className="card p-6">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm text-gray-500">{stat.label}</p>
                                    <p className="text-3xl font-bold text-gray-900 mt-1">{stat.value}</p>
                                </div>
                                <div className={`${stat.color} p-3 rounded-xl`}>
                                    <stat.icon className="h-6 w-6 text-white" />
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Room Grid / Heatmap */}
                    <div className="lg:col-span-2 card p-6">
                        <h2 className="text-lg font-semibold text-gray-900 mb-4">Room Status Overview</h2>
                        <div className="grid grid-cols-5 md:grid-cols-10 gap-2">
                            {rooms.map((room) => (
                                <div
                                    key={room.id}
                                    className={`aspect-square rounded-lg flex items-center justify-center text-xs font-medium cursor-pointer transition-transform hover:scale-110 ${room.status === 'available'
                                            ? 'bg-green-100 text-green-800 hover:bg-green-200'
                                            : room.status === 'occupied'
                                                ? 'bg-orange-100 text-orange-800 hover:bg-orange-200'
                                                : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                                        }`}
                                    title={`Room ${room.room_number} - ${room.status}`}
                                >
                                    {room.room_number}
                                </div>
                            ))}
                        </div>
                        <div className="flex gap-6 mt-4 text-sm">
                            <div className="flex items-center gap-2">
                                <div className="w-4 h-4 bg-green-100 rounded" />
                                <span className="text-gray-600">Available</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <div className="w-4 h-4 bg-orange-100 rounded" />
                                <span className="text-gray-600">Occupied</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <div className="w-4 h-4 bg-gray-100 rounded" />
                                <span className="text-gray-600">Maintenance</span>
                            </div>
                        </div>
                    </div>

                    {/* Recent Activity */}
                    <div className="card p-6">
                        <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
                        <div className="space-y-4">
                            {recentActivity.map((activity, i) => (
                                <div key={i} className="flex items-start gap-3">
                                    <div className={`p-2 rounded-lg ${activity.type === 'check_in' ? 'bg-green-100' :
                                            activity.type === 'check_out' ? 'bg-red-100' : 'bg-blue-100'
                                        }`}>
                                        {activity.type === 'check_in' ? (
                                            <Users className="h-4 w-4 text-green-600" />
                                        ) : activity.type === 'check_out' ? (
                                            <Users className="h-4 w-4 text-red-600" />
                                        ) : (
                                            <Calendar className="h-4 w-4 text-blue-600" />
                                        )}
                                    </div>
                                    <div className="flex-1">
                                        <p className="text-sm font-medium text-gray-900">
                                            {activity.type === 'check_in' ? 'Check In' :
                                                activity.type === 'check_out' ? 'Check Out' : 'New Booking'}
                                        </p>
                                        <p className="text-sm text-gray-500">
                                            {activity.guest} - Room {activity.room}
                                        </p>
                                    </div>
                                    <span className="text-xs text-gray-400">{activity.time}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Quick Actions */}
                <div className="mt-8 card p-6">
                    <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <a href="/admin/" className="btn-secondary text-center">
                            Django Admin
                        </a>
                        <a href="/api/docs" className="btn-secondary text-center">
                            API Docs
                        </a>
                        <button className="btn-secondary">Export Report</button>
                        <button className="btn-primary">New Booking</button>
                    </div>
                </div>
            </div>
        </div>
    );
}
