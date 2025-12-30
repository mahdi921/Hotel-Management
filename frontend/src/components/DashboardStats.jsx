/**
 * Dashboard Stats Component
 * کارت‌های آماری داشبورد
 */

import { useState, useEffect } from 'react';
import { getDashboardStats } from '../api';

export default function DashboardStats() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await getDashboardStats();
                setStats(response.data);
            } catch (err) {
                console.error('Failed to fetch stats:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
        // Refresh every 30 seconds
        const interval = setInterval(fetchStats, 30000);
        return () => clearInterval(interval);
    }, []);

    if (loading) {
        return (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[1, 2, 3, 4].map((i) => (
                    <div key={i} className="bg-gray-100 rounded-xl h-28 animate-pulse"></div>
                ))}
            </div>
        );
    }

    const statCards = [
        {
            title: 'نیازمند نظافت',
            value: stats?.rooms_dirty || 0,
            icon: 'cleaning_services',
            color: 'from-amber-500 to-orange-600',
            bgLight: 'amber',
        },
        {
            title: 'ورودی امروز',
            value: stats?.today_checkins || 0,
            icon: 'login',
            color: 'from-emerald-500 to-green-600',
            bgLight: 'emerald',
        },
        {
            title: 'خروجی امروز',
            value: stats?.today_checkouts || 0,
            icon: 'logout',
            color: 'from-blue-500 to-indigo-600',
            bgLight: 'blue',
        },
        {
            title: 'رزروهای فعال',
            value: stats?.bookings_active || 0,
            icon: 'hotel',
            color: 'from-purple-500 to-pink-600',
            bgLight: 'purple',
        },
    ];

    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {statCards.map((card, idx) => (
                <div
                    key={idx}
                    className={`bg-gradient-to-br ${card.color} rounded-xl p-5 text-white shadow-lg 
                     transition-all duration-300 hover:shadow-xl hover:-translate-y-1`}
                >
                    <div className="flex items-center justify-between">
                        <div>
                            <p className={`text-${card.bgLight}-100 text-sm`}>{card.title}</p>
                            <p className="text-3xl font-bold mt-1">{card.value}</p>
                        </div>
                        <div className="bg-white/20 rounded-full p-3">
                            <span className="material-symbols-outlined text-2xl">{card.icon}</span>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}
