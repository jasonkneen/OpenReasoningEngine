import streamlit as st
import requests
import json
import os

# Custom CSS for dark brushed steel material design
st.markdown("""
<style>
    /* Reset and base styles */
    .stApp, .main, div[data-testid="stToolbar"], section[data-testid="stSidebarContent"] {
        background: linear-gradient(45deg, #141414, #1d1d1d) !important;
    }
    
    /* Ensure full background coverage */
    .stApp {
        background-attachment: fixed !important;
    }
    
    /* Remove default Streamlit margins and padding */
    .stApp > header {
        background: transparent !important;
    }
    
    .main .block-container {
        padding: 1rem 3rem 10rem !important;
        max-width: 1000px !important;
    }

    /* Clean up top decoration bar */
    div[data-testid="stDecoration"] {
        display: none;
    }

    /* Enhanced sidebar styling */
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #1a1a1a, #0f0f0f);
        padding: 2rem 1rem;
    }
    
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(255,255,255,0.05);
        box-shadow: inset -1px 0 3px rgba(0,0,0,0.5);
        background: #0f0f0f;
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem !important;
    }

    /* Improved input fields with metallic effect */
    .stTextInput input, .stSelectbox select, .stNumberInput input {
        background: linear-gradient(145deg, #1a1a1a, #242424) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 6px !important;
        box-shadow: 
            inset 1px 1px 3px rgba(0,0,0,0.3),
            inset -1px -1px 3px rgba(255,255,255,0.05),
            0 1px 2px rgba(0,0,0,0.2) !important;
        color: #e0e0e0 !important;
        padding: 8px 12px !important;
        width: 100% !important;
    }

    /* Clean up selectbox */
    .stSelectbox > div {
        margin-top: 0 !important;
    }
    
    .stSelectbox > div > div {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Enhanced buttons with metallic effect */
    .stButton button {
        background: linear-gradient(145deg, #2a2a2a, #1e1e1e) !important;
        border: none !important;
        border-radius: 6px !important;
        box-shadow: 
            2px 2px 5px rgba(0,0,0,0.3),
            -2px -2px 5px rgba(255,255,255,0.05),
            inset 0 0 0 1px rgba(255,255,255,0.05) !important;
        color: #e0e0e0 !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
        width: auto !important;
        margin: 0 !important;
    }

    /* Enhanced slider styling */
    .stSlider {
        padding: 1rem 0 !important;
    }
    
    .stSlider > div {
        margin-top: 0 !important;
    }
    
    /* Slider track styling */
    .stSlider div[data-baseweb="slider"] {
        background: linear-gradient(90deg, #2a2a2a, #1e1e1e) !important;
        border-radius: 4px !important;
        height: 6px !important;
        box-shadow: 
            inset 1px 1px 3px rgba(0,0,0,0.3),
            inset -1px -1px 3px rgba(255,255,255,0.05) !important;
    }

    /* Slider thumb styling */
    .stSlider div[data-baseweb="slider"] [role="slider"] {
        background: linear-gradient(145deg, #3a3a3a, #2e2e2e) !important;
        border: none !important;
        box-shadow: 
            2px 2px 5px rgba(0,0,0,0.3),
            -1px -1px 3px rgba(255,255,255,0.05),
            inset 0 0 0 1px rgba(255,255,255,0.05) !important;
        width: 20px !important;
        height: 20px !important;
        top: -7px !important;
        transition: all 0.2s ease !important;
    }

    /* Slider thumb hover state */
    .stSlider div[data-baseweb="slider"] [role="slider"]:hover {
        background: linear-gradient(145deg, #404040, #343434) !important;
        box-shadow: 
            3px 3px 6px rgba(0,0,0,0.4),
            -1px -1px 3px rgba(255,255,255,0.07),
            inset 0 0 0 1px rgba(255,255,255,0.07) !important;
        transform: scale(1.1);
    }

    /* Slider value styling */
    .stSlider div[data-baseweb="slider"] div[role="slider"] div {
        color: #e0e0e0 !important;
        font-size: 0.8em !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    /* Enhanced text elements */
    h1, h2, h3 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
        letter-spacing: 0.5px !important;
        margin: 0 !important;
        padding: 1rem 0 !important;
    }

    p, label, .stMarkdown {
        color: #e0e0e0 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        margin: 0 !important;
        padding: 0.5rem 0 !important;
    }

    /* Clean up number input arrows */
    .stNumberInput div[data-baseweb="spinbutton"] span {
        border: none !important;
        background: transparent !important;
    }
    
    .stNumberInput div[data-baseweb="spinbutton"] button {
        border: none !important;
        background: rgba(255,255,255,0.05) !important;
    }

    /* Textarea enhancement */
    .stTextArea textarea {
        background: linear-gradient(145deg, #1a1a1a, #242424) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
        box-shadow: 
            inset 1px 1px 3px rgba(0,0,0,0.3),
            inset -1px -1px 3px rgba(255,255,255,0.05),
            0 1px 2px rgba(0,0,0,0.2) !important;
        color: #e0e0e0 !important;
        padding: 12px !important;
        min-height: 150px !important;
    }

    /* Remove extra margins and padding */
    .row-widget {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Clean up help text */
    .stMarkdown div[data-testid="stMarkdownContainer"] > p {
        font-size: 0.9em !important;
        opacity: 0.8;
    }

    /* Ensure dark background for all containers */
    div[class*="stMarkdown"], div[class*="stBlock"] {
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("OpenAI Reasoning Engine Interface")

# Sidebar for configuration
st.sidebar.markdown("## Configuration")
endpoint_type = st.sidebar.selectbox(
    "Select Mode",
    ["Single Model", "Ensemble", "Direct Endpoint"],
    help="Choose between single model, ensemble reasoning, or direct endpoint access"
)

# Model configuration
with st.sidebar:
    # Fetch the OPENAI_API_KEY from environment variables
    default_api_key = os.getenv("OPENAI_API_KEY", "")
    api_key = st.text_input("API Key", type="password", value=default_api_key)
    
    if endpoint_type == "Direct Endpoint":
        endpoint = st.selectbox(
            "Select Endpoint",
            ["/chat/completions", "/reasoning/think", "/reasoning/plan", "/reasoning/reflect"],
            help="Choose which API endpoint to access directly"
        )
    
    if endpoint_type in ["Single Model", "Ensemble"]:
        if endpoint_type == "Single Model":
            model = st.text_input("Model Name", value="gpt-4o-mini")
            api_url = st.text_input("API URL", value="https://api.openai.com/v1/chat/completions")
        else:  # Ensemble mode
            st.markdown("### Ensemble Configuration")
            num_models = st.number_input("Number of Models", min_value=2, max_value=5, value=2)
            
            models = []
            api_urls = []
            for i in range(num_models):
                col1, col2 = st.columns(2)
                with col1:
                    models.append(st.text_input(f"Model {i+1} Name", value=f"gpt-4", key=f"model_{i}"))
                with col2:
                    api_urls.append(st.text_input(f"API URL {i+1}", value="https://api.openai.com/v1/chat/completions", key=f"url_{i}"))
    
    # Common configuration
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.number_input("Max Tokens", 100, 2000, 500)
    max_reasoning_steps = st.number_input("Max Reasoning Steps", 1, 20, 10)
    
    # Advanced options
    with st.expander("Advanced Options"):
        use_reflection = st.checkbox("Enable Reflection", value=True)
        use_planning = st.checkbox("Enable Planning", value=True)
        if use_planning:
            planning_temperature = st.slider("Planning Temperature", 0.0, 1.0, 0.5)
        
        # Tool configuration
        st.markdown("### Tool Configuration")
        enable_python = st.checkbox("Enable Python Execution", value=True)
        if enable_python:
            python_timeout = st.number_input("Python Timeout (seconds)", 1, 30, 5)
        
        enable_web_search = st.checkbox("Enable Web Search", value=True)
        enable_wolfram = st.checkbox("Enable Wolfram Alpha", value=False)
        if enable_wolfram:
            wolfram_pods = st.multiselect(
                "Wolfram Alpha Pods",
                ["Result", "Definition", "Properties", "Solutions", "Plots"],
                ["Result"]
            )
        
        enable_webpage = st.checkbox("Enable Webpage Retrieval", value=True)

# Main interface
if endpoint_type == "Direct Endpoint":
    st.markdown(f"## {endpoint} Endpoint")
    
    if endpoint == "/reasoning/think":
        task_input = st.text_area("Task:", height=150)
    elif endpoint == "/reasoning/plan":
        task_input = st.text_area("Task:", height=150)
        st.markdown("### Similar Chains (Optional)")
        num_chains = st.number_input("Number of Similar Chains", 0, 5, 0)
        similar_chains = []
        for i in range(num_chains):
            chain = st.text_area(f"Chain {i+1}", height=100, key=f"chain_{i}")
            if chain:
                similar_chains.append(json.loads(chain))
    elif endpoint == "/reasoning/reflect":
        st.markdown("### Previous Steps")
        num_steps = st.number_input("Number of Steps", 1, 10, 1)
        steps = []
        for i in range(num_steps):
            step = st.text_area(f"Step {i+1}", height=100, key=f"step_{i}")
            if step:
                steps.append(json.loads(step))
    else:  # /chat/completions
        messages = []
        num_messages = st.number_input("Number of Messages", 1, 10, 1)
        for i in range(num_messages):
            col1, col2 = st.columns(2)
            with col1:
                role = st.selectbox(f"Message {i+1} Role", ["user", "assistant", "system"], key=f"role_{i}")
            with col2:
                content = st.text_area(f"Message {i+1} Content", height=100, key=f"content_{i}")
            if content:
                messages.append({"role": role, "content": content})
else:
    task_input = st.text_area("Enter your task:", height=150)

# Placeholder for responses
actual_response_placeholder = st.empty()
debug_response_placeholder = st.empty()

# Button to send the request
if st.button("Send Request"):
    if (task_input or endpoint_type == "Direct Endpoint") and api_key:
        try:
            if endpoint_type == "Single Model":
                # Single model payload
                payload = {
                    "task": task_input,
                    "api_key": api_key,
                    "model": model,
                    "api_url": api_url,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "max_reasoning_steps": max_reasoning_steps,
                    "use_reflection": use_reflection,
                    "use_planning": use_planning,
                    "planning_temperature": planning_temperature if use_planning else None,
                    "tools": {
                        "python": {
                            "enabled": enable_python,
                            "timeout": python_timeout if enable_python else None
                        },
                        "web_search": {"enabled": enable_web_search},
                        "wolfram": {
                            "enabled": enable_wolfram,
                            "pods": wolfram_pods if enable_wolfram else None
                        },
                        "webpage": {"enabled": enable_webpage}
                    },
                    "verbose": True
                }
                response = requests.post("http://localhost:5050/reason", json=payload)
            elif endpoint_type == "Ensemble":
                # Ensemble payload
                agents = [
                    {
                        "model": m,
                        "api_key": api_key,
                        "api_url": u,
                        "temperature": temperature
                    } for m, u in zip(models, api_urls)
                ]
                
                # Use the first model as coordinator for simplicity
                coordinator = {
                    "model": models[0],
                    "api_key": api_key,
                    "api_url": api_urls[0],
                    "temperature": temperature
                }
                
                ensemble_payload = {
                    "task": task_input,
                    "agents": agents,
                    "coordinator": coordinator,
                    "max_tokens": max_tokens,
                    "max_reasoning_steps": max_reasoning_steps,
                    "coordinator_max_steps": max_reasoning_steps,
                    "temperature": temperature,
                    "use_reflection": use_reflection,
                    "use_planning": use_planning,
                    "planning_temperature": planning_temperature if use_planning else None,
                    "tools": {
                        "python": {
                            "enabled": enable_python,
                            "timeout": python_timeout if enable_python else None
                        },
                        "web_search": {"enabled": enable_web_search},
                        "wolfram": {
                            "enabled": enable_wolfram,
                            "pods": wolfram_pods if enable_wolfram else None
                        },
                        "webpage": {"enabled": enable_webpage}
                    },
                    "verbose": True,
                    "return_reasoning": True
                }
                response = requests.post("http://localhost:5050/run_ensemble", json=ensemble_payload)
            else:  # Direct Endpoint
                if endpoint == "/chat/completions":
                    payload = {
                        "model": model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                elif endpoint == "/reasoning/think":
                    payload = {
                        "task": task_input,
                        "temperature": temperature,
                        "max_steps": max_reasoning_steps
                    }
                elif endpoint == "/reasoning/plan":
                    payload = {
                        "task": task_input,
                        "similar_chains": similar_chains if similar_chains else None
                    }
                elif endpoint == "/reasoning/reflect":
                    payload = {"steps": steps}
                
                response = requests.post(f"http://localhost:5050{endpoint}", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                # Display the response
                if result:
                    if endpoint_type == "Direct Endpoint":
                        st.json(result)
                    else:
                        actual_response = result.get("response", {}).get("content", "No response content available")
                        actual_response_placeholder.markdown(actual_response)
                        
                        # Display reasoning chain
                        if "reasoning_chain" in result:
                            with st.expander("Show Reasoning Chain"):
                                for step in result.get("reasoning_chain", []):
                                    step_num = step.get("step_number", "N/A")
                                    content = step.get("content", step.get("thought", "N/A"))
                                    
                                    st.markdown(f"### Step {step_num}")
                                    st.markdown(f"**Thought**: {content}")
                                    
                                    # Handle tool calls
                                    tool_calls = step.get("tool_calls", [])
                                    if tool_calls and isinstance(tool_calls, list):
                                        st.markdown("**Tool Calls:**")
                                        for tool_call in tool_calls:
                                            if isinstance(tool_call, dict):
                                                name = tool_call.get("name", tool_call.get("function", {}).get("name", "Unknown Tool"))
                                                params = tool_call.get("parameters", tool_call.get("function", {}).get("parameters", {}))
                                                st.code(f"{name}: {json.dumps(params, indent=2)}")
                                    
                                    # Handle tool results
                                    tool_results = step.get("tool_results", [])
                                    if tool_results and isinstance(tool_results, list):
                                        st.markdown("**Tool Results:**")
                                        for result in tool_results:
                                            if isinstance(result, dict):
                                                st.code(json.dumps(result, indent=2))
                                            else:
                                                st.code(str(result))
                                    
                                    st.markdown("---")
                        
                        # Show ensemble-specific information
                        if endpoint_type == "Ensemble" and "ensemble_results" in result:
                            with st.expander("Show Ensemble Details"):
                                for i, model_result in enumerate(result["ensemble_results"]):
                                    st.markdown(f"### Model {i+1}: {models[i]}")
                                    st.markdown(model_result.get("response", {}).get("content", "No response"))
                                    st.markdown("---")
                
                # Show full debug response in collapsible section
                with st.expander("View Full Debug Information"):
                    st.json(result)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please provide all required inputs")

# Add helpful information
st.sidebar.markdown("""
## How to use
1. Configure your model settings in the sidebar
2. Enter your task in the text area
3. Click 'Send Request' to get a response

The response will show the reasoning process and final answer.
""")