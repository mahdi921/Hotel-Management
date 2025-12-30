/**
 * Header Component
 * هدر سیستم
 */

import { formatJalaliDate } from '../utils';

export default function Header() {
    const today = new Date();

    return (
        <header className="bg-gradient-to-l from-primary-600 to-primary-700 text-white shadow-lg">
            <div className="container mx-auto px-6 py-4">
                <div className="flex items-center justify-between">
                    {/* Logo & Title */}
                    <div className="flex items-center gap-3">
                        <div className="bg-white/20 p-2 rounded-lg">
                            <span className="material-symbols-outlined text-3xl">hotel</span>
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold">سیستم مدیریت هتل</h1>
                            <p className="text-primary-100 text-sm">پنل پذیرش</p>
                        </div>
                    </div>

                    {/* Date & User */}
                    <div className="flex items-center gap-6">
                        {/* Current Date */}
                        <div className="text-left">
                            <div className="text-primary-100 text-sm">امروز</div>
                            <div className="font-bold">{formatJalaliDate(today)}</div>
                        </div>

                        {/* User Menu */}
                        <div className="flex items-center gap-2 bg-white/10 rounded-lg px-4 py-2">
                            <span className="material-symbols-outlined">person</span>
                            <span>کاربر پذیرش</span>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    );
}
