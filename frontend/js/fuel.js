document.addEventListener('DOMContentLoaded', async () => {
    try {
        const fuelData = await fetchAPI('/fuel/metadata');
        const container = document.getElementById('fuel-metadata-container');
        
        fuelData.forEach(f => {
            const el = document.createElement('div');
            el.className = 'glass-card mb-2';
            el.innerHTML = `
                <h2 style="color: var(--primary-color);">${f.type}</h2>
                <p class="mb-1">${f.description}</p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div><strong>Density:</strong> ${f.density}</div>
                    <div><strong>Energy/Litre:</strong> ${f.energy}</div>
                    <div><strong>CO2 Emission:</strong> ${f.co2}</div>
                    <div><strong>Common Grades:</strong> ${f.grades.join(', ')}</div>
                </div>
            `;
            container.appendChild(el);
        });
    } catch (error) {
        showToast('Failed to load fuel data', 'error');
    }

    // Simple Converter
    document.getElementById('convert-btn').addEventListener('click', () => {
        const liters = parseFloat(document.getElementById('liters').value);
        if(isNaN(liters)) return;
        
        const gallons = (liters * 0.264172).toFixed(2);
        const kgPetrol = (liters * 0.74).toFixed(2);
        const kgDiesel = (liters * 0.84).toFixed(2);

        document.getElementById('convert-result').innerHTML = `
            <strong>${liters} Litres equals:</strong><br>
            • ${gallons} US Gallons<br>
            • ~${kgPetrol} kg (Petrol)<br>
            • ~${kgDiesel} kg (Diesel)
        `;
    });
});
