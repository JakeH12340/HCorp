# --- TAB 6: THE AI CORE (POWERED BY GEMINI) ---
with tab6:
    st.header("🤖 HCorp Strategic AI Core")
    
    if not api_key:
        st.warning("Please enter your HCorp Auth API Key in the sidebar to activate the AI Core.")
    else:
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Set the AI's persona
        system_prompt = """
        You are the HCorp Strategic AI Core, an advanced artificial intelligence built by HCorp (a deep-tech aerospace and energy megacorp). 
        You are speaking directly to the Founder of HCorp.
        You are an expert in aerospace engineering, fusion propulsion, orbital mechanics, and space economics.
        You believe in the company's mission: Project Scions, which aims to use Direct Fusion Drive (D-He3) and Lunar Helium-3 mining to colonize Mars. 
        Keep your answers concise, professional, slightly sci-fi, and address the user as 'Founder'. 
        If asked about anything unrelated to space, energy, or business, remind the Founder that our focus must remain on the mission.
        """
        
        # NEW: Model Selector
        model_choice = st.selectbox(
            "Select AI Engine (If one fails, try another):",
            ["gemini-1.5-flash", "gemini-1.0-pro", "gemini-pro"]
        )

        try:
            # Try to load the model with the system prompt
            try:
                model = genai.GenerativeModel(model_choice, system_instruction=system_prompt)
            except:
                # Fallback for older SDK versions that don't support system_instruction
                model = genai.GenerativeModel(model_choice)

            # Initialize chat history
            if "chat_session" not in st.session_state or st.session_state.get('current_model') != model_choice:
                st.session_state.chat_session = model.start_chat(history=[])
                st.session_state.messages = [{"role": "assistant", "content": f"HCorp Strategic AI Core online using {model_choice}. Awaiting your command, Founder."}]
                st.session_state.current_model = model_choice

            # Display chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Accept user input
            if prompt := st.chat_input("Query the HCorp AI..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    response = st.session_state.chat_session.send_message(prompt)
                    st.markdown(response.text)
                    
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
        except Exception as e:
            st.error(f"AI Core Error: {str(e)}")
            st.info("Try selecting a different AI Engine from the dropdown above.")
