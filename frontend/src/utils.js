/**
 * Persian/Jalali date utilities
 * تبدیل تاریخ میلادی به شمسی
 */

// Simple Jalali date converter (without external dependency for reliability)
export function toJalali(date) {
    const d = new Date(date);
    const gy = d.getFullYear();
    const gm = d.getMonth() + 1;
    const gd = d.getDate();

    const g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
    let jy = (gy <= 1600) ? 0 : 979;
    gy -= (gy <= 1600) ? 621 : 1600;
    const gy2 = (gm > 2) ? (gy + 1) : gy;
    let days = (365 * gy) + (Math.floor((gy2 + 3) / 4)) - (Math.floor((gy2 + 99) / 100)) + (Math.floor((gy2 + 399) / 400)) - 80 + gd + g_d_m[gm - 1];
    jy += 33 * (Math.floor(days / 12053));
    days %= 12053;
    jy += 4 * (Math.floor(days / 1461));
    days %= 1461;
    jy += Math.floor((days - 1) / 365);
    if (days > 365) days = (days - 1) % 365;
    const jm = (days < 186) ? 1 + Math.floor(days / 31) : 7 + Math.floor((days - 186) / 30);
    const jd = 1 + ((days < 186) ? (days % 31) : ((days - 186) % 30));

    return { year: jy, month: jm, day: jd };
}

export function formatJalaliDate(date) {
    const j = toJalali(date);
    const months = [
        'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
        'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
    ];
    return `${j.day} ${months[j.month - 1]} ${j.year}`;
}

export function formatJalaliShort(date) {
    const j = toJalali(date);
    return `${j.year}/${String(j.month).padStart(2, '0')}/${String(j.day).padStart(2, '0')}`;
}

export function getWeekdayName(date) {
    const weekdays = ['یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه'];
    return weekdays[new Date(date).getDay()];
}

// Format date for API (YYYY-MM-DD)
export function formatDateForApi(date) {
    const d = new Date(date);
    return d.toISOString().split('T')[0];
}

// Get date range for tape chart (default: 2 weeks)
export function getDateRange(startOffset = 0, days = 14) {
    const start = new Date();
    start.setDate(start.getDate() + startOffset);

    const dates = [];
    for (let i = 0; i < days; i++) {
        const d = new Date(start);
        d.setDate(d.getDate() + i);
        dates.push(d);
    }
    return dates;
}

// Format currency (Rial)
export function formatCurrency(amount) {
    return new Intl.NumberFormat('fa-IR').format(amount) + ' ریال';
}

// Translate room status
export function translateRoomStatus(status) {
    const translations = {
        clean: 'تمیز',
        dirty: 'نیاز به نظافت',
        occupied: 'اشغال',
        maintenance: 'در حال تعمیر',
    };
    return translations[status] || status;
}

// Translate booking status
export function translateBookingStatus(status) {
    const translations = {
        pending: 'در انتظار',
        confirmed: 'تایید شده',
        checked_in: 'ورود انجام شد',
        checked_out: 'خروج انجام شد',
        cancelled: 'لغو شده',
        no_show: 'عدم مراجعه',
    };
    return translations[status] || status;
}
