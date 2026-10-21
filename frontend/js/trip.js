document.addEventListener('DOMContentLoaded', async () => {
    // Populate user vehicles if logged in
    const user = await checkAuth();
    if (user) {
        try {
            const vehicles = await fetchAPI('/vehicles/');
            const sel = document.getElementById('vehicle-select');
            if (vehicles.length > 0) {
                vehicles.forEach(v => {
                    const opt = document.createElement('option');
                    opt.value = JSON.stringify(v);
                    opt.textContent = `${v.year} ${v.make} ${v.model}`;
                    if (v.is_default) opt.selected = true;
                    sel.appendChild(opt);
                });
                sel.addEventListener('change', (e) => {
                    if(!e.target.value) return;
                    const v = JSON.parse(e.target.value);
                    document.getElementById('city-mpg').value = v.city_mpg;
                    document.getElementById('highway-mpg').value = v.highway_mpg;
                });
                sel.dispatchEvent(new Event('change'));
            }
        } catch(e) {}
    }

    document.getElementById('trip-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const req = {
            origin: document.getElementById('origin').value,
            destination: document.getElementById('destination').value,
            city_mpg: parseFloat(document.getElementById('city-mpg').value),
            highway_mpg: parseFloat(document.getElementById('highway-mpg').value),
            fuel_price: parseFloat(document.getElementById('fuel-price').value) || 100 // Default to ₹100/L
        };

        try {
            const btn = e.target.querySelector('button');
            const origText = btn.textContent;
            btn.textContent = 'Calculating...';
            btn.disabled = true;

            const data = await fetchAPI('/trip/calculate', {
                method: 'POST',
                body: JSON.stringify(req)
            });

            document.getElementById('result-section').style.display = 'block';
            document.getElementById('res-dist').textContent = `${data.distance_km} km`;
            document.getElementById('res-cost').textContent = `₹${data.total_cost}`;
            document.getElementById('res-fuel').textContent = `${data.fuel_used_liters} L`;
            document.getElementById('res-co2').textContent = `${data.co2_emitted_kg} kg`;

            // Simple map mock update (If Leaflet was added, update markers here)
            btn.textContent = origText;
            btn.disabled = false;
            
        } catch (error) {
            showToast('Failed to calculate trip cost', 'error');
            const btn = e.target.querySelector('button');
            btn.textContent = 'Calculate Cost';
            btn.disabled = false;
        }
    });
});
