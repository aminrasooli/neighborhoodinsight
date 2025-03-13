document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('search-btn');
    const addressInput = document.getElementById('address-input');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const scoreCircle = document.getElementById('score-circle');
    
    // Add SF neighborhoods for auto-completion
    const sfNeighborhoods = [
        "Mission District", "Hayes Valley", "Pacific Heights", "Marina",
        "North Beach", "Russian Hill", "Nob Hill", "Financial District",
        "SoMa", "Castro", "Haight-Ashbury", "Richmond District",
        "Sunset District", "Noe Valley", "Potrero Hill", "Dogpatch"
    ];

    searchBtn.addEventListener('click', async () => {
        const address = addressInput.value.trim();
        if (!address) {
            alert('Please enter an address');
            return;
        }

        // Show loading
        loading.classList.remove('hidden');
        results.classList.add('hidden');

        try {
            const response = await fetch('http://localhost:4000/insights', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ address: address })
            });

            const data = await response.json();
            
            // Hide loading
            loading.classList.add('hidden');
            
            // Update UI with results
            updateUI(data);
            
            // Show results
            results.classList.remove('hidden');
            
        } catch (error) {
            console.error('Error:', error);
            alert('Error fetching neighborhood data. Please try again.');
            loading.classList.add('hidden');
        }
    });

    // Handle Enter key in input
    addressInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchBtn.click();
        }
    });

    function updateUI(data) {
        // Update neighborhood name
        const neighborhood = getNeighborhoodFromAddress(data.address);
        document.getElementById('neighborhood-name').textContent = neighborhood;

        // Update overall score
        const overallScore = data.ml_insights.overall_score;
        document.getElementById('overall-score').textContent = Math.round(overallScore);
        
        // Update score circle
        const circumference = 2 * Math.PI * 88;
        const offset = circumference - (overallScore / 100) * circumference;
        scoreCircle.style.strokeDashoffset = offset;

        // Update component scores
        const componentScores = document.getElementById('component-scores');
        componentScores.innerHTML = '';
        
        Object.entries(data.ml_insights.component_scores).forEach(([key, value]) => {
            const formattedKey = key.split('_')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');
            
            componentScores.innerHTML += `
                <div class="component-score p-4 bg-gray-50 rounded-lg">
                    <div class="flex justify-between mb-2">
                        <span class="text-gray-700">${formattedKey}</span>
                        <span class="font-semibold">${Math.round(value)}</span>
                    </div>
                    <div class="score-bar">
                        <div class="score-bar-fill" style="width: ${value}%"></div>
                    </div>
                </div>
            `;
        });

        // Update crime info
        const crimeInfo = document.getElementById('crime-info');
        crimeInfo.innerHTML = `
            <p class="text-gray-700"><span class="font-medium">Risk Level:</span> ${data.crime_analysis.risk_level}</p>
            <p class="text-gray-700"><span class="font-medium">Safety Score:</span> ${data.crime_analysis.safety_score}/10</p>
            <p class="text-gray-700"><span class="font-medium">Trend:</span> ${data.crime_analysis.trend}</p>
            <p class="text-gray-700"><span class="font-medium">Comparison:</span> ${data.crime_analysis.comparison}</p>
        `;

        // Update real estate info
        const realEstateInfo = document.getElementById('real-estate-info');
        realEstateInfo.innerHTML = `
            <p class="text-gray-700"><span class="font-medium">Median Price:</span> ${data.real_estate.median_price}</p>
            <p class="text-gray-700"><span class="font-medium">Price Trend:</span> ${data.real_estate.price_trend}</p>
            <p class="text-gray-700"><span class="font-medium">Market Status:</span> ${data.real_estate.market_status}</p>
            <p class="text-gray-700"><span class="font-medium">Price/sqft:</span> ${data.real_estate.price_per_sqft}</p>
        `;

        // Update positive aspects
        const positiveAspects = document.getElementById('positive-aspects');
        positiveAspects.innerHTML = data.community.positive_aspects
            .map(aspect => `<li>${aspect}</li>`)
            .join('');

        // Update complaints
        const complaints = document.getElementById('complaints');
        complaints.innerHTML = data.community.top_complaints
            .map(complaint => `<li>${complaint}</li>`)
            .join('');
    }

    function getNeighborhoodFromAddress(address) {
        // For demo purposes, return a random SF neighborhood
        return sfNeighborhoods[Math.floor(Math.random() * sfNeighborhoods.length)];
    }
}); 