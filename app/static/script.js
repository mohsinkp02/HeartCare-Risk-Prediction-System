let predictedRiskLevel = 1;

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    const heightInput = document.getElementById('Height');
    const weightInput = document.getElementById('Weight');
    const bmiInput = document.getElementById('BMI');
    const modal = document.getElementById('resultModal');
    const closeModalBtn = document.querySelector('.close-modal');

    // Live Preview Elements
    const livePreview = document.getElementById('livePreview');
    const liveRiskScore = document.getElementById('liveRiskScore');
    const liveRiskLabel = document.getElementById('liveRiskLabel');

    // Auto-calculate BMI
    function calculateBMI() {
        const heightCm = parseFloat(heightInput.value);
        const weightKg = parseFloat(weightInput.value);

        if (heightCm > 0 && weightKg > 0) {
            const heightM = heightCm / 100;
            const bmi = (weightKg / (heightM * heightM)).toFixed(2);
            bmiInput.value = bmi;
        } else {
            bmiInput.value = '';
        }
    }

    heightInput.addEventListener('input', calculateBMI);
    weightInput.addEventListener('input', calculateBMI);

    // Live Preview Logic (Debounced)
    let debounceTimer;
    function updateLivePreview() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(async () => {
            // Check if required fields are filled (basic check)
            if (!heightInput.value || !weightInput.value || !document.getElementById('Age').value) return;

            const formData = new FormData(form);
            const data = {};

            formData.forEach((value, key) => {
                if (form.querySelector(`input[name="${key}"][type="checkbox"]`)) {
                    data[key] = "1";
                } else {
                    data[key] = value;
                }
            });

            const checkboxes = form.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(cb => {
                if (!data.hasOwnProperty(cb.name)) data[cb.name] = "0";
            });

            if (!data['BMI']) return;

            try {
                const response = await fetch('/api/v1/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    const result = await response.json();
                    liveRiskScore.textContent = (result.probability * 100).toFixed(1) + '%';
                    liveRiskLabel.textContent = result.risk_label;
                    livePreview.classList.add('visible');

                    if (result.risk_level <= 2) liveRiskScore.style.color = '#10B981';
                    else if (result.risk_level === 3) liveRiskScore.style.color = '#F59E0B';
                    else liveRiskScore.style.color = '#EF4444';
                }
            } catch (e) {
                console.error("Live preview failed", e);
            }
        }, 500);
    }

    form.addEventListener('change', updateLivePreview);

    // Form Submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
        submitBtn.disabled = true;

        const formData = new FormData(form);
        const data = {};

        formData.forEach((value, key) => {
            if (form.querySelector(`input[name="${key}"][type="checkbox"]`)) {
                data[key] = "1";
            } else {
                data[key] = value;
            }
        });

        const checkboxes = form.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(cb => {
            if (!data.hasOwnProperty(cb.name)) {
                data[cb.name] = "0";
            }
        });

        try {
            const response = await fetch('/api/v1/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            window.lastResult = result;
            showResult(result);

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during analysis. Please try again.');
        } finally {
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
        }
    });

    function showResult(result) {
        const riskLevelEl = document.getElementById('riskLevel');
        const riskIconEl = document.getElementById('riskIcon');
        const probFill = document.getElementById('probFill');
        const probValue = document.getElementById('probValue');

        predictedRiskLevel = result.risk_level;

        const probability = result.probability;
        const percentage = (probability * 100).toFixed(1) + '%';

        let colorStart, colorEnd, iconClass, text;

        if (predictedRiskLevel <= 2) {
            text = 'Low Risk';
            iconClass = 'fa-heart-circle-check risk-low';
            colorStart = '#34D399';
            colorEnd = '#10B981';
            riskLevelEl.style.color = '#10B981';
        } else if (predictedRiskLevel === 3) {
            text = 'Moderate Risk';
            iconClass = 'fa-heart-circle-exclamation';
            colorStart = '#FBBF24';
            colorEnd = '#F59E0B';
            riskLevelEl.style.color = '#F59E0B';
            riskIconEl.innerHTML = `<i class="fa-solid ${iconClass}" style="color: #F59E0B"></i>`;
        } else {
            text = 'High Risk';
            iconClass = 'fa-heart-crack risk-high';
            colorStart = '#F87171';
            colorEnd = '#EF4444';
            riskLevelEl.style.color = '#EF4444';
        }

        riskLevelEl.textContent = text;
        if (predictedRiskLevel !== 3) {
            riskLevelEl.className = predictedRiskLevel <= 2 ? 'risk-low' : 'risk-high';
            riskIconEl.innerHTML = `<i class="fa-solid ${iconClass}"></i>`;
        }

        probFill.style.background = `linear-gradient(90deg, ${colorStart}, ${colorEnd})`;
        probFill.style.width = percentage;
        probValue.textContent = percentage;

        modal.classList.add('visible');
    }

    function closeModal() {
        modal.classList.remove('visible');
    }

    closeModalBtn.addEventListener('click', closeModal);
    window.onclick = function (event) {
        if (event.target == modal) {
            closeModal();
        }
    }

    // smooth scroll to sections
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    window.closeModal = closeModal;
});

function goToRecommendations() {
    // Gather key parameters for recommendation personalization
    const params = new URLSearchParams();

    // 1. Pass the exact calculated probability
    if (window.lastResult && window.lastResult.probability) {
        params.append('risk', (window.lastResult.probability * 100).toFixed(1));
    }

    // 2. Selects and Inputs
    const fields = [
        'Age', 'BMI', 'Sex', 'Smoking', 'Diabetes',
        'Alcohol', 'Fried_Potato', 'Fruit', 'Green_Vegetables', 'Exercise', 'General_Health'
    ];

    fields.forEach(id => {
        const el = document.getElementById(id);
        if (el) params.append(id, el.value);
    });

    // 3. Checkboxes (Special handling)
    const checkBoxes = ['Skin_Cancer', 'Other_Cancer', 'Depression', 'Arthritis'];
    checkBoxes.forEach(id => {
        const el = document.getElementById(id);
        if (el) params.append(id, el.checked ? "1" : "0");
    });

    window.location.href = `/recommendation/${predictedRiskLevel}?${params.toString()}`;
}
