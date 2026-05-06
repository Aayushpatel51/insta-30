async function fetchStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        document.getElementById('stat-total-apps').textContent = data.total_apps;
        document.getElementById('stat-high-risk').textContent = data.high_risk_count;
        document.getElementById('stat-total-users').textContent = data.total_exposed_users;
        document.getElementById('alert-count').textContent = data.critical_alerts;
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

async function fetchApps() {
    try {
        const response = await fetch('/api/apps');
        const apps = await response.json();
        const tableBody = document.getElementById('apps-table-body');
        tableBody.innerHTML = '';

        apps.forEach(app => {
            const row = document.createElement('tr');
            row.className = 'hover:bg-white/[0.02] transition-colors';

            const riskClass = app.risk_level === 'High' ? 'risk-high' :
                             app.risk_level === 'Medium' ? 'risk-medium' : 'risk-low';

            const isRevoked = app.status === 'Revoked';

            row.innerHTML = `
                <td class="px-6 py-4">
                    <div class="flex items-center gap-4">
                        <div class="w-10 h-10 bg-[#1f1f23] rounded-lg flex items-center justify-center text-xl shadow-inner border border-white/5">
                            ${app.icon}
                        </div>
                        <div>
                            <div class="text-sm font-semibold text-white">${app.name}</div>
                            <div class="text-xs text-gray-500">${app.category}</div>
                        </div>
                    </div>
                </td>
                <td class="px-6 py-4">
                    <span class="text-xs font-bold uppercase ${riskClass}">${app.risk_level}</span>
                </td>
                <td class="px-6 py-4">
                    <div class="flex items-center gap-2">
                        <i class="fas fa-users text-gray-600 text-xs"></i>
                        <span class="text-sm text-gray-300 mono">${app.users_affected}</span>
                    </div>
                </td>
                <td class="px-6 py-4">
                    <div class="flex flex-wrap gap-1">
                        ${app.scopes.map(scope => `
                            <span class="text-[10px] px-1.5 py-0.5 rounded bg-[#1f1f23] text-gray-400 border border-white/5 mono">
                                ${scope}
                            </span>
                        `).join('')}
                    </div>
                </td>
                <td class="px-6 py-4">
                    ${isRevoked ?
                        `<span class="text-xs text-gray-600 font-medium italic">REVOKED</span>` :
                        `<button onclick="revokeAccess('${app.id}', '${app.name}')"
                                 class="text-xs font-bold text-red-500 hover:text-white hover:bg-red-600 px-3 py-1.5 rounded border border-red-500/30 transition-all uppercase tracking-wider">
                            Revoke
                        </button>`
                    }
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching apps:', error);
    }
}

async function revokeAccess(appId, appName) {
    if (!confirm(`Are you sure you want to REVOKE access for ${appName}? This will disconnect all users.`)) return;

    try {
        const response = await fetch(`/api/revoke/${appId}`, { method: 'POST' });
        if (response.ok) {
            showToast(`Revoked access for ${appName}`);
            fetchApps();
            fetchStats();
        }
    } catch (error) {
        console.error('Error revoking access:', error);
    }
}

function showToast(message) {
    const toast = document.getElementById('toast');
    const toastMsg = document.getElementById('toast-message');
    toastMsg.textContent = message;
    toast.style.display = 'block';
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    fetchApps();
});
