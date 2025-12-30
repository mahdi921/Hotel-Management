import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Star, Users, Wifi, Tv, Coffee, Wind, MapPin, Calendar, ArrowLeft } from 'lucide-react';
import axios from 'axios';

interface Room {
    id: number;
    room_number: string;
    status: string;
    room_type: {
        id: number;
        name: string;
        base_rate: number;
    };
}

export default function RoomDetailPage() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [room, setRoom] = useState<Room | null>(null);
    const [loading, setLoading] = useState(true);
    const [checkIn, setCheckIn] = useState('');
    const [checkOut, setCheckOut] = useState('');

    useEffect(() => {
        axios.get(`/api/rooms/${id}`)
            .then(res => {
                setRoom(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    }, [id]);

    const handleBook = () => {
        if (room && checkIn && checkOut) {
            navigate(`/booking?roomId=${room.id}&checkIn=${checkIn}&checkOut=${checkOut}`);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
            </div>
        );
    }

    if (!room) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <p className="text-gray-500">Room not found</p>
            </div>
        );
    }

    return (
        <div className="bg-gray-50 min-h-screen">
            {/* Back Button */}
            <div className="bg-white border-b">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <button
                        onClick={() => navigate('/rooms')}
                        className="flex items-center text-gray-600 hover:text-indigo-600"
                    >
                        <ArrowLeft className="h-5 w-5 mr-2" />
                        Back to Rooms
                    </button>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Main Content */}
                    <div className="lg:col-span-2 space-y-8">
                        {/* Image Gallery */}
                        <div className="grid grid-cols-2 gap-4">
                            <div className="col-span-2 h-80 rounded-2xl overflow-hidden bg-gradient-to-br from-indigo-500 to-purple-600">
                                <div className="h-full flex items-center justify-center">
                                    <span className="text-8xl font-bold text-white/20">{room.room_number}</span>
                                </div>
                            </div>
                        </div>

                        {/* Room Info */}
                        <div>
                            <div className="flex items-center gap-2 mb-2">
                                <span className={`badge ${room.status === 'available' ? 'badge-success' : 'badge-warning'}`}>
                                    {room.status}
                                </span>
                                <div className="flex items-center text-yellow-500">
                                    <Star className="h-4 w-4 fill-current" />
                                    <span className="ml-1 text-sm font-medium text-gray-700">4.9 (128 reviews)</span>
                                </div>
                            </div>
                            <h1 className="text-3xl font-bold text-gray-900 mb-2">{room.room_type.name}</h1>
                            <p className="flex items-center text-gray-600">
                                <MapPin className="h-5 w-5 mr-2" />
                                Room {room.room_number}, Floor {Math.floor(Number(room.room_number) / 100)}
                            </p>
                        </div>

                        {/* Description */}
                        <div className="card p-6">
                            <h2 className="text-xl font-semibold text-gray-900 mb-4">About This Room</h2>
                            <p className="text-gray-600 leading-relaxed">
                                Experience luxury and comfort in our {room.room_type.name}. This elegantly appointed room
                                features modern amenities, plush bedding, and stunning views. Perfect for both business
                                and leisure travelers seeking a premium experience.
                            </p>
                        </div>

                        {/* Amenities */}
                        <div className="card p-6">
                            <h2 className="text-xl font-semibold text-gray-900 mb-4">Amenities</h2>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                {[
                                    { icon: Wifi, label: 'High-Speed WiFi' },
                                    { icon: Tv, label: '55" Smart TV' },
                                    { icon: Coffee, label: 'Mini Bar' },
                                    { icon: Wind, label: 'Climate Control' },
                                    { icon: Users, label: 'Up to 4 Guests' },
                                ].map((amenity, i) => (
                                    <div key={i} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                                        <amenity.icon className="h-5 w-5 text-indigo-600" />
                                        <span className="text-sm text-gray-700">{amenity.label}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Booking Card */}
                    <div className="lg:col-span-1">
                        <div className="card p-6 sticky top-24">
                            <div className="flex items-baseline gap-2 mb-6">
                                <span className="text-3xl font-bold text-indigo-600">
                                    ${Number(room.room_type.base_rate).toFixed(0)}
                                </span>
                                <span className="text-gray-500">/ night</span>
                            </div>

                            <div className="space-y-4 mb-6">
                                <div>
                                    <label className="label">Check In</label>
                                    <div className="relative">
                                        <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                                        <input
                                            type="date"
                                            value={checkIn}
                                            onChange={(e) => setCheckIn(e.target.value)}
                                            className="input pl-10"
                                        />
                                    </div>
                                </div>
                                <div>
                                    <label className="label">Check Out</label>
                                    <div className="relative">
                                        <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                                        <input
                                            type="date"
                                            value={checkOut}
                                            onChange={(e) => setCheckOut(e.target.value)}
                                            className="input pl-10"
                                        />
                                    </div>
                                </div>
                            </div>

                            <button
                                onClick={handleBook}
                                disabled={room.status !== 'available' || !checkIn || !checkOut}
                                className="btn-primary w-full btn-lg"
                            >
                                {room.status === 'available' ? 'Book Now' : 'Not Available'}
                            </button>

                            <p className="text-center text-sm text-gray-500 mt-4">
                                Free cancellation up to 24 hours before check-in
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
