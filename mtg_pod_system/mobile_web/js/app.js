// MTG Pod Randomizer - Mobile Web Application

class MTGPodRandomizer {
    constructor() {
        this.players = [];
        this.history = [];
        this.config = {
            default_pod_size: 4,
            max_pod_size: 8,
            min_pod_size: 3,
            keep_history: true,
            max_history_items: 50
        };
        
        this.initializeElements();
        this.bindEvents();
        this.loadData();
        this.updateUI();
    }

    initializeElements() {
        // Input elements
        this.playerNameInput = document.getElementById('player-name');
        this.bulkPlayersTextarea = document.getElementById('bulk-players');
        this.targetSizeInput = document.getElementById('target-size');
        this.maxSizeInput = document.getElementById('max-size');
        this.importFileInput = document.getElementById('import-file');

        // Buttons
        this.addPlayerBtn = document.getElementById('add-player-btn');
        this.bulkAddBtn = document.getElementById('bulk-add-btn');
        this.randomizeBtn = document.getElementById('randomize-btn');
        this.saveHistoryBtn = document.getElementById('save-history-btn');
        this.reRandomizeBtn = document.getElementById('re-randomize-btn');
        this.exportBtn = document.getElementById('export-btn');
        this.importBtn = document.getElementById('import-btn');
        this.clearAllBtn = document.getElementById('clear-all-btn');

        // Containers
        this.playersContainer = document.getElementById('players-container');
        this.playerCount = document.getElementById('player-count');
        this.podsContainer = document.getElementById('pods-container');
        this.historyContainer = document.getElementById('history-container');
        this.resultsSection = document.getElementById('results-section');
        this.statsInfo = document.getElementById('stats-info');
        this.loading = document.getElementById('loading');
        this.toast = document.getElementById('toast');
        this.toastMessage = document.getElementById('toast-message');
    }

