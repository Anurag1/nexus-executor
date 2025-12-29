# examples/complete_workflow.py
import asyncio
from nexus_executor import UnifiedHierarchyOrchestrator

async def example_workflow():
    """Complete example of unified hierarchy workflow"""
    
    # Initialize the system
    orchestrator = UnifiedHierarchyOrchestrator()
    
    # Example 1: Simple intent
    print("=== Example 1: Simple Data Processing ===")
    result1 = await orchestrator.process_intent(
        "Process this dataset and find anomalies",
        context={
            "dataset": "sales_data_2024.csv",
            "constraints": {
                "accuracy": ">95%",
                "time": "<5 minutes",
                "cost": "<$0.10"
            }
        }
    )
    print(f"Human Response: {result1['human_response']}")
    print(f"UEIR Graph ID: {result1['execution_details']['ueir_graph']['graph_id']}")
    
    # Example 2: Complex system design
    print("\n=== Example 2: System Architecture ===")
    result2 = await orchestrator.process_intent(
        "Design a distributed system that handles 100k requests/sec with 99.999% availability",
        context={
            "constraints": {
                "throughput": "≥100000 rps",
                "availability": "99.999%",
                "latency": "p99 < 50ms",
                "energy": "≤500 kWh/day",
                "budget": "$10k/month"
            },
            "hardware_options": ["aws", "gcp", "hybrid"],
            "safety_requirements": ["data_encryption", "audit_trails"]
        }
    )
    
    # Example 3: Interactive conversation
    print("\n=== Example 3: Interactive Optimization ===")
    conversation = [
        "I need to train a deep learning model on this image dataset",
        "Make it faster but keep accuracy above 90%",
        "Actually, prioritize energy efficiency over speed",
        "What if I increase the budget to $500?"
    ]
    
    session_id = "example_session"
    for message in conversation:
        print(f"\nUser: {message}")
        result = await orchestrator.process_intent(
            message,
            context={"session_id": session_id}
        )
        print(f"Assistant: {result['human_response']}")
        
        # Show execution details
        if 'execution_details' in result:
            metrics = result['execution_details']['metrics']
            print(f"  → Energy: {metrics.get('energy_joules', 'N/A')}J")
            print(f"  → Cost: ${metrics.get('cost_dollars', 'N/A')}")
            print(f"  → Performance: {metrics.get('performance_score', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(example_workflow())
