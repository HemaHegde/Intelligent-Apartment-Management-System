import { FaCheck, FaTimes } from 'react-icons/fa';

const PasswordStrengthIndicator = ({ password }) => {
    // Password validation rules
    const requirements = [
        {
            label: 'At least 8 characters',
            test: (pwd) => pwd.length >= 8,
        },
        {
            label: 'One uppercase letter',
            test: (pwd) => /[A-Z]/.test(pwd),
        },
        {
            label: 'One number',
            test: (pwd) => /[0-9]/.test(pwd),
        },
        {
            label: 'One special character (!@#$%^&*)',
            test: (pwd) => /[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(pwd),
        },
    ];

    // Calculate how many requirements are met
    const metRequirements = requirements.filter(req => req.test(password)).length;
    const totalRequirements = requirements.length;

    // Determine strength level
    let strength = 'Weak';
    let strengthColor = 'bg-red-500';
    let strengthWidth = '20%';

    if (metRequirements === totalRequirements) {
        strength = 'Strong';
        strengthColor = 'bg-green-500';
        strengthWidth = '100%';
    } else if (metRequirements >= 3) {
        strength = 'Medium';
        strengthColor = 'bg-yellow-500';
        strengthWidth = '60%';
    }

    // Don't show indicator if password is empty
    if (!password) return null;

    return (
        <div className="mt-3 space-y-2 animate-slide-up">
            {/* Strength meter */}
            <div className="space-y-1">
                <div className="flex justify-between items-center">
                    <span className="text-xs text-white/70">Password Strength:</span>
                    <span className={`text-xs font-semibold ${strength === 'Strong' ? 'text-green-400' :
                        strength === 'Medium' ? 'text-yellow-400' :
                            'text-red-400'
                        }`}>
                        {strength}
                    </span>
                </div>
                <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                    <div
                        className={`h-full ${strengthColor} transition-all duration-300 ease-out`}
                        style={{ width: strengthWidth }}
                    />
                </div>
            </div>

            {/* Requirements checklist */}
            <div className="space-y-1">
                {requirements.map((req, index) => {
                    const isMet = req.test(password);
                    return (
                        <div
                            key={index}
                            className={`flex items-center gap-2 text-xs transition-colors duration-200 ${isMet ? 'text-green-400' : 'text-white/50'
                                }`}
                        >
                            {isMet ? (
                                <FaCheck className="text-green-400 flex-shrink-0" />
                            ) : (
                                <FaTimes className="text-white/30 flex-shrink-0" />
                            )}
                            <span>{req.label}</span>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default PasswordStrengthIndicator;
