import { Outlet, Link } from 'react-router-dom';
import { Hotel, Menu, X, User } from 'lucide-react';
import { useState } from 'react';

export default function Layout() {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    return (
        <div className="min-h-screen flex flex-col">
            {/* Header */}
            <header className="glass sticky top-0 z-50 border-b border-gray-200">
                <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16 items-center">
                        {/* Logo */}
                        <Link to="/" className="flex items-center gap-2">
                            <Hotel className="h-8 w-8 text-indigo-600" />
                            <span className="text-xl font-bold text-gradient">LuxeStay</span>
                        </Link>

                        {/* Desktop Nav */}
                        <div className="hidden md:flex items-center gap-8">
                            <Link to="/" className="text-gray-600 hover:text-indigo-600 transition-colors">
                                Home
                            </Link>
                            <Link to="/rooms" className="text-gray-600 hover:text-indigo-600 transition-colors">
                                Rooms
                            </Link>
                            <Link to="/dashboard" className="text-gray-600 hover:text-indigo-600 transition-colors">
                                Dashboard
                            </Link>
                            <a href="/admin/" className="text-gray-600 hover:text-indigo-600 transition-colors">
                                Admin
                            </a>
                        </div>

                        {/* Auth Buttons */}
                        <div className="hidden md:flex items-center gap-4">
                            <button className="btn-secondary">
                                <User className="h-4 w-4 mr-2" />
                                Sign In
                            </button>
                            <Link to="/booking" className="btn-primary">
                                Book Now
                            </Link>
                        </div>

                        {/* Mobile Menu Button */}
                        <button
                            className="md:hidden"
                            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        >
                            {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                        </button>
                    </div>

                    {/* Mobile Nav */}
                    {mobileMenuOpen && (
                        <div className="md:hidden py-4 border-t border-gray-200">
                            <div className="flex flex-col gap-4">
                                <Link to="/" className="text-gray-600 hover:text-indigo-600">Home</Link>
                                <Link to="/rooms" className="text-gray-600 hover:text-indigo-600">Rooms</Link>
                                <Link to="/dashboard" className="text-gray-600 hover:text-indigo-600">Dashboard</Link>
                                <Link to="/booking" className="btn-primary text-center">Book Now</Link>
                            </div>
                        </div>
                    )}
                </nav>
            </header>

            {/* Main Content */}
            <main className="flex-1">
                <Outlet />
            </main>

            {/* Footer */}
            <footer className="bg-gray-900 text-white py-12">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                        <div>
                            <div className="flex items-center gap-2 mb-4">
                                <Hotel className="h-6 w-6" />
                                <span className="text-lg font-bold">LuxeStay</span>
                            </div>
                            <p className="text-gray-400 text-sm">
                                Experience luxury and comfort at its finest.
                            </p>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-4">Quick Links</h4>
                            <ul className="space-y-2 text-gray-400 text-sm">
                                <li><Link to="/rooms" className="hover:text-white">Rooms</Link></li>
                                <li><Link to="/booking" className="hover:text-white">Book Now</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-4">Contact</h4>
                            <ul className="space-y-2 text-gray-400 text-sm">
                                <li>+1 (555) 123-4567</li>
                                <li>info@luxestay.com</li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-4">Address</h4>
                            <p className="text-gray-400 text-sm">
                                123 Luxury Avenue<br />
                                New York, NY 10001
                            </p>
                        </div>
                    </div>
                    <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400 text-sm">
                        © 2024 LuxeStay. All rights reserved.
                    </div>
                </div>
            </footer>
        </div>
    );
}
