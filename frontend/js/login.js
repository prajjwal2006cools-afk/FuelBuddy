document.addEventListener('DOMContentLoaded', () => {
    const phoneForm = document.getElementById('phone-form');
    const otpForm = document.getElementById('otp-form');
    const phoneInput = document.getElementById('phone');
    const otpInput = document.getElementById('otp');
    const countryCode = document.getElementById('country-code');
    const phoneStep = document.getElementById('phone-step');
    const otpStep = document.getElementById('otp-step');
    const displayPhone = document.getElementById('display-phone');
    
    let currentPhone = '';

    phoneForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const rawPhone = phoneInput.value.replace(/\D/g, '');
        if (rawPhone.length < 10) {
            showToast('Please enter a valid phone number', 'error');
            return;
        }

        currentPhone = `${countryCode.value}${rawPhone}`;
        
        try {
            const btn = phoneForm.querySelector('button');
            const originalText = btn.textContent;
            btn.textContent = 'Sending...';
            btn.disabled = true;

            await fetchAPI('/auth/send-otp', {
                method: 'POST',
                body: JSON.stringify({ phone_number: currentPhone })
            });

            // Transition to OTP step
            displayPhone.textContent = currentPhone;
            phoneStep.style.display = 'none';
            otpStep.style.display = 'block';
            otpInput.focus();
            showToast('OTP sent successfully (Check console in DEV mode)');
            
        } catch (error) {
            showToast(error.message, 'error');
        } finally {
            const btn = phoneForm.querySelector('button');
            btn.textContent = 'Send OTP';
            btn.disabled = false;
        }
    });

    otpForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const otp = otpInput.value.trim();
        if (otp.length !== 6) {
            showToast('Please enter a 6-digit OTP', 'error');
            return;
        }

        try {
            const btn = otpForm.querySelector('button');
            btn.textContent = 'Verifying...';
            btn.disabled = true;

            await fetchAPI('/auth/verify-otp', {
                method: 'POST',
                body: JSON.stringify({ 
                    phone_number: currentPhone,
                    otp: otp
                })
            });

            showToast('Login successful!');
            window.location.href = 'dashboard.html';
            
        } catch (error) {
            showToast(error.message, 'error');
            const btn = otpForm.querySelector('button');
            btn.textContent = 'Verify & Login';
            btn.disabled = false;
        }
    });
});
