// static/chatbot.js
class NexusChatbotUI {
    constructor() {
        this.ws = null;
        this.sessionId = this.generateSessionId();
        this.connectWebSocket();
        this.setupEventListeners();
    }
    
    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9);
    }
    
    connectWebSocket() {
        this.ws = new WebSocket(`ws://${window.location.host}/ws/${this.sessionId}`);
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.displayResponse(data);
        };
        
        this.ws.onopen = () => {
            console.log('Connected to Nexus Executor');
        };
    }
    
    async sendMessage() {
        const input = document.getElementById('message-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        this.addMessage('user', message);
        input.value = '';
        
        // Prepare context (can include constraints, preferences, etc.)
        const context = {
            hardware_preferences: this.getHardwarePreferences(),
            energy_constraints: this.getEnergyConstraints(),
            cost_limits: this.getCostLimits()
        };
        
        // Send through WebSocket
        this.ws.send(JSON.stringify({
            message: message,
            context: context
        }));
    }
    
    displayResponse(response) {
        // Show human response
        this.addMessage('assistant', response.human_response);
        
        // Show execution details if available
        if (response.execution_summary) {
            this.showExecutionDetails(response.execution_summary);
        }
        
        // Show learning feedback
        if (response.learning_feedback) {
            this.showLearningFeedback(response.learning_feedback);
        }
    }
    
    showExecutionDetails(summary) {
        const detailsDiv = document.getElementById('execution-details');
        detailsDiv.style.display = 'block';
        
        // Display UEIR graph (simplified visualization)
        const graphViewer = document.getElementById('ueir-graph-viewer');
        graphViewer.innerHTML = this.renderGraphVisualization(summary.ueir_graph_id);
        
        // Display metrics
        const metricsDiv = document.getElementById('metrics-display');
        metricsDiv.innerHTML = `
            <h4>Execution Metrics</h4>
            <ul>
                <li>Energy Used: ${summary.metrics.energy_joules} J</li>
                <li>Cost: $${summary.metrics.cost_dollars}</li>
                <li>Performance Score: ${summary.metrics.performance_score}</li>
                <li>Constraints Satisfied: ${summary.constraints_satisfied ? 'Yes' : 'No'}</li>
            </ul>
        `;
    }
    
    addMessage(sender, text) {
        const historyDiv = document.getElementById('chat-history');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.textContent = `${sender}: ${text}`;
        historyDiv.appendChild(messageDiv);
        historyDiv.scrollTop = historyDiv.scrollHeight;
    }
    
    setupEventListeners() {
        const input = document.getElementById('message-input');
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }
}

// Initialize chatbot
window.onload = () => {
    window.chatbot = new NexusChatbotUI();
};
