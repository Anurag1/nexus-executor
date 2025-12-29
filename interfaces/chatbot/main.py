# interfaces/chatbot/main.py
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import json

app = FastAPI(title="Nexus Executor Chatbot")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class NexusChatbot:
    """Main chatbot interface to unified hierarchy"""
    
    def __init__(self):
        self.orchestrator = UnifiedHierarchyOrchestrator()
        self.sessions = {}
        self.history = ChatHistory()
        
    async def handle_message(self, message, session_id, context=None):
        """Process user message through unified hierarchy"""
        
        # Get or create session
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'context': {},
                'execution_history': [],
                'preferences': {}
            }
        
        session = self.sessions[session_id]
        
        # Update context
        if context:
            session['context'].update(context)
        
        # Add to history
        self.history.add_message(session_id, 'user', message)
        
        try:
            # Process through unified hierarchy
            result = await self.orchestrator.process_intent(
                message,
                session['context']
            )
            
            # Store execution details
            session['execution_history'].append({
                'timestamp': time.time(),
                'intent': message,
                'execution_result': result['execution_details']
            })
            
            # Add response to history
            self.history.add_message(
                session_id, 
                'assistant', 
                result['human_response']
            )
            
            # Return both human and machine readable
            return {
                'human_response': result['human_response'],
                'execution_summary': {
                    'ueir_graph_id': result['execution_details']['ueir_graph']['graph_id'],
                    'metrics': result['execution_details']['metrics'],
                    'constraints_satisfied': result['execution_details']['constraints_satisfied']
                },
                'learning_feedback': result.get('learning_feedback', {})
            }
            
        except Exception as e:
            # Fallback to existing AI if execution system fails
            fallback_response = await self.fallback_to_existing_ai(
                message, session['context']
            )
            
            return {
                'human_response': f"I'll help with that: {fallback_response}",
                'note': 'Used existing AI (execution system unavailable)'
            }
    
    async def fallback_to_existing_ai(self, message, context):
        """Fallback to existing AI models"""
        # Use existing code generation/understanding
        return await self.orchestrator.cognitive_layer.process_simple(
            message, context
        )

# WebSocket endpoint for real-time chat
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    chatbot = NexusChatbot()
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            message = data.get('message', '')
            context = data.get('context', {})
            
            # Process through unified hierarchy
            response = await chatbot.handle_message(
                message, session_id, context
            )
            
            # Send response
            await websocket.send_json(response)
            
    except Exception as e:
        await websocket.close(code=1011)

# REST API endpoints
@app.post("/api/execute")
async def api_execute(request: ExecutionRequest):
    """API endpoint for execution requests"""
    chatbot = NexusChatbot()
    
    result = await chatbot.handle_message(
        request.intent,
        request.session_id,
        request.context
    )
    
    return result

@app.get("/api/history/{session_id}")
async def get_history(session_id: str):
    """Get execution history for session"""
    if session_id in chatbot.sessions:
        return {
            'history': chatbot.history.get_session(session_id),
            'executions': chatbot.sessions[session_id]['execution_history']
        }
    return {"error": "Session not found"}

# HTML interface
@app.get("/", response_class=HTMLResponse)
async def get_interface():
    return """
    <html>
        <head>
            <title>Nexus Executor Chatbot</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <div id="chat-container">
                <div id="chat-history"></div>
                <div id="input-area">
                    <input type="text" id="message-input" placeholder="Describe what you want to execute...">
                    <button onclick="sendMessage()">Execute</button>
                </div>
                <div id="execution-details" style="display: none;">
                    <h3>Execution Details</h3>
                    <div id="ueir-graph-viewer"></div>
                    <div id="metrics-display"></div>
                </div>
            </div>
            <script src="/static/chatbot.js"></script>
        </body>
    </html>
    """
