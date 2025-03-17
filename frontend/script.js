import { v4 as uuidv4 } from 'uuid';

document.addEventListener('DOMContentLoaded', () => {
    const buscarButton = document.getElementById('buscar');
    const roommateList = document.getElementById('roommate-list');
    const emailInput = document.getElementById('email');

    buscarButton.addEventListener('click', async () => {
        const userData = {
            nombre: document.getElementById('nombre').value,
            email: emailInput.value,
            telefono: document.getElementById('telefono').value,
            redes_sociales: document.getElementById('redes_sociales').value,
            fecha_nacimiento: document.getElementById('fecha_nacimiento').value,
            genero: document.getElementById('genero').value,
            ocupacion: document.getElementById('ocupacion').value,
            deportes: document.getElementById('deportes').value,
            presupuesto_maximo: document.getElementById('presupuesto_maximo').value,
            habitos_limpieza: document.getElementById('habitos_limpieza').value,
            horario_trabajo: document.getElementById('horario_trabajo').value,
            tiene_mascota: document.getElementById('tiene_mascota').value === 'true',
            acepta_mascota: document.getElementById('acepta_mascota').value === 'true',
            es_fumador: document.getElementById('es_fumador').value === 'true',
            acepta_fumador: document.getElementById('acepta_fumador').value === 'true',
            intereses: JSON.parse(document.getElementById('intereses').value || '[]'),
            preferencias_roommate: JSON.parse(document.getElementById('preferencias_roommate').value || '{}'),
            fecha_registro: new Date().toISOString()
        };

        try {
            // Simulate API call
            const mockApiResponse = createMockRoommates(10);

            displayRoommates(mockApiResponse);
        } catch (error) {
            console.error('Error fetching data:', error);
            roommateList.innerHTML = '<p>Error al buscar compañeros. Por favor, inténtalo de nuevo.</p>';
        }
    });

    function createMockRoommates(count) {
        const mockRoommates = [];
        for (let i = 0; i < count; i++) {
            mockRoommates.push({
                id: uuidv4(),
                nombre: `Roommate ${i + 1}`,
                email: `roommate${i + 1}@example.com`,
                telefono: `1234567890${i}`,
                redes_sociales: `https://example.com/${i}`,
                compatibilidad: Math.floor(Math.random() * 100) + 1 // Mock compatibility score
            });
        }
        return mockRoommates;
    }


    function displayRoommates(roommates) {
        roommateList.innerHTML = ''; // Clear previous results
        roommates.forEach(roommate => {
            const roommateDiv = document.createElement('div');
            roommateDiv.classList.add('roommate');
            roommateDiv.innerHTML = `
                <div class="compatibilidad-badge">${roommate.compatibilidad}%</div>
                <h3>${roommate.nombre}</h3>
                <p>📧 ${roommate.email}</p>
                <p>📱 ${roommate.telefono || 'No especificado'}</p>
                ${roommate.redes_sociales ? `<p>🌐 ${roommate.redes_sociales}</p>` : ''}
            `;
            roommateList.appendChild(roommateDiv);
        });
    }
});