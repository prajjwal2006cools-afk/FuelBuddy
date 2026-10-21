document.addEventListener('DOMContentLoaded', async () => {
    const user = await checkAuth();
    if (!user) return; // Will redirect

    document.getElementById('user-phone').textContent = user.phone_number;

    document.getElementById('logout-btn').addEventListener('click', async (e) => {
        e.preventDefault();
        try {
            await fetchAPI('/auth/logout', { method: 'POST' });
            window.location.href = '/';
        } catch (error) {
            showToast('Logout failed', 'error');
        }
    });

    await loadVehicles();

    document.getElementById('add-vehicle-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const vehicleData = {
            make: document.getElementById('make').value,
            model: document.getElementById('model').value,
            year: parseInt(document.getElementById('year').value),
            trim: document.getElementById('trim').value,
            fuel_type: document.getElementById('fuel-type').value,
            fuel_grade: document.getElementById('fuel-grade').value,
            tank_size: parseFloat(document.getElementById('tank-size').value),
            city_mpg: parseFloat(document.getElementById('city-mpg').value),
            highway_mpg: parseFloat(document.getElementById('highway-mpg').value),
            is_default: document.getElementById('is-default').checked
        };

        try {
            await fetchAPI('/vehicles/', {
                method: 'POST',
                body: JSON.stringify(vehicleData)
            });
            showToast('Vehicle added successfully');
            document.getElementById('add-vehicle-form').reset();
            await loadVehicles();
        } catch (error) {
            showToast(error.message, 'error');
        }
    });
});

async function loadVehicles() {
    try {
        const vehicles = await fetchAPI('/vehicles/');
        const container = document.getElementById('vehicles-container');
        container.innerHTML = '';

        if (vehicles.length === 0) {
            container.innerHTML = '<p class="text-light">No vehicles added yet. Add one to get personalized recommendations.</p>';
            return;
        }

        vehicles.forEach(v => {
            const el = document.createElement('div');
            el.className = 'glass-card mb-1';
            el.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <h3 style="margin-bottom: 0.5rem;">${v.year} ${v.make} ${v.model} ${v.is_default ? '<span style="font-size:0.8rem; background:var(--primary-color); color:white; padding:2px 8px; border-radius:12px; margin-left:8px;">Default</span>' : ''}</h3>
                        <p class="text-light" style="font-size: 0.9rem;">
                            ${v.trim} • ${v.fuel_type} (${v.fuel_grade})
                        </p>
                        <p class="text-light" style="font-size: 0.9rem; margin-top:0.5rem;">
                            Tank: ${v.tank_size}L • City: ${v.city_mpg} km/L • Hwy: ${v.highway_mpg} km/L
                        </p>
                    </div>
                    <button class="btn btn-secondary" onclick="deleteVehicle(${v.id})" style="padding: 0.5rem 1rem; font-size: 0.8rem;">Delete</button>
                </div>
            `;
            container.appendChild(el);
        });
    } catch (error) {
        showToast('Failed to load vehicles', 'error');
    }
}

async function deleteVehicle(id) {
    if(!confirm("Delete this vehicle?")) return;
    try {
        await fetchAPI(`/vehicles/${id}`, { method: 'DELETE' });
        showToast('Vehicle deleted');
        await loadVehicles();
    } catch (error) {
        showToast('Failed to delete vehicle', 'error');
    }
}
