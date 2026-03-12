// leaderboard.js
document.addEventListener('DOMContentLoaded', function() {
    fetch('leaderboard.csv')
        .then(response => response.text())
        .then(csvText => {
            const rows = csvText.trim().split('\n');
            // Skip header row if present (your CSV has headers)
            const dataRows = rows[0].toLowerCase().includes('rank') ? rows.slice(1) : rows;
            
            const data = dataRows.map(row => {
                const cols = row.split(',');
                return {
                    rank: parseInt(cols[0]),
                    team: cols[1],
                    f1Ideal: parseFloat(cols[2]),
                    f1Pert: parseFloat(cols[3]),
                    gap: parseFloat(cols[4])
                };
            });

            // Update last updated time
            const now = new Date();
            document.getElementById('last-updated').textContent =
                `Last updated: ${now.toLocaleString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })} at ${now.toLocaleTimeString()}`;

            const tbody = document.getElementById('table-body');
            tbody.innerHTML = '';

            data.forEach(entry => {
                const tr = document.createElement('tr');
                
                // Add medal emoji for top 3 ranks
                let rankDisplay = entry.rank;
                if (entry.rank === 1) rankDisplay = '🥇 1';
                else if (entry.rank === 2) rankDisplay = '🥈 2';
                else if (entry.rank === 3) rankDisplay = '🥉 3';

                tr.innerHTML = `
                    <td class="rank">${rankDisplay}</td>
                    <td class="team-name">${entry.team}</td>
                    <td class="score primary-score">${entry.f1Ideal.toFixed(4)}</td>
                    <td class="score primary-score">${entry.f1Pert.toFixed(4)}</td>
                    <td class="score">${entry.gap.toFixed(4)}</td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(error => {
            console.error('Error loading CSV:', error);
            document.getElementById('table-body').innerHTML = `
                <tr><td colspan="5" class="empty">Failed to load leaderboard data.</td></tr>
            `;
        });
});