    bindEvents() {
        // Player management
        this.addPlayerBtn.addEventListener('click', () => this.addPlayer());
        this.playerNameInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addPlayer();
        });

        this.bulkAddBtn.addEventListener('click', () => this.addBulkPlayers());

        // Randomization
        this.randomizeBtn.addEventListener('click', () => this.createPods());
        this.reRandomizeBtn.addEventListener('click', () => this.createPods());
        this.saveHistoryBtn.addEventListener('click', () => this.saveToHistory());

        // Data management
        this.exportBtn.addEventListener('click', () => this.exportData());
        this.importBtn.addEventListener('click', () => this.importFileInput.click());
        this.importFileInput.addEventListener('change', (e) => this.importData(e));
        this.clearAllBtn.addEventListener('click', () => this.clearAllData());

        // Configuration
        this.targetSizeInput.addEventListener('change', () => this.updateConfig());
        this.maxSizeInput.addEventListener('change', () => this.updateConfig());
    }

    // Data Persistence
    loadData() {
        try {
            const savedPlayers = localStorage.getItem('mtg_players');
            const savedConfig = localStorage.getItem('mtg_config');
            const savedHistory = localStorage.getItem('mtg_history');

            if (savedPlayers) {
                this.players = JSON.parse(savedPlayers);
            }

            if (savedConfig) {
                this.config = { ...this.config, ...JSON.parse(savedConfig) };
            }

            if (savedHistory) {
                this.history = JSON.parse(savedHistory);
            }
        } catch (error) {
            this.showToast('Error loading data', 'error');
            console.error('Load error:', error);
        }
    }

    saveData() {
        try {
            localStorage.setItem('mtg_players', JSON.stringify(this.players));
            localStorage.setItem('mtg_config', JSON.stringify(this.config));
            localStorage.setItem('mtg_history', JSON.stringify(this.history));
        } catch (error) {
            this.showToast('Error saving data', 'error');
            console.error('Save error:', error);
        }
    }

    updateConfig() {
        this.config.default_pod_size = Math.max(3, Math.min(8, parseInt(this.targetSizeInput.value) || 4));
        this.config.max_pod_size = Math.max(4, Math.min(8, parseInt(this.maxSizeInput.value) || 8));
        this.targetSizeInput.value = this.config.default_pod_size;
        this.maxSizeInput.value = this.config.max_pod_size;
        this.saveData();
    }

    // Player Management
    addPlayer() {
        const name = this.playerNameInput.value.trim();
        if (!name) {
            this.showToast('Please enter a player name', 'warning');
            return;
        }

        if (this.players.some(p => p.toLowerCase() === name.toLowerCase())) {
            this.showToast('Player already exists', 'warning');
            return;
        }

        this.players.push(name);
        this.playerNameInput.value = '';
        this.saveData();
        this.updateUI();
        this.showToast(`Added player: ${name}`, 'success');
    }

    addBulkPlayers() {
        const bulkText = this.bulkPlayersTextarea.value.trim();
        if (!bulkText) {
            this.showToast('Please enter player names', 'warning');
            return;
        }

        const names = bulkText.split('\n')
            .map(name => name.trim())
            .filter(name => name && !this.players.some(p => p.toLowerCase() === name.toLowerCase()));

        if (names.length === 0) {
            this.showToast('No new players to add', 'warning');
            return;
        }

        this.players.push(...names);
        this.bulkPlayersTextarea.value = '';
        this.saveData();
        this.updateUI();
        this.showToast(`Added ${names.length} player(s)`, 'success');
    }

    removePlayer(index) {
        const removed = this.players[index];
        this.players.splice(index, 1);
        this.saveData();
        this.updateUI();
        this.showToast(`Removed player: ${removed}`, 'success');
    }

    // Pod Randomization
    createPods() {
        if (this.players.length < 3) {
            this.showToast('Need at least 3 players to create pods', 'error');
            return;
        }

        this.showLoading(true);

        setTimeout(() => {
            try {
                const pods = this.calculatePodDistribution();
                this.displayPods(pods);
                this.currentPods = pods;
                this.resultsSection.classList.remove('hidden');
                
                // Scroll to results
                this.resultsSection.scrollIntoView({ behavior: 'smooth' });
            } catch (error) {
                this.showToast('Error creating pods', 'error');
                console.error('Pod creation error:', error);
            } finally {
                this.showLoading(false);
            }
        }, 500);
    }

    calculatePodDistribution() {
        const shuffled = [...this.players];
        this.shuffleArray(shuffled);

        const targetSize = parseInt(this.targetSizeInput.value) || this.config.default_pod_size;
        const maxSize = parseInt(this.maxSizeInput.value) || this.config.max_pod_size;
        
        const totalPlayers = shuffled.length;
        const pods = [];

        // Calculate optimal distribution
        const minPods = Math.ceil(totalPlayers / maxSize);
        const maxPods = Math.floor(totalPlayers / 3); // Minimum 3 players per pod

        for (let numPods = minPods; numPods <= maxPods; numPods++) {
            const baseSize = Math.floor(totalPlayers / numPods);
            const remainder = totalPlayers % numPods;

            const currentPods = [];
            let currentIndex = 0;

            for (let i = 0; i < numPods; i++) {
                const podSize = baseSize + (i < remainder ? 1 : 0);
                
                if (podSize === 0) continue;
                
                const finalPodSize = Math.max(3, Math.min(podSize, maxSize));
                const podPlayers = shuffled.slice(currentIndex, currentIndex + finalPodSize);
                
                currentPods.push({
                    id: i + 1,
                    players: podPlayers,
                    size: podPlayers.length
                });
                
                currentIndex += finalPodSize;
            }

            if (currentIndex >= totalPlayers) {
                pods.push(...currentPods);
                break;
            }
        }

        // Fallback simple distribution
        if (pods.length === 0) {
            return this.simpleDistribution(shuffled, targetSize, maxSize);
        }

        return pods;
    }

    simpleDistribution(players, targetSize, maxSize) {
        const pods = [];
        let podId = 1;
        let i = 0;

        while (i < players.length) {
            let podSize = Math.min(targetSize, players.length - i);
            
            // Handle last pod if too small
            if (players.length - i < 3 && pods.length > 0) {
                if (pods[pods.length - 1].players.length + (players.length - i) <= maxSize) {
                    pods[pods.length - 1].players.push(...players.slice(i));
                    pods[pods.length - 1].size = pods[pods.length - 1].players.length;
                    break;
                }
                podSize = players.length - i;
            }

            pods.push({
                id: podId++,
                players: players.slice(i, i + podSize),
                size: podSize
            });

            i += podSize;
        }

        return pods;
    }

    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    displayPods(pods) {
        this.podsContainer.innerHTML = '';

        pods.forEach(pod => {
            const podCard = document.createElement('div');
            podCard.className = 'pod-card';
            
            const podHeader = document.createElement('div');
            podHeader.className = 'pod-header';
            podHeader.textContent = `Pod ${pod.id} (${pod.size} players)`;
            
            const podPlayers = document.createElement('div');
            podPlayers.className = 'pod-players';
            
            pod.players.forEach(player => {
                const playerDiv = document.createElement('div');
                playerDiv.className = 'pod-player';
                playerDiv.textContent = player;
                podPlayers.appendChild(playerDiv);
            });

            podCard.appendChild(podHeader);
            podCard.appendChild(podPlayers);
            this.podsContainer.appendChild(podCard);
        });

        // Update statistics
        const totalPlayers = pods.reduce((sum, pod) => sum + pod.size, 0);
        const avgSize = (totalPlayers / pods.length).toFixed(1);
        this.statsInfo.textContent = 
            `Total: ${totalPlayers} players | ${pods.length} pods | Average: ${avgSize} per pod`;
    }

    // History Management
    saveToHistory() {
        if (!this.currentPods || this.currentPods.length === 0) {
            this.showToast('No pods to save', 'warning');
            return;
        }

        const historyEntry = {
            timestamp: new Date().toISOString(),
            pods: this.currentPods.map(pod => ({
                id: pod.id,
                players: pod.players,
                size: pod.size
            }))
        };

        this.history.unshift(historyEntry);
        
        // Keep only recent items
        if (this.history.length > this.config.max_history_items) {
            this.history = this.history.slice(0, this.config.max_history_items);
        }

        this.saveData();
        this.updateHistory();
        this.showToast('Saved to history', 'success');
    }

    updateHistory() {
        if (this.history.length === 0) {
            this.historyContainer.innerHTML = '<p class="no-history">No history available</p>';
            return;
        }

        this.historyContainer.innerHTML = '';

        this.history.slice(0, 10).forEach((entry, index) => {
            const date = new Date(entry.timestamp);
            const formattedDate = date.toLocaleString();
            const podCount = entry.pods.length;
            const playerCount = entry.pods.reduce((sum, pod) => sum + pod.size, 0);

            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            historyItem.innerHTML = `
                <h4>${formattedDate}</h4>
                <div class="history-summary">
                    ${podCount} pods, ${playerCount} players
                </div>
            `;

            this.historyContainer.appendChild(historyItem);
        });
    }

    // Data Import/Export
    exportData() {
        const exportData = {
            players: this.players,
            config: this.config,
            history: this.history,
            export_timestamp: new Date().toISOString(),
            version: '1.0'
        };

        const dataStr = JSON.stringify(exportData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `mtg_pods_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        
        URL.revokeObjectURL(url);
        this.showToast('Data exported successfully', 'success');
    }

    importData(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const importData = JSON.parse(e.target.result);
                
                if (importData.players) {
                    const merge = confirm('Merge with existing players? (OK = Merge, Cancel = Replace)');
                    
                    if (merge) {
                        // Merge players without duplicates
                        importData.players.forEach(player => {
                            if (!this.players.some(p => p.toLowerCase() === player.toLowerCase())) {
                                this.players.push(player);
                            }
                        });
                    } else {
                        // Replace all data
                        this.players = importData.players;
                    }
                }

                if (importData.config) {
                    this.config = { ...this.config, ...importData.config };
                }

                if (importData.history) {
                    this.history = importData.history;
                }

                this.saveData();
                this.updateUI();
                this.showToast('Data imported successfully', 'success');
            } catch (error) {
                this.showToast('Error importing data', 'error');
                console.error('Import error:', error);
            }
        };

        reader.readAsText(file);
        event.target.value = ''; // Reset file input
    }

    clearAllData() {
        if (!confirm('Are you sure you want to clear all data? This cannot be undone!')) {
            return;
        }

        this.players = [];
        this.history = [];
        this.currentPods = [];
        this.resultsSection.classList.add('hidden');
        
        this.saveData();
        this.updateUI();
        this.showToast('All data cleared', 'success');
    }

    // UI Updates
    updateUI() {
        this.updatePlayerList();
        this.updateHistory();
        this.updateConfigInputs();
    }

    updatePlayerList() {
        this.playersContainer.innerHTML = '';
        this.playerCount.textContent = this.players.length;

        if (this.players.length === 0) {
            this.playersContainer.innerHTML = '<p style="color: #666; text-align: center;">No players added yet</p>';
            return;
        }

        this.players.forEach((player, index) => {
            const playerItem = document.createElement('div');
            playerItem.className = 'player-item';
            
            const nameSpan = document.createElement('span');
            nameSpan.className = 'player-name';
            nameSpan.textContent = player;
            
            const removeBtn = document.createElement('button');
            removeBtn.className = 'remove-btn';
            removeBtn.textContent = 'Remove';
            removeBtn.onclick = () => this.removePlayer(index);
            
            playerItem.appendChild(nameSpan);
            playerItem.appendChild(removeBtn);
            this.playersContainer.appendChild(playerItem);
        });
    }

    updateConfigInputs() {
        this.targetSizeInput.value = this.config.default_pod_size;
        this.maxSizeInput.value = this.config.max_pod_size;
    }

    // UI Helpers
    showLoading(show) {
        this.loading.classList.toggle('hidden', !show);
    }

    showToast(message, type = 'success') {
        this.toastMessage.textContent = message;
        this.toast.className = `toast ${type}`;
        this.toast.classList.remove('hidden');

        setTimeout(() => {
            this.toast.classList.add('hidden');
        }, 3000);
    }
}

// Service Worker Registration for PWA
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new MTGPodRandomizer();
});