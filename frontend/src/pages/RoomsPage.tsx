import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { Star, Users, Wifi, Tv, Coffee, Wind } from 'lucide-react';
import axios from 'axios';

interface RoomType {
    id: number;
    name: string;
    base_rate: number;
}

interface Room {
    id: number;
    room_number: string;
    status: string;
    room_type: RoomType;
}

export default function RoomsPage() {
    const [searchParams] = useSearchParams();
    const [rooms, setRooms] = useState<Room[]>([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('all');

    useEffect(() => {
        axios.get('/api/rooms/')
            .then(res => {
                setRooms(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    }, []);

    const filteredRooms = filter === 'all'
        ? rooms
        : rooms.filter(r => r.status === filter);

    const getAmenityIcons = () => [
        { icon: Wifi, label: 'Wi-Fi' },
        { icon: Tv, label: 'TV' },
        { icon: Coffee, label: 'Mini Bar' },
        { icon: Wind, label: 'AC' },
    ];

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
            </div>
        );
    }

    return (
        <div className="bg-gray-50 min-h-screen">
            {/* Header */}
            <div className="bg-indigo-600 py-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <h1 className="text-4xl font-bold text-white mb-4">Our Rooms</h1>
                    <p className="text-indigo-100 text-lg">
                        Find the perfect room for your stay
                    </p>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                {/* Filters */}
                <div className="flex flex-wrap gap-4 mb-8">
                    {[
                        { value: 'all', label: 'All Rooms' },
                        { value: 'available', label: 'Available' },
                        { value: 'occupied', label: 'Occupied' },
                    ].map((f) => (
                        <button
                            key={f.value}
                            onClick={() => setFilter(f.value)}
                            className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === f.value
                                    ? 'bg-indigo-600 text-white'
                                    : 'bg-white text-gray-600 hover:bg-gray-100'
                                }`}
                        >
                            {f.label}
                        </button>
                    ))}
                </div>

                {/* Room Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {filteredRooms.map((room) => (
                        <Link
                            key={room.id}
                            to={`/rooms/${room.id}`}
                            className="card group"
                        >
                            <div className="relative h-56 overflow-hidden bg-gradient-to-br from-indigo-500 to-purple-600">
                                <div className="absolute inset-0 flex items-center justify-center">
                                    <span className="text-6xl font-bold text-white/20">{room.room_number}</span>
                                </div>
                                <div className="absolute top-4 right-4">
                                    <span className={`badge ${room.status === 'available' ? 'badge-success' : 'badge-warning'
                                        }`}>
                                        {room.status}
                                    </span>
                                </div>
                            </div>
                            <div className="p-6">
                                <div className="flex justify-between items-start mb-4">
                                    <div>
                                        <h3 className="text-xl font-semibold text-gray-900 group-hover:text-indigo-600 transition-colors">
                                            {room.room_type.name}
                                        </h3>
                                        <p className="text-gray-500">Room {room.room_number}</p>
                                    </div>
                                    <div className="flex items-center gap-1 text-yellow-500">
                                        <Star className="h-4 w-4 fill-current" />
                                        <span className="text-sm font-medium text-gray-700">4.8</span>
                                    </div>
                                </div>

                                {/* Amenities */}
                                <div className="flex gap-3 mb-4">
                                    {getAmenityIcons().map((amenity, i) => (
                                        <div key={i} className="text-gray-400" title={amenity.label}>
                                            <amenity.icon className="h-5 w-5" />
                                        </div>
                                    ))}
                                </div>

                                {/* Price */}
                                <div className="flex items-baseline justify-between pt-4 border-t border-gray-100">
                                    <div>
                                        <span className="text-2xl font-bold text-indigo-600">
                                            ${Number(room.room_type.base_rate).toFixed(0)}
                                        </span>
                                        <span className="text-gray-500 text-sm"> / night</span>
                                    </div>
                                    <Users className="h-5 w-5 text-gray-400" />
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>

                {filteredRooms.length === 0 && (
                    <div className="text-center py-12">
                        <p className="text-gray-500 text-lg">No rooms found</p>
                    </div>
                )}
            </div>
        </div>
    );
}
