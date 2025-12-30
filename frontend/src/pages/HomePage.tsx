import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Search, Calendar, Users, Star, Wifi, Car, Coffee, Waves } from 'lucide-react';

export default function HomePage() {
    const navigate = useNavigate();
    const [checkIn, setCheckIn] = useState('');
    const [checkOut, setCheckOut] = useState('');
    const [guests, setGuests] = useState('2');

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        navigate(`/rooms?checkIn=${checkIn}&checkOut=${checkOut}&guests=${guests}`);
    };

    return (
        <div>
            {/* Hero Section */}
            <section className="relative h-[600px] bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 overflow-hidden">
                {/* Background Pattern */}
                <div className="absolute inset-0 opacity-20">
                    <div className="absolute inset-0" style={{
                        backgroundImage: 'url("data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%23ffffff" fill-opacity="0.4"%3E%3Ccircle cx="30" cy="30" r="2"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")',
                    }} />
                </div>

                <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex flex-col justify-center">
                    <div className="text-center text-white mb-12">
                        <h1 className="text-5xl md:text-6xl font-bold mb-6">
                            Experience Luxury<br />
                            <span className="text-pink-300">Like Never Before</span>
                        </h1>
                        <p className="text-xl text-gray-200 max-w-2xl mx-auto">
                            Discover world-class amenities, stunning views, and unforgettable experiences at LuxeStay Hotel.
                        </p>
                    </div>

                    {/* Search Form */}
                    <form onSubmit={handleSearch} className="glass rounded-2xl p-6 max-w-4xl mx-auto w-full shadow-2xl">
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                            <div>
                                <label className="label text-gray-600">Check In</label>
                                <div className="relative">
                                    <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                                    <input
                                        type="date"
                                        value={checkIn}
                                        onChange={(e) => setCheckIn(e.target.value)}
                                        className="input pl-10"
                                        required
                                    />
                                </div>
                            </div>
                            <div>
                                <label className="label text-gray-600">Check Out</label>
                                <div className="relative">
                                    <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                                    <input
                                        type="date"
                                        value={checkOut}
                                        onChange={(e) => setCheckOut(e.target.value)}
                                        className="input pl-10"
                                        required
                                    />
                                </div>
                            </div>
                            <div>
                                <label className="label text-gray-600">Guests</label>
                                <div className="relative">
                                    <Users className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                                    <select
                                        value={guests}
                                        onChange={(e) => setGuests(e.target.value)}
                                        className="input pl-10 appearance-none"
                                    >
                                        {[1, 2, 3, 4, 5, 6].map((n) => (
                                            <option key={n} value={n}>{n} Guest{n > 1 ? 's' : ''}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>
                            <div className="flex items-end">
                                <button type="submit" className="btn-primary w-full btn-lg">
                                    <Search className="h-5 w-5 mr-2" />
                                    Search
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-20 bg-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl font-bold text-gray-900 mb-4">Why Choose LuxeStay?</h2>
                        <p className="text-gray-600 max-w-2xl mx-auto">
                            We offer an unparalleled experience with world-class amenities and exceptional service.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                        {[
                            { icon: Wifi, title: 'High-Speed WiFi', desc: 'Stay connected with complimentary high-speed internet' },
                            { icon: Car, title: 'Free Parking', desc: 'Secure parking available for all guests' },
                            { icon: Coffee, title: 'Breakfast', desc: 'Start your day with our gourmet breakfast' },
                            { icon: Waves, title: 'Pool & Spa', desc: 'Relax in our infinity pool and luxury spa' },
                        ].map((feature, i) => (
                            <div key={i} className="text-center p-6">
                                <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-100 rounded-2xl mb-4">
                                    <feature.icon className="h-8 w-8 text-indigo-600" />
                                </div>
                                <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
                                <p className="text-gray-600 text-sm">{feature.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Featured Rooms */}
            <section className="py-20 bg-gray-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-end mb-12">
                        <div>
                            <h2 className="text-3xl font-bold text-gray-900 mb-2">Featured Rooms</h2>
                            <p className="text-gray-600">Explore our most popular accommodations</p>
                        </div>
                        <Link to="/rooms" className="btn-secondary">
                            View All Rooms
                        </Link>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {[
                            { name: 'Deluxe Suite', price: 250, rating: 4.9, image: 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800' },
                            { name: 'Ocean View Room', price: 180, rating: 4.8, image: 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800' },
                            { name: 'Penthouse', price: 500, rating: 5.0, image: 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800' },
                        ].map((room, i) => (
                            <div key={i} className="card group cursor-pointer" onClick={() => navigate('/rooms')}>
                                <div className="relative h-64 overflow-hidden">
                                    <img
                                        src={room.image}
                                        alt={room.name}
                                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                                    />
                                    <div className="absolute top-4 right-4 bg-white/90 backdrop-blur px-3 py-1 rounded-full flex items-center gap-1">
                                        <Star className="h-4 w-4 text-yellow-500 fill-yellow-500" />
                                        <span className="text-sm font-medium">{room.rating}</span>
                                    </div>
                                </div>
                                <div className="p-6">
                                    <h3 className="text-xl font-semibold text-gray-900 mb-2">{room.name}</h3>
                                    <div className="flex items-baseline gap-1">
                                        <span className="text-2xl font-bold text-indigo-600">${room.price}</span>
                                        <span className="text-gray-500">/ night</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 bg-indigo-600">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h2 className="text-3xl font-bold text-white mb-4">
                        Ready to Experience Luxury?
                    </h2>
                    <p className="text-indigo-100 mb-8 text-lg">
                        Book your stay today and enjoy exclusive member benefits.
                    </p>
                    <Link to="/booking" className="inline-flex items-center px-8 py-4 bg-white text-indigo-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors">
                        Book Your Stay
                    </Link>
                </div>
            </section>
        </div>
    );
}
