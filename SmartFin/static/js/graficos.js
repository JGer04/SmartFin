
    const ctx = document.getElementById('grafico').getContext('2d');
    let chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Montos',
                data: [],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    document.getElementById('actualizar').addEventListener('click', () => {
        const empresa = document.getElementById('empresa').value;
        const cuenta = document.getElementById('cuenta').value;
        const tipo = document.querySelector(`#cuenta option[value="${cuenta}"]`).getAttribute('data-tipo');

        if (empresa && cuenta) {
            fetch(`/obtener-datos/?cuenta_id=${cuenta}&tipo_cuenta=${tipo}&empresa_id=${empresa}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        chart.data.labels = Object.keys(data.datos);
                        chart.data.datasets[0].data = Object.values(data.datos);
                        chart.update();
                    }
                });
        } else {
            alert("Debe seleccionar una empresa y una cuenta.");
        }
    });
