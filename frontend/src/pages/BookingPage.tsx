import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Calendar, User, CreditCard, Check, AlertCircle } from 'lucide-react';
import axios from 'axios';

export default function BookingPage() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const [step, setStep] = useState(1);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

    const [formData, setFormData] = useState({
        roomId: searchParams.get('roomId') || '',
        checkIn: searchParams.get('checkIn') || '',
        checkOut: searchParams.get('checkOut') || '',
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        specialRequests: '',
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async () => {
        setLoading(true);
        setError('');

        try {
            await axios.post('/api/bookings/', {
                room_id: Number(formData.roomId),
                check_in: formData.checkIn,
                check_out: formData.checkOut,
            });
            setSuccess(true);
            setStep(4);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Booking failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const steps = [
        { num: 1, label: 'Dates' },
        { num: 2, label: 'Guest Info' },
        { num: 3, label: 'Confirm' },
    ];

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-indigo-600 py-12">
                <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
                    <h1 className="text-3xl font-bold text-white mb-2">Complete Your Booking</h1>
                    <p className="text-indigo-100">Secure your stay in just a few steps</p>
                </div>
            </div>

            <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                {/* Progress Steps */}
                {!success && (
                    <div className="flex items-center justify-center mb-12">
                        {steps.map((s, i) => (
                            <div key={s.num} className="flex items-center">
                                <div className={`flex items-center justify-center w-10 h-10 rounded-full font-semibold ${step >= s.num ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-500'
                                    }`}>
                                    {step > s.num ? <Check className="h-5 w-5" /> : s.num}
                                </div>
                                <span className={`ml-2 ${step >= s.num ? 'text-gray-900' : 'text-gray-400'}`}>
                                    {s.label}
                                </span>
                                {i < steps.length - 1 && (
                                    <div className={`w-16 h-0.5 mx-4 ${step > s.num ? 'bg-indigo-600' : 'bg-gray-200'}`} />
                                )}
                            </div>
                        ))}
                    </div>
                )}

                {/* Error Message */}
                {error && (
                    <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-3">
                        <AlertCircle className="h-5 w-5 text-red-500" />
                        <span className="text-red-700">{error}</span>
                    </div>
                )}

                {/* Step 1: Dates */}
                {step === 1 && (
                    <div className="card p-8">
                        <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center gap-2">
                            <Calendar className="h-6 w-6 text-indigo-600" />
                            Select Your Dates
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="label">Check In</label>
                                <input
                                    type="date"
                                    name="checkIn"
                                    value={formData.checkIn}
                                    onChange={handleChange}
                                    className="input"
                                    required
                                />
                            </div>
                            <div>
                                <label className="label">Check Out</label>
                                <input
                                    type="date"
                                    name="checkOut"
                                    value={formData.checkOut}
                                    onChange={handleChange}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <button
                            onClick={() => setStep(2)}
                            disabled={!formData.checkIn || !formData.checkOut}
                            className="btn-primary w-full mt-8"
                        >
                            Continue
                        </button>
                    </div>
                )}

                {/* Step 2: Guest Info */}
                {step === 2 && (
                    <div className="card p-8">
                        <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center gap-2">
                            <User className="h-6 w-6 text-indigo-600" />
                            Guest Information
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="label">First Name</label>
                                <input
                                    type="text"
                                    name="firstName"
                                    value={formData.firstName}
                                    onChange={handleChange}
                                    className="input"
                                    required
                                />
                            </div>
                            <div>
                                <label className="label">Last Name</label>
                                <input
                                    type="text"
                                    name="lastName"
                                    value={formData.lastName}
                                    onChange={handleChange}
                                    className="input"
                                    required
                                />
                            </div>
                            <div>
                                <label className="label">Email</label>
                                <input
                                    type="email"
                                    name="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                    className="input"
                                    required
                                />
                            </div>
                            <div>
                                <label className="label">Phone</label>
                                <input
                                    type="tel"
                                    name="phone"
                                    value={formData.phone}
                                    onChange={handleChange}
                                    className="input"
                                />
                            </div>
                        </div>
                        <div className="mt-6">
                            <label className="label">Special Requests</label>
                            <textarea
                                name="specialRequests"
                                value={formData.specialRequests}
                                onChange={handleChange}
                                rows={3}
                                className="input"
                                placeholder="Any special requests or preferences..."
                            />
                        </div>
                        <div className="flex gap-4 mt-8">
                            <button onClick={() => setStep(1)} className="btn-secondary flex-1">
                                Back
                            </button>
                            <button
                                onClick={() => setStep(3)}
                                disabled={!formData.firstName || !formData.lastName || !formData.email}
                                className="btn-primary flex-1"
                            >
                                Continue
                            </button>
                        </div>
                    </div>
                )}

                {/* Step 3: Confirm */}
                {step === 3 && (
                    <div className="card p-8">
                        <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center gap-2">
                            <CreditCard className="h-6 w-6 text-indigo-600" />
                            Confirm Your Booking
                        </h2>

                        <div className="bg-gray-50 rounded-lg p-6 mb-6">
                            <h3 className="font-medium text-gray-900 mb-4">Booking Summary</h3>
                            <div className="space-y-2 text-sm">
                                <div className="flex justify-between">
                                    <span className="text-gray-600">Check In</span>
                                    <span className="font-medium">{formData.checkIn}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-gray-600">Check Out</span>
                                    <span className="font-medium">{formData.checkOut}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-gray-600">Guest</span>
                                    <span className="font-medium">{formData.firstName} {formData.lastName}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-gray-600">Email</span>
                                    <span className="font-medium">{formData.email}</span>
                                </div>
                            </div>
                        </div>

                        <div className="flex gap-4">
                            <button onClick={() => setStep(2)} className="btn-secondary flex-1">
                                Back
                            </button>
                            <button
                                onClick={handleSubmit}
                                disabled={loading}
                                className="btn-primary flex-1"
                            >
                                {loading ? 'Processing...' : 'Confirm Booking'}
                            </button>
                        </div>
                    </div>
                )}

                {/* Step 4: Success */}
                {success && (
                    <div className="card p-8 text-center">
                        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                            <Check className="h-8 w-8 text-green-600" />
                        </div>
                        <h2 className="text-2xl font-bold text-gray-900 mb-2">Booking Confirmed!</h2>
                        <p className="text-gray-600 mb-8">
                            Thank you for your reservation. A confirmation email has been sent to {formData.email}.
                        </p>
                        <button onClick={() => navigate('/')} className="btn-primary">
                            Return Home
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}
